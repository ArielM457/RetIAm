import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  ApiService,
  CertificationRouteResponse,
  CertificationSummary,
  CourseCatalogSummary,
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
  protected readonly catalog = signal<CertificationSummary[]>([]);
  protected readonly latestPlan = signal<StudyPlanResponse | null>(null);
  protected readonly latestRoute = signal<CertificationRouteResponse | null>(null);
  protected readonly reminders = signal<ReminderResponse[]>([]);
  protected readonly courses = signal<CourseCatalogSummary[]>([]);
  protected readonly loading = signal(true);
  protected readonly creatingReminders = signal(false);

  protected readonly recommendedCourses = computed(() =>
    [...this.courses()].sort((a, b) => b.lesson_count - a.lesson_count).slice(0, 10),
  );

  protected coverClass(track: string): string {
    if (track === 'github') return 'cover-github';
    if (track === 'aws') return 'cover-aws';
    return 'cover-azure';
  }

  protected levelLabel(level: string): string {
    return { basic: 'Básico', intermediate: 'Intermedio', advanced: 'Avanzado' }[level] ?? level;
  }

  protected formatDuration(minutes: number): string {
    if (!minutes) return '—';
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    if (h && m) return `${h} h ${m} min`;
    if (h) return `${h} h`;
    return `${m} min`;
  }

  constructor() {
    void this.load();
  }

  protected readonly needsOnboarding = computed(() => !this.profile()?.onboarding_completed_at);
  protected readonly hasPlan = computed(() => !!this.latestPlan()?.id);
  protected readonly hasRoute = computed(() => !!this.latestRoute()?.id);
  protected readonly nextMilestone = computed(() => this.latestPlan()?.weekly_milestones[0] ?? null);
  protected readonly pendingReminder = computed(() => this.reminders()[0] ?? null);
  protected readonly pendingReminderMessage = computed(
    () =>
      this.pendingReminder()?.message ||
      (this.hasPlan()
        ? 'Aun no generaste recordatorios para este plan.'
        : 'Completa tu perfil y genera un plan para recibir recordatorios utiles.'),
  );
  protected readonly dashboardBadge = computed(() => {
    if (this.needsOnboarding()) {
      return 'Perfil pendiente';
    }
    if (this.hasPlan()) {
      return 'En curso';
    }
    if (this.hasRoute()) {
      return 'Ruta lista';
    }
    return 'Listo para empezar';
  });
  protected readonly heroTitle = computed(() => {
    if (this.needsOnboarding()) {
      return 'Completa tu perfil para recibir recomendaciones';
    }
    return this.latestRoute()?.target_certification || this.profile()?.target_certification || 'Explora certificaciones disponibles';
  });
  protected readonly heroDescription = computed(() => {
    if (this.needsOnboarding()) {
      return 'Necesitamos tu rol, disponibilidad y estilo de aprendizaje para recomendarte una certificacion y construir tu ruta.';
    }
    if (!this.hasRoute()) {
      return 'Ya tienes perfil base. El siguiente paso es elegir una certificacion y generar tu primera ruta.';
    }
    return 'Tu ruta ya esta activa y puedes seguir con plan, hitos y sesiones guiadas.';
  });
  protected readonly completionRatio = computed(() => {
    const plan = this.latestPlan();
    if (!plan) {
      return 0;
    }

    return Math.min(100, Math.round((1 / Math.max(plan.weekly_milestones.length, 1)) * 100));
  });
  protected readonly recommendedCertifications = computed(() => {
    const profile = this.profile();
    const roleTokens = (profile?.professional_role || '')
      .toLowerCase()
      .split(/[^a-z0-9]+/)
      .filter(Boolean);
    const catalog = this.catalog();
    const matched = catalog.filter((item) =>
      roleTokens.some((token) => item.recommended_for.some((entry) => entry.toLowerCase().includes(token))),
    );

    if (matched.length) {
      return matched;
    }

    if (!profile?.professional_role) {
      return catalog.filter((item) => item.level === 'basic');
    }

    return catalog;
  });

  private async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [catalog, route, plan, reminders, courses] = await Promise.all([
        this.api.listCertifications().catch(() => []),
        this.api.getLatestRoute().catch(() => null),
        this.api.getLatestPlan().catch(() => null),
        this.api.listMyReminders().catch(() => []),
        this.api.listCourses().catch(() => []),
      ]);
      this.catalog.set(catalog);
      this.latestRoute.set(route);
      this.latestPlan.set(plan);
      this.reminders.set(reminders);
      this.courses.set(courses);
    } finally {
      this.loading.set(false);
    }
  }

  protected async generateReminders(): Promise<void> {
    this.creatingReminders.set(true);
    try {
      const response = await this.api.generateReminders();
      this.reminders.set(response.reminders);
    } finally {
      this.creatingReminders.set(false);
    }
  }
}
