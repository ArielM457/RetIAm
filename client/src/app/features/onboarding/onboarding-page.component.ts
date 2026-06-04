import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { ApiService, OnboardingQuestion } from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

@Component({
  selector: 'app-onboarding-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, EmptyStateComponent, StatusPillComponent],
  templateUrl: './onboarding-page.component.html',
  styleUrl: './onboarding-page.component.css',
})
export class OnboardingPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(ApiService);

  protected readonly loading = signal(false);
  protected readonly targetCertification = signal('AZ-900');
  protected readonly questions = signal<OnboardingQuestion[]>([]);
  protected readonly result = signal<{
    score: number;
    max_score: number;
    summary: string;
    recommendations: string[];
    profile: { detected_level: string };
  } | null>(null);

  protected readonly setupForm = this.fb.nonNullable.group({
    professional_role: ['Backend Developer', Validators.required],
    target_certification: ['AZ-900', Validators.required],
    weekly_hours_available: [6, [Validators.required, Validators.min(1), Validators.max(40)]],
    preferred_time: ['morning', Validators.required],
    learning_style: ['documentation,hands_on', Validators.required],
  });

  protected readonly canEvaluate = computed(() => this.questions().length >= 5);

  constructor() {
    void this.loadQuestions();
  }

  protected async loadQuestions(): Promise<void> {
    this.loading.set(true);
    try {
      const target = this.setupForm.controls.target_certification.value;
      this.targetCertification.set(target);
      const response = await this.api.getOnboardingQuestions(target);
      this.questions.set(response.questions);
    } finally {
      this.loading.set(false);
    }
  }

  protected async evaluate(): Promise<void> {
    this.loading.set(true);
    try {
      const response = await this.api.evaluateOnboarding({
        professional_role: this.setupForm.controls.professional_role.value,
        target_certification: this.setupForm.controls.target_certification.value,
        weekly_hours_available: this.setupForm.controls.weekly_hours_available.value,
        preferred_time: this.setupForm.controls.preferred_time.value as 'morning' | 'afternoon' | 'night',
        learning_style: this.setupForm.controls.learning_style.value
          .split(',')
          .map((item) => item.trim()) as Array<'documentation' | 'code_examples' | 'hands_on' | 'mixed'>,
        answers: this.questions().slice(0, 5).map((question) => ({
          question_id: question.id,
          selected_option_key: question.options[0]?.key || 'a',
        })),
      });
      this.result.set(response);
    } finally {
      this.loading.set(false);
    }
  }
}
