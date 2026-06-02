import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { runtimeConfig } from '../config/runtime-config';

export type UserProfile = {
  id: string;
  email: string;
  full_name: string | null;
  role: string;
  org_id: string | null;
  team_id: string | null;
  target_certification: string | null;
  detected_level: string | null;
  weekly_hours_available: number | null;
  preferred_time: string | null;
  learning_style: string[];
};

type EmailValidationResponse = {
  email: string;
  is_valid: boolean;
  message: string;
};

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = runtimeConfig.apiBaseUrl;

  validateCorporateEmail(email: string): Promise<EmailValidationResponse> {
    return firstValueFrom(
      this.http.post<EmailValidationResponse>(`${this.apiBaseUrl}/auth/validate-email`, { email }),
    );
  }

  getCurrentProfile(): Promise<UserProfile> {
    return firstValueFrom(this.http.get<UserProfile>(`${this.apiBaseUrl}/users/me`));
  }
}
