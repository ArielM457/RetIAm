import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';

import {
  ApiService,
  CertificationRouteResponse,
  CertificationSummary,
  StudyPlanResponse,
} from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

@Component({
  selector: 'app-learning-plan-page',
  standalone: true,
  imports: [CommonModule, EmptyStateComponent, StatusPillComponent],
  templateUrl: './learning-plan-page.component.html',
  styleUrl: './learning-plan-page.component.css',
})
export class LearningPlanPageComponent {
  private readonly api = inject(ApiService);

  protected readonly catalog = signal<CertificationSummary[]>([]);
  protected readonly route = signal<CertificationRouteResponse | null>(null);
  protected readonly plan = signal<StudyPlanResponse | null>(null);
  protected readonly selectedCertification = signal('AZ-900');
  protected readonly loading = signal(true);

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [catalog, route, plan] = await Promise.all([
        this.api.listCertifications(),
        this.api.getLatestRoute(),
        this.api.getLatestPlan(),
      ]);
      this.catalog.set(catalog);
      this.route.set(route);
      this.plan.set(plan);
    } finally {
      this.loading.set(false);
    }
  }

  protected async createRoute(): Promise<void> {
    this.loading.set(true);
    try {
      const route = await this.api.generateRoute(this.selectedCertification());
      this.route.set(route);
    } finally {
      this.loading.set(false);
    }
  }

  protected async createPlan(): Promise<void> {
    const route = this.route();
    if (!route?.id) {
      return;
    }

    this.loading.set(true);
    try {
      const plan = await this.api.generatePlan({
        route_id: route.id,
        weekly_hours: 6,
        preferred_time: 'morning',
      });
      this.plan.set(plan);
    } finally {
      this.loading.set(false);
    }
  }
}
