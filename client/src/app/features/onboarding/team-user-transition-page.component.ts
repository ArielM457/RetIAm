import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, ElementRef, OnDestroy, inject } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-team-user-transition-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './team-user-transition-page.component.html',
  styleUrl: './team-user-transition-page.component.css',
})
export class TeamUserTransitionPageComponent implements AfterViewInit, OnDestroy {
  private readonly host = inject(ElementRef<HTMLElement>);
  private readonly router = inject(Router);
  private animationFrame = 0;
  private navigationTimeout = 0;
  private resizeHandler = () => this.resizeCanvas();
  private startTime: number | null = null;
  private globalT = 0;
  private titleShown = false;
  private titleHidden = false;

  ngAfterViewInit(): void {
    this.resizeCanvas();
    window.addEventListener('resize', this.resizeHandler);
    this.loop();
    this.navigationTimeout = window.setTimeout(() => {
      void this.router.navigate(['/onboarding']);
    }, 5200);
  }

  ngOnDestroy(): void {
    cancelAnimationFrame(this.animationFrame);
    window.clearTimeout(this.navigationTimeout);
    window.removeEventListener('resize', this.resizeHandler);
  }

  private resizeCanvas(): void {
    const canvas = this.host.nativeElement.querySelector('#wave-canvas') as HTMLCanvasElement | null;
    if (!canvas) {
      return;
    }
    const ratio = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * ratio;
    canvas.height = window.innerHeight * ratio;
    canvas.style.width = `${window.innerWidth}px`;
    canvas.style.height = `${window.innerHeight}px`;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }
  }

  private loop(): void {
    const canvas = this.host.nativeElement.querySelector('#wave-canvas') as HTMLCanvasElement | null;
    const title = this.host.nativeElement.querySelector('#title') as HTMLDivElement | null;
    if (!canvas || !title) {
      return;
    }
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      return;
    }

    const timings = {
      blank: 1000,
      enter: 1500,
      hold: 600,
      clip: 1100,
    };
    const phases = ['blank', 'enter', 'hold', 'clip', 'active'] as const;
    const phaseStart: Record<string, number> = {};
    let acc = 0;
    phases.forEach((phase) => {
      phaseStart[phase] = acc;
      acc += timings[phase as keyof typeof timings] ?? 0;
    });

    const easeInOut = (t: number) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t);
    const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);

    const getPhase = (elapsed: number) => {
      for (let index = phases.length - 1; index >= 0; index -= 1) {
        const phase = phases[index];
        if (elapsed >= phaseStart[phase]) {
          const duration = timings[phase as keyof typeof timings] ?? 1;
          return {
            name: phase,
            t: phase === 'active' ? 1 : Math.min(1, (elapsed - phaseStart[phase]) / duration),
          };
        }
      }
      return { name: 'blank' as const, t: 0 };
    };

    const drawWave = (
      time: number,
      offsetNorm: number,
      leftClip: number,
      rightClip: number,
      intensity: number,
    ) => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      const cy = height / 2;
      const totalLen = width * 1.6;
      const waveCenter = width / 2;
      const startX = waveCenter - totalLen / 2 + offsetNorm * width;
      const clipLeft = leftClip * width;
      const clipRight = rightClip * width;

      ctx.save();
      ctx.beginPath();
      ctx.rect(clipLeft, 0, clipRight - clipLeft, height);
      ctx.clip();

      const layers = [
        { amp: 42, freq: 2.6, speed: 1.0, alpha: 0.92, lw: 2.4, blur: 18 },
        { amp: 26, freq: 5.0, speed: 1.65, alpha: 0.5, lw: 1.3, blur: 9 },
        { amp: 16, freq: 8.8, speed: 2.5, alpha: 0.25, lw: 0.9, blur: 5 },
      ];

      layers.forEach(({ amp, freq, speed, alpha, lw, blur }) => {
        const points = 300;
        ctx.beginPath();
        for (let i = 0; i <= points; i += 1) {
          const frac = i / points;
          const x = startX + frac * totalLen;
          const localFrac = (x - clipLeft) / (clipRight - clipLeft);
          const edgeFade = Math.pow(Math.sin(Math.PI * Math.max(0, Math.min(1, localFrac))), 0.5);
          const center = (x - waveCenter) / (totalLen * 0.38);
          const gauss = Math.exp(-center * center * 0.8);
          const y =
            cy +
            Math.sin(frac * Math.PI * 2 * freq + time * speed) * amp * intensity * gauss * edgeFade;
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        const gradient = ctx.createLinearGradient(clipLeft, 0, clipRight, 0);
        gradient.addColorStop(0, 'rgba(168,85,247,0)');
        gradient.addColorStop(0.12, `rgba(168,85,247,${alpha})`);
        gradient.addColorStop(0.5, `rgba(191,90,242,${alpha})`);
        gradient.addColorStop(0.88, `rgba(168,85,247,${alpha})`);
        gradient.addColorStop(1, 'rgba(168,85,247,0)');
        ctx.strokeStyle = gradient;
        ctx.lineWidth = lw;
        ctx.shadowColor = '#A855F7';
        ctx.shadowBlur = blur;
        ctx.stroke();
        ctx.shadowBlur = 0;
      });

      ctx.restore();
    };

    const render = (ts?: number) => {
      if (!canvas || !ctx) {
        return;
      }
      if (!this.startTime) {
        this.startTime = ts ?? performance.now();
      }
      const elapsed = (ts ?? performance.now()) - this.startTime;
      this.globalT += 0.044;
      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      const phase = getPhase(elapsed);

      if (phase.name === 'enter') {
        const progress = easeOut(phase.t);
        drawWave(this.globalT, 1 - progress, 0, 1, easeOut(Math.min(1, phase.t * 1.8)));
        if (phase.t > 0.55 && !this.titleShown) {
          this.titleShown = true;
          title.classList.add('show');
        }
      } else if (phase.name === 'hold') {
        drawWave(this.globalT, 0, 0, 1, 1);
        if (!this.titleShown) {
          this.titleShown = true;
          title.classList.add('show');
        }
      } else if (phase.name === 'clip') {
        const progress = easeInOut(phase.t);
        const targetLeft = 0.35;
        const targetRight = 0.65;
        drawWave(this.globalT, 0, progress * targetLeft, 1 - progress * (1 - targetRight), 1);
        if (phase.t > 0.1 && !this.titleHidden) {
          this.titleHidden = true;
          title.classList.add('hide');
        }
      } else if (phase.name === 'active') {
        drawWave(this.globalT, 0, 0.35, 0.65, 1);
      }

      this.animationFrame = requestAnimationFrame(render);
    };

    this.animationFrame = requestAnimationFrame(render);
  }
}
