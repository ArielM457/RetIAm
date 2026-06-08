import { CommonModule } from '@angular/common';
import { Component, OnDestroy, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  ApiService,
  FinalExamAttemptResponse,
  StudyPlanResponse,
} from '../../core/services/api.service';

@Component({
  selector: 'app-exam-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './exam-page.component.html',
  styleUrl: './exam-page.component.css',
})
export class ExamPageComponent implements OnDestroy {
  private readonly api = inject(ApiService);

  protected readonly plan = signal<StudyPlanResponse | null>(null);
  protected readonly loading = signal(true);
  protected readonly phase = signal<'intro' | 'running' | 'result'>('intro');
  protected readonly attempt = signal<FinalExamAttemptResponse | null>(null);
  protected readonly currentIndex = signal(0);
  protected readonly answers = signal<Record<string, number>>({});
  protected readonly remaining = signal(0);
  protected readonly starting = signal(false);
  protected readonly submitting = signal(false);
  protected readonly error = signal<string | null>(null);

  private timer: ReturnType<typeof setInterval> | null = null;

  protected readonly questions = computed(() => this.attempt()?.questions ?? []);
  protected readonly current = computed(() => this.questions()[this.currentIndex()] ?? null);
  protected readonly answeredCount = computed(() => Object.keys(this.answers()).length);
  protected readonly clock = computed(() => {
    const total = this.remaining();
    const m = Math.floor(total / 60).toString().padStart(2, '0');
    const s = (total % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  });

  constructor() {
    void this.load();
  }

  ngOnDestroy(): void {
    this.stopTimer();
  }

  private async load(): Promise<void> {
    this.loading.set(true);
    try {
      this.plan.set(await this.api.getLatestPlan());
    } finally {
      this.loading.set(false);
    }
  }

  protected async startExam(): Promise<void> {
    const plan = this.plan();
    if (!plan?.id) return;
    this.starting.set(true);
    this.error.set(null);
    try {
      const attempt = await this.api.startFinalExam(plan.id);
      this.attempt.set(attempt);
      this.remaining.set((attempt.time_limit_minutes || 60) * 60);
      this.phase.set('running');
      this.startTimer();
    } catch (err: unknown) {
      const detail = (err as { error?: { detail?: string } })?.error?.detail;
      this.error.set(detail || 'Aún no puedes iniciar el examen. Completa todas las secciones de tu plan.');
    } finally {
      this.starting.set(false);
    }
  }

  private startTimer(): void {
    this.stopTimer();
    this.timer = setInterval(() => {
      this.remaining.update((value) => value - 1);
      if (this.remaining() <= 0) {
        void this.submit();
      }
    }, 1000);
  }

  private stopTimer(): void {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  protected select(questionId: string, optionIndex: number): void {
    this.answers.update((current) => ({ ...current, [questionId]: optionIndex }));
  }

  protected isSelected(questionId: string, optionIndex: number): boolean {
    return this.answers()[questionId] === optionIndex;
  }

  protected next(): void {
    if (this.currentIndex() < this.questions().length - 1) {
      this.currentIndex.update((index) => index + 1);
    }
  }

  protected prev(): void {
    if (this.currentIndex() > 0) {
      this.currentIndex.update((index) => index - 1);
    }
  }

  protected async submit(): Promise<void> {
    const attempt = this.attempt();
    if (!attempt?.id || this.submitting()) return;
    this.submitting.set(true);
    this.stopTimer();
    try {
      const answers = this.questions().map((q) => ({
        question_id: q.question_id,
        selected_option_index: this.answers()[q.question_id] ?? -1,
      }));
      this.attempt.set(await this.api.submitFinalExam(attempt.id, answers));
      this.phase.set('result');
    } finally {
      this.submitting.set(false);
    }
  }

  protected readonly result = computed(() => (this.phase() === 'result' ? this.attempt() : null));
}
