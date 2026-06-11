import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthStore } from '../../core/auth/auth.store';
import {
  ApiService,
  CourseCatalogSummary,
  CourseDetail,
  CourseEnrollmentResponse,
} from '../../core/services/api.service';

type TrackFilter = 'all' | 'azure' | 'github' | 'aws';
type LevelFilter = 'all' | 'basic' | 'intermediate' | 'advanced';

@Component({
  selector: 'app-catalog-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './catalog-page.component.html',
  styleUrl: './catalog-page.component.css',
})
export class CatalogPageComponent {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);
  protected readonly authStore = inject(AuthStore);

  protected readonly courses = signal<CourseCatalogSummary[]>([]);
  protected readonly enrollments = signal<CourseEnrollmentResponse[]>([]);
  protected readonly loading = signal(true);
  protected readonly query = signal('');
  protected readonly track = signal<TrackFilter>('all');
  protected readonly level = signal<LevelFilter>('all');

  protected readonly selected = signal<CourseDetail | null>(null);
  protected readonly detailLoading = signal(false);
  protected readonly enrolling = signal(false);
  protected readonly showEnrollConfirm = signal(false);
  protected readonly selectedEnrollmentCode = signal<string | null>(null);

  protected readonly tracks: Array<{ key: TrackFilter; label: string }> = [
    { key: 'all', label: 'Todos' },
    { key: 'azure', label: 'Azure' },
    { key: 'github', label: 'GitHub' },
    { key: 'aws', label: 'AWS' },
  ];

  protected readonly levels: Array<{ key: LevelFilter; label: string }> = [
    { key: 'all', label: 'Todos los niveles' },
    { key: 'basic', label: 'Básico' },
    { key: 'intermediate', label: 'Intermedio' },
    { key: 'advanced', label: 'Avanzado' },
  ];

  protected readonly enrollmentMap = computed(
    () =>
      new Map(
        this.enrollments().map((enrollment) => [enrollment.certification_code, enrollment] as const),
      ),
  );

  protected readonly featured = computed(() =>
    [...this.courses()].sort((a, b) => this.compareCourses(a, b)).slice(0, 10),
  );

  protected readonly filtered = computed(() => {
    const q = this.query().trim().toLowerCase();
    const track = this.track();
    const level = this.level();
    return this.courses()
      .filter((course) => {
        if (track !== 'all' && course.track !== track) return false;
        if (level !== 'all' && course.level !== level) return false;
        if (q && !`${course.title} ${course.summary ?? ''}`.toLowerCase().includes(q)) return false;
        return true;
      })
      .sort((a, b) => this.compareCourses(a, b));
  });

  protected readonly trackCount = computed(() => {
    const counts: Record<string, number> = { all: this.courses().length };
    for (const course of this.courses()) counts[course.track] = (counts[course.track] ?? 0) + 1;
    return counts;
  });

  protected readonly preferenceFacts = computed(() => {
    const profile = this.authStore.profile();
    return [
      { label: 'Horas semanales', value: `${profile?.weekly_hours_available || 0} horas` },
      { label: 'Horario preferido', value: profile?.preferred_time || 'Sin definir' },
      {
        label: 'Estilo de aprendizaje',
        value: profile?.learning_style?.length ? profile.learning_style.join(', ') : 'Sin definir',
      },
    ];
  });

  protected readonly enrolledCount = computed(() => this.enrollments().length);

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [courses, enrollments] = await Promise.all([
        this.api.listCourses(),
        this.api.listMyEnrollments().catch(() => []),
      ]);
      this.courses.set(courses);
      this.enrollments.set(enrollments);
    } finally {
      this.loading.set(false);
    }
  }

  protected isEnrolled(code: string): boolean {
    return this.enrollmentMap().has(code);
  }

  protected coverClass(track: string): string {
    if (track === 'github') return 'cover-github';
    if (track === 'aws') return 'cover-aws';
    return 'cover-azure';
  }

  protected levelClass(level: string): string {
    return `level-${level}`;
  }

  protected levelLabel(level: string): string {
    return { basic: 'Básico', intermediate: 'Intermedio', advanced: 'Avanzado' }[level] ?? level;
  }

  protected formatDuration(minutes: number): string {
    if (!minutes) return '—';
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    if (h && m) return `${h} h ${m} min`;
    if (h) return `${h} h`;
    return `${m} min`;
  }

  protected async openCourse(code: string): Promise<void> {
    this.detailLoading.set(true);
    this.selected.set(null);
    try {
      this.selected.set(await this.api.getCourse(code));
    } finally {
      this.detailLoading.set(false);
    }
  }

  protected closeDrawer(): void {
    this.selected.set(null);
  }

  protected requestEnrollment(code: string): void {
    if (this.isEnrolled(code)) {
      void this.openEnrolledCourse(code);
      return;
    }
    this.selectedEnrollmentCode.set(code);
    this.showEnrollConfirm.set(true);
  }

  protected closeEnrollmentConfirm(): void {
    this.showEnrollConfirm.set(false);
    this.selectedEnrollmentCode.set(null);
  }

  protected async confirmEnrollment(): Promise<void> {
    const code = this.selectedEnrollmentCode();
    if (!code) return;
    this.enrolling.set(true);
    try {
      this.selected.set(null);
      this.showEnrollConfirm.set(false);
      const flow = await this.api.enrollInCourse(code);
      this.enrollments.update((current) => {
        const next = current.filter((item) => item.certification_code !== flow.enrollment.certification_code);
        next.unshift(flow.enrollment);
        return next;
      });
      await this.openEnrolledCourse(code);
    } finally {
      this.enrolling.set(false);
      this.selectedEnrollmentCode.set(null);
    }
  }

  protected async openEnrolledCourse(code: string): Promise<void> {
    this.selected.set(null);
    this.showEnrollConfirm.set(false);
    await this.router.navigate(['/sessions'], { queryParams: { course: code } });
  }

  private compareCourses(a: CourseCatalogSummary, b: CourseCatalogSummary): number {
    const aEnrolled = this.isEnrolled(a.certification_code) ? 1 : 0;
    const bEnrolled = this.isEnrolled(b.certification_code) ? 1 : 0;
    if (aEnrolled !== bEnrolled) return bEnrolled - aEnrolled;
    if (a.lesson_count !== b.lesson_count) return b.lesson_count - a.lesson_count;
    return a.title.localeCompare(b.title);
  }
}
