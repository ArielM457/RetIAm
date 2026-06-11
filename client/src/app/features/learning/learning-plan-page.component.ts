import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import {
  ApiService,
  CertificationRouteResponse,
  CertificationSummary,
  CourseEnrollmentResponse,
  StudyPlanResponse,
  StudySessionPlan,
} from '../../core/services/api.service';
import { AuthStore } from '../../core/auth/auth.store';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

type CalendarDay = {
  key: string;
  label: string;
  shortLabel: string;
  sessions: CalendarSession[];
};

type CalendarSession = {
  raw: StudySessionPlan;
  startMinutes: number;
  endMinutes: number;
  top: number;
  height: number;
};

const DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const DAY_LABELS: Record<string, { label: string; short: string }> = {
  Monday: { label: 'Lunes', short: 'LUN' },
  Tuesday: { label: 'Martes', short: 'MAR' },
  Wednesday: { label: 'Miercoles', short: 'MIE' },
  Thursday: { label: 'Jueves', short: 'JUE' },
  Friday: { label: 'Viernes', short: 'VIE' },
  Saturday: { label: 'Sabado', short: 'SAB' },
  Sunday: { label: 'Domingo', short: 'DOM' },
};

@Component({
  selector: 'app-learning-plan-page',
  standalone: true,
  imports: [CommonModule, EmptyStateComponent, StatusPillComponent],
  templateUrl: './learning-plan-page.component.html',
  styleUrl: './learning-plan-page.component.css',
})
export class LearningPlanPageComponent {
  private readonly api = inject(ApiService);
  private readonly authStore = inject(AuthStore);
  private readonly router = inject(Router);

  protected readonly catalog = signal<CertificationSummary[]>([]);
  protected readonly route = signal<CertificationRouteResponse | null>(null);
  protected readonly plan = signal<StudyPlanResponse | null>(null);
  protected readonly enrollments = signal<CourseEnrollmentResponse[]>([]);
  protected readonly selectedCertification = signal('AZ-900');
  protected readonly loading = signal(true);
  protected readonly activeWeekIndex = signal(0);

  protected readonly selectedCatalogItem = computed(
    () => this.catalog().find((item) => item.code === this.selectedCertification()) ?? null,
  );
  protected readonly activeEnrollment = computed(
    () =>
      this.enrollments().find(
        (item) =>
          item.certification_code === (this.route()?.target_certification || this.selectedCertification()),
      ) ?? null,
  );
  protected readonly courseAccessCode = computed(
    () =>
      this.activeEnrollment()?.certification_code ||
      this.route()?.target_certification ||
      this.selectedCertification(),
  );

  protected readonly overviewFacts = computed(() => {
    const route = this.route();
    if (!route) return [];
    const context = route.profile_context;
    return [
      { label: 'Nivel detectado', value: route.detected_level },
      { label: 'Horas por semana', value: `${context.weekly_hours_available || 0} horas` },
      { label: 'Horario ideal', value: this.formatPreferredTime(context.preferred_time) },
      {
        label: 'Sesion sugerida',
        value: `${context.recommended_session_duration_minutes || 0} min por bloque`,
      },
      {
        label: 'Dias sugeridos',
        value: context.recommended_study_days?.length
          ? context.recommended_study_days.map((day) => this.dayLabel(day)).join(', ')
          : 'Por definir',
      },
    ];
  });

  protected readonly weeks = computed(() => this.plan()?.weekly_milestones ?? []);
  protected readonly activeWeek = computed(() => {
    const weeks = this.weeks();
    if (!weeks.length) return null;
    return weeks[Math.min(this.activeWeekIndex(), weeks.length - 1)] ?? weeks[0];
  });

  protected readonly activeWeekSessions = computed(() => this.activeWeek()?.sessions ?? []);
  protected readonly calendarRange = computed(() => {
    const sessions = this.activeWeekSessions();
    if (!sessions.length) {
      return { startHour: 7, endHour: 21 };
    }
    const minutes = sessions
      .map((session) => this.parseTimeWindow(session.time_window, session.duration_minutes))
      .filter((value): value is { startMinutes: number; endMinutes: number } => value !== null);
    if (!minutes.length) {
      return { startHour: 7, endHour: 21 };
    }
    const start = Math.max(6, Math.floor(Math.min(...minutes.map((item) => item.startMinutes)) / 60) - 1);
    const end = Math.min(23, Math.ceil(Math.max(...minutes.map((item) => item.endMinutes)) / 60) + 1);
    return { startHour: start, endHour: end };
  });

  protected readonly calendarHours = computed(() => {
    const { startHour, endHour } = this.calendarRange();
    return Array.from({ length: endHour - startHour + 1 }, (_, index) => startHour + index);
  });

  protected readonly calendarDays = computed<CalendarDay[]>(() => {
    const sessions = this.activeWeekSessions();
    const { startHour, endHour } = this.calendarRange();
    const totalMinutes = Math.max(60, (endHour - startHour) * 60);
    const pxPerMinute = 52 / 60;

    return DAY_ORDER.map((day) => {
      const label = DAY_LABELS[day];
      const daySessions = sessions
        .filter((session) => session.day_name === day)
        .map((session) => {
          const parsed = this.parseTimeWindow(session.time_window, session.duration_minutes);
          const startMinutes = parsed?.startMinutes ?? startHour * 60;
          const endMinutes = parsed?.endMinutes ?? startMinutes + Math.max(session.duration_minutes, 45);
          const safeStart = Math.max(startHour * 60, startMinutes);
          const safeEnd = Math.min(endHour * 60, Math.max(safeStart + 30, endMinutes));
          return {
            raw: session,
            startMinutes: safeStart,
            endMinutes: safeEnd,
            top: (safeStart - startHour * 60) * pxPerMinute,
            height: Math.max(44, (safeEnd - safeStart) * pxPerMinute),
          };
        })
        .sort((a, b) => a.startMinutes - b.startMinutes);

      return {
        key: day,
        label: label.label,
        shortLabel: label.short,
        sessions: daySessions,
      };
    }).filter((day) => day.sessions.length || totalMinutes > 0);
  });

  protected readonly planSummary = computed(() => {
    const plan = this.plan();
    if (!plan) return null;
    const sessionCount = plan.weekly_milestones.reduce((acc, week) => acc + week.sessions.length, 0);
    const reviewCount = plan.weekly_milestones.reduce(
      (acc, week) => acc + week.sessions.filter((session) => session.is_review).length,
      0,
    );
    return {
      sessionCount,
      reviewCount,
      weekCount: plan.weekly_milestones.length,
    };
  });

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [catalog, route, plan, enrollments] = await Promise.all([
        this.api.listCertifications().catch(() => []),
        this.api.getLatestRoute().catch(() => null),
        this.api.getLatestPlan().catch(() => null),
        this.api.listMyEnrollments().catch(() => []),
      ]);
      this.catalog.set(catalog);
      this.route.set(route);
      this.plan.set(plan);
      this.enrollments.set(enrollments);
      this.selectedCertification.set(
        route?.target_certification ||
          this.authStore.profile()?.target_certification ||
          catalog[0]?.code ||
          'AZ-900',
      );
      this.activeWeekIndex.set(0);
    } finally {
      this.loading.set(false);
    }
  }

  protected async createRoute(): Promise<void> {
    this.loading.set(true);
    try {
      const route = await this.api.generateRoute(this.selectedCertification());
      this.route.set(route);
      this.plan.set(null);
      this.activeWeekIndex.set(0);
    } finally {
      this.loading.set(false);
    }
  }

  protected async createPlan(): Promise<void> {
    const route = this.route();
    if (!route?.id) return;

    this.loading.set(true);
    try {
      const plan = await this.api.generatePlan({
        route_id: route.id,
        weekly_hours: route.profile_context.weekly_hours_available || 6,
        preferred_time: route.profile_context.preferred_time || 'morning',
      });
      this.plan.set(plan);
      this.activeWeekIndex.set(0);
    } finally {
      this.loading.set(false);
    }
  }

  protected async openCourseView(): Promise<void> {
    const code = this.courseAccessCode();
    if (!code) return;
    await this.router.navigate(['/sessions'], { queryParams: { course: code } });
  }

  protected selectWeek(index: number): void {
    this.activeWeekIndex.set(index);
  }

  protected calendarHeight(): number {
    return this.calendarHours().length * 52;
  }

  protected hourLabel(hour: number): string {
    const suffix = hour >= 12 ? 'PM' : 'AM';
    const display = hour % 12 === 0 ? 12 : hour % 12;
    return `${display} ${suffix}`;
  }

  protected sessionTone(session: StudySessionPlan): string {
    if (session.is_review) return 'review';
    if (session.session_type.toLowerCase().includes('lab')) return 'lab';
    return 'study';
  }

  protected formatPreferredTime(value: string | null | undefined): string {
    const lowered = (value || '').toLowerCase();
    if (lowered.includes('morn')) return 'Manana';
    if (lowered.includes('after')) return 'Tarde';
    if (lowered.includes('night')) return 'Noche';
    return value || 'Por definir';
  }

  protected dayLabel(day: string): string {
    return DAY_LABELS[day]?.label || day;
  }

  private parseTimeWindow(
    raw: string,
    durationMinutes: number,
  ): { startMinutes: number; endMinutes: number } | null {
    if (!raw) return null;
    const parts = raw.split('-').map((item) => item.trim());
    if (!parts.length) return null;
    const start = this.parseClock(parts[0]);
    if (start === null) return null;
    const end = parts[1] ? this.parseClock(parts[1], start) : start + Math.max(durationMinutes, 45);
    const safeEnd = end ?? start + Math.max(durationMinutes, 45);
    return { startMinutes: start, endMinutes: Math.max(start + 30, safeEnd) };
  }

  private parseClock(raw: string, fallbackStart?: number): number | null {
    const match = raw.toLowerCase().match(/(\d{1,2})(?::(\d{2}))?\s*(am|pm)?/);
    if (!match) return fallbackStart ?? null;
    let hour = Number(match[1]);
    const minutes = Number(match[2] || '0');
    const suffix = match[3];
    if (suffix === 'pm' && hour < 12) hour += 12;
    if (suffix === 'am' && hour === 12) hour = 0;
    if (!suffix && fallbackStart !== undefined) {
      const fallbackHour = Math.floor(fallbackStart / 60);
      if (fallbackHour >= 12 && hour < 12) hour += 12;
    }
    return hour * 60 + minutes;
  }
}
