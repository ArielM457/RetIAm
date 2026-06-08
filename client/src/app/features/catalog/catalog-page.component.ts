import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { ApiService, CourseCatalogSummary, CourseDetail } from '../../core/services/api.service';

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

  protected readonly courses = signal<CourseCatalogSummary[]>([]);
  protected readonly loading = signal(true);
  protected readonly query = signal('');
  protected readonly track = signal<TrackFilter>('all');
  protected readonly level = signal<LevelFilter>('all');

  protected readonly selected = signal<CourseDetail | null>(null);
  protected readonly detailLoading = signal(false);
  protected readonly starting = signal(false);

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

  protected readonly featured = computed(() =>
    [...this.courses()].sort((a, b) => b.lesson_count - a.lesson_count).slice(0, 10),
  );

  protected readonly filtered = computed(() => {
    const q = this.query().trim().toLowerCase();
    const track = this.track();
    const level = this.level();
    return this.courses().filter((course) => {
      if (track !== 'all' && course.track !== track) return false;
      if (level !== 'all' && course.level !== level) return false;
      if (q && !`${course.title} ${course.summary ?? ''}`.toLowerCase().includes(q)) return false;
      return true;
    });
  });

  protected readonly trackCount = computed(() => {
    const counts: Record<string, number> = { all: this.courses().length };
    for (const course of this.courses()) counts[course.track] = (counts[course.track] ?? 0) + 1;
    return counts;
  });

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      this.courses.set(await this.api.listCourses());
    } finally {
      this.loading.set(false);
    }
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

  /** Selecciona un solo curso y te lleva a la sesión para entrar a su contenido (sin armar ruta). */
  protected async startCourse(code: string): Promise<void> {
    this.starting.set(true);
    try {
      this.selected.set(null);
      await this.router.navigate(['/sessions'], { queryParams: { course: code } });
    } finally {
      this.starting.set(false);
    }
  }
}
