import { Injectable, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Session, User } from '@supabase/supabase-js';

import { supabase } from '../config/supabase-client';
import { ApiService, AuthSessionResponse, UserProfile } from '../services/api.service';

type AuthMode = 'signin' | 'signup';

type AuthState = {
  initialized: boolean;
  loading: boolean;
  mode: AuthMode;
  session: Session | null;
  user: User | null;
  profile: UserProfile | null;
  error: string | null;
};

type AuthPayload = {
  email: string;
  password: string;
  fullName?: string;
  role?: 'manager' | 'employee';
};

@Injectable({ providedIn: 'root' })
export class AuthStore {
  private readonly router = inject(Router);
  private readonly apiService = inject(ApiService);
  private readonly state = signal<AuthState>({
    initialized: false,
    loading: true,
    mode: 'signin',
    session: null,
    user: null,
    profile: null,
    error: null,
  });
  private initializationPromise: Promise<void> | null = null;

  readonly initialized = computed(() => this.state().initialized);
  readonly loading = computed(() => this.state().loading);
  readonly session = computed(() => this.state().session);
  readonly user = computed(() => this.state().user);
  readonly profile = computed(() => this.state().profile);
  readonly mode = computed(() => this.state().mode);
  readonly error = computed(() => this.state().error);
  readonly isManager = computed(() => this.profile()?.role === 'manager');

  constructor() {
    void this.ensureInitialized();
    supabase.auth.onAuthStateChange((_event, session) => {
      this.state.update((current) => ({
        ...current,
        session,
        user: session?.user ?? null,
      }));

      if (session?.user) {
        void this.refreshProfile();
        return;
      }

      this.state.update((current) => ({
        ...current,
        profile: null,
        loading: false,
      }));
    });
  }

  async ensureInitialized(): Promise<void> {
    if (this.initializationPromise) {
      return this.initializationPromise;
    }

    this.initializationPromise = (async () => {
      const { data } = await supabase.auth.getSession();
      const session = data.session;

      this.state.update((current) => ({
        ...current,
        initialized: true,
        session,
        user: session?.user ?? null,
      }));

      if (session?.user) {
        await this.refreshProfile();
      } else {
        this.state.update((current) => ({
          ...current,
          loading: false,
        }));
      }
    })();

    return this.initializationPromise;
  }

  setMode(mode: AuthMode): void {
    this.state.update((current) => ({ ...current, mode, error: null }));
  }

  async signIn(payload: AuthPayload): Promise<void> {
    this.setLoading(true);
    this.clearError();

    try {
      const response = await this.apiService.login({
        email: payload.email,
        password: payload.password,
      });

      await this.applyBackendSession(response);

      await this.refreshProfile();
      await this.router.navigate(['/dashboard']);
    } catch (error) {
      this.setError(error instanceof Error ? error.message : 'No se pudo iniciar sesion.');
    } finally {
      this.setLoading(false);
    }
  }

  async signUp(payload: AuthPayload): Promise<void> {
    this.setLoading(true);
    this.clearError();

    try {
      const emailCheck = await this.apiService.validateEmail(payload.email);
      if (!emailCheck.is_valid) {
        throw new Error(emailCheck.message);
      }

      const response = await this.apiService.register({
        email: payload.email,
        password: payload.password,
        full_name: payload.fullName,
        role: payload.role ?? 'employee',
      });

      await this.applyBackendSession(response);

      await this.refreshProfile();
      await this.router.navigate(['/dashboard']);
    } catch (error) {
      this.setError(error instanceof Error ? error.message : 'No se pudo crear la cuenta.');
    } finally {
      this.setLoading(false);
    }
  }

  async refreshProfile(): Promise<void> {
    try {
      const profile = await this.apiService.getCurrentProfile();
      this.state.update((current) => ({
        ...current,
        profile,
        loading: false,
      }));
    } catch (error) {
      this.setError(
        error instanceof Error
          ? error.message
          : 'No se pudo cargar el perfil desde el backend.',
      );
      this.setLoading(false);
    }
  }

  async signOut(): Promise<void> {
    await supabase.auth.signOut();
    this.state.set({
      initialized: true,
      loading: false,
      mode: 'signin',
      session: null,
      user: null,
      profile: null,
      error: null,
    });
    await this.router.navigate(['/login']);
  }

  private setLoading(loading: boolean): void {
    this.state.update((current) => ({ ...current, loading }));
  }

  private setError(error: string | null): void {
    this.state.update((current) => ({ ...current, error }));
  }

  private clearError(): void {
    this.setError(null);
  }

  private async applyBackendSession(payload: AuthSessionResponse): Promise<void> {
    const { error } = await supabase.auth.setSession({
      access_token: payload.access_token,
      refresh_token: payload.refresh_token,
    });

    if (error) {
      throw error;
    }
  }
}
