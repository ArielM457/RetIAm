import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ApiService, CustomCourseResult, TeamSummary } from '../../core/services/api.service';

const TEMPLATE = `# Título del curso
Resumen breve del curso (opcional).

## Sección 1: Fundamentos
### Lección 1.1: Conceptos clave
Aquí va el contenido de la lección en Markdown. Explica el tema con el detalle
que quieras; este texto es lo que leerá el estudiante y lo que la IA usará para
responder dudas.

#### Lab: Práctica guiada
Instrucciones del laboratorio (opcional).

## Sección 2: Implementación
### Lección 2.1: Paso a paso
Contenido…

## Sección 3: Operación
### Lección 3.1: Buenas prácticas
Contenido…
`;

@Component({
  selector: 'app-manager-custom-course-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <section class="page-shell cc">
      <header class="cc-head">
        <p class="eyebrow">Team Lead · Curso personalizado</p>
        <h1 class="cc-title">Crea un <span class="grad">curso a medida</span> para tu equipo</h1>
        <p class="cc-sub">
          Sube o pega un Markdown con la estructura del curso. La IA lo organiza, valida que
          cumpla los mínimos para ser certificable e indexa el contenido para que el tutor
          pueda responder dudas. Queda visible <strong>solo para tu equipo</strong>.
        </p>
      </header>

      <div class="cc-grid">
        <!-- Editor -->
        <div class="glass-card cc-editor">
          <label class="field">
            <span class="field-label">Equipo</span>
            <select class="input-pill" [(ngModel)]="selectedTeamId">
              <option *ngFor="let t of teams()" [value]="t.id">{{ t.name }}</option>
            </select>
          </label>

          <label class="field">
            <span class="field-label">Título (opcional, si tu Markdown no trae # Título)</span>
            <input class="input-pill" [(ngModel)]="title" placeholder="Ej. Onboarding de nuestra plataforma" />
          </label>

          <label class="field">
            <span class="field-label">Markdown del curso</span>
            <textarea
              class="input-pill cc-md"
              [(ngModel)]="markdown"
              rows="16"
              placeholder="Pega aquí el Markdown del curso…"
            ></textarea>
          </label>

          <div class="cc-actions">
            <input type="file" accept=".md,.markdown,.txt,text/plain" (change)="onFile($event)" />
            <button class="btn btn-ghost btn-sm" (click)="useTemplate()">📄 Usar plantilla</button>
            <span class="spacer"></span>
            <button class="btn btn-ghost" [disabled]="!canSubmit() || busy()" (click)="doPreview()">
              {{ previewing() ? 'Analizando…' : '👁 Previsualizar' }}
            </button>
            <button class="btn btn-primary" [disabled]="!canSubmit() || busy()" (click)="doCreate()">
              {{ creating() ? 'Creando…' : '✨ Crear curso' }}
            </button>
          </div>
          <p class="cc-error" *ngIf="error()">{{ error() }}</p>
        </div>

        <!-- Resultado -->
        <div class="glass-card cc-result" *ngIf="result() as r; else hint">
          <div class="cc-badges">
            <span class="badge" [class.ok]="r.is_certifiable" [class.warn]="!r.is_certifiable">
              {{ r.is_certifiable ? '✅ Certificable' : '⚠️ Borrador' }}
            </span>
            <span class="badge muted">{{ r.section_count }} secciones</span>
            <span class="badge muted">{{ r.lesson_count }} lecciones</span>
            <span class="badge muted">{{ r.lab_count }} labs</span>
            <span class="badge muted">{{ r.total_duration_minutes }} min</span>
          </div>

          <h2 class="cc-rtitle">{{ r.title }}</h2>
          <p class="cc-code" *ngIf="created()">
            Código: <code>{{ r.certification_code }}</code> · {{ r.chunk_count || 0 }} fragmentos indexados (RAG)
          </p>
          <p class="cc-msg" *ngIf="r.message">{{ r.message }}</p>

          <div class="cc-issues" *ngIf="r.issues.length">
            <p class="mini-label">Falta para ser certificable</p>
            <ul>
              <li *ngFor="let i of r.issues">{{ i }}</li>
            </ul>
          </div>
          <p class="cc-cert" *ngIf="r.is_certifiable">
            Examen de certificación: {{ r.exam_questions }} preguntas · aprueba con {{ r.exam_pass_percent }}%.
          </p>

          <div class="cc-outline">
            <p class="mini-label">Estructura</p>
            <div class="cc-section" *ngFor="let s of r.sections">
              <strong>{{ s.title }}</strong>
              <ul>
                <li *ngFor="let l of s.lessons">📘 {{ l }}</li>
                <li *ngFor="let lab of s.labs">🧪 {{ lab }}</li>
              </ul>
            </div>
          </div>
        </div>

        <ng-template #hint>
          <div class="glass-card cc-result cc-empty">
            <p>Pega tu Markdown y pulsa <strong>Previsualizar</strong> para ver la estructura y si
            cumple los mínimos. Luego <strong>Crear curso</strong> lo publica para tu equipo.</p>
            <p class="mini-label">Formato esperado</p>
            <pre>{{ templatePreview }}</pre>
          </div>
        </ng-template>
      </div>
    </section>
  `,
  styles: [
    `
      :host { display: block; }
      .cc { padding-block: 1.5rem 3rem; display: flex; flex-direction: column; gap: 1.25rem; }
      .cc-title { font-size: clamp(1.5rem, 3vw, 2.1rem); }
      .grad { background: linear-gradient(120deg, #a855f7, #2563eb); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .cc-sub { color: var(--muted); max-width: 80ch; line-height: 1.6; }
      .cc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; align-items: start; }
      @media (max-width: 900px) { .cc-grid { grid-template-columns: 1fr; } }
      .cc-editor, .cc-result { padding: 1.4rem; border-radius: 1.1rem; display: flex; flex-direction: column; gap: 0.9rem; }
      .field { display: flex; flex-direction: column; gap: 0.35rem; }
      .field-label { font-size: 0.8rem; color: var(--muted); }
      select.input-pill { appearance: none; cursor: pointer; }
      .cc-md { width: 100%; resize: vertical; font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 0.84rem; line-height: 1.5; }
      .cc-actions { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }
      .cc-actions .spacer { flex: 1; }
      .cc-error { color: #fca5a5; font-size: 0.85rem; }
      .cc-badges { display: flex; gap: 0.4rem; flex-wrap: wrap; }
      .badge { font-size: 0.74rem; padding: 0.25rem 0.6rem; border-radius: 999px; border: 1px solid var(--line); }
      .badge.ok { background: rgba(34,197,94,0.16); border-color: #22c55e; color: #bbf7d0; }
      .badge.warn { background: rgba(234,179,8,0.16); border-color: #eab308; color: #fde68a; }
      .badge.muted { color: var(--muted); }
      .cc-rtitle { font-size: 1.3rem; }
      .cc-code { font-size: 0.82rem; color: var(--muted); }
      .cc-code code { color: #c4b5fd; }
      .cc-msg { color: #dbe2f0; font-size: 0.9rem; }
      .mini-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em; color: #c4b5fd; margin-bottom: 0.25rem; }
      .cc-issues ul, .cc-section ul, .cc-outline ul { margin: 0.2rem 0 0.6rem 1rem; display: flex; flex-direction: column; gap: 0.2rem; }
      .cc-issues li { color: #fde68a; font-size: 0.86rem; }
      .cc-cert { color: #bbf7d0; font-size: 0.86rem; }
      .cc-section { margin-bottom: 0.6rem; }
      .cc-section li { font-size: 0.86rem; color: var(--ink); }
      .cc-empty p { color: var(--muted); line-height: 1.6; }
      .cc-empty pre { background: rgba(2,6,23,0.5); border: 1px solid var(--line); border-radius: 0.7rem; padding: 0.9rem; overflow-x: auto; font-size: 0.78rem; color: #cbd5e1; }
    `,
  ],
})
export class ManagerCustomCoursePageComponent {
  private readonly api = inject(ApiService);

  protected readonly teams = signal<TeamSummary[]>([]);
  protected selectedTeamId = '';
  protected title = '';
  protected markdown = '';

  protected readonly previewing = signal(false);
  protected readonly creating = signal(false);
  protected readonly preview = signal<CustomCourseResult | null>(null);
  protected readonly created = signal<CustomCourseResult | null>(null);
  protected readonly error = signal<string | null>(null);

  protected readonly templatePreview = TEMPLATE;

  constructor() {
    void this.loadTeams();
  }

  protected result(): CustomCourseResult | null {
    return this.created() ?? this.preview();
  }

  protected busy(): boolean {
    return this.previewing() || this.creating();
  }

  protected canSubmit(): boolean {
    return !!this.selectedTeamId && this.markdown.trim().length > 20;
  }

  private async loadTeams(): Promise<void> {
    try {
      const teams = await this.api.listTeams();
      this.teams.set(teams);
      if (teams.length) this.selectedTeamId = teams[0].id;
    } catch {
      this.error.set('No pude cargar tus equipos.');
    }
  }

  protected onFile(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      this.markdown = String(reader.result || '').slice(0, 40000);
    };
    reader.readAsText(file);
  }

  protected useTemplate(): void {
    if (!this.markdown.trim()) this.markdown = TEMPLATE;
  }

  protected async doPreview(): Promise<void> {
    if (!this.canSubmit()) return;
    this.error.set(null);
    this.created.set(null);
    this.previewing.set(true);
    try {
      this.preview.set(
        await this.api.previewCustomCourse(this.selectedTeamId, this.markdown, this.title || undefined),
      );
    } catch (e) {
      this.error.set(e instanceof Error ? e.message : 'No se pudo previsualizar el curso.');
    } finally {
      this.previewing.set(false);
    }
  }

  protected async doCreate(): Promise<void> {
    if (!this.canSubmit()) return;
    this.error.set(null);
    this.creating.set(true);
    try {
      const res = await this.api.createCustomCourse(
        this.selectedTeamId,
        this.markdown,
        this.title || undefined,
      );
      this.created.set(res);
      this.preview.set(null);
    } catch (e) {
      this.error.set(e instanceof Error ? e.message : 'No se pudo crear el curso.');
    } finally {
      this.creating.set(false);
    }
  }
}
