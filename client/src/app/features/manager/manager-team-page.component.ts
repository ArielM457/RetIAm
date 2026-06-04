import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  ApiService,
  ManagerMemberDetailResponse,
  TeamMemberSummary,
  TeamSummary,
} from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';

@Component({
  selector: 'app-manager-team-page',
  standalone: true,
  imports: [CommonModule, FormsModule, EmptyStateComponent],
  templateUrl: './manager-team-page.component.html',
  styleUrl: './manager-team-page.component.css',
})
export class ManagerTeamPageComponent {
  private readonly api = inject(ApiService);

  protected readonly teams = signal<TeamSummary[]>([]);
  protected readonly members = signal<TeamMemberSummary[]>([]);
  protected readonly selectedMember = signal<ManagerMemberDetailResponse | null>(null);
  protected readonly selectedTeam = signal<TeamSummary | null>(null);
  protected newTeamName = 'Equipo Demo';
  protected newOrganizationName = 'RetAIM Org';
  protected inviteEmails = '';

  constructor() {
    void this.loadTeams();
  }

  protected async loadTeams(): Promise<void> {
    const teams = await this.api.listTeams();
    this.teams.set(teams);
    if (teams.length) {
      this.selectedTeam.set(teams[0]);
      await this.loadMembers(teams[0].id);
    }
  }

  protected async createTeam(): Promise<void> {
    const team = await this.api.createTeam({
      team_name: this.newTeamName,
      organization_name: this.newOrganizationName,
    });
    this.selectedTeam.set(team);
    await this.loadTeams();
  }

  protected async loadMembers(teamId: string): Promise<void> {
    this.members.set(await this.api.listTeamMembers(teamId));
  }

  protected async inviteMembers(): Promise<void> {
    const team = this.selectedTeam();
    if (!team) {
      return;
    }
    await this.api.inviteTeamMembers(
      team.id,
      this.inviteEmails
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
    );
    this.inviteEmails = '';
    await this.loadMembers(team.id);
  }

  protected async openMember(memberId: string): Promise<void> {
    const team = this.selectedTeam();
    if (!team) {
      return;
    }
    this.selectedMember.set(await this.api.getManagerMemberDetail(team.id, memberId));
  }
}
