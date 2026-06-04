import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';

import { ApiService, CertificateResponse } from '../../core/services/api.service';
import { EmptyStateComponent } from '../../shared/components/empty-state.component';

@Component({
  selector: 'app-certificates-page',
  standalone: true,
  imports: [CommonModule, EmptyStateComponent],
  templateUrl: './certificates-page.component.html',
  styleUrl: './certificates-page.component.css',
})
export class CertificatesPageComponent {
  private readonly api = inject(ApiService);

  protected readonly certificates = signal<CertificateResponse[]>([]);

  constructor() {
    void this.load();
  }

  protected async load(): Promise<void> {
    this.certificates.set(await this.api.listCertificates());
  }
}
