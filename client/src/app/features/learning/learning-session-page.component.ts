import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';

import {
  ApiService,
  CertificationRouteResponse,
  CompleteLessonResponse,
  CourseLesson,
  LearningSessionResponse,
  LessonChatMessage,
  RouteSection,
  StudyPlanResponse,
} from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { CourseSessionComponent } from './course-session.component';
import { LessonContentComponent } from './lesson-content.component';

@Component({
  selector: 'app-learning-session-page',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    EmptyStateComponent,
    LessonContentComponent,
    CourseSessionComponent,
  ],
  templateUrl: './learning-session-page.component.html',
  styleUrl: './learning-session-page.component.css',
})
export class LearningSessionPageComponent {
  private readonly api = inject(ApiService);
  private readonly activatedRoute = inject(ActivatedRoute);

  /** Si viene ?course=CODE, entramos en "modo curso" (lectura directa, sin ruta). */
  protected readonly courseCode = signal<string | null>(null);

  protected readonly plan = signal<StudyPlanResponse | null>(null);
  protected readonly route = signal<CertificationRouteResponse | null>(null);
  protected readonly loading = signal(true);

  protected readonly section = signal<RouteSection | null>(null);
  protected readonly session = signal<LearningSessionResponse | null>(null);
  protected readonly activeLesson = signal<CourseLesson | null>(null);
  protected readonly starting = signal(false);

  // Tutor
  protected readonly tutorOpen = signal(true);
  protected readonly chat = signal<LessonChatMessage[]>([]);
  protected readonly suggested = signal<string[]>([]);
  protected readonly tutorLoading = signal(false);
  protected tutorInput = '';

  // Gate de seccion
  protected mandatoryAnswer = '';
  protected readonly mandatorySending = signal(false);
  protected readonly quizSelections = signal<Record<string, number>>({});
  protected readonly quizSubmitting = signal(false);
  protected readonly completeResult = signal<CompleteLessonResponse | null>(null);

  protected readonly sections = computed(() => this.route()?.sections ?? []);

  protected readonly mandatoryPassed = computed(
    () => this.session()?.evaluation?.mandatory_answer?.is_correct === true,
  );
  protected readonly quizResult = computed(() => this.session()?.evaluation?.quiz ?? null);
  protected readonly quizQuestions = computed(
    () => this.session()?.evaluation?.quiz_questions ?? [],
  );

  constructor() {
    const code = this.activatedRoute.snapshot.queryParamMap.get('course');
    if (code) {
      this.courseCode.set(code);
      this.loading.set(false);
      return; // modo curso: el contenido lo maneja CourseSessionComponent
    }
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [plan, route] = await Promise.all([this.api.getLatestPlan(), this.api.getLatestRoute()]);
      this.plan.set(plan);
      this.route.set(route);
      this.section.set(route?.sections[0] ?? null);
    } finally {
      this.loading.set(false);
    }
  }

  protected selectSection(section: RouteSection): void {
    if (this.section()?.section_id === section.section_id) return;
    this.section.set(section);
    this.session.set(null);
    this.activeLesson.set(null);
    this.chat.set([]);
    this.suggested.set([]);
    this.completeResult.set(null);
  }

  protected async startSession(): Promise<void> {
    const plan = this.plan();
    const section = this.section();
    if (!plan?.id || !section) return;
    this.starting.set(true);
    try {
      const session = await this.api.startSession({
        plan_id: plan.id,
        section_id: section.section_id,
        section_title: section.title,
        session_type: 'theory',
      });
      this.session.set(session);
      const firstLesson = section.lessons[0] ?? null;
      if (firstLesson) {
        await this.selectLesson(firstLesson);
      }
    } finally {
      this.starting.set(false);
    }
  }

  protected async selectLesson(lesson: CourseLesson): Promise<void> {
    this.activeLesson.set(lesson);
    this.completeResult.set(null);
    this.chat.set([]);
    this.suggested.set([]);
    const session = this.session();
    if (!session?.id || !lesson.id) return;
    try {
      const [history, suggested] = await Promise.all([
        this.api.getLessonChat(session.id, lesson.id).catch(() => []),
        this.api.getSuggestedQuestions(session.id, lesson.id).catch(() => ({ questions: [] }) as { questions: string[] }),
      ]);
      this.chat.set(history);
      this.suggested.set(suggested.questions);
    } catch {
      /* tutor opcional */
    }
  }

  protected async sendTutor(text?: string): Promise<void> {
    const question = (text ?? this.tutorInput).trim();
    const session = this.session();
    const lesson = this.activeLesson();
    if (!question || !session?.id || !lesson?.id) return;
    this.tutorInput = '';
    this.tutorOpen.set(true);
    // eco optimista del usuario
    this.chat.update((messages) => [
      ...messages,
      { id: null, role: 'user', content: question, sources: [], suggested_questions: [], source_mode: 'mock', created_at: null },
    ]);
    this.tutorLoading.set(true);
    try {
      const response = await this.api.askTutor(session.id, lesson.id, question);
      this.chat.set(response.history);
      this.suggested.set(response.answer.suggested_questions);
    } finally {
      this.tutorLoading.set(false);
    }
  }

  protected async completeActiveLesson(): Promise<void> {
    const session = this.session();
    const lesson = this.activeLesson();
    if (!session?.id || !lesson?.id) return;
    const result = await this.api.completeLesson(session.id, lesson.id);
    this.completeResult.set(result);
    // avanzar a la siguiente leccion
    const lessons = this.section()?.lessons ?? [];
    const idx = lessons.findIndex((l) => l.id === lesson.id);
    if (idx >= 0 && idx + 1 < lessons.length) {
      await this.selectLesson(lessons[idx + 1]);
    }
  }

  protected async sendMandatory(): Promise<void> {
    const session = this.session();
    if (!session?.id || !this.mandatoryAnswer.trim()) return;
    this.mandatorySending.set(true);
    try {
      this.session.set(await this.api.submitMandatoryAnswer(session.id, this.mandatoryAnswer));
    } finally {
      this.mandatorySending.set(false);
    }
  }

  protected selectQuizOption(questionId: string, optionIndex: number): void {
    this.quizSelections.update((current) => ({ ...current, [questionId]: optionIndex }));
  }

  protected isSelected(questionId: string, optionIndex: number): boolean {
    return this.quizSelections()[questionId] === optionIndex;
  }

  protected readonly allQuizAnswered = computed(() => {
    const questions = this.quizQuestions();
    const selections = this.quizSelections();
    return questions.length > 0 && questions.every((q) => selections[q.question_id] !== undefined);
  });

  protected async submitQuiz(): Promise<void> {
    const session = this.session();
    if (!session?.id) return;
    const selections = this.quizSelections();
    const quizAnswers = this.quizQuestions().map((q) => ({
      question_id: q.question_id,
      selected_option_index: selections[q.question_id] ?? 0,
    }));
    this.quizSubmitting.set(true);
    try {
      this.session.set(await this.api.submitEvaluation(session.id, { quiz_answers: quizAnswers }));
    } finally {
      this.quizSubmitting.set(false);
    }
  }

  protected async saveSurvey(skip: boolean): Promise<void> {
    const session = this.session();
    if (!session?.id) return;
    this.session.set(
      await this.api.submitSurvey(
        session.id,
        skip ? { skipped: true } : { skipped: false, clarity_score: 5, preferred_format: 'hands_on' },
      ),
    );
  }

  protected toggleTutor(): void {
    this.tutorOpen.update((open) => !open);
  }

  // --- Navegación y progreso de lecciones ---
  protected readonly lessonList = computed(() => this.section()?.lessons ?? []);

  protected readonly lessonIndex = computed(() => {
    const active = this.activeLesson();
    if (!active) return -1;
    return this.lessonList().findIndex((l) => l.id === active.id && l.lesson_key === active.lesson_key);
  });

  protected readonly readingProgress = computed(() => {
    const total = this.lessonList().length;
    const idx = this.lessonIndex();
    if (total <= 0 || idx < 0) return 0;
    return Math.round(((idx + 1) / total) * 100);
  });

  protected async goToLessonOffset(offset: number): Promise<void> {
    const lessons = this.lessonList();
    const next = this.lessonIndex() + offset;
    if (next >= 0 && next < lessons.length) {
      await this.selectLesson(lessons[next]);
    }
  }

  protected formatDuration(minutes: number): string {
    if (!minutes) return '';
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    if (h && m) return `${h} h ${m} min`;
    if (h) return `${h} h`;
    return `${m} min`;
  }
}
