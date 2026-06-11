import { CommonModule } from '@angular/common';
import { Component, computed, effect, inject, input, OnDestroy, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { AuthStore } from '../../core/auth/auth.store';
import {
  ApiService,
  CourseDetail,
  CourseLesson,
  CourseSectionContent,
  LessonChatMessage,
  LessonReviewResponse,
} from '../../core/services/api.service';
import { LessonContentComponent } from './lesson-content.component';

type LessonPartSummary = {
  id: string;
  title: string;
};

type SessionTechniqueOption = {
  key: string;
  label: string;
  description: string;
};

type MethodologyPromptConfig = {
  title: string;
  description: string;
  placeholder: string;
  confirmLabel: string;
};

type TutorMode =
  | { kind: 'general' }
  | {
      kind: 'checkpoint';
      title: string;
      description: string;
      placeholder: string;
      confirmLabel: string;
    };

type MethodologyEntry = {
  lessonId: string;
  lessonTitle: string;
  partIndex: number;
  partTitle: string;
  sectionIndex: number;
  technique: string;
  explanation: string;
  accepted: boolean;
  skipped: boolean;
  feedback: string;
  reinforcement: string | null;
  reviewedAt: string;
  reviewStatus?: 'pending' | 'remembered' | 'later';
};

type MethodologySessionState = {
  selectedTechnique: string | null;
  skipCount: number;
  reviewCount: number;
  acceptedCount: number;
  rejectedCount: number;
  entries: MethodologyEntry[];
  startedAt: string;
};

type StoredCourseProgress = {
  readLessonIds: string[];
  lastLessonId: string | null;
  lastLessonKey: string | null;
  lastPartIndex: number;
};

type PendingTechniqueAction =
  | { kind: 'set_part'; index: number }
  | { kind: 'part_offset'; offset: number }
  | { kind: 'complete_and_next' };

const SESSION_TECHNIQUE_OPTIONS: Record<string, SessionTechniqueOption> = {
  pomodoro: {
    key: 'pomodoro',
    label: 'Pomodoro',
    description: 'Activa bloques de 25 minutos con pausas cortas para mantener enfoque.',
  },
  'regla de 5 minutos': {
    key: 'regla de 5 minutos',
    label: 'Regla de 5 minutos',
    description: 'Empieza con una accion muy corta para romper la friccion inicial.',
  },
  'aprendizaje continuo': {
    key: 'aprendizaje continuo',
    label: 'Aprendizaje continuo',
    description: 'Prioriza avances pequenos y constantes dentro de la sesion.',
  },
  feynman: {
    key: 'feynman',
    label: 'Metodo Feynman',
    description: 'Te invita a explicar lo aprendido con palabras simples al cerrar cada parte.',
  },
  'repeticion espaciada': {
    key: 'repeticion espaciada',
    label: 'Repeticion espaciada',
    description: 'Marca conceptos clave para repasarlos despues en otros momentos.',
  },
  'active recall': {
    key: 'active recall',
    label: 'Active recall',
    description: 'Hace pausas para recordar primero y luego validar con el contenido.',
  },
  intercalado: {
    key: 'intercalado',
    label: 'Intercalado',
    description: 'Alterna partes de teoria y practica para evitar monotonia.',
  },
};

function parseLessonPartSummaries(content: string | null | undefined): LessonPartSummary[] {
  const raw = (content ?? '').trim();
  if (!raw) return [];

  return raw
    .split(/\n+---\n+/g)
    .map((chunk) => chunk.trim())
    .filter(Boolean)
    .map((chunk, index) => {
      const plainChunk = chunk.replace(/[_*]/g, '').trim().toLowerCase();
      if (plainChunk.startsWith('fuente oficial')) return null;

      const headingMatch = chunk.match(/^#{1,6}\s+(.+?)\s*$/m);
      return {
        id: `unit-${index}`,
        title: headingMatch?.[1]?.trim() || `Parte ${index + 1}`,
      };
    })
    .filter((part): part is LessonPartSummary => !!part);
}

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
export class CourseSessionComponent implements OnInit, OnDestroy {
  private readonly api = inject(ApiService);
  private readonly authStore = inject(AuthStore);

  readonly code = input.required<string>();

  protected readonly course = signal<CourseDetail | null>(null);
  protected readonly loading = signal(true);
  protected readonly activeLesson = signal<CourseLesson | null>(null);
  protected readonly activeUnitIndex = signal(0);
  protected readonly sessionTechnique = signal<string | null>(null);
  protected readonly sessionTechniqueConfirmed = signal(false);
  protected readonly pomodoroRunning = signal(false);
  protected readonly pomodoroSecondsLeft = signal(25 * 60);
  protected readonly methodologyDockOpen = signal(false);
  protected readonly methodologyReviewLoading = signal(false);
  protected readonly methodologyReviewResult = signal<LessonReviewResponse | null>(null);
  protected readonly methodologyCanContinue = signal(false);
  protected readonly methodologySkipCount = signal(0);
  protected readonly methodologySessionState = signal<MethodologySessionState | null>(null);

  // Tutor (sin sesión)
  protected readonly tutorOpen = signal(false);
  protected readonly tutorMode = signal<TutorMode>({ kind: 'general' });
  protected readonly chat = signal<LessonChatMessage[]>([]);
  protected readonly suggested = signal<string[]>([]);
  protected readonly tutorLoading = signal(false);
  protected tutorInput = '';

  // Progreso local (lecciones leídas)
  protected readonly readSet = signal<Set<string>>(new Set());
  protected readonly methodologyCheckpointSet = signal<Set<string>>(new Set());
  protected readonly lastLessonId = signal<string | null>(null);
  protected readonly lastLessonKey = signal<string | null>(null);
  protected readonly lastPartIndex = signal(0);
  protected readonly profile = computed(() => this.authStore.profile());
  protected readonly availableTechniques = computed(() => {
    const values = this.profile()?.study_techniques ?? [];
    const normalized = values
      .map((item) => item.trim().toLowerCase())
      .filter(Boolean);

    const unique = Array.from(new Set(normalized));
    return unique.map((key) => SESSION_TECHNIQUE_OPTIONS[key] ?? {
      key,
      label: key,
      description: 'Adaptaremos la sesion segun esta metodologia seleccionada en tu perfil.',
    });
  });
  protected readonly shouldChooseTechnique = computed(
    () => this.availableTechniques().length > 1 && !this.sessionTechniqueConfirmed(),
  );
  protected readonly activeTechniqueOption = computed(() => {
    const key = this.sessionTechnique();
    if (!key) return null;
    return SESSION_TECHNIQUE_OPTIONS[key] ?? {
      key,
      label: key,
      description: 'Adaptaremos esta sesion con esta metodologia seleccionada.',
    };
  });
  protected readonly pomodoroMinutes = computed(() =>
    String(Math.floor(this.pomodoroSecondsLeft() / 60)).padStart(2, '0'),
  );
  protected readonly pomodoroSeconds = computed(() =>
    String(this.pomodoroSecondsLeft() % 60).padStart(2, '0'),
  );
  protected readonly techniqueTips = computed(() => {
    switch (this.sessionTechnique()) {
      case 'pomodoro':
        return [
          'Enfocate solo en esta parte durante 25 minutos.',
          'Cuando el reloj termine, toma una pausa corta antes de continuar.',
        ];
      case 'regla de 5 minutos':
        return [
          'Empieza con una lectura o accion minima de cinco minutos.',
          'Cuando arranques, sigue con la siguiente parte sin reiniciar el contexto.',
        ];
      case 'aprendizaje continuo':
        return [
          'Divide cada parte en bloques pequenos para sostener progreso constante.',
          'Lee un bloque corto, revisa la nota de Reti y sigue con el siguiente sin saturarte.',
        ];
      case 'feynman':
        return [
          'Al terminar una parte, explica con tus palabras que entendiste.',
          'Si no puedes explicarlo facil, vuelve a revisar ese bloque.',
        ];
      case 'repeticion espaciada':
        return [
          'Identifica ideas clave para repasarlas despues.',
          'Usa las fuentes y objetivos como puntos de repaso futuros.',
        ];
      case 'active recall':
        return [
          'Antes de leer la siguiente parte, intenta recordar la anterior sin mirar.',
          'Valida luego tu respuesta con el contenido.',
        ];
      case 'intercalado':
        return [
          'Alterna lectura, ejemplos y practica durante la sesion.',
          'No te quedes demasiado tiempo en un solo formato.',
        ];
      default:
        return [];
    }
  });
  protected readonly methodologyButtonLabel = computed(
    () => this.activeTechniqueOption()?.label || 'Metodologia',
  );
  protected readonly activeSectionPartLabel = computed(() => {
    const sectionIndex = this.activeSectionIndex();
    const part = this.activePart();
    if (sectionIndex < 0 && !part) return 'Sesion en curso';
    if (sectionIndex < 0) return `Parte ${part!.index + 1}`;
    if (!part) return `Seccion ${sectionIndex + 1}`;
    return `Seccion ${sectionIndex + 1} - Parte ${part.index + 1}`;
  });
  protected readonly methodologyEffectivenessLabel = computed(() => {
    const state = this.methodologySessionState();
    if (!state) return 'Sin actividad registrada todavia.';

    const completed = state.acceptedCount;
    const skipped = state.skipCount;
    const retries = state.rejectedCount;

    if (!completed && !skipped && !retries) {
      return 'Aun no registramos respuestas en esta sesion.';
    }

    return `${completed} revisiones aprobadas, ${retries} ajustes y ${skipped}/2 saltos usados.`;
  });
  protected readonly isCheckpointTutorMode = computed(
    () => this.tutorMode().kind === 'checkpoint',
  );
  protected readonly dueSpacedEntry = computed(() => {
    if (this.sessionTechnique() !== 'repeticion espaciada') return null;
    const state = this.methodologySessionState();
    const lesson = this.activeLesson();
    if (!state || !lesson) return null;

    const currentLessonIndex = this.lessonIndex();
    return (
      state.entries.find((entry) => {
        if (entry.technique !== 'repeticion espaciada') return false;
        if (entry.skipped || entry.reviewStatus === 'remembered') return false;

        const entryLessonIndex = this.flatLessons().findIndex((candidate) => candidate.id === entry.lessonId);
        if (entryLessonIndex < 0) return false;

        if (entryLessonIndex < currentLessonIndex) return true;
        return entryLessonIndex === currentLessonIndex && entry.partIndex < this.activeUnitIndex();
      }) ?? null
    );
  });
  protected readonly tutorLauncherLabel = computed(() =>
    this.tutorOpen() ? 'Ocultar' : 'Abrir',
  );
  protected readonly tutorInputPlaceholder = computed(() => {
    const mode = this.tutorMode();
    return mode.kind === 'checkpoint' ? mode.placeholder : 'Escribe tu pregunta...';
  });
  protected readonly tutorSubmitLabel = computed(() => {
    const mode = this.tutorMode();
    return mode.kind === 'checkpoint' ? mode.confirmLabel : 'Enviar';
  });
  protected readonly tutorHeadline = computed(() => {
    const mode = this.tutorMode();
    if (mode.kind === 'checkpoint') return mode.title;
    return 'Reti tu tutor IA';
  });
  protected readonly tutorDescription = computed(() => {
    const mode = this.tutorMode();
    if (mode.kind === 'checkpoint') return mode.description;
    return 'Hazme preguntas sobre esta parte del curso y te respondo con el contexto real de la leccion.';
  });

  private pomodoroTimerId: ReturnType<typeof setInterval> | null = null;
  private pendingTechniqueAction: PendingTechniqueAction | null = null;
  private checkpointAdvanceTimerId: ReturnType<typeof setTimeout> | null = null;

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
  protected readonly activeSection = computed(() => {
    const active = this.activeLesson();
    if (!active) return null;
    return (
      this.sections().find((section) =>
        section.lessons.some((lesson) => lesson.id === active.id && lesson.lesson_key === active.lesson_key),
      ) ?? null
    );
  });
  protected readonly activeSectionIndex = computed(() => {
    const section = this.activeSection();
    if (!section) return -1;
    return this.sections().findIndex((item) => item.section_key === section.section_key);
  });
  protected readonly activeLessonParts = computed(() => parseLessonPartSummaries(this.activeLesson()?.content_md));
  protected readonly activePart = computed(() => {
    const parts = this.activeLessonParts();
    if (!parts.length) return null;
    const requested = this.activeUnitIndex();
    const index = Math.min(Math.max(requested, 0), parts.length - 1);
    return {
      part: parts[index],
      index,
      total: parts.length,
    };
  });

  constructor() {
    effect(() => {
      const profile = this.profile();
      const techniques = this.availableTechniques();
      if (!profile) return;

      if (!techniques.length) {
        if (!this.sessionTechnique()) {
          this.sessionTechniqueConfirmed.set(true);
        }
        return;
      }

      if (techniques.length === 1 && !this.sessionTechnique()) {
        this.sessionTechnique.set(techniques[0].key);
        this.sessionTechniqueConfirmed.set(true);
      }
    });
  }

  ngOnInit(): void {
    void this.load();
  }

  ngOnDestroy(): void {
    this.stopPomodoroTimer();
    this.clearCheckpointAdvanceTimer();
  }

  private storageKey(): string {
    return `retaim:read:${this.code()}`;
  }

  private methodologyStorageKey(): string {
    return `retaim:methodology:${this.code()}`;
  }

  private async load(): Promise<void> {
    this.loading.set(true);
    try {
      const course = await this.api.getCourse(this.code());
      this.course.set(course);
      this.restoreProgress();
      this.restoreMethodologySession();
      const target = this.findStoredLesson(course) ?? course.sections[0]?.lessons[0] ?? null;
      if (target) {
        await this.selectLesson(target, this.findStoredLesson(course) ? this.lastPartIndex() : 0);
      }
    } finally {
      this.loading.set(false);
    }
  }

  private restoreProgress(): void {
    try {
      const raw = localStorage.getItem(this.storageKey());
      if (!raw) return;

      const parsed = JSON.parse(raw) as string[] | StoredCourseProgress;
      if (Array.isArray(parsed)) {
        this.readSet.set(new Set(parsed));
        return;
      }

      this.readSet.set(new Set(parsed.readLessonIds ?? []));
      this.lastLessonId.set(parsed.lastLessonId ?? null);
      this.lastLessonKey.set(parsed.lastLessonKey ?? null);
      this.lastPartIndex.set(parsed.lastPartIndex ?? 0);
    } catch {
      /* sin persistencia */
    }
  }

  private persistProgress(): void {
    try {
      const payload: StoredCourseProgress = {
        readLessonIds: [...this.readSet()],
        lastLessonId: this.lastLessonId(),
        lastLessonKey: this.lastLessonKey(),
        lastPartIndex: this.lastPartIndex(),
      };
      localStorage.setItem(this.storageKey(), JSON.stringify(payload));
    } catch {
      /* sin persistencia */
    }
  }

  private findStoredLesson(course: CourseDetail): CourseLesson | null {
    const lessonId = this.lastLessonId();
    const lessonKey = this.lastLessonKey();
    if (!lessonId && !lessonKey) return null;

    for (const section of course.sections) {
      const found = section.lessons.find(
        (lesson) => lesson.id === lessonId || lesson.lesson_key === lessonKey,
      );
      if (found) return found;
    }
    return null;
  }

  private restoreMethodologySession(): void {
    try {
      const raw = localStorage.getItem(this.methodologyStorageKey());
      if (!raw) return;

      const parsed = JSON.parse(raw) as MethodologySessionState;
      this.methodologySessionState.set(parsed);
      this.methodologySkipCount.set(parsed.skipCount ?? 0);
      this.methodologyCheckpointSet.set(
        new Set(
          (parsed.entries ?? []).map(
            (entry) => `${entry.technique}:${entry.lessonId}:${entry.partIndex}`,
          ),
        ),
      );

      if (parsed.selectedTechnique) {
        this.sessionTechnique.set(parsed.selectedTechnique);
        this.sessionTechniqueConfirmed.set(true);
        if (parsed.selectedTechnique === 'pomodoro') this.resetPomodoro();
      }
    } catch {
      /* sin persistencia */
    }
  }

  private persistMethodologySession(): void {
    try {
      const current = this.methodologySessionState();
      if (current) {
        localStorage.setItem(this.methodologyStorageKey(), JSON.stringify(current));
      }
    } catch {
      /* sin persistencia */
    }
  }

  private ensureMethodologySessionState(): MethodologySessionState {
    const existing = this.methodologySessionState();
    if (existing) return existing;

    const next: MethodologySessionState = {
      selectedTechnique: this.sessionTechnique(),
      skipCount: this.methodologySkipCount(),
      reviewCount: 0,
      acceptedCount: 0,
      rejectedCount: 0,
      entries: [],
      startedAt: new Date().toISOString(),
    };
    this.methodologySessionState.set(next);
    return next;
  }

  private updateMethodologySessionState(
    updater: (current: MethodologySessionState) => MethodologySessionState,
  ): void {
    const current = this.ensureMethodologySessionState();
    const next = updater(current);
    this.methodologySessionState.set(next);
    this.methodologySkipCount.set(next.skipCount);
    this.persistMethodologySession();
  }

  protected isActive(lesson: CourseLesson): boolean {
    const a = this.activeLesson();
    return a?.id === lesson.id && a?.lesson_key === lesson.lesson_key;
  }

  protected isRead(lesson: CourseLesson): boolean {
    return !!lesson.id && this.readSet().has(lesson.id);
  }

  protected async selectLesson(lesson: CourseLesson, preferredPartIndex = 0): Promise<void> {
    this.activeLesson.set(lesson);
    this.lastLessonId.set(lesson.id ?? null);
    this.lastLessonKey.set(lesson.lesson_key ?? null);
    this.activeUnitIndex.set(0);
    this.chat.set([]);
    this.suggested.set([]);
    this.methodologyReviewResult.set(null);
    this.methodologyCanContinue.set(false);
    this.tutorMode.set({ kind: 'general' });
    this.clearCheckpointAdvanceTimer();
    this.setPartIndex(preferredPartIndex);
    this.persistProgress();
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
    if (this.openTechniqueCheckpointIfNeeded({ kind: 'complete_and_next' })) return;

    const lesson = this.activeLesson();
    const parts = this.activeLessonParts();
    if (parts.length && this.activeUnitIndex() < parts.length - 1) {
      this.setPartIndex(this.activeUnitIndex() + 1);
      return;
    }
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

  protected lessonParts(lesson: CourseLesson): LessonPartSummary[] {
    return parseLessonPartSummaries(lesson.content_md);
  }

  protected isActivePart(index: number): boolean {
    return this.activeUnitIndex() === index;
  }

  protected goToPart(index: number): void {
    if (index > this.activeUnitIndex() && this.openTechniqueCheckpointIfNeeded({ kind: 'set_part', index })) {
      return;
    }
    this.setPartIndex(index);
  }

  private setPartIndex(index: number): void {
    const parts = this.activeLessonParts();
    if (!parts.length) return;
    const nextIndex = Math.min(Math.max(index, 0), parts.length - 1);
    this.activeUnitIndex.set(nextIndex);
    this.lastPartIndex.set(nextIndex);
    this.persistProgress();
  }

  private buildSummaryMethodologyReview(text: string): LessonReviewResponse {
    const wantsChange =
      /cambiar|cambio|otro|otra|distinto|diferente|probar/i.test(text);

    return {
      lesson_id: this.activeLesson()?.id ?? '',
      accepted: text.trim().length >= 8,
      feedback: wantsChange
        ? 'Perfecto. Queda registrado que quieres probar otra metodologia en el siguiente tema.'
        : 'Perfecto. Queda registrado que esta metodologia te funciono bien para continuar.',
      reinforcement: wantsChange
        ? 'En el siguiente tema podemos volver a elegir una metodologia distinta para la sesion.'
        : 'Seguimos con esta metodologia en el siguiente tema para mantener continuidad.',
      source_mode: 'checkpoint',
    };
  }

  protected async goToPartOffset(offset: number): Promise<void> {
    if (offset > 0 && this.openTechniqueCheckpointIfNeeded({ kind: 'part_offset', offset })) return;

    const parts = this.activeLessonParts();
    if (!parts.length) return;
    const lessons = this.flatLessons();
    const lessonIndex = this.lessonIndex();

    const nextIndex = this.activeUnitIndex() + offset;
    if (nextIndex >= 0 && nextIndex < parts.length) {
      this.setPartIndex(nextIndex);
      return;
    }

    if (nextIndex < 0) {
      const previousLesson = lessonIndex > 0 ? lessons[lessonIndex - 1] : null;
      if (!previousLesson) return;
      await this.selectLesson(previousLesson);
      const previousParts = this.lessonParts(previousLesson);
      if (previousParts.length) this.activeUnitIndex.set(previousParts.length - 1);
      return;
    }

    const lesson = this.activeLesson();
    if (lesson?.id && !this.readSet().has(lesson.id)) this.toggleRead(lesson);
    const nextLesson = lessonIndex >= 0 && lessonIndex < lessons.length - 1 ? lessons[lessonIndex + 1] : null;
    if (!nextLesson) return;
    await this.selectLesson(nextLesson);
  }

  protected footerPreviousLabel(): string {
    return this.activeUnitIndex() > 0 ? 'Parte anterior' : 'Anterior';
  }

  protected footerNextLabel(): string {
    const parts = this.activeLessonParts();
    return this.activeUnitIndex() < parts.length - 1 ? 'Siguiente parte' : 'Siguiente';
  }

  protected canGoPreviousPart(): boolean {
    return this.activeUnitIndex() > 0 || this.lessonIndex() > 0;
  }

  protected canGoNextPart(): boolean {
    const parts = this.activeLessonParts();
    if (this.activeUnitIndex() < parts.length - 1) return true;
    return this.lessonIndex() < this.flatLessons().length - 1;
  }

  protected showContinueAction(): boolean {
    const parts = this.activeLessonParts();
    if (this.activeUnitIndex() < parts.length - 1) return true;
    return this.lessonIndex() < this.flatLessons().length - 1;
  }

  protected continueActionLabel(): string {
    const parts = this.activeLessonParts();
    return this.activeUnitIndex() < parts.length - 1 ? 'Completar y seguir con la parte' : 'Marcar y continuar';
  }

  protected chooseTechnique(techniqueKey: string): void {
    this.sessionTechnique.set(techniqueKey);
    this.sessionTechniqueConfirmed.set(true);
    this.methodologyDockOpen.set(false);
    this.updateMethodologySessionState((current) => ({
      ...current,
      selectedTechnique: techniqueKey,
    }));
    if (techniqueKey === 'pomodoro') {
      this.resetPomodoro();
    } else {
      this.stopPomodoroTimer();
    }
  }

  protected startOrPausePomodoro(): void {
    if (this.sessionTechnique() !== 'pomodoro') return;

    if (this.pomodoroRunning()) {
      this.stopPomodoroTimer();
      return;
    }

    this.pomodoroRunning.set(true);
    this.pomodoroTimerId = setInterval(() => {
      const next = this.pomodoroSecondsLeft() - 1;
      if (next <= 0) {
        this.pomodoroSecondsLeft.set(0);
        this.stopPomodoroTimer();
        return;
      }
      this.pomodoroSecondsLeft.set(next);
    }, 1000);
  }

  protected resetPomodoro(): void {
    this.stopPomodoroTimer();
    this.pomodoroSecondsLeft.set(25 * 60);
  }

  protected toggleMethodologyDock(): void {
    this.methodologyDockOpen.update((open) => !open);
  }

  protected closeMethodologyDock(): void {
    this.methodologyDockOpen.set(false);
  }

  protected async submitMethodologyPrompt(): Promise<void> {
    const text = this.tutorInput.trim();
    const lesson = this.activeLesson();
    const part = this.activePart();
    const technique = this.sessionTechnique();
    if (!text || !lesson?.id) return;

    this.chat.update((messages) => [
      ...messages,
      {
        id: null,
        role: 'user',
        content: text,
        sources: [],
        suggested_questions: [],
        source_mode: 'checkpoint',
        created_at: null,
      },
    ]);
    this.tutorInput = '';
    this.methodologyReviewLoading.set(true);
    this.methodologyReviewResult.set(null);
    this.methodologyCanContinue.set(false);

    try {
      const result = this.isSummaryCheckpoint()
        ? this.buildSummaryMethodologyReview(text)
        : technique === 'repeticion espaciada'
          ? {
              lesson_id: lesson.id,
              accepted: text.trim().length >= 8,
              feedback: 'Perfecto. Guardé esta idea como repaso para retomarla más adelante.',
              reinforcement: 'Te la volveré a mostrar en las siguientes partes para que confirmes si ya la recuerdas.',
              source_mode: 'checkpoint',
            }
        : await this.api.reviewLessonExplanation(lesson.id, {
            explanation: text,
            part_title: part?.part.title ?? lesson.title,
            technique,
          });

      this.methodologyReviewResult.set(result);
      this.updateMethodologySessionState((current) => ({
        ...current,
        selectedTechnique: technique,
        reviewCount: current.reviewCount + 1,
        acceptedCount: current.acceptedCount + (result.accepted ? 1 : 0),
        rejectedCount: current.rejectedCount + (result.accepted ? 0 : 1),
        entries: [
          ...current.entries,
          {
            lessonId: lesson.id!,
            lessonTitle: lesson.title,
            partIndex: part?.index ?? 0,
            partTitle: part?.part.title ?? lesson.title,
            sectionIndex: Math.max(this.activeSectionIndex(), 0),
            technique: technique ?? 'general',
            explanation: text,
            accepted: result.accepted,
            skipped: false,
            feedback: result.feedback,
            reinforcement: result.reinforcement,
            reviewedAt: new Date().toISOString(),
            reviewStatus: technique === 'repeticion espaciada' ? 'pending' : undefined,
          },
        ],
      }));

      if (result.accepted) {
        this.methodologyCanContinue.set(true);
        this.clearCheckpointAdvanceTimer();
        this.checkpointAdvanceTimerId = setTimeout(() => {
          this.continueAfterMethodologyReview();
        }, 1600);
      }
    } finally {
      this.methodologyReviewLoading.set(false);
    }
  }

  protected skipMethodologyPrompt(): void {
    if (this.methodologySkipCount() >= 2) return;

    const lesson = this.activeLesson();
    const part = this.activePart();
    const technique = this.sessionTechnique();

    this.updateMethodologySessionState((current) => ({
      ...current,
      selectedTechnique: technique,
      skipCount: current.skipCount + 1,
      entries: lesson?.id
        ? [
            ...current.entries,
            {
              lessonId: lesson.id,
              lessonTitle: lesson.title,
              partIndex: part?.index ?? 0,
              partTitle: part?.part.title ?? lesson.title,
              sectionIndex: Math.max(this.activeSectionIndex(), 0),
              technique: technique ?? 'general',
              explanation: '',
              accepted: false,
              skipped: true,
              feedback: 'El usuario omitio este checkpoint.',
              reinforcement: null,
              reviewedAt: new Date().toISOString(),
            },
          ]
        : current.entries,
    }));

    this.finishTechniqueCheckpoint();
  }

  protected continueAfterMethodologyReview(): void {
    if (!this.methodologyCanContinue()) return;
    this.finishTechniqueCheckpoint();
  }

  protected async sendTutor(text?: string): Promise<void> {
    if (this.isCheckpointTutorMode()) {
      const value = text?.trim();
      if (value) this.tutorInput = value;
      await this.submitMethodologyPrompt();
      return;
    }

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

  protected openTutorAssistant(): void {
    this.tutorOpen.set(true);
    if (!this.chat().length && !this.isCheckpointTutorMode()) {
      this.chat.set([
        {
          id: null,
          role: 'assistant',
          content:
            'Soy Reti, tu tutor IA. Si tienes cualquier duda sobre esta parte del curso, pegala aqui y la revisamos juntos.',
          sources: [],
          suggested_questions: [],
          source_mode: 'mock',
          created_at: null,
        },
      ]);
    }
  }

  protected levelLabel(level: string): string {
    return { basic: 'Básico', intermediate: 'Intermedio', advanced: 'Avanzado' }[level] ?? level;
  }

  protected sectionProgress(section: CourseSectionContent): number {
    const total = section.lessons.length;
    if (!total) return 0;
    const read = section.lessons.filter((lesson) => this.isRead(lesson)).length;
    return Math.round((read / total) * 100);
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

  protected trackLesson(_: number, lesson: CourseLesson): string {
    return lesson.id ?? lesson.lesson_key;
  }

  protected updateSpacedReview(status: 'remembered' | 'later'): void {
    const dueEntry = this.dueSpacedEntry();
    if (!dueEntry) return;

    this.updateMethodologySessionState((current) => ({
      ...current,
      entries: current.entries.map((entry) =>
        entry.reviewedAt === dueEntry.reviewedAt && entry.lessonId === dueEntry.lessonId
          ? { ...entry, reviewStatus: status }
          : entry,
      ),
    }));
  }

  protected isCompletedPart(lesson: CourseLesson, partIndex: number): boolean {
    if (this.isRead(lesson)) return true;
    if (!this.isActive(lesson)) return false;
    return partIndex < this.activeUnitIndex();
  }

  private isSummaryCheckpoint(): boolean {
    const lesson = this.activeLesson();
    const part = this.activePart()?.part;
    const text = `${lesson?.title ?? ''} ${part?.title ?? ''}`.toLowerCase();
    return text.includes('summary') || text.includes('resumen');
  }

  private checkpointKey(): string | null {
    const lesson = this.activeLesson();
    const technique = this.sessionTechnique();
    if (!lesson || !technique) return null;
    return `${technique}:${lesson.id ?? lesson.lesson_key}:${this.activeUnitIndex()}`;
  }

  private openTechniqueCheckpointIfNeeded(action: PendingTechniqueAction): boolean {
    const technique = this.sessionTechnique();
    if (technique !== 'active recall' && technique !== 'feynman' && technique !== 'repeticion espaciada') return false;

    const key = this.checkpointKey();
    if (!key || this.methodologyCheckpointSet().has(key)) return false;

    this.pendingTechniqueAction = action;
    this.methodologyReviewResult.set(null);
    this.methodologyCanContinue.set(false);
    const config: MethodologyPromptConfig =
      technique === 'active recall'
        ? {
            title: this.isSummaryCheckpoint() ? 'Cierre de active recall' : 'Checkpoint de active recall',
            description: this.isSummaryCheckpoint()
              ? 'Llegaste al resumen. Como te parecio estudiar con active recall en esta sesion. Quieres mantenerlo para el siguiente tema o prefieres cambiar?'
              : 'Veo que elegiste active recall. Sin mirar el contenido, cuentame las ideas clave que recuerdas antes de seguir.',
            placeholder: this.isSummaryCheckpoint()
              ? 'Cuéntame si este metodo te sirvio o si prefieres cambiarlo...'
              : 'Escribe aqui lo que recuerdas de esta parte...',
            confirmLabel: this.isSummaryCheckpoint() ? 'Guardar preferencia' : 'Revisar resumen',
          }
        : technique === 'feynman'
          ? {
            title: this.isSummaryCheckpoint() ? 'Cierre del metodo Feynman' : 'Checkpoint del metodo Feynman',
            description: this.isSummaryCheckpoint()
              ? 'Llegaste al resumen. Como te parecio estudiar con el metodo Feynman. Quieres seguir con este metodo en el siguiente tema o prefieres cambiar?'
              : 'Veo que elegiste el metodo Feynman. Explicame esta parte con palabras simples, como si se la contaras a otra persona.',
            placeholder: this.isSummaryCheckpoint()
              ? 'Cuéntame si este metodo te funciono para el siguiente tema...'
              : 'Explica aqui con palabras simples...',
            confirmLabel: this.isSummaryCheckpoint() ? 'Guardar preferencia' : 'Revisar explicacion',
          }
          : {
            title: this.isSummaryCheckpoint() ? 'Cierre de repeticion espaciada' : 'Checkpoint de repeticion espaciada',
            description: this.isSummaryCheckpoint()
              ? 'Llegaste al resumen. Como te parecio estudiar con repeticion espaciada. Quieres mantener este metodo o probar otro en el siguiente tema?'
              : 'Antes de seguir, escribe la idea clave de esta parte que te conviene repasar despues. La guardaremos para mostrarla otra vez mas adelante.',
            placeholder: this.isSummaryCheckpoint()
              ? 'Cuéntame si este metodo te ayudo para el siguiente tema...'
              : 'Escribe la idea clave que quieres repasar despues...',
            confirmLabel: this.isSummaryCheckpoint() ? 'Guardar preferencia' : 'Guardar repaso',
          };

    this.tutorMode.set({
      kind: 'checkpoint',
      title: config.title,
      description: config.description,
      placeholder: config.placeholder,
      confirmLabel: config.confirmLabel,
    });
    this.tutorInput = '';
    this.tutorOpen.set(true);
    this.chat.set([
      {
        id: null,
        role: 'assistant',
        content: this.isSummaryCheckpoint()
          ? 'Soy tu tutor para este cierre. Cuéntame cómo te funcionó esta metodología y te ayudo a decidir si mantenerla o cambiarla en el siguiente tema.'
          : technique === 'active recall'
            ? 'Soy tu tutor para este checkpoint. Cuentame que recuerdas de esta parte y te dire si vas bien o si conviene ajustar algo.'
            : technique === 'feynman'
              ? 'Soy tu tutor para este checkpoint. Cuentame esta parte con palabras simples y te dire si la explicacion va en la direccion correcta.'
              : 'Soy tu tutor para este checkpoint. Guarda aqui la idea clave que quieras repasar luego y la traeremos de vuelta mas adelante.',
        sources: [],
        suggested_questions: [],
        source_mode: 'checkpoint',
        created_at: null,
      },
    ]);
    return true;
  }

  private finishTechniqueCheckpoint(): void {
    const key = this.checkpointKey();
    if (key) {
      this.methodologyCheckpointSet.update((current) => new Set([...current, key]));
    }

    this.methodologyReviewResult.set(null);
    this.methodologyCanContinue.set(false);
    this.tutorMode.set({ kind: 'general' });
    this.tutorInput = '';
    this.tutorOpen.set(false);
    this.clearCheckpointAdvanceTimer();

    const action = this.pendingTechniqueAction;
    this.pendingTechniqueAction = null;
    if (!action) return;

    if (action.kind === 'set_part') {
      this.setPartIndex(action.index);
      return;
    }

    if (action.kind === 'part_offset') {
      void this.goToPartOffset(action.offset);
      return;
    }

    this.completeAndNext();
  }

  private stopPomodoroTimer(): void {
    if (this.pomodoroTimerId) {
      clearInterval(this.pomodoroTimerId);
      this.pomodoroTimerId = null;
    }
    this.pomodoroRunning.set(false);
  }

  private clearCheckpointAdvanceTimer(): void {
    if (this.checkpointAdvanceTimerId) {
      clearTimeout(this.checkpointAdvanceTimerId);
      this.checkpointAdvanceTimerId = null;
    }
  }
}
