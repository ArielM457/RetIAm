import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-status-pill',
  standalone: true,
  template: `
    <span
      class="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]"
      [style.background]="background"
      [style.color]="color"
    >
      {{ label }}
    </span>
  `,
})
export class StatusPillComponent {
  @Input({ required: true }) label = '';
  @Input() tone: 'neutral' | 'success' | 'warning' | 'danger' | 'info' = 'neutral';

  get background(): string {
    switch (this.tone) {
      case 'success':
        return 'rgba(34, 197, 94, 0.18)';
      case 'warning':
        return 'rgba(245, 158, 11, 0.18)';
      case 'danger':
        return 'rgba(239, 68, 68, 0.18)';
      case 'info':
        return 'rgba(99, 102, 241, 0.18)';
      default:
        return 'rgba(148, 163, 184, 0.16)';
    }
  }

  get color(): string {
    switch (this.tone) {
      case 'success':
        return '#86efac';
      case 'warning':
        return '#fcd34d';
      case 'danger':
        return '#fca5a5';
      case 'info':
        return '#c4b5fd';
      default:
        return '#cbd5e1';
    }
  }
}
