import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';

import { ApiService, TeamSummary, WeeklyTeamSummaryResponse } from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';

@Component({
  selector: 'app-manager-weekly-summary-page',
  standalone: true,
  imports: [CommonModule, EmptyStateComponent],
  templateUrl: './manager-weekly-summary-page.component.html',
  styleUrl: './manager-weekly-summary-page.component.css',
})
export class ManagerWeeklySummaryPageComponent {
  private readonly api = inject(ApiService);

  protected readonly teams = signal<TeamSummary[]>([]);
  protected readonly summary = signal<WeeklyTeamSummaryResponse | null>(null);
  protected readonly pdfUrl = signal<string | null>(null);

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    const teams = await this.api.listTeams();
    this.teams.set(teams);
    if (!teams.length) {
      return;
    }
    this.summary.set(await this.api.getWeeklySummary(teams[0].id));
  }

  protected async exportPdf(): Promise<void> {
    const team = this.teams()[0];
    if (!team) {
      return;
    }
    const response = await this.api.exportManagerPdf(team.id);
    this.pdfUrl.set(response.pdf_url);
  }
}
