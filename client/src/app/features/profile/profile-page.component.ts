import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';

import { AuthStore } from '../../core/auth/auth.store';
import { ApiService, SavedAssessmentResponse } from '../../core/services/api.service';
import { AppIconComponent } from '../../shared/components/app-icon.component';

const PROFESSIONAL_ROLE_OPTIONS = [
  'Backend Developer',
  'Frontend Developer',
  'Fullstack Developer',
  'QA Engineer',
  'DevOps Engineer',
  'Cloud Engineer',
  'Data Engineer',
  'Data Analyst',
  'Cybersecurity Analyst',
  'Support Engineer',
  'Team Lead',
  'Engineering Manager',
  'Project Manager',
  'Product Manager',
  'Solutions Architect',
];

@Component({
  selector: 'app-profile-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, AppIconComponent],
  templateUrl: './profile-page.component.html',
  styleUrl: './profile-page.component.css',
})
export class ProfilePageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(ApiService);
  protected readonly authStore = inject(AuthStore);
  protected readonly latestAssessment = signal<SavedAssessmentResponse | null>(null);
  protected readonly saving = signal(false);
  protected readonly saved = signal(false);
  protected readonly saveError = signal<string | null>(null);
  protected readonly professionalRoleOptions = PROFESSIONAL_ROLE_OPTIONS;

  protected readonly form = this.fb.group({
    full_name: [''],
    professional_role: [''],
    target_certification: [''],
    weekly_hours_available: [6],
    preferred_time: ['morning'],
    learning_style: ['documentation,mixed'],
  });

  constructor() {
    const profile = this.authStore.profile();
    this.form.patchValue({
      full_name: profile?.full_name || '',
      professional_role: profile?.professional_role || '',
      target_certification: profile?.target_certification || '',
      weekly_hours_available: profile?.weekly_hours_available || 6,
      preferred_time: profile?.preferred_time || 'morning',
      learning_style: profile?.learning_style?.join(', ') || 'documentation,mixed',
    });
    void this.loadAssessment();
  }

  protected async save(): Promise<void> {
    this.saving.set(true);
    this.saved.set(false);
    this.saveError.set(null);
    try {
      const payload = this.form.getRawValue();
      await this.api.updateCurrentProfile({
        ...payload,
        learning_style: payload.learning_style
          ?.split(',')
          .map((item) => item.trim())
          .filter(Boolean),
      });
      await this.authStore.refreshProfile();
      this.saved.set(true);
    } catch (error) {
      this.saveError.set(
        error instanceof Error ? error.message : 'No se pudo guardar el perfil.',
      );
    } finally {
      this.saving.set(false);
    }
  }

  protected readonly profileFacts = computed(() => {
    const profile = this.authStore.profile();
    return [
      { label: 'Correo', value: profile?.email || 'Sin correo' },
      { label: 'Rol en plataforma', value: profile?.role === 'manager' ? 'Manager' : 'Employee' },
      { label: 'Rol profesional', value: profile?.professional_role || 'Sin definir' },
      { label: 'Certificacion objetivo', value: profile?.target_certification || 'Aun no elegida' },
      { label: 'Nivel detectado', value: profile?.detected_level || 'Pendiente' },
      {
        label: 'Horas por semana',
        value: profile?.weekly_hours_available ? `${profile.weekly_hours_available} horas` : 'Pendiente',
      },
      {
        label: 'Horario preferido',
        value: this.formatPreferredTime(profile?.preferred_time),
      },
      {
        label: 'Estilos de aprendizaje',
        value: profile?.learning_style?.length ? profile.learning_style.join(', ') : 'Pendiente',
      },
      { label: 'Equipo', value: profile?.team_id || 'Sin equipo' },
      { label: 'Organizacion', value: profile?.org_id || 'Sin organizacion' },
      { label: 'Version de perfil', value: String(profile?.profile_version || 1) },
      {
        label: 'Onboarding inicial',
        value: profile?.onboarding_completed_at
          ? new Date(profile.onboarding_completed_at).toLocaleString()
          : 'Pendiente',
      },
    ];
  });

  protected readonly intakeAnswers = computed(() => {
    const answers = this.latestAssessment()?.answers || [];
    return answers
      .map((answer) => ({
        title: answer.title || answer.key || answer.question_id || 'Dato',
        value:
          answer.answer ||
          answer.selected_option_key ||
          answer.correct_option_key ||
          'Sin respuesta registrada',
      }))
      .filter((entry) => entry.value && entry.value !== 'Sin respuesta registrada');
  });

  protected readonly assessmentSummary = computed(() => {
    const assessment = this.latestAssessment();
    if (!assessment) {
      return null;
    }
    return {
      notes: assessment.notes || 'Sin resumen adicional.',
      createdAt: new Date(assessment.created_at).toLocaleString(),
      scoreLabel:
        assessment.max_score > 0 ? `${assessment.score}/${assessment.max_score}` : 'Perfil conversacional',
    };
  });

  protected readonly roleOptionsForSelect = computed(() => {
    const currentRole = this.form.controls.professional_role.value?.trim();
    if (!currentRole || this.professionalRoleOptions.includes(currentRole)) {
      return this.professionalRoleOptions;
    }
    return [currentRole, ...this.professionalRoleOptions];
  });

  private async loadAssessment(): Promise<void> {
    this.latestAssessment.set(await this.api.getLatestAssessment());
  }

  private formatPreferredTime(value: string | null | undefined): string {
    if (!value) {
      return 'Pendiente';
    }
    if (value === 'morning') {
      return 'Morning';
    }
    if (value === 'afternoon') {
      return 'Afternoon';
    }
    if (value === 'night') {
      return 'Night';
    }
    return value;
  }
}
