import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, ElementRef, OnDestroy, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthStore } from '../../core/auth/auth.store';
import { ApiService } from '../../core/services/api.service';
import { AppIconComponent } from '../../shared/components/app-icon.component';

type IntakeKey =
  | 'professional_role'
  | 'age_range'
  | 'weekly_hours_available'
  | 'preferred_time'
  | 'learning_style'
  | 'content_preferences'
  | 'technology_experience'
  | 'learning_goals'
  | 'study_techniques';

type IntakeQuestion = {
  key: IntakeKey;
  title: string;
  prompt: string;
  placeholder: string;
  quickReplies?: string[];
};

type IntakeMessage = {
  id: number;
  role: 'ai' | 'user' | 'status';
  text: string;
};

const INTAKE_QUESTIONS: IntakeQuestion[] = [
  {
    key: 'professional_role',
    title: 'Tu rol actual',
    prompt: 'Empecemos por tu rol actual dentro del equipo o de la organizacion.',
    placeholder: 'Ejemplo: Backend Developer',
    quickReplies: ['Backend Developer', 'Team Lead', 'QA Engineer'],
  },
  {
    key: 'age_range',
    title: 'Rango de edad',
    prompt: 'Para adaptar mejor el ritmo, dime tu rango de edad aproximado.',
    placeholder: 'Ejemplo: 25-34',
    quickReplies: ['18-24', '25-34', '35-44'],
  },
  {
    key: 'weekly_hours_available',
    title: 'Disponibilidad semanal',
    prompt: 'Cuantas horas reales por semana puedes dedicar al aprendizaje.',
    placeholder: 'Ejemplo: 6',
    quickReplies: ['4', '6', '8'],
  },
  {
    key: 'preferred_time',
    title: 'Horario ideal',
    prompt: 'En que momento del dia aprendes mejor o te resulta mas facil estudiar.',
    placeholder: 'Ejemplo: night',
    quickReplies: ['morning', 'afternoon', 'night'],
  },
  {
    key: 'learning_style',
    title: 'Preferencia de aprendizaje',
    prompt: 'Que formato te ayuda mas a aprender. Puedes combinar video, textos, practica o ejemplos de codigo.',
    placeholder: 'Ejemplo: practica, video',
    quickReplies: ['practica, video', 'textos, ejemplos', 'mixto'],
  },
  {
    key: 'content_preferences',
    title: 'Contenido que mas valoras',
    prompt: 'Que tipo de contenido te interesa mas cuando estudias un tema tecnico.',
    placeholder: 'Ejemplo: labs reales y casos de uso',
  },
  {
    key: 'technology_experience',
    title: 'Experiencia tecnica',
    prompt: 'Que tecnologias ya manejas o en cuales tienes algo de experiencia.',
    placeholder: 'Ejemplo: JavaScript, Azure, Docker',
  },
  {
    key: 'learning_goals',
    title: 'Lo que quieres aprender',
    prompt: 'Que te gustaria aprender o profundizar durante esta etapa.',
    placeholder: 'Ejemplo: arquitectura cloud y automatizacion',
  },
  {
    key: 'study_techniques',
    title: 'Tecnicas de estudio',
    prompt: 'Que tecnicas usas o te gustaria probar. Puede ser pomodoro, regla de 5 minutos, aprendizaje continuo o algo propio.',
    placeholder: 'Ejemplo: pomodoro y bloques cortos',
    quickReplies: ['pomodoro', 'regla de 5 minutos', 'aprendizaje continuo'],
  },
];

@Component({
  selector: 'app-onboarding-page',
  standalone: true,
  imports: [CommonModule, FormsModule, AppIconComponent],
  templateUrl: './onboarding-page.component.html',
  styleUrl: './onboarding-page.component.css',
})
export class OnboardingPageComponent implements AfterViewInit, OnDestroy {
  private readonly api = inject(ApiService);
  private readonly authStore = inject(AuthStore);
  private readonly router = inject(Router);
  private readonly host = inject(ElementRef<HTMLElement>);

  protected readonly profile = computed(() => this.authStore.profile());
  protected readonly messages = signal<IntakeMessage[]>([]);
  protected readonly currentQuestionIndex = signal(0);
  protected readonly answers = signal<Record<string, string>>({});
  protected readonly typingActive = signal(false);
  protected readonly agentBusy = signal(false);
  protected readonly error = signal<string | null>(null);
  protected readonly completed = signal(false);
  protected readonly totalQuestions = INTAKE_QUESTIONS.length;
  protected readonly progressStages = Array.from({ length: this.totalQuestions }, (_, index) => index + 1);
  protected readonly currentQuestion = computed(() => INTAKE_QUESTIONS[this.currentQuestionIndex()] ?? null);
  protected readonly currentStepNumber = computed(() => Math.min(this.currentQuestionIndex() + 1, this.totalQuestions));
  protected readonly quickReplies = computed(() => this.currentQuestion()?.quickReplies ?? []);
  protected readonly stepLabel = computed(() => `Step ${this.currentStepNumber()} of ${this.totalQuestions}`);
  protected readonly progressTrackPercent = computed(() => ((this.currentStepNumber() - 1) / (this.totalQuestions - 1)) * 100);
  protected readonly chatPlaceholder = computed(() => this.currentQuestion()?.placeholder ?? 'Listo');

  protected draftReply = '';

  private readonly storageKey = computed(() => `retaim-intake-${this.profile()?.id || 'guest'}`);
  private messageId = 0;
  private scrollFrame = 0;
  private hudAnimationFrame = 0;
  private waveformSpeaking = false;
  private waveformPhase = 0;
  private waveformIntensity = 0;
  private resizeHandler = () => this.resizeHudCanvas();

  constructor() {
    this.restoreState();
    void this.startAgent();
  }

  ngAfterViewInit(): void {
    this.resizeHudCanvas();
    this.drawHudLoop();
    window.addEventListener('resize', this.resizeHandler);
  }

  ngOnDestroy(): void {
    cancelAnimationFrame(this.scrollFrame);
    cancelAnimationFrame(this.hudAnimationFrame);
    window.removeEventListener('resize', this.resizeHandler);
  }

  protected async submit(): Promise<void> {
    const question = this.currentQuestion();
    const value = this.draftReply.trim();
    if (!question || !value || this.agentBusy()) {
      return;
    }

    this.pushMessage('user', value);
    this.draftReply = '';
    let finalAnswer = value;

    if (this.shouldUseAssist(question.key, value)) {
      const assist = await this.api.assistAgentIntake({
        question_key: question.key,
        question_title: question.title,
        question_prompt: question.prompt,
        user_message: value,
        collected_answers: this.answers(),
      });

      if (Object.keys(assist.extracted_answers).length) {
        this.answers.update((current) => ({ ...current, ...assist.extracted_answers }));
        this.persistState();
      }

      await this.deliverAiMessage(assist.message);
      if (!assist.should_advance || !assist.normalized_answer) {
        return;
      }
      finalAnswer = assist.normalized_answer;
      this.answers.update((current) => ({
        ...current,
        ...assist.extracted_answers,
        [question.key]: finalAnswer,
      }));
    } else {
      finalAnswer = this.normalizeLocalAnswer(question.key, value);
      this.answers.update((current) => ({ ...current, [question.key]: finalAnswer }));
      await this.deliverAiMessage(this.buildConfirmation(question.title, finalAnswer));
    }
    this.persistState();

    const nextIndex = this.currentQuestionIndex() + 1;
    this.currentQuestionIndex.set(nextIndex);
    this.persistState();

    if (nextIndex >= INTAKE_QUESTIONS.length) {
      await this.finish();
      return;
    }

    await this.deliverAiMessage(INTAKE_QUESTIONS[nextIndex].prompt);
  }

  protected useQuickReply(value: string): void {
    if (this.agentBusy()) {
      return;
    }
    this.draftReply = value;
    void this.submit();
  }

  private async startAgent(): Promise<void> {
    if (this.messages().length) {
      if (this.currentQuestion()) {
        await this.deliverAiMessage(
          `Retomemos donde quedamos. ${this.currentQuestion()!.prompt}`,
          { skipIfMessagesExist: true },
        );
      }
      return;
    }

    const name = this.profile()?.full_name || 'equipo';
    await this.deliverAiMessage(
      `Hola ${name}. Voy a registrar tu perfil de aprendizaje inicial para personalizar mejor tus certificaciones y sesiones.`,
    );
    await this.deliverAiMessage(this.currentQuestion()!.prompt);
  }

  private async finish(): Promise<void> {
    this.agentBusy.set(true);
    this.error.set(null);
    this.pushMessage('status', 'Guardando tu perfil inicial...');

    try {
      const answers = this.answers();
      const learningStyle = this.normalizeLearningStyle(answers['learning_style'] || '');
      await this.api.saveAgentIntake({
        professional_role: answers['professional_role'] || this.profile()?.professional_role || 'Profesional',
        weekly_hours_available: Math.max(1, Number((answers['weekly_hours_available'] || '6').replace(/[^\d]/g, '')) || 6),
        preferred_time: this.normalizePreferredTime(answers['preferred_time'] || 'night'),
        learning_style: learningStyle,
        target_certification: this.profile()?.target_certification || null,
        answers: INTAKE_QUESTIONS.map((question) => ({
          key: question.key,
          title: question.title,
          answer: answers[question.key] || '',
        })),
      });
      await this.authStore.refreshProfile();
      window.localStorage.removeItem(this.storageKey());
      this.completed.set(true);
      await this.deliverAiMessage('Perfecto. Tu perfil de aprendizaje inicial ya quedo listo.');
      await this.router.navigate([this.profile()?.role === 'manager' ? '/manager/dashboard' : '/dashboard']);
    } catch (error) {
      this.error.set(error instanceof Error ? error.message : 'No se pudo guardar el perfil inicial.');
    } finally {
      this.agentBusy.set(false);
    }
  }

  private restoreState(): void {
    const profile = this.profile();
    if (!profile || profile.onboarding_completed_at) {
      return;
    }
    const raw = window.localStorage.getItem(this.storageKey());
    if (!raw) {
      const seededAnswers: Record<string, string> = {};
      if (profile.professional_role) {
        seededAnswers['professional_role'] = profile.professional_role;
      }
      if (profile.weekly_hours_available) {
        seededAnswers['weekly_hours_available'] = String(profile.weekly_hours_available);
      }
      if (profile.preferred_time) {
        seededAnswers['preferred_time'] = profile.preferred_time;
      }
      if (profile.learning_style?.length) {
        seededAnswers['learning_style'] = profile.learning_style.join(', ');
      }
      this.answers.set(seededAnswers);
      this.currentQuestionIndex.set(this.getNextQuestionIndex(seededAnswers));
      return;
    }
    try {
      const parsed = JSON.parse(raw) as { answers?: Record<string, string>; currentQuestionIndex?: number };
      const restoredAnswers = parsed.answers || {};
      this.answers.set(restoredAnswers);
      this.currentQuestionIndex.set(this.getNextQuestionIndex(restoredAnswers));
    } catch {
      window.localStorage.removeItem(this.storageKey());
    }
  }

  private getNextQuestionIndex(answers: Record<string, string>): number {
    const nextIndex = INTAKE_QUESTIONS.findIndex((question) => !answers[question.key]?.trim());
    return nextIndex === -1 ? INTAKE_QUESTIONS.length - 1 : nextIndex;
  }

  private persistState(): void {
    window.localStorage.setItem(
      this.storageKey(),
      JSON.stringify({
        answers: this.answers(),
        currentQuestionIndex: this.currentQuestionIndex(),
      }),
    );
  }

  private pushMessage(role: IntakeMessage['role'], text: string): void {
    this.messages.update((current) => [...current, { id: ++this.messageId, role, text }]);
    this.scheduleScrollToBottom();
  }

  private async deliverAiMessage(
    text: string,
    options: { typingMs?: number; wordMs?: number; skipIfMessagesExist?: boolean } = {},
  ): Promise<void> {
    if (options.skipIfMessagesExist && this.messages().some((message) => message.text.includes(text))) {
      return;
    }
    this.agentBusy.set(true);
    this.typingActive.set(true);
    this.waveformSpeaking = true;
    this.scheduleScrollToBottom();
    await this.sleep(options.typingMs ?? 1100);
    this.typingActive.set(false);

    const id = ++this.messageId;
    this.messages.update((current) => [...current, { id, role: 'ai', text: '' }]);
    const words = text.split(' ');
    for (const word of words) {
      this.messages.update((current) =>
        current.map((message) =>
          message.id === id ? { ...message, text: `${message.text}${message.text ? ' ' : ''}${word}` } : message,
        ),
      );
      this.scheduleScrollToBottom();
      await this.sleep(options.wordMs ?? 34);
    }
    this.waveformSpeaking = false;
    this.agentBusy.set(false);
  }

  private buildConfirmation(title: string, answer: string): string {
    return `Entiendo. Registre ${title.toLowerCase()} como ${answer}.`;
  }

  private shouldUseAssist(questionKey: IntakeKey, value: string): boolean {
    const lowered = value.trim().toLowerCase();
    if (
      value.includes('?') ||
      lowered.startsWith('que ') ||
      lowered.startsWith('qué ') ||
      lowered.startsWith('como ') ||
      lowered.startsWith('cómo ') ||
      lowered.startsWith('cual ') ||
      lowered.startsWith('cuál ') ||
      lowered.startsWith('puedo ') ||
      lowered.startsWith('debo ')
    ) {
      return true;
    }

    if (questionKey === 'weekly_hours_available') {
      return !/\d/.test(value);
    }
    if (questionKey === 'preferred_time') {
      return !this.tryNormalizePreferredTime(value);
    }
    if (questionKey === 'learning_style') {
      return !this.normalizeLearningStyle(value).length;
    }
    if (questionKey === 'age_range') {
      return !this.tryNormalizeAgeRange(value);
    }
    return false;
  }

  private normalizeLocalAnswer(questionKey: IntakeKey, value: string): string {
    if (questionKey === 'weekly_hours_available') {
      return String(Math.max(1, Number(value.replace(/[^\d]/g, '')) || 6));
    }
    if (questionKey === 'preferred_time') {
      return this.tryNormalizePreferredTime(value) || 'night';
    }
    if (questionKey === 'learning_style') {
      return this.normalizeLearningStyle(value).join(', ');
    }
    if (questionKey === 'age_range') {
      return this.tryNormalizeAgeRange(value) || value.trim();
    }
    return value.trim();
  }

  private normalizeLearningStyle(rawValue: string): string[] {
    const normalized = rawValue
      .toLowerCase()
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);
    if (!normalized.length) {
      return ['mixed'];
    }
    return normalized;
  }

  private normalizePreferredTime(rawValue: string): 'morning' | 'afternoon' | 'night' {
    return this.tryNormalizePreferredTime(rawValue) || 'night';
  }

  private tryNormalizePreferredTime(rawValue: string): 'morning' | 'afternoon' | 'night' | null {
    const normalized = rawValue.toLowerCase();
    if (normalized.includes('morn') || normalized.includes('mañ')) {
      return 'morning';
    }
    if (normalized.includes('after') || normalized.includes('tarde')) {
      return 'afternoon';
    }
    if (normalized.includes('night') || normalized.includes('noche')) {
      return 'night';
    }
    return null;
  }

  private tryNormalizeAgeRange(rawValue: string): string | null {
    const trimmed = rawValue.trim();
    if (/^\d{2}\s*-\s*\d{2}$/.test(trimmed)) {
      return trimmed.replace(/\s+/g, '');
    }
    const digits = Number(trimmed.replace(/[^\d]/g, ''));
    if (!digits) {
      return null;
    }
    if (digits >= 18 && digits <= 24) {
      return '18-24';
    }
    if (digits >= 25 && digits <= 34) {
      return '25-34';
    }
    if (digits >= 35 && digits <= 44) {
      return '35-44';
    }
    if (digits >= 45 && digits <= 54) {
      return '45-54';
    }
    if (digits >= 55) {
      return '55+';
    }
    return null;
  }

  private scheduleScrollToBottom(): void {
    cancelAnimationFrame(this.scrollFrame);
    this.scrollFrame = requestAnimationFrame(() => {
      const container = this.host.nativeElement.querySelector('.chat-messages') as HTMLDivElement | null;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    });
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  }

  private resizeHudCanvas(): void {
    const canvas = this.host.nativeElement.querySelector('#hud-canvas') as HTMLCanvasElement | null;
    if (!canvas) {
      return;
    }
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.floor(rect.width * ratio));
    canvas.height = Math.max(1, Math.floor(rect.height * ratio));
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }
  }

  private drawHudLoop(): void {
    const canvas = this.host.nativeElement.querySelector('#hud-canvas') as HTMLCanvasElement | null;
    if (!canvas) {
      return;
    }
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      return;
    }

    const render = () => {
      const ratio = window.devicePixelRatio || 1;
      const width = canvas.width / ratio;
      const height = canvas.height / ratio;
      ctx.clearRect(0, 0, width, height);

      this.waveformPhase += 0.045;
      if (this.waveformSpeaking) {
        this.waveformIntensity = Math.min(1, this.waveformIntensity + 0.04);
      } else {
        this.waveformIntensity = Math.max(0.18, this.waveformIntensity - 0.02);
      }

      const cy = height / 2;
      const x0 = 20;
      const x1 = width - 20;
      const len = x1 - x0;
      const nPts = 200;
      const layers = [
        { amp: 36, freq: 2.8, speed: 1.0, alpha: 0.82, lw: 2.2, blur: 14 },
        { amp: 22, freq: 5.1, speed: 1.6, alpha: 0.48, lw: 1.2, blur: 8 },
        { amp: 14, freq: 8.3, speed: 2.4, alpha: 0.24, lw: 0.8, blur: 4 },
      ];

      layers.forEach(({ amp, freq, speed, alpha, lw, blur }) => {
        ctx.beginPath();
        for (let i = 0; i <= nPts; i += 1) {
          const t = i / nPts;
          const x = x0 + t * len;
          const envelope = Math.sin(Math.PI * t);
          const y =
            cy +
            Math.sin(t * Math.PI * 2 * freq + this.waveformPhase * speed) *
              amp *
              this.waveformIntensity *
              envelope;
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        const gradient = ctx.createLinearGradient(x0, 0, x1, 0);
        gradient.addColorStop(0, `rgba(168,85,247,0)`);
        gradient.addColorStop(0.2, `rgba(168,85,247,${alpha})`);
        gradient.addColorStop(0.5, `rgba(216,180,254,${alpha})`);
        gradient.addColorStop(0.8, `rgba(168,85,247,${alpha})`);
        gradient.addColorStop(1, `rgba(168,85,247,0)`);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = lw;
        ctx.shadowColor = '#a855f7';
        ctx.shadowBlur = blur * this.waveformIntensity;
        ctx.stroke();
        ctx.shadowBlur = 0;
      });

      this.hudAnimationFrame = requestAnimationFrame(render);
    };

    render();
  }
}
