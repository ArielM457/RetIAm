import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';

import { ApiService, ReminderGenerationResponse, ReminderResponse } from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

@Component({
  selector: 'app-reminders-page',
  standalone: true,
  imports: [CommonModule, EmptyStateComponent, StatusPillComponent],
  templateUrl: './reminders-page.component.html',
  styleUrl: './reminders-page.component.css',
})
export class RemindersPageComponent {
  private readonly api = inject(ApiService);

  protected readonly reminders = signal<ReminderResponse[]>([]);
  protected readonly context = signal<Record<string, unknown>>({});
  protected readonly loading = signal(true);

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.loading.set(true);
    try {
      this.reminders.set(await this.api.listMyReminders());
    } finally {
      this.loading.set(false);
    }
  }

  protected async generate(): Promise<void> {
    const response: ReminderGenerationResponse = await this.api.generateReminders();
    this.reminders.set(response.reminders);
    this.context.set(response.workiq_context);
  }
}
