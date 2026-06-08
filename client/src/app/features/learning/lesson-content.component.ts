import { CommonModule } from '@angular/common';
import { Component, computed, inject, input, signal } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

interface LessonUnit {
  id: string;
  title: string;
  html: SafeHtml;
}

const CALLOUT_KINDS = 'Note|Important|Tip|Caution|Warning';

/**
 * Renderiza el contenido de una leccion (Markdown de MS Learn) de forma agradable
 * e interactiva: cada unidad (separada por '---') es una tarjeta colapsable, con
 * indice de subtemas, cajas de Nota/Tip/Importante y tipografia cuidada.
 *
 * Usa ::ng-deep en el CSS porque el HTML entra por [innerHTML] (Angular no le
 * aplica los estilos encapsulados de otra forma).
 */
@Component({
  selector: 'app-lesson-content',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './lesson-content.component.html',
  styleUrl: './lesson-content.component.css',
})
export class LessonContentComponent {
  private readonly sanitizer = inject(DomSanitizer);

  readonly content = input<string | null>(null);

  /** Estado de apertura por unidad (id -> abierto). */
  private readonly openState = signal<Record<string, boolean>>({});

  protected readonly parsed = computed(() => {
    const raw = (this.content() ?? '').trim();
    if (!raw) return { units: [] as LessonUnit[], source: null as string | null };

    const chunks = raw
      .split(/\n+---\n+/g)
      .map((c) => c.trim())
      .filter(Boolean);

    let source: string | null = null;
    const units: LessonUnit[] = [];
    chunks.forEach((chunk, index) => {
      // El pie con la fuente oficial lo mostramos aparte.
      const sourceMatch = chunk.match(/_?Fuente oficial:\s*(\S+)/i);
      if (sourceMatch && chunk.replace(/[_*]/g, '').trim().toLowerCase().startsWith('fuente oficial')) {
        source = sourceMatch[1];
        return;
      }
      const headingMatch = chunk.match(/^#{1,6}\s+(.+?)\s*$/m);
      const title = headingMatch ? headingMatch[1].trim() : `Sección ${index + 1}`;
      // Quitamos el primer encabezado del cuerpo (ya va en el título de la tarjeta).
      const body = headingMatch ? chunk.replace(headingMatch[0], '').trim() : chunk;
      units.push({
        id: `unit-${index}`,
        title,
        html: this.render(body),
      });
    });

    return { units, source };
  });

  protected readonly toc = computed(() => this.parsed().units.map((u) => ({ id: u.id, title: u.title })));

  private render(markdown: string): SafeHtml {
    let html = marked.parse(markdown, { async: false, gfm: true, breaks: false }) as string;
    // Convierte "Note/Important/Tip/..." + parrafo siguiente en una caja con estilo.
    html = html.replace(
      new RegExp(`<p>(${CALLOUT_KINDS})</p>\\s*<p>([\\s\\S]*?)</p>`, 'gi'),
      (_m, kind: string, body: string) => {
        const k = kind.toLowerCase();
        return `<div class="callout callout-${k}"><span class="callout-h">${this.icon(k)} ${kind}</span><p>${body}</p></div>`;
      },
    );
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  private icon(kind: string): string {
    return { note: 'ℹ️', important: '❗', tip: '💡', caution: '⚠️', warning: '⚠️' }[kind] ?? 'ℹ️';
  }

  protected isOpen(id: string, index: number): boolean {
    const state = this.openState();
    return id in state ? state[id] : index === 0; // primera unidad abierta por defecto
  }

  protected toggle(id: string, index: number): void {
    const current = this.isOpen(id, index);
    this.openState.update((s) => ({ ...s, [id]: !current }));
  }

  protected openAndScroll(id: string): void {
    this.openState.update((s) => ({ ...s, [id]: true }));
    setTimeout(() => {
      document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 60);
  }
}
