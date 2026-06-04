import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-icon',
  standalone: true,
  imports: [CommonModule],
  template: `
    <svg
      [attr.viewBox]="'0 0 24 24'"
      [ngClass]="className"
      fill="none"
      stroke="currentColor"
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="1.8"
    >
      @switch (name) {
        @case ('home') {
          <path d="M3 10.5 12 3l9 7.5"></path>
          <path d="M5 9.5V21h14V9.5"></path>
        }
        @case ('plan') {
          <path d="M4 6h16"></path>
          <path d="M4 12h10"></path>
          <path d="M4 18h7"></path>
          <path d="m16 15 2 2 4-5"></path>
        }
        @case ('session') {
          <path d="M4 5h16v10H4z"></path>
          <path d="m10 9 5 3-5 3z"></path>
          <path d="M8 19h8"></path>
        }
        @case ('bell') {
          <path d="M6 16h12"></path>
          <path d="M8 16V10a4 4 0 1 1 8 0v6"></path>
          <path d="M10 19a2 2 0 0 0 4 0"></path>
        }
        @case ('award') {
          <circle cx="12" cy="8" r="5"></circle>
          <path d="m8.5 13.5-1 7 4.5-2.5 4.5 2.5-1-7"></path>
        }
        @case ('profile') {
          <circle cx="12" cy="8" r="4"></circle>
          <path d="M5 20a7 7 0 0 1 14 0"></path>
        }
        @case ('team') {
          <path d="M16 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"></path>
          <circle cx="9.5" cy="7" r="3.5"></circle>
          <path d="M20 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M15 3.13a3.5 3.5 0 0 1 0 6.74"></path>
        }
        @case ('chart') {
          <path d="M4 20h16"></path>
          <path d="M7 16v-5"></path>
          <path d="M12 16V8"></path>
          <path d="M17 16v-9"></path>
        }
        @case ('summary') {
          <path d="M7 4h10l3 3v13H7z"></path>
          <path d="M17 4v4h4"></path>
          <path d="M10 12h6"></path>
          <path d="M10 16h6"></path>
        }
        @case ('logout') {
          <path d="M14 8V4H5v16h9v-4"></path>
          <path d="m10 12 10 0"></path>
          <path d="m17 9 3 3-3 3"></path>
        }
        @case ('spark') {
          <path d="m12 3 1.8 4.7L18.5 9l-4.7 1.3L12 15l-1.8-4.7L5.5 9l4.7-1.3z"></path>
        }
        @case ('clock') {
          <circle cx="12" cy="12" r="8"></circle>
          <path d="M12 8v4l3 2"></path>
        }
        @case ('shield') {
          <path d="M12 3 5 6v5c0 5 3.5 8.5 7 10 3.5-1.5 7-5 7-10V6z"></path>
        }
        @case ('book') {
          <path d="M5 4h12a2 2 0 0 1 2 2v14H7a2 2 0 0 0-2 2"></path>
          <path d="M5 4v16"></path>
        }
        @case ('menu') {
          <path d="M4 7h16"></path>
          <path d="M4 12h16"></path>
          <path d="M4 17h16"></path>
        }
        @case ('close') {
          <path d="m6 6 12 12"></path>
          <path d="m18 6-12 12"></path>
        }
        @case ('notification') {
          <path d="M6 16h12"></path>
          <path d="M8 16V10a4 4 0 1 1 8 0v6"></path>
          <path d="M10 19a2 2 0 0 0 4 0"></path>
        }
        @case ('ai') {
          <rect x="5" y="7" width="14" height="10" rx="3"></rect>
          <path d="M9 7V5"></path>
          <path d="M15 7V5"></path>
          <circle cx="10" cy="12" r="1"></circle>
          <circle cx="14" cy="12" r="1"></circle>
          <path d="M10 15h4"></path>
        }
        @case ('arrow-right') {
          <path d="M5 12h14"></path>
          <path d="m13 6 6 6-6 6"></path>
        }
        @case ('progress') {
          <path d="M4 20h16"></path>
          <path d="M7 16v-4"></path>
          <path d="M12 16V7"></path>
          <path d="M17 16v-7"></path>
        }
        @case ('warning') {
          <path d="M12 4 3 20h18L12 4z"></path>
          <path d="M12 10v4"></path>
          <path d="M12 17h.01"></path>
        }
        @case ('document') {
          <path d="M8 3h7l4 4v14H8z"></path>
          <path d="M15 3v4h4"></path>
          <path d="M10 12h6"></path>
          <path d="M10 16h6"></path>
        }
        @case ('check-circle') {
          <circle cx="12" cy="12" r="9"></circle>
          <path d="m8.5 12.5 2.5 2.5 4.5-5"></path>
        }
        @default {
          <circle cx="12" cy="12" r="8"></circle>
        }
      }
    </svg>
  `,
})
export class AppIconComponent {
  @Input({ required: true }) name = 'home';
  @Input() className = 'h-5 w-5';
}
