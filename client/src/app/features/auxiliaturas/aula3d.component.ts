import {
  AfterViewInit,
  Component,
  effect,
  ElementRef,
  input,
  OnDestroy,
  viewChild,
} from '@angular/core';
import {
  AnimationGroup,
  ArcRotateCamera,
  Color3,
  Color4,
  DirectionalLight,
  DynamicTexture,
  Engine,
  GlowLayer,
  HemisphericLight,
  Mesh,
  MeshBuilder,
  PBRMaterial,
  PointLight,
  Scene,
  SceneLoader,
  StandardMaterial,
  TransformNode,
  Vector3,
} from '@babylonjs/core';
import '@babylonjs/loaders/glTF';

import { PresentationSlide } from '../../core/services/api.service';

/**
 * Aula 3D (Capa B) — sala estilo "metaverso" con un robot presentador y una
 * pantalla que muestra el slide actual. El robot "habla" (su boca pulsa) cuando
 * la narración está activa. La voz la maneja el componente padre (Auxiliaturas).
 */
@Component({
  selector: 'app-aula3d',
  standalone: true,
  template: `<canvas #canvas class="aula-canvas"></canvas>`,
  styles: [
    `:host { display: block; }
     .aula-canvas { width: 100%; height: 82vh; min-height: 520px; border-radius: 1.1rem; outline: none; display: block; touch-action: none; }`,
  ],
})
export class Aula3dComponent implements AfterViewInit, OnDestroy {
  readonly slide = input<PresentationSlide | null>(null);
  readonly title = input<string>('');
  readonly playing = input<boolean>(false);

  private readonly canvasRef = viewChild.required<ElementRef<HTMLCanvasElement>>('canvas');

  private engine?: Engine;
  private scene?: Scene;
  private camera?: ArcRotateCamera;
  private glow?: GlowLayer;
  private screenTexture?: DynamicTexture;
  private faceTex?: DynamicTexture;
  private presenter?: TransformNode; // profesor estático
  private presenterBaseY = 0;
  private avatar?: TransformNode; // alumno controlable
  private walkAnim?: AnimationGroup;
  private readonly pressed = new Set<string>();
  // Obstáculos (rectángulos XZ) para que el avatar no atraviese mesas/pilares/profesor.
  private readonly obstacles: { x: number; z: number; hw: number; hd: number }[] = [];
  private moving = false;
  private mouthOpen = false;
  private clock = 0;

  constructor() {
    // Cuando cambian el slide o el estado de narración, actualiza la escena.
    effect(() => {
      const slide = this.slide();
      const title = this.title();
      this.playing(); // se lee para reaccionar; el pulso se aplica en el render loop
      if (this.scene && this.screenTexture) this.drawSlide(slide, title);
    });
  }

  ngAfterViewInit(): void {
    const canvas = this.canvasRef().nativeElement;
    this.engine = new Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
    const scene = new Scene(this.engine);
    this.scene = scene;
    scene.clearColor = new Color4(0.04, 0.05, 0.09, 1);

    // Cámara en 3ª persona (sigue al avatar; el mouse orbita, la rueda acerca).
    const camera = new ArcRotateCamera('cam', -Math.PI / 2, Math.PI / 2.4, 7, new Vector3(0, 1.4, -2), scene);
    camera.attachControl(canvas, true);
    camera.lowerRadiusLimit = 3.5;
    camera.upperRadiusLimit = 14;
    camera.upperBetaLimit = Math.PI / 2.05;
    camera.wheelPrecision = 40;
    this.camera = camera;

    // Luces.
    const hemi = new HemisphericLight('hemi', new Vector3(0, 1, 0), scene);
    hemi.intensity = 0.75;
    const dir = new DirectionalLight('dir', new Vector3(-0.3, -1, 0.4), scene);
    dir.intensity = 0.6;

    this.buildEnvironment(scene);
    this.buildScreen(scene);
    void this.loadPresenter(scene);
    void this.loadAvatar(scene);
    this.drawSlide(this.slide(), this.title());

    // Bucle: profesor (boca/flotar/asentir) + avatar (movimiento WASD + cámara).
    scene.onBeforeRenderObservable.add(() => {
      const dt = this.engine!.getDeltaTime() / 1000;
      this.clock += dt;
      const open = this.playing() ? Math.sin(this.clock * 12) > 0 : false;
      if (open !== this.mouthOpen) {
        this.mouthOpen = open;
        this.drawFace(open);
      }
      if (this.presenter) {
        this.presenter.position.y = this.presenterBaseY + Math.sin(this.clock * 1.5) * 0.05;
        this.presenter.rotation.x = this.playing() ? Math.sin(this.clock * 6) * 0.05 : 0;
      }
      this.updateAvatar(dt);
    });

    this.engine.runRenderLoop(() => scene.render());
    window.addEventListener('resize', this.onResize);
    window.addEventListener('keydown', this.onKeyDown);
    window.addEventListener('keyup', this.onKeyUp);
  }

  private onResize = () => this.engine?.resize();

  private mat(scene: Scene, name: string, color: Color3, emissive?: Color3): StandardMaterial {
    const m = new StandardMaterial(name, scene);
    m.diffuseColor = color;
    if (emissive) m.emissiveColor = emissive;
    return m;
  }

  /** Material emisivo "neón" (con GlowLayer brilla como letrero). */
  private neon(scene: Scene, name: string, color: Color3): StandardMaterial {
    const m = new StandardMaterial(name, scene);
    m.diffuseColor = new Color3(0, 0, 0);
    m.emissiveColor = color;
    m.disableLighting = true;
    return m;
  }

  /** Textura de rejilla tech para el piso. */
  private gridTexture(scene: Scene, bg: Color3, line: Color3): DynamicTexture {
    const size = 1024;
    const tex = new DynamicTexture('grid', { width: size, height: size }, scene, true);
    const ctx = tex.getContext() as unknown as CanvasRenderingContext2D;
    ctx.fillStyle = bg.toHexString();
    ctx.fillRect(0, 0, size, size);
    ctx.strokeStyle = line.toHexString();
    ctx.lineWidth = 3;
    const step = size / 16;
    for (let i = 0; i <= 16; i++) {
      ctx.beginPath();
      ctx.moveTo(i * step, 0);
      ctx.lineTo(i * step, size);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, i * step);
      ctx.lineTo(size, i * step);
      ctx.stroke();
    }
    tex.update();
    tex.uScale = 6;
    tex.vScale = 6;
    return tex;
  }

  /** Auditorio futurista: piso pulido, paredes, techo, neón y paneles de luz. */
  private buildEnvironment(scene: Scene): void {
    const glow = new GlowLayer('glow', scene);
    glow.intensity = 0.9;
    this.glow = glow;

    scene.fogMode = Scene.FOGMODE_EXP2;
    scene.fogColor = new Color3(0.03, 0.04, 0.08);
    scene.fogDensity = 0.019;

    const H = 8;
    const FRONT = 7.4; // pared tras la pantalla

    // --- Piso PBR oscuro con rejilla ---
    const floor = MeshBuilder.CreateGround('floor', { width: 26, height: 26 }, scene);
    const floorMat = new PBRMaterial('floorMat', scene);
    floorMat.albedoColor = new Color3(0.05, 0.06, 0.1);
    floorMat.metallic = 0.6;
    floorMat.roughness = 0.4;
    floorMat.albedoTexture = this.gridTexture(scene, new Color3(0.03, 0.04, 0.07), new Color3(0.06, 0.24, 0.42));
    floor.material = floorMat;

    // --- Paredes + techo PBR ---
    const wallMat = new PBRMaterial('wallMat', scene);
    wallMat.albedoColor = new Color3(0.06, 0.07, 0.11);
    wallMat.metallic = 0.3;
    wallMat.roughness = 0.6;
    const mkWall = (w: number, h: number, d: number, x: number, y: number, z: number): void => {
      const b = MeshBuilder.CreateBox('wall', { width: w, height: h, depth: d }, scene);
      b.position.set(x, y, z);
      b.material = wallMat;
    };
    mkWall(26, H, 0.4, 0, H / 2, FRONT); // frontal (tras la pantalla)
    mkWall(26, H, 0.4, 0, H / 2, -12); // trasera
    mkWall(0.4, H, 24, -12, H / 2, -2.5); // izquierda
    mkWall(0.4, H, 24, 12, H / 2, -2.5); // derecha
    mkWall(26, 0.4, 26, 0, H, -2.5); // techo

    // --- Tiras neón (zócalo cyan, techo magenta) ---
    const cyan = this.neon(scene, 'neonCyan', new Color3(0.0, 0.7, 1.0));
    const mag = this.neon(scene, 'neonMag', new Color3(0.7, 0.2, 1.0));
    const strip = (w: number, h: number, d: number, x: number, y: number, z: number, m: StandardMaterial): void => {
      const s = MeshBuilder.CreateBox('strip', { width: w, height: h, depth: d }, scene);
      s.position.set(x, y, z);
      s.material = m;
    };
    strip(24, 0.12, 0.12, 0, 0.15, FRONT - 0.3, cyan);
    strip(24, 0.12, 0.12, 0, 0.15, -11.8, cyan);
    strip(0.12, 0.12, 23, -11.8, 0.15, -2.5, cyan);
    strip(0.12, 0.12, 23, 11.8, 0.15, -2.5, cyan);
    strip(24, 0.1, 0.1, 0, H - 0.3, FRONT - 0.4, mag);
    strip(24, 0.1, 0.1, 0, H - 0.3, -11.6, mag);

    // --- Paneles de luz en el techo ---
    const panelMat = this.neon(scene, 'panel', new Color3(0.45, 0.55, 0.85));
    for (const x of [-6, 0, 6]) {
      for (const z of [-8, -3, 2]) {
        const p = MeshBuilder.CreatePlane('lightPanel', { width: 2.4, height: 1.2 }, scene);
        p.rotation.x = Math.PI / 2;
        p.position.set(x, H - 0.25, z);
        p.material = panelMat;
      }
    }

    // --- Luces de acento (la hemisférica/direccional ya están en ngAfterViewInit) ---
    const p1 = new PointLight('p1', new Vector3(0, 6, 2), scene);
    p1.diffuse = new Color3(0.5, 0.7, 1);
    p1.intensity = 0.5;
    const p2 = new PointLight('p2', new Vector3(-4, 5, 5), scene);
    p2.diffuse = new Color3(0.8, 0.4, 1);
    p2.intensity = 0.35;

    this.buildProps(scene, cyan);
  }

  /** Pupitres mirando a la pantalla + pilares con luz. */
  private buildProps(scene: Scene, accent: StandardMaterial): void {
    const deskMat = new PBRMaterial('deskMat', scene);
    deskMat.albedoColor = new Color3(0.08, 0.1, 0.16);
    deskMat.metallic = 0.4;
    deskMat.roughness = 0.5;

    for (let row = 0; row < 3; row++) {
      for (const x of [-6, -2.5, 2.5, 6]) {
        const z = -7 + row * 3;
        const desk = MeshBuilder.CreateBox('desk', { width: 2, height: 0.15, depth: 0.9 }, scene);
        desk.position.set(x, 0.9, z);
        desk.material = deskMat;
        const legs = MeshBuilder.CreateBox('legs', { width: 1.8, height: 0.9, depth: 0.1 }, scene);
        legs.position.set(x, 0.45, z + 0.4);
        legs.material = deskMat;
        const s = MeshBuilder.CreateBox('deskStrip', { width: 1.9, height: 0.05, depth: 0.05 }, scene);
        s.position.set(x, 0.84, z - 0.45);
        s.material = accent;
        this.obstacles.push({ x, z, hw: 1, hd: 0.6 });
      }
    }

    const pillarMat = new PBRMaterial('pillarMat', scene);
    pillarMat.albedoColor = new Color3(0.07, 0.08, 0.12);
    pillarMat.metallic = 0.5;
    pillarMat.roughness = 0.4;
    for (const x of [-10.5, 10.5]) {
      for (const z of [-9, 3]) {
        const col = MeshBuilder.CreateBox('pillar', { width: 0.6, height: 8, depth: 0.6 }, scene);
        col.position.set(x, 4, z);
        col.material = pillarMat;
        const ls = MeshBuilder.CreateBox('pillarStrip', { width: 0.12, height: 6, depth: 0.12 }, scene);
        ls.position.set(x + (x < 0 ? 0.32 : -0.32), 4, z);
        ls.material = accent;
        this.obstacles.push({ x, z, hw: 0.4, hd: 0.4 });
      }
    }
  }

  private buildScreen(scene: Scene): void {
    // Alta resolución para que el texto/código se lean nítidos.
    this.screenTexture = new DynamicTexture('screenTex', { width: 1920, height: 1080 }, scene, true);
    this.screenTexture.updateSamplingMode(3); // trilineal (más nítido)
    const screenMat = new StandardMaterial('screenMat', scene);
    screenMat.diffuseTexture = this.screenTexture;
    screenMat.emissiveTexture = this.screenTexture; // auto-iluminada para leerse en lo oscuro
    screenMat.emissiveColor = new Color3(1, 1, 1);
    screenMat.disableLighting = true; // que el texto se vea nítido, sin lavar
    if (screenMat.diffuseTexture) screenMat.diffuseTexture.anisotropicFilteringLevel = 8;
    // Pantalla grande (16:9), ocupa casi toda la pared frontal.
    const W = 13;
    const Hs = (W * 9) / 16;
    const cy = 4.1;
    const screen = MeshBuilder.CreatePlane(
      'screen',
      { width: W, height: Hs, sideOrientation: Mesh.DOUBLESIDE },
      scene,
    );
    screen.position.set(0, cy, 6.7);
    screen.material = screenMat;
    // CLAVE: excluir la pantalla del glow, si no el bloom la "quema" en blanco.
    this.glow?.addExcludedMesh(screen);
    // marco
    const frame = MeshBuilder.CreateBox('frame', { width: W + 0.5, height: Hs + 0.5, depth: 0.1 }, scene);
    frame.position.set(0, cy, 6.82);
    frame.material = this.mat(scene, 'frameMat', new Color3(0.02, 0.02, 0.04));
  }

  /** Profesor estático junto a la pantalla (robot_profesor.glb); fallback: primitivas. */
  private async loadPresenter(scene: Scene): Promise<void> {
    try {
      const result = await SceneLoader.ImportMeshAsync('', '/models/', 'robot_profesor.glb', scene);
      const holder = new TransformNode('presenter', scene);
      const rootMesh = result.meshes[0];
      rootMesh.parent = holder;
      const b = rootMesh.getHierarchyBoundingVectors(true);
      const s = 2.6 / Math.max(0.001, b.max.y - b.min.y);
      holder.scaling.setAll(s);
      this.presenterBaseY = -b.min.y * s;
      holder.position.set(-2.8, this.presenterBaseY, 4.6); // a un lado de la pantalla
      holder.rotation.y = Math.PI; // mira a los alumnos
      this.presenter = holder;
      this.obstacles.push({ x: -2.8, z: 4.6, hw: 0.8, hd: 0.8 });
      result.animationGroups.forEach((a) => a.stop()); // profe quieto
    } catch {
      this.buildRobot(scene); // mascota de primitivas como profe
    }
  }

  /** Avatar del alumno (robot.glb con walk_animation), controlable con WASD. */
  private async loadAvatar(scene: Scene): Promise<void> {
    try {
      const result = await SceneLoader.ImportMeshAsync('', '/models/', 'robot.glb', scene);
      const holder = new TransformNode('avatar', scene);
      const rootMesh = result.meshes[0];
      rootMesh.parent = holder;
      const b = rootMesh.getHierarchyBoundingVectors(true);
      const s = 1.8 / Math.max(0.001, b.max.y - b.min.y);
      holder.scaling.setAll(s);
      holder.position.set(0, -b.min.y * s, -2); // arranca cerca del alumno
      this.avatar = holder;
      this.walkAnim =
        result.animationGroups.find((a) => /walk/i.test(a.name)) || result.animationGroups[0];
      this.walkAnim?.stop();
    } catch (error) {
      console.warn('No se pudo cargar el avatar /models/robot.glb', error);
    }
  }

  private readonly onKeyDown = (e: KeyboardEvent) => this.pressed.add(e.key.toLowerCase());
  private readonly onKeyUp = (e: KeyboardEvent) => this.pressed.delete(e.key.toLowerCase());

  private updateAvatar(dt: number): void {
    const avatar = this.avatar;
    const cam = this.camera;
    if (!avatar || !cam) return;
    const fwd = cam.getDirection(Vector3.Forward());
    fwd.y = 0;
    fwd.normalize();
    const right = cam.getDirection(Vector3.Right());
    right.y = 0;
    right.normalize();
    const move = Vector3.Zero();
    const p = this.pressed;
    if (p.has('w') || p.has('arrowup')) move.addInPlace(fwd);
    if (p.has('s') || p.has('arrowdown')) move.subtractInPlace(fwd);
    if (p.has('a') || p.has('arrowleft')) move.subtractInPlace(right);
    if (p.has('d') || p.has('arrowright')) move.addInPlace(right);

    const isMoving = move.lengthSquared() > 0.0001;
    if (isMoving) {
      move.normalize();
      const speed = 3.5 * dt;
      const cx = avatar.position.x;
      const cz = avatar.position.z;
      // Movimiento con deslizamiento: probamos cada eje por separado y solo
      // avanzamos en el que no choque (así no atravesamos mesas/profesor).
      const nx = Math.max(-10, Math.min(10, cx + move.x * speed));
      if (!this.blocked(nx, cz)) avatar.position.x = nx;
      const nz = Math.max(-10, Math.min(5, cz + move.z * speed));
      if (!this.blocked(avatar.position.x, nz)) avatar.position.z = nz;
      // El frente del modelo robot.glb apunta a -Z, por eso sumamos PI: así
      // camina mirando hacia donde se mueve (sin esto parece retroceder).
      avatar.rotation.y = Math.atan2(move.x, move.z) + Math.PI;
    }
    if (isMoving !== this.moving) {
      this.moving = isMoving;
      if (this.walkAnim) isMoving ? this.walkAnim.play(true) : this.walkAnim.pause();
    }
    cam.target.set(avatar.position.x, avatar.position.y + 1.4, avatar.position.z);
  }

  /** ¿La posición (x,z) cae dentro de algún obstáculo (+ radio del avatar)? */
  private blocked(x: number, z: number): boolean {
    const r = 0.45;
    for (const o of this.obstacles) {
      if (
        x > o.x - o.hw - r &&
        x < o.x + o.hw + r &&
        z > o.z - o.hd - r &&
        z < o.z + o.hd + r
      ) {
        return true;
      }
    }
    return false;
  }

  private buildRobot(scene: Scene): void {
    const root = new TransformNode('robot', scene);
    root.position.set(-2.8, 0, 4.6);
    root.rotation.y = Math.PI;
    this.presenterBaseY = 0;
    this.presenter = root;
    this.obstacles.push({ x: -2.8, z: 4.6, hw: 0.8, hd: 0.8 });

    const white = this.mat(scene, 'rWhite', new Color3(0.94, 0.96, 0.99), new Color3(0.22, 0.24, 0.3));
    const black = this.mat(scene, 'rBlack', new Color3(0.05, 0.05, 0.07), new Color3(0.02, 0.02, 0.03));

    // Cuerpo y cabeza redondeados (look mascota chibi).
    const body = MeshBuilder.CreateSphere('body', { diameter: 1.7, segments: 24 }, scene);
    body.scaling.set(1, 0.95, 0.9);
    body.position.y = 1.2;
    body.material = white;
    body.parent = root;

    const head = MeshBuilder.CreateSphere('head', { diameter: 1.5, segments: 24 }, scene);
    head.position.y = 2.3;
    head.material = white;
    head.parent = root;

    // Cara: textura con ojos naranjas + boca, sobre el frente de la cabeza.
    this.faceTex = new DynamicTexture('faceTex', { width: 512, height: 512 }, scene, true);
    this.faceTex.hasAlpha = true;
    const faceMat = new StandardMaterial('faceMat', scene);
    faceMat.diffuseTexture = this.faceTex;
    faceMat.diffuseTexture.hasAlpha = true;
    faceMat.useAlphaFromDiffuseTexture = true;
    faceMat.emissiveTexture = this.faceTex;
    faceMat.emissiveColor = new Color3(1, 1, 1);
    faceMat.disableLighting = true;
    faceMat.backFaceCulling = false;
    const face = MeshBuilder.CreatePlane('face', { width: 1.3, height: 1.3, sideOrientation: Mesh.DOUBLESIDE }, scene);
    face.position.set(0, 2.34, 0.73);
    face.material = faceMat;
    face.parent = root;
    this.drawFace(false);

    // Antena negra curva con bolita.
    const antenna = MeshBuilder.CreateCylinder('antenna', { height: 0.7, diameter: 0.06 }, scene);
    antenna.position.set(0.18, 3.15, 0);
    antenna.rotation.z = -0.5;
    antenna.material = black;
    antenna.parent = root;
    const ball = MeshBuilder.CreateSphere('antennaBall', { diameter: 0.18 }, scene);
    ball.position.set(0.5, 3.42, 0);
    ball.material = black;
    ball.parent = root;

    // Orejitas redondas (como el mascota).
    for (const x of [-0.62, 0.62]) {
      const ear = MeshBuilder.CreateSphere('ear', { diameter: 0.4 }, scene);
      ear.position.set(x, 2.85, 0);
      ear.material = white;
      ear.parent = root;
    }

    // Brazos: el derecho levantado saludando.
    const armL = MeshBuilder.CreateCapsule('armL', { height: 0.9, radius: 0.14 }, scene);
    armL.position.set(-0.95, 1.45, 0.1);
    armL.rotation.z = 0.45;
    armL.material = white;
    armL.parent = root;
    const armR = MeshBuilder.CreateCapsule('armR', { height: 0.9, radius: 0.14 }, scene);
    armR.position.set(1.0, 2.0, 0.1);
    armR.rotation.z = 2.4; // levantado, saludando
    armR.material = white;
    armR.parent = root;

    // Piernas cortas.
    for (const x of [-0.38, 0.38]) {
      const leg = MeshBuilder.CreateCapsule('leg', { height: 0.55, radius: 0.17 }, scene);
      leg.position.set(x, 0.4, 0);
      leg.material = white;
      leg.parent = root;
    }
  }

  /** Dibuja la cara del robot (ojos naranjas + boca). open=true => boca abierta (hablando). */
  private drawFace(open: boolean): void {
    const dt = this.faceTex;
    if (!dt) return;
    const ctx = dt.getContext() as unknown as CanvasRenderingContext2D;
    const { width, height } = dt.getSize();
    ctx.clearRect(0, 0, width, height);

    // Ojos naranjas grandes.
    ctx.fillStyle = '#ff5a1f';
    ctx.beginPath();
    ctx.ellipse(width * 0.34, height * 0.44, 52, 66, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(width * 0.66, height * 0.44, 52, 66, 0, 0, Math.PI * 2);
    ctx.fill();

    // Boca negra.
    ctx.fillStyle = '#141414';
    ctx.strokeStyle = '#141414';
    ctx.lineCap = 'round';
    if (open) {
      ctx.beginPath();
      ctx.ellipse(width * 0.5, height * 0.66, 58, 46, 0, 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.lineWidth = 22;
      ctx.beginPath();
      ctx.arc(width * 0.5, height * 0.6, 78, 0.12 * Math.PI, 0.88 * Math.PI);
      ctx.stroke();
    }
    dt.update();
  }

  private drawSlide(slide: PresentationSlide | null, title: string): void {
    const dt = this.screenTexture;
    if (!dt) return;
    const ctx = dt.getContext() as unknown as CanvasRenderingContext2D;
    const { width, height } = dt.getSize();
    // Dibujamos en un espacio lógico 1280x720 y lo escalamos a la textura real
    // (1920x1080) → resolución-independiente y nítido.
    const LW = 1280;
    const LH = 720;
    ctx.setTransform(width / LW, 0, 0, height / LH, 0, 0);

    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, LW, LH);

    // Barra superior con el título de la clase.
    ctx.fillStyle = '#1e3a8a';
    ctx.fillRect(0, 0, LW, 56);
    ctx.fillStyle = '#dbeafe';
    ctx.font = 'bold 28px sans-serif';
    ctx.fillText((title || 'Metaverso RetIAm').slice(0, 64), 36, 38);

    if (!slide) {
      ctx.fillStyle = '#64748b';
      ctx.font = '38px sans-serif';
      ctx.fillText('Pídele un tema al profesor para empezar…', 60, 200);
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      dt.update();
      return;
    }

    ctx.fillStyle = '#1e3a8a';
    ctx.font = 'bold 52px sans-serif';
    let y = this.wrapText(ctx, slide.title, 56, 130, LW - 112, 60);

    ctx.fillStyle = '#1f2937';
    ctx.font = '32px sans-serif';
    y += 26;
    for (const b of slide.bullets) {
      y = this.wrapText(ctx, '•  ' + b, 76, y, LW - 150, 44) + 18;
      if (y > LH - 150) break;
    }

    // Diagrama de flujo (solo si el slide lo trae).
    if (slide.diagram && slide.diagram.length && y < LH - 180) {
      y = this.drawDiagram(ctx, LW, LH, slide.diagram, y + 12);
    }

    // Bloque de código (solo si aplica).
    if (slide.code && y < LH - 110) {
      const boxH = Math.min(300, LH - y - 18);
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(56, y, LW - 112, boxH);
      ctx.fillStyle = '#7dd3fc';
      ctx.font = '18px monospace';
      ctx.fillText('// ejemplo', 74, y + 26);
      ctx.fillStyle = '#e2e8f0';
      ctx.font = '24px monospace';
      const maxLines = Math.floor((boxH - 44) / 30);
      const lines = slide.code.split('\n').slice(0, maxLines);
      let cy = y + 58;
      for (const line of lines) {
        ctx.fillText(line.slice(0, 84), 74, cy);
        cy += 30;
      }
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    dt.update();
  }

  /** Dibuja un flujo de pasos (cajas con flechas). Devuelve la Y final. */
  private drawDiagram(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    steps: string[],
    top: number,
  ): number {
    const margin = 60;
    const gap = 24;
    const arrow = 28;
    const boxH = 86;
    const avail = width - margin * 2;
    const n = steps.length;

    // ¿Cuántas cajas por fila caben con un ancho mínimo legible?
    let perRow = n;
    let boxW = (avail - (perRow - 1) * (gap + arrow)) / perRow;
    if (boxW < 220) {
      perRow = Math.max(1, Math.floor((avail + gap + arrow) / (220 + gap + arrow)));
      boxW = (avail - (perRow - 1) * (gap + arrow)) / perRow;
    }

    let x = margin;
    let y = top;
    for (let i = 0; i < n; i++) {
      if (i > 0 && i % perRow === 0) {
        y += boxH + 38;
        x = margin;
        if (y > height - boxH - 20) break;
      }
      // Caja.
      this.roundRect(ctx, x, y, boxW, boxH, 14);
      ctx.fillStyle = '#ede9fe';
      ctx.fill();
      ctx.strokeStyle = '#7c3aed';
      ctx.lineWidth = 3;
      ctx.stroke();
      // Número.
      ctx.fillStyle = '#7c3aed';
      ctx.beginPath();
      ctx.arc(x + 26, y + boxH / 2, 15, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 20px sans-serif';
      ctx.fillText(String(i + 1), x + 20, y + boxH / 2 + 7);
      // Texto del paso.
      ctx.fillStyle = '#3730a3';
      ctx.font = '22px sans-serif';
      this.wrapText(ctx, steps[i], x + 50, y + 34, boxW - 64, 26);
      // Flecha al siguiente (si sigue en la misma fila).
      const lastInRow = i % perRow === perRow - 1 || i === n - 1;
      if (!lastInRow) {
        const ay = y + boxH / 2;
        ctx.strokeStyle = '#7c3aed';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(x + boxW + 4, ay);
        ctx.lineTo(x + boxW + gap + arrow - 6, ay);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x + boxW + gap + arrow - 4, ay);
        ctx.lineTo(x + boxW + gap + arrow - 18, ay - 9);
        ctx.lineTo(x + boxW + gap + arrow - 18, ay + 9);
        ctx.closePath();
        ctx.fillStyle = '#7c3aed';
        ctx.fill();
      }
      x += boxW + gap + arrow;
    }
    return y + boxH + 24;
  }

  private roundRect(
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
    r: number,
  ): void {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  /** Dibuja texto con salto de línea; devuelve la Y final. */
  private wrapText(
    ctx: CanvasRenderingContext2D,
    text: string,
    x: number,
    y: number,
    maxWidth: number,
    lineHeight: number,
  ): number {
    const words = text.split(' ');
    let line = '';
    for (const word of words) {
      const test = line ? line + ' ' + word : word;
      if (ctx.measureText(test).width > maxWidth && line) {
        ctx.fillText(line, x, y);
        line = word;
        y += lineHeight;
      } else {
        line = test;
      }
    }
    if (line) {
      ctx.fillText(line, x, y);
      y += lineHeight;
    }
    return y;
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize);
    window.removeEventListener('keydown', this.onKeyDown);
    window.removeEventListener('keyup', this.onKeyUp);
    this.scene?.dispose();
    this.engine?.dispose();
  }
}
