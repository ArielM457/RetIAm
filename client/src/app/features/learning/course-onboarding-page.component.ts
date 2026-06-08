import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { AuthStore } from '../../core/auth/auth.store';
import { ApiService, CertificationSummary, OnboardingQuestion } from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

@Component({
  selector: 'app-course-onboarding-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, EmptyStateComponent, StatusPillComponent],
  templateUrl: './course-onboarding-page.component.html',
  styleUrl: './course-onboarding-page.component.css',
})
export class CourseOnboardingPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(ApiService);
  private readonly authStore = inject(AuthStore);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly loading = signal(false);
  protected readonly targetCertification = signal('AZ-900');
  protected readonly catalog = signal<CertificationSummary[]>([]);
  protected readonly questions = signal<OnboardingQuestion[]>([]);
  protected readonly result = signal<{
    score: number;
    max_score: number;
    summary: string;
    recommendations: string[];
    profile: { detected_level: string };
  } | null>(null);

  protected readonly setupForm = this.fb.nonNullable.group({
    professional_role: ['', Validators.required],
    target_certification: ['AZ-900', Validators.required],
    weekly_hours_available: [6, [Validators.required, Validators.min(1), Validators.max(40)]],
    preferred_time: ['morning', Validators.required],
    learning_style: ['documentation,hands_on', Validators.required],
  });

  protected readonly canEvaluate = computed(() => this.questions().length >= 5);

  constructor() {
    void this.bootstrap();
  }

  protected readonly selectedCertificationMeta = computed(() =>
    this.catalog().find((item) => item.code === this.setupForm.controls.target_certification.value) ?? null,
  );

  private async bootstrap(): Promise<void> {
    this.loading.set(true);
    try {
      const [catalog] = await Promise.all([this.api.listCertifications().catch(() => [])]);
      this.catalog.set(catalog);

      const currentProfile = this.authStore.profile();
      const certFromQuery = this.route.snapshot.queryParamMap.get('cert');
      const initialCertification =
        certFromQuery ||
        currentProfile?.target_certification ||
        catalog[0]?.code ||
        this.setupForm.controls.target_certification.value;

      this.setupForm.patchValue({
        professional_role: currentProfile?.professional_role || '',
        target_certification: initialCertification,
        weekly_hours_available: currentProfile?.weekly_hours_available || 6,
        preferred_time: (currentProfile?.preferred_time as 'morning' | 'afternoon' | 'night' | null) || 'morning',
        learning_style:
          currentProfile?.learning_style?.length
            ? currentProfile.learning_style.join(', ')
            : 'documentation, hands_on',
      });

      await this.loadQuestions();
    } finally {
      this.loading.set(false);
    }
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
      await this.authStore.refreshProfile();
      await this.router.navigate(['/plan']);
    } finally {
      this.loading.set(false);
    }
  }
}
