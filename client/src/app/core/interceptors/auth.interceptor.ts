import { HttpInterceptorFn } from '@angular/common/http';
import { from } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { supabase } from '../config/supabase-client';

let cachedAccessToken: string | null = null;
const sessionBootstrap = supabase.auth.getSession().then(({ data }) => {
  cachedAccessToken = data.session?.access_token ?? null;
});

supabase.auth.onAuthStateChange((_event, session) => {
  cachedAccessToken = session?.access_token ?? null;
});

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  return from(sessionBootstrap).pipe(
    switchMap(() => {
      const token = cachedAccessToken;
      const authorizedRequest = token
        ? request.clone({
            setHeaders: {
              Authorization: `Bearer ${token}`,
            },
          })
        : request;

      return next(authorizedRequest);
    }),
  );
};
