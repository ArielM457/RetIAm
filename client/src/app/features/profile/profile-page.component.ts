import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';

import { AuthStore } from '../../core/auth/auth.store';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-profile-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './profile-page.component.html',
  styleUrl: './profile-page.component.css',
})
export class ProfilePageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(ApiService);
  protected readonly authStore = inject(AuthStore);

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
  }

  protected async save(): Promise<void> {
    const payload = this.form.getRawValue();
    await this.api.updateCurrentProfile({
      ...payload,
      learning_style: payload.learning_style
        ?.split(',')
        .map((item) => item.trim())
        .filter(Boolean),
    });
    await this.authStore.refreshProfile();
  }
}
