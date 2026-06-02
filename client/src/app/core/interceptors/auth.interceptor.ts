import { HttpInterceptorFn } from '@angular/common/http';
import { from } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { supabase } from '../config/supabase-client';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  return from(supabase.auth.getSession()).pipe(
    switchMap(({ data }) => {
      const token = data.session?.access_token;
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
