import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ApiService, TeamRanking, TeamSummary } from '../../core/services/api.service';

@Component({
  selector: 'app-manager-insights-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <section class="page-shell ins">
      <header class="ins-head">
        <p class="eyebrow">Team Lead · Insights</p>
        <h1 class="ins-title">Ranking y <span class="grad">acciones</span> del equipo</h1>
        <p class="ins-sub">
          Un agente cruza el progreso, los tiempos y la aprobación de exámenes para destacar a tu
          mejor talento, el récord de tiempo y la metodología que mejor rinde. Y notificas a los
          que están en riesgo con un clic.
        </p>
      </header>

      <div class="ins-bar">
        <label class="field">
          <span class="field-label">Equipo</span>
          <select class="input-pill" [(ngModel)]="selectedTeamId" (ngModelChange)="load()">
            <option *ngFor="let t of teams()" [value]="t.id">{{ t.name }}</option>
          </select>
        </label>
        <span class="spacer"></span>
        <button class="btn btn-ghost" [disabled]="!selectedTeamId || loading()" (click)="load()">
          ↻ Actualizar
        </button>
        <button class="btn btn-primary" [disabled]="!selectedTeamId || nudging()" (click)="doNudgeAtRisk()">
          {{ nudging() ? 'Avisando…' : '🔔 Avisar a los en riesgo' }}
        </button>
      </div>

      <p class="ins-note" *ngIf="nudgeResult()">{{ nudgeResult() }}</p>
      <p class="ins-error" *ngIf="error()">{{ error() }}</p>

      <ng-container *ngIf="ranking() as r">
        <!-- Insight del agente -->
        <div class="glass-card ins-narr">
          <span class="badge">🤖 Agente</span>
          <p>{{ r.narrative }}</p>
        </div>

        <!-- Tarjetas destacadas -->
        <div class="ins-cards">
          <div class="glass-card hl">
            <p class="mini-label">🏆 Top performer</p>
            <strong>{{ r.members.length ? r.members[0].full_name : '—' }}</strong>
            <span *ngIf="r.members.length">score {{ r.members[0].score }} · {{ r.members[0].progress_percent }}%</span>
          </div>
          <div class="glass-card hl">
            <p class="mini-label">⏱ Récord de tiempo</p>
            <strong>{{ r.record_holder ? r.record_holder.full_name : 'Sin datos' }}</strong>
            <span *ngIf="r.record_holder">{{ r.record_holder.fastest_minutes }} min / sección</span>
          </div>
          <div class="glass-card hl">
            <p class="mini-label">🎯 Mejor metodología</p>
            <strong>{{ r.best_methodology ? r.best_methodology.style : 'Sin datos' }}</strong>
            <span *ngIf="r.best_methodology">{{ r.best_methodology.avg_progress }}% progreso medio</span>
          </div>
        </div>

        <!-- Tabla de ranking -->
        <div class="glass-card ins-table">
          <p class="mini-label">Ranking del equipo</p>
          <table>
            <thead>
              <tr>
                <th>#</th><th>Miembro</th><th>Score</th><th>Progreso</th>
                <th>Sesiones</th><th>Aprob.</th><th>Más rápido</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let m of r.members">
                <td>{{ m.rank }}</td>
                <td>{{ m.full_name }}</td>
                <td>{{ m.score }}</td>
                <td>{{ m.progress_percent }}%</td>
                <td>{{ m.completed_sessions }}</td>
                <td>{{ m.pass_rate }}%</td>
                <td>{{ m.fastest_minutes !== null ? m.fastest_minutes + ' min' : '—' }}</td>
              </tr>
              <tr *ngIf="!r.members.length">
                <td colspan="7" class="empty">Aún no hay miembros con datos en este equipo.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </ng-container>

      <p class="ins-empty" *ngIf="!ranking() && !loading()">Selecciona un equipo para ver su ranking.</p>
      <p class="ins-empty" *ngIf="loading()">Calculando ranking…</p>
    </section>
  `,
  styles: [
    `
      :host { display: block; }
      .ins { padding-block: 1.5rem 3rem; display: flex; flex-direction: column; gap: 1.1rem; }
      .ins-title { font-size: clamp(1.5rem, 3vw, 2.1rem); }
      .grad { background: linear-gradient(120deg, #a855f7, #2563eb); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .ins-sub { color: var(--muted); max-width: 80ch; line-height: 1.6; }
      .ins-bar { display: flex; align-items: flex-end; gap: 0.6rem; flex-wrap: wrap; }
      .ins-bar .spacer { flex: 1; }
      .field { display: flex; flex-direction: column; gap: 0.35rem; min-width: 220px; }
      .field-label { font-size: 0.8rem; color: var(--muted); }
      select.input-pill { appearance: none; cursor: pointer; }
      .ins-note { color: #bbf7d0; font-size: 0.9rem; }
      .ins-error { color: #fca5a5; font-size: 0.9rem; }
      .ins-narr { display: flex; gap: 0.8rem; align-items: flex-start; padding: 1.1rem 1.3rem; border-radius: 1.1rem; }
      .ins-narr p { color: #e8edf7; line-height: 1.6; }
      .badge { flex: 0 0 auto; font-size: 0.72rem; padding: 0.25rem 0.55rem; border-radius: 999px; background: linear-gradient(120deg, #7c3aed, #2563eb); color: #fff; }
      .ins-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
      @media (max-width: 800px) { .ins-cards { grid-template-columns: 1fr; } }
      .hl { padding: 1.1rem 1.2rem; border-radius: 1.1rem; display: flex; flex-direction: column; gap: 0.25rem; }
      .hl strong { font-size: 1.15rem; }
      .hl span { color: var(--muted); font-size: 0.85rem; }
      .mini-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em; color: #c4b5fd; }
      .ins-table { padding: 1.2rem; border-radius: 1.1rem; overflow-x: auto; }
      table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-size: 0.88rem; }
      th, td { text-align: left; padding: 0.55rem 0.7rem; border-bottom: 1px solid var(--line); }
      th { color: var(--muted); font-weight: 600; font-size: 0.78rem; }
      td.empty, .empty { color: var(--muted); text-align: center; }
      .ins-empty { color: var(--muted); }
    `,
  ],
})
export class ManagerInsightsPageComponent {
  private readonly api = inject(ApiService);

  protected readonly teams = signal<TeamSummary[]>([]);
  protected selectedTeamId = '';
  protected readonly ranking = signal<TeamRanking | null>(null);
  protected readonly loading = signal(false);
  protected readonly nudging = signal(false);
  protected readonly nudgeResult = signal<string | null>(null);
  protected readonly error = signal<string | null>(null);

  constructor() {
    void this.init();
  }

  private async init(): Promise<void> {
    try {
      const teams = await this.api.listTeams();
      this.teams.set(teams);
      if (teams.length) {
        this.selectedTeamId = teams[0].id;
        await this.load();
      }
    } catch {
      this.error.set('No pude cargar tus equipos.');
    }
  }

  protected async load(): Promise<void> {
    if (!this.selectedTeamId) return;
    this.loading.set(true);
    this.error.set(null);
    this.nudgeResult.set(null);
    try {
      this.ranking.set(await this.api.getTeamRanking(this.selectedTeamId));
    } catch (e) {
      this.error.set(e instanceof Error ? e.message : 'No se pudo cargar el ranking.');
    } finally {
      this.loading.set(false);
    }
  }

  protected async doNudgeAtRisk(): Promise<void> {
    if (!this.selectedTeamId) return;
    this.nudging.set(true);
    this.nudgeResult.set(null);
    this.error.set(null);
    try {
      const res = await this.api.nudgeAtRisk(this.selectedTeamId);
      this.nudgeResult.set(
        res.count
          ? `Se notificó a ${res.count} miembro(s) en riesgo para que retomen su aprendizaje.`
          : 'No hay miembros en riesgo ahora mismo. ¡Buen trabajo!',
      );
    } catch (e) {
      this.error.set(e instanceof Error ? e.message : 'No se pudieron enviar las notificaciones.');
    } finally {
      this.nudging.set(false);
    }
  }
}
