import { CommonModule } from '@angular/common';
import { Component, computed, inject, OnDestroy, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AuthStore } from '../../core/auth/auth.store';
import {
  ApiService,
  CourseCatalogSummary,
  PresentationResponse,
  PresentationSlide,
} from '../../core/services/api.service';
import { Aula3dComponent } from './aula3d.component';

/**
 * Sala de Auxiliaturas (Sala 1) — metaverso conversacional.
 * El aula 3D está siempre visible. El alumno pulsa el micrófono y le habla al
 * profesor IA ("hola, necesito ayuda"); el profesor saluda, abre una ventana
 * para elegir curso + tema y, al confirmar, genera la presentación y la **narra
 * y avanza solo** (voz neuronal de Azure si está, si no la del navegador).
 */
@Component({
  selector: 'app-auxiliaturas-page',
  standalone: true,
  imports: [CommonModule, FormsModule, Aula3dComponent],
  templateUrl: './auxiliaturas-page.component.html',
  styleUrl: './auxiliaturas-page.component.css',
})
export class AuxiliaturasPageComponent implements OnDestroy {
  private readonly api = inject(ApiService);
  private readonly authStore = inject(AuthStore);

  protected readonly entered = signal(false); // overlay de bienvenida
  protected readonly userName = computed(() => {
    const p = this.authStore.profile() as { full_name?: string } | null;
    return (p?.full_name || '').trim().split(' ')[0] || 'estudiante';
  });

  protected readonly courses = signal<CourseCatalogSummary[]>([]);
  protected courseCode = '';
  protected topic = '';
  protected question = ''; // duda durante la clase
  protected articleText = ''; // texto/artículo que sube el alumno

  protected readonly askingOpen = signal(false); // panel de "tengo una duda"
  protected readonly answering = signal(false); // la IA está respondiendo la duda
  private micPausedForSpeech = false; // pausa el mic mientras la IA habla (evita eco)

  protected readonly generating = signal(false);
  protected readonly presentation = signal<PresentationResponse | null>(null);
  protected readonly slideIndex = signal(0);

  // Estado conversacional.
  protected readonly helpOpen = signal(false); // ventana emergente curso+tema
  protected readonly micActive = signal(false); // micrófono "hablar con el profesor"
  protected readonly agentLine = signal(''); // lo que el profesor está diciendo (caption)

  // Voz.
  protected readonly playing = signal(false); // narración de la clase en curso
  protected readonly speaking = signal(false); // hay audio sonando (mueve la boca del robot)
  protected readonly listening = signal(false); // dictado del tema en el modal
  protected readonly azureVoice = signal(false);
  private audio?: HTMLAudioElement;
  private currentStop?: () => void;
  private recognizer?: any;

  protected readonly voiceSupported =
    typeof window !== 'undefined' && 'speechSynthesis' in window;
  protected readonly sttSupported =
    typeof window !== 'undefined' &&
    ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window);

  protected readonly activeSlide = computed<PresentationSlide | null>(() => {
    const deck = this.presentation();
    if (!deck || !deck.slides.length) return null;
    return deck.slides[this.slideIndex()] ?? null;
  });
  protected readonly deckTitle = computed(() => this.presentation()?.title ?? '');
  protected readonly courseTitle = computed(() => {
    const code = this.courseCode;
    return this.courses().find((c) => c.certification_code === code)?.title ?? code;
  });

  constructor() {
    void this.loadCourses();
    this.api
      .speechStatus()
      .then((s) => this.azureVoice.set(s.enabled))
      .catch(() => this.azureVoice.set(false));
  }

  private async loadCourses(): Promise<void> {
    try {
      this.courses.set(await this.api.listCourses());
    } catch {
      /* el catálogo es opcional; igual se puede usar el demo */
    }
  }

  // --- Micrófono: hablar con el profesor (STT continuo del navegador) ---
  protected toggleMic(): void {
    if (this.micActive()) {
      this.stopMic();
      return;
    }
    if (!this.sttSupported) {
      this.openHelp();
      return;
    }
    const Recognition =
      (window as unknown as Record<string, unknown>)['webkitSpeechRecognition'] ||
      (window as unknown as Record<string, unknown>)['SpeechRecognition'];
    const rec = new (Recognition as new () => any)();
    rec.lang = 'es-ES';
    rec.continuous = true;
    rec.interimResults = false;
    rec.onresult = (event: any) => {
      const t = event.results[event.results.length - 1][0].transcript.trim();
      if (t) this.onSpeech(t);
    };
    rec.onend = () => {
      // No reanudar si lo pausamos a propósito mientras la IA habla.
      if (this.micActive() && !this.micPausedForSpeech) {
        try {
          rec.start();
        } catch {
          /* ya estaba activo */
        }
      }
    };
    rec.onerror = () => {};
    this.recognizer = rec;
    this.micActive.set(true);
    try {
      rec.start();
    } catch {
      /* noop */
    }
  }

  private stopMic(): void {
    this.micActive.set(false);
    try {
      this.recognizer?.stop();
    } catch {
      /* noop */
    }
    this.recognizer = undefined;
  }

  /** El alumno habló: abre el selector, o interrumpe la clase con una duda. */
  private onSpeech(text: string): void {
    if (this.generating() || this.helpOpen() || this.askingOpen() || this.answering()) return;
    if (!this.presentation()) {
      this.openHelp();
      return;
    }
    if (this.playing()) {
      // Interrupción por voz: tratamos lo dicho como una duda.
      this.question = text;
      this.pauseForQuestion();
      void this.submitQuestion();
    }
  }

  // --- Interrupción: preguntar una duda sin regenerar la presentación ---
  protected pauseForQuestion(): void {
    if (!this.presentation()) return;
    this.stopNarration(); // pausa la narración (mantiene el slide actual)
    this.question = this.question || '';
    this.askingOpen.set(true);
  }

  protected async submitQuestion(): Promise<void> {
    const q = this.question.trim();
    if (!q || this.answering()) return;
    const deck = this.presentation();
    this.answering.set(true);
    this.agentLine.set('Déjame pensar tu duda…');
    try {
      const res = await this.api.askPresentation(
        q,
        this.courseCode.trim() || undefined,
        deck?.topic,
      );
      this.agentLine.set(res.answer);
      await this.speakText(res.answer);
    } catch {
      this.agentLine.set('No pude responder esa duda ahora mismo.');
    } finally {
      this.answering.set(false);
      this.askingOpen.set(false);
      this.question = '';
      this.resumeClass();
    }
  }

  protected cancelQuestion(): void {
    this.askingOpen.set(false);
    this.question = '';
    this.resumeClass();
  }

  /** Retoma la clase desde el slide actual. */
  private resumeClass(): void {
    if (!this.presentation()) return;
    this.playing.set(true);
    void this.narrateFrom(this.slideIndex());
  }

  protected dictateQuestion(): void {
    const Recognition =
      (window as unknown as Record<string, unknown>)['webkitSpeechRecognition'] ||
      (window as unknown as Record<string, unknown>)['SpeechRecognition'];
    if (!Recognition) return;
    const rec = new (Recognition as new () => any)();
    rec.lang = 'es-ES';
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    this.listening.set(true);
    rec.onresult = (event: any) => {
      this.question = event.results[0][0].transcript;
    };
    rec.onend = () => this.listening.set(false);
    rec.onerror = () => this.listening.set(false);
    rec.start();
  }

  /** Lee un archivo de texto (.txt/.md) y lo pone en el campo de artículo. */
  protected onArticleFile(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      this.articleText = String(reader.result || '').slice(0, 20000);
    };
    reader.readAsText(file);
  }

  /** Entrada al metaverso: la IA da la bienvenida (la voz necesita este gesto). */
  protected enterMetaverse(): void {
    if (this.entered()) return;
    this.entered.set(true);
    const name = this.userName();
    this.say(
      `¡Bienvenido ${name}! Este es el metaverso de RetIAm. Aquí puedes resolver tus dudas de ` +
        'cualquier tema, realizar tus laboratorios en tiempo real y debatir con tus amigos sobre ' +
        'algún tema. Todo este entorno está supervisado por mí, tu agente de inteligencia ' +
        'artificial del metaverso. Cuando quieras, pulsa el micrófono y dime en qué te ayudo.',
    );
  }

  protected openHelp(): void {
    this.topic = '';
    this.helpOpen.set(true);
    this.say('¡Hola! Claro que sí. Dime qué quieres aprender y lo busco en todos los cursos.');
  }

  protected closeHelp(): void {
    this.helpOpen.set(false);
  }

  // --- Generar y presentar la clase ---
  protected async present(): Promise<void> {
    const code = this.courseCode.trim(); // vacío = todos los cursos
    const topic = this.topic.trim();
    const article = this.articleText.trim();
    if (!topic && !article) return;
    this.stopNarration();
    this.generating.set(true);
    this.helpOpen.set(false);
    this.agentLine.set(
      article ? 'Leyendo tu material…' : `Preparando tu clase sobre "${topic}"…`,
    );
    try {
      let deck: PresentationResponse;
      try {
        deck = article
          ? await this.api.createPresentationFromText(article, topic || undefined)
          : await this.api.createPresentation(code, topic);
      } catch {
        deck = this.demoDeck(topic || 'Tu material'); // sin backend → clase demo
      }
      this.presentation.set(deck);
      this.slideIndex.set(0);
      this.articleText = '';
      this.startPresentation();
    } finally {
      this.generating.set(false);
    }
  }

  /** Carga una clase de ejemplo (sin backend) y la presenta. */
  protected loadDemo(): void {
    this.stopNarration();
    this.helpOpen.set(false);
    this.presentation.set(this.demoDeck(this.topic.trim() || 'Redes virtuales en Azure'));
    this.slideIndex.set(0);
    this.startPresentation();
  }

  /** Empieza a narrar la clase desde el primer slide (auto-avance). */
  private startPresentation(): void {
    this.playing.set(true);
    void this.narrateFrom(0);
  }

  protected reset(): void {
    this.stopNarration();
    this.presentation.set(null);
    this.slideIndex.set(0);
    this.agentLine.set('');
  }

  // --- Narración: el profesor habla y avanza los slides solo ---
  private async narrateFrom(index: number): Promise<void> {
    const deck = this.presentation();
    if (!deck || index >= deck.slides.length) {
      this.playing.set(false);
      this.say('Eso es todo por ahora. ¿Quieres que profundice en algún punto?');
      return;
    }
    this.slideIndex.set(index);
    const slide = deck.slides[index];
    this.agentLine.set(slide.narration || slide.title);
    await this.speakText(slide.narration || slide.title);
    if (this.playing()) void this.narrateFrom(index + 1);
  }

  protected stopNarration(): void {
    this.playing.set(false);
    if (this.voiceSupported) window.speechSynthesis.cancel();
    if (this.audio) {
      this.audio.pause();
      this.audio = undefined;
    }
    const stop = this.currentStop;
    this.currentStop = undefined;
    stop?.();
  }

  /** El profesor "dice" algo: caption + voz. */
  private say(text: string): void {
    this.agentLine.set(text);
    void this.speakText(text);
  }

  /** Narra un texto; resuelve al terminar o al detener. Mueve la boca del robot. */
  private async speakText(text: string): Promise<void> {
    this.pauseMicForSpeech(); // evita que el mic capte la voz de la IA (eco)
    this.speaking.set(true);
    try {
      await (this.azureVoice() ? this.speakAzure(text) : this.speakBrowser(text));
    } finally {
      this.speaking.set(false);
      this.resumeMicAfterSpeech();
    }
  }

  private pauseMicForSpeech(): void {
    if (this.micActive() && this.recognizer && !this.micPausedForSpeech) {
      this.micPausedForSpeech = true;
      try {
        this.recognizer.stop();
      } catch {
        /* noop */
      }
    }
  }

  private resumeMicAfterSpeech(): void {
    if (this.micActive() && this.recognizer && this.micPausedForSpeech) {
      this.micPausedForSpeech = false;
      try {
        this.recognizer.start();
      } catch {
        /* noop */
      }
    }
  }

  private speakAzure(text: string): Promise<void> {
    return new Promise<void>((resolve) => {
      this.currentStop = resolve;
      this.api
        .synthesizeSpeech(text)
        .then((blob) => {
          if (this.currentStop !== resolve) {
            resolve();
            return;
          }
          const url = URL.createObjectURL(blob);
          const audio = new Audio(url);
          this.audio = audio;
          const done = () => {
            URL.revokeObjectURL(url);
            if (this.currentStop === resolve) this.currentStop = undefined;
            resolve();
          };
          audio.onended = done;
          audio.onerror = done;
          void audio.play().catch(done);
        })
        .catch(() => {
          this.currentStop = undefined;
          void this.speakBrowser(text).then(resolve);
        });
    });
  }

  private speakBrowser(text: string): Promise<void> {
    return new Promise<void>((resolve) => {
      if (!this.voiceSupported) {
        resolve();
        return;
      }
      this.currentStop = resolve;
      const utter = this.utteranceFor(text);
      utter.onend = () => {
        if (this.currentStop === resolve) this.currentStop = undefined;
        resolve();
      };
      utter.onerror = () => resolve();
      window.speechSynthesis.speak(utter);
    });
  }

  private utteranceFor(text: string): SpeechSynthesisUtterance {
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'es-ES';
    utter.rate = 1;
    const voice = window.speechSynthesis
      .getVoices()
      .find((v) => (v.lang || '').toLowerCase().startsWith('es'));
    if (voice) utter.voice = voice;
    return utter;
  }

  // --- Dictado del tema dentro del modal (STT puntual) ---
  protected dictateTopic(): void {
    const Recognition =
      (window as unknown as Record<string, unknown>)['webkitSpeechRecognition'] ||
      (window as unknown as Record<string, unknown>)['SpeechRecognition'];
    if (!Recognition) return;
    const rec = new (Recognition as new () => any)();
    rec.lang = 'es-ES';
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    this.listening.set(true);
    rec.onresult = (event: any) => {
      this.topic = event.results[0][0].transcript;
    };
    rec.onend = () => this.listening.set(false);
    rec.onerror = () => this.listening.set(false);
    rec.start();
  }

  private demoDeck(topic: string): PresentationResponse {
    return {
      course_code: this.courseCode.trim() || 'DEMO',
      topic,
      title: `Clase de ejemplo: ${topic}`,
      grounded: false,
      source_mode: 'demo',
      message: 'Modo demo (sin backend) — contenido de ejemplo para probar el aula 3D.',
      sources: [],
      slides: [
        {
          title: '¿Qué es una red virtual (VNet)?',
          bullets: [
            'Es tu red privada y aislada dentro de Azure.',
            'Define rangos de IP, subredes y reglas de tráfico.',
            'Permite que tus recursos se comuniquen de forma segura.',
          ],
          code: null,
          diagram: [],
          narration:
            'Bienvenido al aula. Hoy veremos qué es una red virtual en Azure y por qué es la base de tu infraestructura.',
        },
        {
          title: 'Cómo se crea, paso a paso',
          bullets: ['El flujo típico para montar tu red:'],
          code: null,
          diagram: [
            'Crear la VNet',
            'Definir el espacio de IPs',
            'Agregar subredes',
            'Asociar recursos',
          ],
          narration:
            'Montar una red sigue siempre el mismo flujo: creas la red, defines su espacio de direcciones, agregas subredes y asocias tus recursos.',
        },
        {
          title: 'Crear una VNet con la CLI',
          bullets: ['Un solo comando crea la red y su primera subred.'],
          code:
            'az network vnet create \\\n' +
            '  --name miVNet \\\n' +
            '  --resource-group miGrupo \\\n' +
            '  --address-prefix 10.0.0.0/16 \\\n' +
            '  --subnet-name app --subnet-prefix 10.0.1.0/24',
          diagram: [],
          narration:
            'Con la CLI de Azure podemos crear la red virtual y su primera subred en un único comando.',
        },
      ],
    };
  }

  ngOnDestroy(): void {
    this.stopNarration();
    this.stopMic();
  }
}
