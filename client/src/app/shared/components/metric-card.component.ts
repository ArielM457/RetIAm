import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-metric-card',
  standalone: true,
  template: `
    <article class="gradient-border glass-card relative rounded-[1.5rem] p-5">
      <p class="text-sm text-[var(--muted)]">{{ label }}</p>
      <p class="mt-3 text-3xl font-semibold">{{ value }}</p>
      @if (hint) {
        <p class="mt-2 text-sm text-[var(--muted)]">{{ hint }}</p>
      }
    </article>
  `,
})
export class MetricCardComponent {
  @Input({ required: true }) label = '';
  @Input({ required: true }) value = '';
  @Input() hint = '';
}
