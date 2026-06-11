import { HttpInterceptorFn } from '@angular/common/http';
import { from } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { supabase } from '../config/supabase-client';

let cachedAccessToken: string | null = null;
let tokenBootstrap: Promise<void> | null = null;

supabase.auth.onAuthStateChange((_event, session) => {
  cachedAccessToken = session?.access_token ?? null;
});

async function ensureAccessTokenLoaded(): Promise<void> {
  if (cachedAccessToken) {
    return;
  }

  if (!tokenBootstrap) {
    tokenBootstrap = supabase.auth
      .getSession()
      .then(({ data }) => {
        cachedAccessToken = data.session?.access_token ?? null;
      })
      .catch(() => {
        // Si el lock de Supabase esta ocupado, dejamos que el request siga y
        // el siguiente cambio de estado rehidrate el token.
        cachedAccessToken = null;
      })
      .finally(() => {
        tokenBootstrap = null;
      });
  }

  await tokenBootstrap;
}

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  return from(ensureAccessTokenLoaded()).pipe(
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
