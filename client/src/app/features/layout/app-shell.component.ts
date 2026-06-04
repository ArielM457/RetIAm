import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { AuthStore } from '../../core/auth/auth.store';
import { AppIconComponent } from '../../shared/components/app-icon.component';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, AppIconComponent],
  templateUrl: './app-shell.component.html',
  styleUrl: './app-shell.component.css',
})
export class AppShellComponent {
  protected readonly authStore = inject(AuthStore);
  protected readonly profile = computed(() => this.authStore.profile());
  protected readonly menuOpen = signal(false);

  protected readonly employeeLinks = [
    { label: 'Inicio', path: '/dashboard', icon: 'home' },
    { label: 'Mi Plan', path: '/plan', icon: 'plan' },
    { label: 'Sesiones', path: '/sessions', icon: 'session' },
    { label: 'Brechas', path: '/suggestions', icon: 'spark' },
    { label: 'Recordatorios', path: '/reminders', icon: 'bell' },
    { label: 'Certificados', path: '/certificates', icon: 'award' },
  ];

  protected readonly managerLinks = [
    { label: 'Inicio', path: '/dashboard', icon: 'home' },
    { label: 'Equipo', path: '/manager/team', icon: 'team' },
    { label: 'Brechas', path: '/manager/dashboard', icon: 'chart' },
    { label: 'Resumen', path: '/manager/weekly-summary', icon: 'summary' },
  ];

  protected readonly links = computed(() =>
    this.profile()?.role === 'manager' ? this.managerLinks : this.employeeLinks,
  );

  protected toggleMenu(): void {
    this.menuOpen.update((current) => !current);
  }

  protected closeMenu(): void {
    this.menuOpen.set(false);
  }

  protected async signOut(): Promise<void> {
    await this.authStore.signOut();
  }
}
