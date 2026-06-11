import { CommonModule } from '@angular/common';
import { Component, computed, inject, input } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

interface LessonUnit {
  id: string;
  title: string;
  html: SafeHtml;
  body: string;
}

interface LessonMicroSection {
  id: string;
  title: string;
  html: SafeHtml;
  coachNote: string;
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
  readonly unitIndex = input(0);
  readonly technique = input<string | null>(null);

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
        body,
        html: this.render(body),
      });
    });

    return { units, source };
  });

  protected readonly activeUnit = computed(() => {
    const units = this.parsed().units;
    if (!units.length) return null;
    const requested = this.unitIndex();
    const index = Math.min(Math.max(requested, 0), units.length - 1);
    return {
      unit: units[index],
      index,
      total: units.length,
    };
  });

  protected readonly microLearningMode = computed(() => {
    const technique = (this.technique() ?? '').toLowerCase();
    return technique === 'aprendizaje continuo' || technique === 'regla de 5 minutos';
  });

  protected readonly activeMicroSections = computed(() => {
    const active = this.activeUnit();
    if (!active || !this.microLearningMode()) return [];

    const technique = (this.technique() ?? '').toLowerCase();
    const wordLimit = technique === 'regla de 5 minutos' ? 85 : 120;
    return this.buildMicroSections(active.unit, wordLimit);
  });

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

  private buildMicroSections(unit: LessonUnit, wordLimit: number): LessonMicroSection[] {
    const blocks = unit.body
      .split(/\n{2,}/g)
      .map((block) => block.trim())
      .filter(Boolean);

    if (!blocks.length) {
      return [
        {
          id: `${unit.id}-micro-0`,
          title: unit.title,
          html: unit.html,
          coachNote: 'Reti te sugiere cerrar este bloque diciendo en una frase cual fue la idea principal.',
        },
      ];
    }

    const sections: Array<{ title: string; markdown: string }> = [];
    let currentTitle = unit.title;
    let currentBlocks: string[] = [];
    let currentWords = 0;

    const flush = () => {
      if (!currentBlocks.length) return;
      sections.push({
        title: currentTitle,
        markdown: currentBlocks.join('\n\n'),
      });
      currentBlocks = [];
      currentWords = 0;
    };

    blocks.forEach((block) => {
      const heading = block.match(/^#{1,6}\s+(.+?)\s*$/);
      if (heading) {
        flush();
        currentTitle = heading[1].trim();
        return;
      }

      const blockWords = this.countWords(block);
      if (currentBlocks.length && currentWords + blockWords > wordLimit) {
        flush();
      }

      currentBlocks.push(block);
      currentWords += blockWords;
    });

    flush();

    return sections.map((section, index) => ({
      id: `${unit.id}-micro-${index}`,
      title: sections.length > 1 ? `${section.title} · Bloque ${index + 1}` : section.title,
      html: this.render(section.markdown),
      coachNote: this.buildCoachNote(section.markdown),
    }));
  }

  private buildCoachNote(markdown: string): string {
    const plain = markdown
      .replace(/```[\s\S]*?```/g, ' ')
      .replace(/`[^`]+`/g, ' ')
      .replace(/!\[[^\]]*\]\([^)]+\)/g, ' ')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/^#{1,6}\s+/gm, '')
      .replace(/[*_>~-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    const firstSentence = plain.match(/[^.!?]+[.!?]?/)?.[0]?.trim() ?? plain;
    const compact = firstSentence.length > 120 ? `${firstSentence.slice(0, 117).trim()}...` : firstSentence;
    return compact
      ? `Reti añade: aquí conviene quedarte con esta idea clave: ${compact}`
      : 'Reti añade: termina este bloque diciendo con tus palabras qué fue lo más importante.';
  }

  private countWords(text: string): number {
    return text.split(/\s+/).filter(Boolean).length;
  }
}
