import { Routes } from '@angular/router';

import { authGuard, guestGuard, managerGuard } from './core/auth/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    canActivate: [guestGuard],
    loadComponent: () =>
      import('./features/auth/login-page/login-page.component').then(
        (module) => module.LoginPageComponent,
      ),
  },
  {
    path: '',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/layout/app-shell.component').then((module) => module.AppShellComponent),
    children: [
      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'dashboard',
      },
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/dashboard/dashboard-page.component').then(
            (module) => module.DashboardPageComponent,
          ),
      },
      {
        path: 'onboarding',
        loadComponent: () =>
          import('./features/onboarding/onboarding-page.component').then(
            (module) => module.OnboardingPageComponent,
          ),
      },
      {
        path: 'plan',
        loadComponent: () =>
          import('./features/learning/learning-plan-page.component').then(
            (module) => module.LearningPlanPageComponent,
          ),
      },
      {
        path: 'sessions',
        loadComponent: () =>
          import('./features/learning/learning-session-page.component').then(
            (module) => module.LearningSessionPageComponent,
          ),
      },
      {
        path: 'reminders',
        loadComponent: () =>
          import('./features/coach/reminders-page.component').then(
            (module) => module.RemindersPageComponent,
          ),
      },
      {
        path: 'suggestions',
        loadComponent: () =>
          import('./features/suggestions/suggestions-page.component').then(
            (module) => module.SuggestionsPageComponent,
          ),
      },
      {
        path: 'certificates',
        loadComponent: () =>
          import('./features/certificates/certificates-page.component').then(
            (module) => module.CertificatesPageComponent,
          ),
      },
      {
        path: 'profile',
        loadComponent: () =>
          import('./features/profile/profile-page.component').then(
            (module) => module.ProfilePageComponent,
          ),
      },
      {
        path: 'manager/dashboard',
        canActivate: [managerGuard],
        loadComponent: () =>
          import('./features/manager/manager-dashboard-page.component').then(
            (module) => module.ManagerDashboardPageComponent,
          ),
      },
      {
        path: 'manager/team',
        canActivate: [managerGuard],
        loadComponent: () =>
          import('./features/manager/manager-team-page.component').then(
            (module) => module.ManagerTeamPageComponent,
          ),
      },
      {
        path: 'manager/weekly-summary',
        canActivate: [managerGuard],
        loadComponent: () =>
          import('./features/manager/manager-weekly-summary-page.component').then(
            (module) => module.ManagerWeeklySummaryPageComponent,
          ),
      },
    ],
  },
  {
    path: '**',
    redirectTo: 'dashboard',
  },
];
