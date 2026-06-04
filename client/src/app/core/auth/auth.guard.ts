import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { AuthStore } from './auth.store';

export const authGuard: CanActivateFn = async () => {
  const authStore = inject(AuthStore);
  const router = inject(Router);

  await authStore.ensureInitialized();
  return authStore.user() ? true : router.parseUrl('/login');
};

export const guestGuard: CanActivateFn = async () => {
  const authStore = inject(AuthStore);
  const router = inject(Router);

  await authStore.ensureInitialized();
  return authStore.user() ? router.parseUrl('/dashboard') : true;
};

export const managerGuard: CanActivateFn = async () => {
  const authStore = inject(AuthStore);
  const router = inject(Router);

  await authStore.ensureInitialized();
  return authStore.profile()?.role === 'manager' ? true : router.parseUrl('/dashboard');
};
