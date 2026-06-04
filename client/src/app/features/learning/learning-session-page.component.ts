import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  ApiService,
  CertificationRouteResponse,
  LearningSessionResponse,
  StudyPlanResponse,
} from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

@Component({
  selector: 'app-learning-session-page',
  standalone: true,
  imports: [CommonModule, FormsModule, EmptyStateComponent, StatusPillComponent],
  templateUrl: './learning-session-page.component.html',
  styleUrl: './learning-session-page.component.css',
})
export class LearningSessionPageComponent {
  private readonly api = inject(ApiService);

  protected readonly plan = signal<StudyPlanResponse | null>(null);
  protected readonly route = signal<CertificationRouteResponse | null>(null);
  protected readonly session = signal<LearningSessionResponse | null>(null);
  protected readonly loading = signal(true);
  protected mandatoryAnswer = '';
  protected freeQuestion = '';

  protected readonly currentSection = computed(() => this.route()?.sections[0] ?? null);

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [plan, route] = await Promise.all([this.api.getLatestPlan(), this.api.getLatestRoute()]);
      this.plan.set(plan);
      this.route.set(route);
    } finally {
      this.loading.set(false);
    }
  }

  protected async startSession(): Promise<void> {
    const plan = this.plan();
    const section = this.currentSection();
    if (!plan?.id || !section) {
      return;
    }

    this.session.set(
      await this.api.startSession({
        plan_id: plan.id,
        section_id: section.section_id,
        section_title: section.title,
        session_type: 'quiz',
      }),
    );
  }

  protected async sendMandatoryAnswer(): Promise<void> {
    const session = this.session();
    if (!session?.id || !this.mandatoryAnswer.trim()) {
      return;
    }
    this.session.set(await this.api.submitMandatoryAnswer(session.id, this.mandatoryAnswer));
  }

  protected async sendFreeQuestion(): Promise<void> {
    const session = this.session();
    if (!session?.id || !this.freeQuestion.trim()) {
      return;
    }
    this.session.set(await this.api.askFreeQuestion(session.id, this.freeQuestion));
    this.freeQuestion = '';
  }

  protected async passEvaluation(): Promise<void> {
    const session = this.session();
    if (!session?.id) {
      return;
    }
    this.session.set(
      await this.api.submitEvaluation(session.id, {
        answers: [{ is_correct: true }, { is_correct: true }, { is_correct: true }, { is_correct: false }],
      }),
    );
  }

  protected async saveSurvey(skip = false): Promise<void> {
    const session = this.session();
    if (!session?.id) {
      return;
    }
    this.session.set(
      await this.api.submitSurvey(session.id, skip ? { skipped: true } : { skipped: false, clarity_score: 4, preferred_format: 'hands_on labs' }),
    );
  }
}
