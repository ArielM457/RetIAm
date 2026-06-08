import { CommonModule } from '@angular/common';
import { Component, computed, inject, input, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import {
  ApiService,
  CourseDetail,
  CourseLesson,
  CourseSectionContent,
  LessonChatMessage,
} from '../../core/services/api.service';
import { LessonContentComponent } from './lesson-content.component';

/**
 * Modo curso: el usuario eligió un curso en el catálogo y entra a leer su
 * contenido directamente (sin ruta ni plan). Contenido enriquecido + tutor por
 * lección (sin sesión) + progreso local (lecciones marcadas como leídas).
 */
@Component({
  selector: 'app-course-session',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LessonContentComponent],
  templateUrl: './course-session.component.html',
  styleUrl: './course-session.component.css',
})
export class CourseSessionComponent implements OnInit {
  private readonly api = inject(ApiService);

  readonly code = input.required<string>();

  protected readonly course = signal<CourseDetail | null>(null);
  protected readonly loading = signal(true);
  protected readonly activeLesson = signal<CourseLesson | null>(null);

  // Tutor (sin sesión)
  protected readonly tutorOpen = signal(true);
  protected readonly chat = signal<LessonChatMessage[]>([]);
  protected readonly suggested = signal<string[]>([]);
  protected readonly tutorLoading = signal(false);
  protected tutorInput = '';

  // Progreso local (lecciones leídas)
  protected readonly readSet = signal<Set<string>>(new Set());

  protected readonly sections = computed(() => this.course()?.sections ?? []);
  protected readonly flatLessons = computed(() =>
    this.sections().flatMap((s) => s.lessons),
  );
  protected readonly readCount = computed(() => {
    const set = this.readSet();
    return this.flatLessons().filter((l) => l.id && set.has(l.id)).length;
  });
  protected readonly progress = computed(() => {
    const total = this.flatLessons().length;
    return total ? Math.round((this.readCount() / total) * 100) : 0;
  });

  ngOnInit(): void {
    void this.load();
  }

  private storageKey(): string {
    return `retaim:read:${this.code()}`;
  }

  private async load(): Promise<void> {
    this.loading.set(true);
    try {
      const course = await this.api.getCourse(this.code());
      this.course.set(course);
      this.restoreProgress();
      const first = course.sections[0]?.lessons[0] ?? null;
      if (first) await this.selectLesson(first);
    } finally {
      this.loading.set(false);
    }
  }

  private restoreProgress(): void {
    try {
      const raw = localStorage.getItem(this.storageKey());
      if (raw) this.readSet.set(new Set(JSON.parse(raw) as string[]));
    } catch {
      /* sin persistencia */
    }
  }

  private persistProgress(): void {
    try {
      localStorage.setItem(this.storageKey(), JSON.stringify([...this.readSet()]));
    } catch {
      /* sin persistencia */
    }
  }

  protected isActive(lesson: CourseLesson): boolean {
    const a = this.activeLesson();
    return a?.id === lesson.id && a?.lesson_key === lesson.lesson_key;
  }

  protected isRead(lesson: CourseLesson): boolean {
    return !!lesson.id && this.readSet().has(lesson.id);
  }

  protected async selectLesson(lesson: CourseLesson): Promise<void> {
    this.activeLesson.set(lesson);
    this.chat.set([]);
    this.suggested.set([]);
    if (!lesson.id) return;
    try {
      const [history, suggested] = await Promise.all([
        this.api.getLessonChatByLesson(lesson.id).catch(() => []),
        this.api
          .getLessonSuggestions(lesson.id)
          .catch(() => ({ questions: [] }) as { questions: string[] }),
      ]);
      this.chat.set(history);
      this.suggested.set(suggested.questions);
    } catch {
      /* tutor opcional */
    }
  }

  protected toggleRead(lesson: CourseLesson | null): void {
    if (!lesson?.id) return;
    const id = lesson.id;
    this.readSet.update((set) => {
      const next = new Set(set);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
    this.persistProgress();
  }

  /** Marca la lección activa como leída y avanza a la siguiente. */
  protected completeAndNext(): void {
    const lesson = this.activeLesson();
    if (lesson?.id && !this.readSet().has(lesson.id)) this.toggleRead(lesson);
    void this.goToLessonOffset(1);
  }

  protected lessonIndex(): number {
    const a = this.activeLesson();
    if (!a) return -1;
    return this.flatLessons().findIndex((l) => l.id === a.id && l.lesson_key === a.lesson_key);
  }

  protected async goToLessonOffset(offset: number): Promise<void> {
    const lessons = this.flatLessons();
    const next = this.lessonIndex() + offset;
    if (next >= 0 && next < lessons.length) await this.selectLesson(lessons[next]);
  }

  protected async sendTutor(text?: string): Promise<void> {
    const question = (text ?? this.tutorInput).trim();
    const lesson = this.activeLesson();
    if (!question || !lesson?.id) return;
    this.tutorInput = '';
    this.tutorOpen.set(true);
    this.chat.update((messages) => [
      ...messages,
      {
        id: null,
        role: 'user',
        content: question,
        sources: [],
        suggested_questions: [],
        source_mode: 'mock',
        created_at: null,
      },
    ]);
    this.tutorLoading.set(true);
    try {
      const response = await this.api.askLessonTutor(lesson.id, question);
      this.chat.set(response.history);
      this.suggested.set(response.answer.suggested_questions);
    } finally {
      this.tutorLoading.set(false);
    }
  }

  protected toggleTutor(): void {
    this.tutorOpen.update((open) => !open);
  }

  protected levelLabel(level: string): string {
    return { basic: 'Básico', intermediate: 'Intermedio', advanced: 'Avanzado' }[level] ?? level;
  }

  protected formatDuration(minutes: number): string {
    if (!minutes) return '';
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    if (h && m) return `${h} h ${m} min`;
    if (h) return `${h} h`;
    return `${m} min`;
  }

  protected trackSection(_: number, section: CourseSectionContent): string {
    return section.section_key;
  }
}
