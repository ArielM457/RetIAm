import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  computed,
  inject,
  signal,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthStore } from '../../core/auth/auth.store';
import {
  ApiService,
  CertificationSummary,
  ManagerMemberDetailResponse,
  TeamAccessCodeSummary,
  TeamMemberSummary,
  TeamSummary,
} from '../../core/services/api.service';
import { AppIconComponent } from '../../shared/components/app-icon.component';

type SetupQuestionKey =
  | 'professional_role'
  | 'organization_name'
  | 'team_name'
  | 'sector'
  | 'member_capacity'
  | 'work_style'
  | 'notes';

type AgentMessage = {
  id: number;
  role: 'ai' | 'user' | 'status';
  text: string;
};

type SetupQuestion = {
  key: SetupQuestionKey;
  title: string;
  prompt: string;
  placeholder: string;
  quickReplies?: string[];
};

type SetupAnswers = Record<SetupQuestionKey, string>;

const SETUP_QUESTIONS: SetupQuestion[] = [
  {
    key: 'professional_role',
    title: 'Tu rol dentro del equipo',
    prompt:
      'Quiero empezar por ti. Dime cual es tu rol dentro del equipo o la organizacion.',
    placeholder: 'Ejemplo: Engineering Manager',
    quickReplies: ['Engineering Manager', 'Team Lead', 'Project Manager'],
  },
  {
    key: 'organization_name',
    title: 'Nombre de la organizacion',
    prompt:
      'Ahora necesito el nombre de la empresa, startup o area principal para dejar bien registrado el contexto.',
    placeholder: 'Ejemplo: RetAIM Labs',
  },
  {
    key: 'team_name',
    title: 'Nombre del equipo',
    prompt: 'Perfecto. Como se llama el equipo que vas a liderar dentro de la plataforma.',
    placeholder: 'Ejemplo: Equipo Plataforma Cloud',
  },
  {
    key: 'sector',
    title: 'Rubro o sector',
    prompt:
      'Que rubro describe mejor el trabajo del equipo. Puede ser tecnologia, producto, ventas, soporte o algo mas especifico.',
    placeholder: 'Ejemplo: Tecnologia educativa',
    quickReplies: ['Tecnologia', 'Producto', 'Soporte'],
  },
  {
    key: 'member_capacity',
    title: 'Cantidad de personas',
    prompt:
      'Cuantas personas planeas tener aproximadamente en el equipo. Dame un numero para preparar el seguimiento.',
    placeholder: 'Ejemplo: 8',
    quickReplies: ['5', '8', '12'],
  },
  {
    key: 'work_style',
    title: 'Modalidad de trabajo',
    prompt:
      'Como trabajan normalmente. Me sirve una frase corta como remoto, hibrido, presencial o algo mas puntual.',
    placeholder: 'Ejemplo: Hibrido con reuniones semanales',
    quickReplies: ['Remoto', 'Hibrido', 'Presencial'],
  },
  {
    key: 'notes',
    title: 'Contexto adicional',
    prompt:
      'Ultimo punto. Si quieres, agrega una nota breve sobre metas, retos o contexto del equipo. Si no hay nada, escribe sin notas.',
    placeholder: 'Ejemplo: Equipo nuevo con foco en certificaciones Azure',
    quickReplies: ['Sin notas'],
  },
];

@Component({
  selector: 'app-manager-team-page',
  standalone: true,
  imports: [CommonModule, FormsModule, AppIconComponent],
  templateUrl: './manager-team-page.component.html',
  styleUrl: './manager-team-page.component.css',
})
export class ManagerTeamPageComponent implements AfterViewInit, OnDestroy {
  private readonly api = inject(ApiService);
  protected readonly authStore = inject(AuthStore);
  private readonly host = inject(ElementRef<HTMLElement>);
  private readonly router = inject(Router);

  protected readonly profile = computed(() => this.authStore.profile());
  protected readonly loading = signal(false);
  protected readonly setupSubmitting = signal(false);
  protected readonly teams = signal<TeamSummary[]>([]);
  protected readonly members = signal<TeamMemberSummary[]>([]);
  protected readonly catalog = signal<CertificationSummary[]>([]);
  protected readonly selectedMember = signal<ManagerMemberDetailResponse | null>(null);
  protected readonly selectedTeam = signal<TeamSummary | null>(null);
  protected readonly accessCode = signal<TeamAccessCodeSummary | null>(null);
  protected readonly messages = signal<AgentMessage[]>([]);
  protected readonly currentQuestionIndex = signal(0);
  protected readonly setupAnswers = signal<SetupAnswers>({
    professional_role: '',
    organization_name: '',
    team_name: '',
    sector: '',
    member_capacity: '',
    work_style: '',
    notes: '',
  });
  protected readonly setupError = signal<string | null>(null);
  protected readonly introDone = signal(false);
  protected readonly typingActive = signal(false);
  protected readonly agentBusy = signal(false);

  protected draftReply = '';
  protected inviteEmails = '';
  protected selectedCertification = 'AZ-900';
  protected supportMessage = '';

  protected readonly currentQuestion = computed(
    () => SETUP_QUESTIONS[this.currentQuestionIndex()] ?? null,
  );
  protected readonly totalQuestions = SETUP_QUESTIONS.length;
  protected readonly progressStages = Array.from(
    { length: this.totalQuestions },
    (_, index) => index + 1,
  );
  protected readonly currentStepNumber = computed(() =>
    Math.min(this.currentQuestionIndex() + 1, this.totalQuestions),
  );
  protected readonly quickReplies = computed(() => this.currentQuestion()?.quickReplies ?? []);
  protected readonly stepLabel = computed(
    () => `Step ${this.currentStepNumber()} of ${this.totalQuestions}`,
  );
  protected readonly progressPercent = computed(() =>
    Math.round(((this.currentQuestionIndex() + 1) / this.totalQuestions) * 100),
  );
  protected readonly progressTrackPercent = computed(() => {
    if (this.totalQuestions <= 1) {
      return 100;
    }
    return ((this.currentStepNumber() - 1) / (this.totalQuestions - 1)) * 100;
  });
  protected readonly collectedSummary = computed(() => this.setupAnswers());
  protected readonly needsSetup = computed(() => !this.selectedTeam());
  protected readonly chatPlaceholder = computed(
    () => this.currentQuestion()?.placeholder ?? 'La recopilacion ya termino.',
  );
  protected readonly storageKey = computed(() => `retaim-manager-team-${this.profile()?.id || 'guest'}`);

  private cubeAnimationFrame = 0;
  private hudAnimationFrame = 0;
  private cubeAngle = 0;
  private cubeShrunk = false;
  private waveformSpeaking = false;
  private waveformPhase = 0;
  private waveformIntensity = 0;
  private introTimeouts: number[] = [];
  private messageId = 0;
  private scrollFrame = 0;
  private shouldStartAgentAfterIntro = false;
  private canvasResizeHandler = () => {
    if (!this.cubeShrunk) {
      this.resizeCubeCanvas();
    }
    this.resizeHudCanvas();
  };

  constructor() {
    this.restoreState();
    void this.loadTeams();
  }

  ngAfterViewInit(): void {
    this.setupScene();
  }

  ngOnDestroy(): void {
    cancelAnimationFrame(this.cubeAnimationFrame);
    cancelAnimationFrame(this.hudAnimationFrame);
    cancelAnimationFrame(this.scrollFrame);
    this.introTimeouts.forEach((timeoutId) => window.clearTimeout(timeoutId));
    window.removeEventListener('resize', this.canvasResizeHandler);
  }

  protected async loadTeams(preferredTeamId?: string): Promise<void> {
    this.loading.set(true);
    try {
      const [teams, catalog] = await Promise.all([
        this.api.listTeams(),
        this.api.listCertifications(),
      ]);
      this.teams.set(teams);
      this.catalog.set(catalog);
      if (catalog.length) {
        this.selectedCertification = catalog[0].code;
      }

      if (teams.length) {
        const nextTeam = teams.find((team) => team.id === preferredTeamId) || teams[0];
        const profile = this.authStore.profile();
        await this.router.navigate([
          profile?.onboarding_completed_at ? '/manager/dashboard' : '/onboarding',
        ]);
        return;
      }

      this.shouldStartAgentAfterIntro = true;
      if (this.introDone()) {
        void this.startAgent();
      }
    } finally {
      this.loading.set(false);
    }
  }

  protected async loadMembers(teamId: string): Promise<void> {
    this.members.set(await this.api.listTeamMembers(teamId));
  }

  protected async submitAgentReply(): Promise<void> {
    const question = this.currentQuestion();
    const rawValue = this.draftReply.trim();
    if (!question || !rawValue || this.setupSubmitting() || this.agentBusy()) {
      return;
    }
    this.pushMessage('user', rawValue);
    this.draftReply = '';

    if (this.shouldUseSetupAgent(question.key, rawValue)) {
      const assist = await this.api.assistManagerSetup({
        question_key: question.key,
        question_title: question.title,
        question_prompt: question.prompt,
        user_message: rawValue,
        collected_answers: this.setupAnswers(),
      });

      await this.deliverAiMessage(assist.message);

      if (!assist.should_advance || !assist.normalized_answer) {
        return;
      }

      await this.commitAnswerAndContinue(question.key, assist.normalized_answer);
      return;
    }

    const normalizedValue = this.normalizeAnswer(question.key, rawValue);
    await this.commitAnswerAndContinue(question.key, normalizedValue);
  }

  protected useQuickReply(value: string): void {
    if (this.agentBusy() || this.setupSubmitting()) {
      return;
    }
    this.draftReply = value;
    void this.submitAgentReply();
  }

  protected async generateAccessCode(): Promise<void> {
    const team = this.selectedTeam();
    if (!team) {
      return;
    }
    this.accessCode.set(await this.api.createTeamAccessCode(team.id));
  }

  protected async inviteMembers(): Promise<void> {
    const team = this.selectedTeam();
    if (!team) {
      return;
    }
    await this.api.inviteTeamMembers(
      team.id,
      this.inviteEmails
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
    );
    this.inviteEmails = '';
    await this.loadMembers(team.id);
  }

  protected async assignCertificationToMember(): Promise<void> {
    const team = this.selectedTeam();
    const member = this.selectedMember();
    if (!team || !member) {
      return;
    }
    await this.api.assignCertificationToTeam(team.id, this.selectedCertification, [member.user_id]);
    await this.loadMembers(team.id);
    this.selectedMember.set(await this.api.getManagerMemberDetail(team.id, member.user_id));
  }

  protected async sendSupport(): Promise<void> {
    const team = this.selectedTeam();
    const member = this.selectedMember();
    if (!team || !member || !this.supportMessage.trim()) {
      return;
    }
    await this.api.sendSupportMessage(team.id, member.user_id, this.supportMessage.trim());
    this.supportMessage = '';
  }

  protected async openMember(memberId: string): Promise<void> {
    const team = this.selectedTeam();
    if (!team) {
      return;
    }
    this.selectedMember.set(await this.api.getManagerMemberDetail(team.id, memberId));
  }

  private async startAgent(): Promise<void> {
    if (this.messages().length) {
      return;
    }

    const managerName = this.profile()?.full_name || 'manager';
    await this.deliverAiMessage(
      `Hola ${managerName}. Voy a recopilar solo la informacion necesaria para configurar tu espacio inicial.`,
      { typingMs: 1300, wordMs: 48 },
    );
    await this.deliverAiMessage(SETUP_QUESTIONS[0].prompt, { typingMs: 1450, wordMs: 42 });
  }

  private async completeAgentSetup(answers: SetupAnswers): Promise<void> {
    this.setupSubmitting.set(true);
    this.setupError.set(null);
    this.pushMessage('status', 'Procesando la informacion y creando el equipo...');

    try {
      await this.api.updateCurrentProfile({
        professional_role: answers.professional_role,
      });

      const team = await this.api.createTeam({
        team_name: answers.team_name,
        organization_name: answers.organization_name,
        sector: answers.sector,
        member_capacity: Number(answers.member_capacity) || 1,
        work_style: answers.work_style,
        notes: answers.notes === 'Sin notas' ? '' : answers.notes,
      });

      window.localStorage.removeItem(this.storageKey());
      await this.authStore.refreshProfile();
      await this.deliverAiMessage(
        'Genial. Ya deje listo tu equipo. Ahora vamos a completar tu perfil de aprendizaje para poder recomendarte certificaciones tambien a ti.',
        { typingMs: 1400, wordMs: 40 },
      );
      await this.router.navigate(['/team-user-transition']);
    } catch (error) {
      this.setupError.set(
        error instanceof Error ? error.message : 'No se pudo completar la configuracion inicial.',
      );
      this.pushMessage(
        'status',
        'No pude terminar la configuracion. Revisa el mensaje de error y vuelve a intentar.',
      );
    } finally {
      this.setupSubmitting.set(false);
    }
  }

  private pushMessage(role: AgentMessage['role'], text: string): number {
    const id = ++this.messageId;
    this.messages.update((current) => [...current, { id, role, text }]);
    this.scheduleScrollToBottom();
    return id;
  }

  private setupScene(): void {
    this.resizeCubeCanvas();
    this.resizeHudCanvas();
    window.addEventListener('resize', this.canvasResizeHandler);
    this.drawCubeLoop();
    this.drawHudLoop();

    this.introTimeouts.push(
      window.setTimeout(() => {
        this.shrinkCube();
        this.introTimeouts.push(
          window.setTimeout(() => {
            this.introDone.set(true);
            if (this.shouldStartAgentAfterIntro && !this.selectedTeam()) {
              void this.startAgent();
            }
          }, 1500),
        );
      }, 2400),
    );
  }

  private resizeCubeCanvas(): void {
    const canvas = this.host.nativeElement.querySelector('#cube-canvas') as HTMLCanvasElement | null;
    if (!canvas) {
      return;
    }
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
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

  private shrinkCube(): void {
    this.cubeShrunk = true;
    const canvas = this.host.nativeElement.querySelector('#cube-canvas') as HTMLCanvasElement | null;
    if (!canvas) {
      return;
    }
    canvas.classList.add('shrink');
  }

  private drawCubeLoop(): void {
    const canvas = this.host.nativeElement.querySelector('#cube-canvas') as HTMLCanvasElement | null;
    if (!canvas) {
      return;
    }
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      return;
    }

    const render = () => {
      const width = canvas.width;
      const height = canvas.height;
      const cx = width / 2;
      const cy = height / 2;
      const radius = Math.min(width, height) * 0.28;
      this.cubeAngle += 0.006;
      this.drawCube(ctx, width, height, cx, cy, radius, this.cubeAngle);
      this.cubeAnimationFrame = requestAnimationFrame(render);
    };

    render();
  }

  private drawCube(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    cx: number,
    cy: number,
    r: number,
    rot: number,
  ): void {
    ctx.clearRect(0, 0, width, height);

    const edgeColor = this.cubeShrunk ? 'rgba(255,255,255,0.88)' : 'rgba(191,90,242,0.72)';
    const extraColor = this.cubeShrunk ? 'rgba(255,255,255,0.18)' : 'rgba(168,85,247,0.12)';
    const nodeColor = this.cubeShrunk ? '#ffffff' : '#d8b4fe';
    const shadowColor = this.cubeShrunk ? '#ffffff' : '#a855f7';

    const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 1.2);
    gradient.addColorStop(0, this.cubeShrunk ? 'rgba(255,255,255,0.08)' : 'rgba(168,85,247,0.08)');
    gradient.addColorStop(1, this.cubeShrunk ? 'rgba(255,255,255,0)' : 'rgba(168,85,247,0)');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(cx, cy, r * 1.2, 0, Math.PI * 2);
    ctx.fill();

    const size = r * 0.72;
    const cube = [
      [-size, -size, -size],
      [size, -size, -size],
      [size, size, -size],
      [-size, size, -size],
      [-size, -size, size],
      [size, -size, size],
      [size, size, size],
      [-size, size, size],
    ];
    const cosY = Math.cos(rot);
    const sinY = Math.sin(rot);
    const cosX = Math.cos(rot * 0.42);
    const sinX = Math.sin(rot * 0.42);
    const scale = r * 2.2;

    const rotate = ([x, y, z]: number[]) => {
      const nx = x * cosY - z * sinY;
      const nz = x * sinY + z * cosY;
      const ny = y * cosX - nz * sinX;
      const nz2 = y * sinX + nz * cosX;
      return [nx, ny, nz2];
    };

    const project = (x: number, y: number, z: number) => {
      const factor = scale / (scale + z);
      return { x: cx + x * factor, y: cy + y * factor };
    };

    const points = cube.map((point) => {
      const [x, y, z] = rotate(point);
      return project(x, y, z);
    });

    const edges = [
      [0, 1],
      [1, 2],
      [2, 3],
      [3, 0],
      [4, 5],
      [5, 6],
      [6, 7],
      [7, 4],
      [0, 4],
      [1, 5],
      [2, 6],
      [3, 7],
    ];
    const extras = [
      [0, 2],
      [1, 3],
      [4, 6],
      [5, 7],
      [0, 6],
      [1, 7],
      [2, 4],
      [3, 5],
      [0, 5],
      [1, 4],
      [2, 7],
      [3, 6],
    ];

    extras.forEach(([a, b]) => {
      ctx.beginPath();
      ctx.moveTo(points[a].x, points[a].y);
      ctx.lineTo(points[b].x, points[b].y);
      ctx.strokeStyle = extraColor;
      ctx.lineWidth = 0.6;
      ctx.stroke();
    });

    edges.forEach(([a, b]) => {
      ctx.beginPath();
      ctx.moveTo(points[a].x, points[a].y);
      ctx.lineTo(points[b].x, points[b].y);
      ctx.strokeStyle = edgeColor;
      ctx.lineWidth = 1.1;
      ctx.shadowColor = shadowColor;
      ctx.shadowBlur = 6;
      ctx.stroke();
      ctx.shadowBlur = 0;
    });

    points.forEach((point, index) => {
      const pulse = 0.8 + 0.2 * Math.sin(Date.now() * 0.002 + index);
      ctx.beginPath();
      ctx.arc(point.x, point.y, 4.5 * pulse, 0, Math.PI * 2);
      ctx.fillStyle = nodeColor;
      ctx.shadowColor = shadowColor;
      ctx.shadowBlur = 12;
      ctx.fill();
      ctx.shadowBlur = 0;
    });
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
        for (let i = 0; i <= nPts; i++) {
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

  private async commitAnswerAndContinue(
    questionKey: SetupQuestionKey,
    normalizedValue: string,
  ): Promise<void> {
    const answers = {
      ...this.setupAnswers(),
      [questionKey]: normalizedValue,
    };
    this.setupAnswers.set(answers);
    this.persistState();

    const currentQuestion = SETUP_QUESTIONS[this.currentQuestionIndex()];
    await this.deliverAiMessage(this.buildConfirmation(currentQuestion.title, normalizedValue), {
      typingMs: 1050,
      wordMs: 38,
    });

    const nextIndex = this.currentQuestionIndex() + 1;
    this.currentQuestionIndex.set(nextIndex);
    this.persistState();

    if (nextIndex >= SETUP_QUESTIONS.length) {
      await this.completeAgentSetup(answers);
      return;
    }

    await this.deliverAiMessage(SETUP_QUESTIONS[nextIndex].prompt, {
      typingMs: 1400,
      wordMs: 40,
    });
  }

  private shouldUseSetupAgent(questionKey: SetupQuestionKey, rawValue: string): boolean {
    const lowered = rawValue.trim().toLowerCase();
    if (!lowered) {
      return false;
    }
    if (rawValue.includes('?')) {
      return true;
    }
    if (
      lowered.startsWith('que ') ||
      lowered.startsWith('qué ') ||
      lowered.startsWith('como ') ||
      lowered.startsWith('cómo ') ||
      lowered.startsWith('cual ') ||
      lowered.startsWith('cuál ') ||
      lowered.startsWith('me recomiendas') ||
      lowered.startsWith('puedo ') ||
      lowered.startsWith('debo ')
    ) {
      return true;
    }
    if (['no se', 'nose', 'no estoy seguro', 'no estoy segura', 'depende', 'cualquiera'].includes(lowered)) {
      return true;
    }
    if (questionKey === 'member_capacity' && !/\d/.test(rawValue)) {
      return true;
    }
    return false;
  }

  private normalizeAnswer(questionKey: SetupQuestionKey, rawValue: string): string {
    if (questionKey === 'member_capacity') {
      return String(Math.max(1, Number(rawValue.replace(/[^\d]/g, '')) || 0));
    }
    return rawValue.trim();
  }

  private buildConfirmation(questionTitle: string, answer: string): string {
    const confirmations = [
      'Muy bien.',
      'Entiendo.',
      'Genial.',
      'Perfecto.',
      'Listo.',
    ];
    const confirmation =
      confirmations[(this.currentQuestionIndex() + answer.length) % confirmations.length];
    return `${confirmation} Registre ${questionTitle.toLowerCase()} como ${answer}.`;
  }

  private async deliverAiMessage(
    text: string,
    options: { typingMs?: number; wordMs?: number } = {},
  ): Promise<void> {
    const typingMs = options.typingMs ?? 1200;
    const wordMs = options.wordMs ?? 36;

    this.agentBusy.set(true);
    this.typingActive.set(true);
    this.waveformSpeaking = true;
    this.scheduleScrollToBottom();

    await this.sleep(typingMs);

    this.typingActive.set(false);
    const messageId = this.pushMessage('ai', '');
    const words = text.split(' ');

    for (let index = 0; index < words.length; index += 1) {
      this.messages.update((current) =>
        current.map((message) =>
          message.id === messageId
            ? {
                ...message,
                text: `${message.text}${message.text ? ' ' : ''}${words[index]}`,
              }
            : message,
        ),
      );
      this.scheduleScrollToBottom();
      await this.sleep(wordMs + Math.round(Math.random() * 30));
    }

    this.waveformSpeaking = false;
    this.agentBusy.set(false);
  }

  private scheduleScrollToBottom(): void {
    cancelAnimationFrame(this.scrollFrame);
    this.scrollFrame = requestAnimationFrame(() => {
      const container = this.host.nativeElement.querySelector('.chat-messages') as HTMLDivElement | null;
      if (!container) {
        return;
      }
      container.scrollTop = container.scrollHeight;
    });
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => {
      const timeoutId = window.setTimeout(resolve, ms);
      this.introTimeouts.push(timeoutId);
    });
  }

  private restoreState(): void {
    const raw = window.localStorage.getItem(this.storageKey());
    if (!raw) {
      return;
    }
    try {
      const parsed = JSON.parse(raw) as {
        answers?: Partial<SetupAnswers>;
        currentQuestionIndex?: number;
      };
      const restoredAnswers = {
        professional_role: '',
        organization_name: '',
        team_name: '',
        sector: '',
        member_capacity: '',
        work_style: '',
        notes: '',
        ...(parsed.answers || {}),
      };
      this.setupAnswers.set(restoredAnswers);
      const nextIndex = SETUP_QUESTIONS.findIndex((question) => !restoredAnswers[question.key]?.trim());
      this.currentQuestionIndex.set(nextIndex === -1 ? Math.min(parsed.currentQuestionIndex ?? 0, this.totalQuestions - 1) : nextIndex);
    } catch {
      window.localStorage.removeItem(this.storageKey());
    }
  }

  private persistState(): void {
    window.localStorage.setItem(
      this.storageKey(),
      JSON.stringify({
        answers: this.setupAnswers(),
        currentQuestionIndex: this.currentQuestionIndex(),
      }),
    );
  }
}
