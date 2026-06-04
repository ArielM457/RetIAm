import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { AuthStore } from '../../../core/auth/auth.store';

@Component({
  selector: 'app-login-page',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.css',
})
export class LoginPageComponent {
  private readonly fb = inject(FormBuilder);
  protected readonly authStore = inject(AuthStore);
  protected readonly mode = computed(() => this.authStore.mode());
  protected readonly loading = computed(() => this.authStore.loading());
  protected readonly error = computed(() => this.authStore.error());
  protected readonly submitted = signal(false);
  protected readonly showPassword = signal(false);

  protected readonly form = this.fb.nonNullable.group({
    fullName: [''],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
    role: ['employee' as 'manager' | 'employee'],
  });

  protected setMode(mode: 'signin' | 'signup'): void {
    this.authStore.setMode(mode);
    this.submitted.set(false);
  }

  protected togglePasswordVisibility(): void {
    this.showPassword.update((value) => !value);
  }

  protected async submit(): Promise<void> {
    this.submitted.set(true);
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const rawValue = this.form.getRawValue();
    if (this.mode() === 'signup') {
      await this.authStore.signUp(rawValue);
      return;
    }

    await this.authStore.signIn(rawValue);
  }
}
