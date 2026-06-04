import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';

import { ApiService, SuggestionResponse } from '../../core/services/api.service';
import { AppIconComponent } from '../../shared/components/app-icon.component';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';
import { StatusPillComponent } from '../../shared/components/status-pill.component';

@Component({
  selector: 'app-suggestions-page',
  standalone: true,
  imports: [CommonModule, AppIconComponent, EmptyStateComponent, StatusPillComponent],
  templateUrl: './suggestions-page.component.html',
  styleUrl: './suggestions-page.component.css',
})
export class SuggestionsPageComponent {
  private readonly api = inject(ApiService);

  protected readonly suggestions = signal<SuggestionResponse[]>([]);

  constructor() {
    void this.load();
  }

  protected unreadCount(): number {
    return this.suggestions().filter((item) => item.status !== 'read').length;
  }

  protected suggestionTone(category: string): 'info' | 'warning' | 'success' {
    if (category.toLowerCase().includes('horario')) {
      return 'info';
    }

    if (category.toLowerCase().includes('rendimiento')) {
      return 'warning';
    }

    return 'success';
  }

  private async load(): Promise<void> {
    this.suggestions.set(await this.api.listMySuggestions());
  }
}
