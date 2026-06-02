import { CommonModule } from '@angular/common';
import { Component, computed, inject } from '@angular/core';

import { AuthStore } from '../../core/auth/auth.store';

@Component({
  selector: 'app-dashboard-page',
  imports: [CommonModule],
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.css',
})
export class DashboardPageComponent {
  protected readonly authStore = inject(AuthStore);
  protected readonly profile = computed(() => this.authStore.profile());
  protected readonly user = computed(() => this.authStore.user());
  protected readonly learningStyle = computed(
    () => this.profile()?.learning_style.join(', ') || 'Todavia no definido',
  );

  protected async signOut(): Promise<void> {
    await this.authStore.signOut();
  }
}
