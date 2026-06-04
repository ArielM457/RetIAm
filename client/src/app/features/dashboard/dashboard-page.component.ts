import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  ApiService,
  CertificationRouteResponse,
  ReminderResponse,
  StudyPlanResponse,
} from '../../core/services/api.service';
import { AuthStore } from '../../core/auth/auth.store';
import { AppIconComponent } from '../../shared/components/app-icon.component';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, RouterLink, AppIconComponent],
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.css',
})
export class DashboardPageComponent {
  private readonly api = inject(ApiService);
  protected readonly authStore = inject(AuthStore);

  protected readonly profile = computed(() => this.authStore.profile());
  protected readonly latestPlan = signal<StudyPlanResponse | null>(null);
  protected readonly latestRoute = signal<CertificationRouteResponse | null>(null);
  protected readonly reminders = signal<ReminderResponse[]>([]);
  protected readonly loading = signal(true);

  constructor() {
    void this.load();
  }

  protected readonly nextMilestone = computed(() => this.latestPlan()?.weekly_milestones[0] ?? null);
  protected readonly pendingReminder = computed(() => this.reminders()[0] ?? null);
  protected readonly pendingReminderMessage = computed(
    () => this.pendingReminder()?.message || 'Genera recordatorios cuando tengas un plan activo.',
  );
  protected readonly completionRatio = computed(() => {
    const plan = this.latestPlan();
    if (!plan) {
      return 0;
    }

    return Math.min(100, Math.round((1 / Math.max(plan.weekly_milestones.length, 1)) * 100));
  });

  private async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [route, plan, reminders] = await Promise.all([
        this.api.getLatestRoute(),
        this.api.getLatestPlan(),
        this.api.listMyReminders().catch(() => []),
      ]);
      this.latestRoute.set(route);
      this.latestPlan.set(plan);
      this.reminders.set(reminders);
    } finally {
      this.loading.set(false);
    }
  }
}
