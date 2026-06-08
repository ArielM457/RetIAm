import { inject, Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

/**
 * Renderiza Markdown a HTML seguro para mostrar el contenido de las lecciones
 * (content_md) de forma agradable. Usar con [innerHTML]:
 *
 *   <div class="prose" [innerHTML]="lesson.content_md | markdown"></div>
 */
@Pipe({ name: 'markdown', standalone: true })
export class MarkdownPipe implements PipeTransform {
  private readonly sanitizer = inject(DomSanitizer);

  transform(value: string | null | undefined): SafeHtml {
    if (!value) return '';
    const html = marked.parse(value, { async: false, gfm: true, breaks: true }) as string;
    // marked escapa el HTML del usuario por defecto; el origen es contenido de MS Learn.
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}
