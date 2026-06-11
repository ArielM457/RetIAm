import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import {
  AgendaItemResponse,
  ApiService,
  CourseEnrollmentResponse,
} from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';

type DayColumn = {
  key: string;
  date: Date;
  dayName: string;
  dayLabel: string;
  isToday: boolean;
  items: PositionedAgendaItem[];
};

type PositionedAgendaItem = {
  item: AgendaItemResponse;
  top: number;
  height: number;
  startLabel: string;
  endLabel: string;
  tone: 'study' | 'review' | 'lab' | 'checkin' | 'reminder';
};

type MiniCalendarCell = {
  key: string;
  date: Date;
  day: number;
  inCurrentMonth: boolean;
  isToday: boolean;
  isSelectedWeek: boolean;
};

const PIXELS_PER_HOUR = 64;
const START_HOUR = 7;
const END_HOUR = 21;
const DAY_NAMES = ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'];
const DAY_NAMES_LONG = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'];

@Component({
  selector: 'app-agenda-page',
  standalone: true,
  imports: [CommonModule, RouterLink, EmptyStateComponent],
  templateUrl: './agenda-page.component.html',
  styleUrl: './agenda-page.component.css',
})
export class AgendaPageComponent {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);

  protected readonly loading = signal(true);
  protected readonly items = signal<AgendaItemResponse[]>([]);
  protected readonly enrollments = signal<CourseEnrollmentResponse[]>([]);
  protected readonly anchorDate = signal(this.startOfDay(new Date()));
  protected readonly search = signal('');

  protected readonly enrollmentMap = computed(
    () => new Map(this.enrollments().map((item) => [item.id ?? '', item.certification_code] as const)),
  );

  protected readonly weekStart = computed(() => this.startOfWeek(this.anchorDate()));
  protected readonly visibleDays = computed<DayColumn[]>(() => {
    const weekStart = this.weekStart();
    const today = this.startOfDay(new Date());
    const items = this.filteredWeekItems();
    return Array.from({ length: 5 }, (_, index) => {
      const date = this.addDays(weekStart, index);
      const key = this.toDateKey(date);
      return {
        key,
        date,
        dayName: DAY_NAMES[(date.getDay() + 7) % 7].toUpperCase(),
        dayLabel: String(date.getDate()),
        isToday: this.toDateKey(today) === key,
        items: items
          .filter((item) => this.toDateKey(new Date(item.scheduled_start)) === key)
          .map((item) => this.positionItem(item)),
      };
    });
  });

  protected readonly hours = computed(() =>
    Array.from({ length: END_HOUR - START_HOUR + 1 }, (_, index) => START_HOUR + index),
  );

  protected readonly monthLabel = computed(() =>
    this.formatMonthRange(this.visibleDays().map((day) => day.date)),
  );

  protected readonly miniCalendarTitle = computed(() =>
    this.anchorDate().toLocaleDateString('es-BO', { month: 'long', year: 'numeric' }),
  );

  protected readonly miniCalendarCells = computed<MiniCalendarCell[]>(() => {
    const anchor = this.anchorDate();
    const first = new Date(anchor.getFullYear(), anchor.getMonth(), 1);
    const firstVisible = this.addDays(first, -first.getDay());
    const todayKey = this.toDateKey(new Date());
    const selectedWeek = this.visibleDays().map((day) => day.key);

    return Array.from({ length: 42 }, (_, index) => {
      const date = this.addDays(firstVisible, index);
      const key = this.toDateKey(date);
      return {
        key,
        date,
        day: date.getDate(),
        inCurrentMonth: date.getMonth() === anchor.getMonth(),
        isToday: key === todayKey,
        isSelectedWeek: selectedWeek.includes(key),
      };
    });
  });

  protected readonly filteredWeekItems = computed(() => {
    const q = this.search().trim().toLowerCase();
    const start = this.weekStart();
    const end = this.addDays(start, 5);
    return this.items().filter((item) => {
      const date = new Date(item.scheduled_start);
      if (date < start || date >= end) return false;
      if (!q) return true;
      const focus = Array.isArray(item.metadata['focus_points']) ? (item.metadata['focus_points'] as string[]).join(' ') : '';
      const criteria = Array.isArray(item.metadata['success_criteria']) ? (item.metadata['success_criteria'] as string[]).join(' ') : '';
      return `${item.title} ${item.item_type} ${focus} ${criteria}`.toLowerCase().includes(q);
    });
  });

  protected readonly selectedWeekSummary = computed(() => {
    const items = this.filteredWeekItems();
    return {
      total: items.length,
      sessions: items.filter((item) => item.item_type === 'study_session').length,
      reviews: items.filter((item) => item.item_type === 'review').length,
    };
  });

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      const [items, enrollments] = await Promise.all([
        this.api.listMyAgenda().catch(() => []),
        this.api.listMyEnrollments().catch(() => []),
      ]);
      this.items.set(items);
      this.enrollments.set(enrollments);
      const firstDate = items[0]?.scheduled_start ? this.startOfDay(new Date(items[0].scheduled_start)) : new Date();
      this.anchorDate.set(firstDate);
    } finally {
      this.loading.set(false);
    }
  }

  protected goToday(): void {
    this.anchorDate.set(this.startOfDay(new Date()));
  }

  protected moveWeek(offset: number): void {
    this.anchorDate.set(this.addDays(this.anchorDate(), offset * 7));
  }

  protected moveMonth(offset: number): void {
    const current = this.anchorDate();
    this.anchorDate.set(this.startOfDay(new Date(current.getFullYear(), current.getMonth() + offset, 1)));
  }

  protected selectMiniCalendarDate(date: Date): void {
    this.anchorDate.set(this.startOfDay(date));
  }

  protected async openItem(item: AgendaItemResponse): Promise<void> {
    const code = item.enrollment_id ? this.enrollmentMap().get(item.enrollment_id) : null;
    if (!code) return;
    await this.router.navigate(['/sessions'], { queryParams: { course: code } });
  }

  protected itemTypeLabel(type: string): string {
    return (
      {
        study_session: 'Sesion',
        review: 'Revision',
        lab: 'Lab',
        checkin: 'Check-in',
        reminder: 'Recordatorio',
      }[type] ?? type
    );
  }

  protected focusText(item: AgendaItemResponse): string {
    const focusPoints = Array.isArray(item.metadata['focus_points']) ? (item.metadata['focus_points'] as string[]) : [];
    const criteria = Array.isArray(item.metadata['success_criteria']) ? (item.metadata['success_criteria'] as string[]) : [];
    return focusPoints.join(' · ') || criteria.join(' · ') || 'Bloque guiado por el agente.';
  }

  protected canOpenItem(item: AgendaItemResponse): boolean {
    return !!(item.enrollment_id && this.enrollmentMap().get(item.enrollment_id));
  }

  protected hourLabel(hour: number): string {
    const suffix = hour >= 12 ? 'PM' : 'AM';
    const display = hour % 12 === 0 ? 12 : hour % 12;
    return `${display} ${suffix}`;
  }

  protected currentTimeTop(): number | null {
    const now = new Date();
    const today = this.visibleDays().find((day) => day.isToday);
    if (!today) return null;
    const minutes = now.getHours() * 60 + now.getMinutes();
    const startMinutes = START_HOUR * 60;
    const endMinutes = END_HOUR * 60;
    if (minutes < startMinutes || minutes > endMinutes) return null;
    return ((minutes - startMinutes) / 60) * PIXELS_PER_HOUR;
  }

  private positionItem(item: AgendaItemResponse): PositionedAgendaItem {
    const start = new Date(item.scheduled_start);
    const end = new Date(item.scheduled_end);
    const startMinutes = start.getHours() * 60 + start.getMinutes();
    const endMinutes = end.getHours() * 60 + end.getMinutes();
    const safeStart = Math.max(startMinutes, START_HOUR * 60);
    const safeEnd = Math.max(safeStart + 30, Math.min(endMinutes, END_HOUR * 60));

    return {
      item,
      top: ((safeStart - START_HOUR * 60) / 60) * PIXELS_PER_HOUR,
      height: Math.max(28, ((safeEnd - safeStart) / 60) * PIXELS_PER_HOUR),
      startLabel: start.toLocaleTimeString('es-BO', { hour: 'numeric', minute: '2-digit' }),
      endLabel: end.toLocaleTimeString('es-BO', { hour: 'numeric', minute: '2-digit' }),
      tone: this.resolveTone(item.item_type),
    };
  }

  private resolveTone(type: string): PositionedAgendaItem['tone'] {
    if (type === 'review') return 'review';
    if (type === 'lab') return 'lab';
    if (type === 'checkin') return 'checkin';
    if (type === 'reminder') return 'reminder';
    return 'study';
  }

  private formatMonthRange(days: Date[]): string {
    if (!days.length) return '';
    const first = days[0];
    const last = days[days.length - 1];
    const firstMonth = first.toLocaleDateString('en-US', { month: 'short' });
    const lastMonth = last.toLocaleDateString('en-US', { month: 'short' });
    if (firstMonth === lastMonth) {
      return `${firstMonth} ${first.getDate()} - ${last.getDate()}`;
    }
    return `${firstMonth} ${first.getDate()} - ${lastMonth} ${last.getDate()}`;
  }

  private startOfWeek(date: Date): Date {
    const day = date.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    return this.startOfDay(this.addDays(date, diff));
  }

  private startOfDay(date: Date): Date {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate());
  }

  private addDays(date: Date, amount: number): Date {
    const next = new Date(date);
    next.setDate(next.getDate() + amount);
    return this.startOfDay(next);
  }

  private toDateKey(date: Date): string {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
  }
}
