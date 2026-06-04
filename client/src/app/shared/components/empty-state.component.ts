import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-empty-state',
  standalone: true,
  template: `
    <div class="rounded-[1.5rem] border border-dashed border-white/15 bg-white/[0.03] p-6 text-center">
      <h3 class="text-lg font-semibold">{{ title }}</h3>
      <p class="mt-2 text-sm text-[var(--muted)]">{{ message }}</p>
    </div>
  `,
})
export class EmptyStateComponent {
  @Input({ required: true }) title = '';
  @Input({ required: true }) message = '';
}
