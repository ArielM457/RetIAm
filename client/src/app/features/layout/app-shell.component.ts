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
  protected readonly progressMenuOpen = signal(false);
  protected readonly mobileProgressMenuOpen = signal(false);

  protected readonly employeePrimaryLinks = [
    { label: 'Inicio', path: '/dashboard', icon: 'home' },
    { label: 'Cursos', path: '/catalog', icon: 'plan' },
    { label: 'Metaverso', path: '/auxiliaturas', icon: 'spark' },
  ];

  protected readonly employeeProgressLinks = [
    { label: 'Mi Plan', path: '/plan', icon: 'plan' },
    { label: 'Sesiones', path: '/sessions', icon: 'session' },
    { label: 'Brechas', path: '/suggestions', icon: 'spark' },
    { label: 'Recordatorios', path: '/reminders', icon: 'bell' },
    { label: 'Certificados', path: '/certificates', icon: 'award' },
  ];

  protected readonly managerPrimaryLinks = [
    { label: 'Inicio', path: '/dashboard', icon: 'home' },
    { label: 'Equipo', path: '/manager/dashboard', icon: 'team' },
    { label: 'Ranking', path: '/manager/insights', icon: 'chart' },
    { label: 'Curso a medida', path: '/manager/custom-course', icon: 'plan' },
  ];

  protected readonly managerProgressLinks = [
    { label: 'Mi Plan', path: '/plan', icon: 'plan' },
    { label: 'Sesiones', path: '/sessions', icon: 'session' },
    { label: 'Recordatorios', path: '/reminders', icon: 'bell' },
    { label: 'Certificados', path: '/certificates', icon: 'award' },
    { label: 'Brechas', path: '/manager/dashboard', icon: 'chart' },
    { label: 'Resumen', path: '/manager/weekly-summary', icon: 'summary' },
  ];

  protected readonly primaryLinks = computed(() =>
    this.profile()?.role === 'manager' ? this.managerPrimaryLinks : this.employeePrimaryLinks,
  );

  protected readonly progressLinks = computed(() =>
    this.profile()?.role === 'manager' ? this.managerProgressLinks : this.employeeProgressLinks,
  );

  protected readonly homePath = computed(() =>
    '/dashboard',
  );

  protected toggleMenu(): void {
    this.menuOpen.update((current) => !current);
  }

  protected toggleProgressMenu(): void {
    this.progressMenuOpen.update((current) => !current);
  }

  protected toggleMobileProgressMenu(): void {
    this.mobileProgressMenuOpen.update((current) => !current);
  }

  protected closeMenu(): void {
    this.menuOpen.set(false);
    this.mobileProgressMenuOpen.set(false);
  }

  protected closeProgressMenu(): void {
    this.progressMenuOpen.set(false);
  }

  protected async signOut(): Promise<void> {
    await this.authStore.signOut();
  }
}
