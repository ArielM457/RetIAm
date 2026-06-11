import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthStore } from '../../core/auth/auth.store';
import { ApiService, TeamSummary } from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';

@Component({
  selector: 'app-team-join-page',
  standalone: true,
  imports: [CommonModule, FormsModule, EmptyStateComponent],
  templateUrl: './team-join-page.component.html',
  styleUrl: './team-join-page.component.css',
})
export class TeamJoinPageComponent {
  private readonly api = inject(ApiService);
  private readonly authStore = inject(AuthStore);
  private readonly router = inject(Router);

  protected readonly loading = signal(false);
  protected readonly joinedTeam = signal<TeamSummary | null>(null);
  protected readonly error = signal<string | null>(null);
  protected accessCode = '';

  protected async joinWithCode(): Promise<void> {
    this.loading.set(true);
    this.error.set(null);
    try {
      const team = await this.api.joinTeamWithCode(this.accessCode);
      this.joinedTeam.set(team);
      const profile = await this.authStore.refreshProfile();
      if (!profile?.onboarding_completed_at) {
        await this.router.navigate(['/onboarding']);
        return;
      }
      await this.router.navigate(['/catalog']);
    } catch (error) {
      this.error.set(error instanceof Error ? error.message : 'No se pudo unir al equipo.');
    } finally {
      this.loading.set(false);
    }
  }
}
