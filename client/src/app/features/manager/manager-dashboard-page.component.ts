import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import {
  ApiService,
  ManagerDashboardResponse,
  ManagerMemberDetailResponse,
  TeamAccessCodeSummary,
  TeamMemberSummary,
  TeamSummary,
} from '../../core/services/api.service';
import { AppIconComponent } from '../../shared/components/app-icon.component';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

@Component({
  selector: 'app-manager-dashboard-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, EmptyStateComponent, StatusPillComponent, AppIconComponent],
  templateUrl: './manager-dashboard-page.component.html',
  styleUrl: './manager-dashboard-page.component.css',
})
export class ManagerDashboardPageComponent {
  private readonly api = inject(ApiService);

  protected readonly teams = signal<TeamSummary[]>([]);
  protected readonly selectedTeamId = signal('');
  protected readonly activeSection = signal<'control' | 'members'>('control');
  protected readonly dashboard = signal<ManagerDashboardResponse | null>(null);
  protected readonly exportUrl = signal<string | null>(null);
  protected readonly members = signal<TeamMemberSummary[]>([]);
  protected readonly accessCode = signal<TeamAccessCodeSummary | null>(null);
  protected readonly selectedMember = signal<ManagerMemberDetailResponse | null>(null);
  protected readonly loadingMembers = signal(false);

  protected inviteEmails = '';

  constructor() {
    void this.load();
  }

  protected gapCount(): string {
    return String(this.dashboard()?.top_gaps.length || 0);
  }

  protected teamRiskCount(): number {
    return this.dashboard()?.members.filter((member) => member.risk_status === 'red').length || 0;
  }

  protected completedGoalCount(): number {
    return this.dashboard()?.members.filter((member) => member.progress_percent >= 80).length || 0;
  }

  protected teamProgressDelta(): number {
    return Math.max((this.dashboard()?.team_progress_percent || 0) - 50, 0);
  }

  protected setSection(section: 'control' | 'members'): void {
    this.activeSection.set(section);
  }

  protected selectedTeam(): TeamSummary | null {
    return this.teams().find((team) => team.id === this.selectedTeamId()) || null;
  }

  protected async selectTeam(teamId: string): Promise<void> {
    this.selectedTeamId.set(teamId);
    this.exportUrl.set(null);
    this.dashboard.set(await this.api.getManagerDashboard(teamId));
    await this.loadMembers(teamId);
  }

  protected async exportPdf(): Promise<void> {
    const teamId = this.selectedTeamId();
    if (!teamId) {
      return;
    }

    const result = await this.api.exportManagerPdf(teamId);
    this.exportUrl.set(result.pdf_url);
  }

  protected async generateAccessCode(): Promise<void> {
    const teamId = this.selectedTeamId();
    if (!teamId) {
      return;
    }
    this.accessCode.set(await this.api.createTeamAccessCode(teamId));
  }

  protected async inviteMembers(): Promise<void> {
    const teamId = this.selectedTeamId();
    const emails = this.inviteEmails
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);

    if (!teamId || !emails.length) {
      return;
    }

    await this.api.inviteTeamMembers(teamId, emails);
    this.inviteEmails = '';
    await this.loadMembers(teamId);
  }

  protected async openMember(memberId: string): Promise<void> {
    const teamId = this.selectedTeamId();
    if (!teamId) {
      return;
    }
    this.selectedMember.set(await this.api.getManagerMemberDetail(teamId, memberId));
  }

  protected async load(): Promise<void> {
    const teams = await this.api.listTeams();
    this.teams.set(teams);
    if (teams.length) {
      await this.selectTeam(teams[0].id);
    }
  }

  private async loadMembers(teamId: string): Promise<void> {
    this.loadingMembers.set(true);
    try {
      this.members.set(await this.api.listTeamMembers(teamId));
      this.selectedMember.set(null);
    } finally {
      this.loadingMembers.set(false);
    }
  }
}
