import { Input } from '../tools/Input.js';
import { Camera } from './camera/Camera.js';
import { Scene } from './scene/Scene.js';

export class Game {
  constructor(canvas) {
    /** @type {HTMLCanvasElement} */
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.ctx.imageSmoothingEnabled = false;

    this.fixedDelta = 1000 / 60; // ms per tick
    this.accumulator = 0;
    this.lastTime = 0;
    this.running = false;

    this.input = new Input();
    this.camera = new Camera(0, 0, canvas.width, canvas.height);
    this.scene = new Scene(this);

    // Resize handling
    window.addEventListener('resize', () => this.#fitToWindow());
    this.#fitToWindow();
  }

  start() {
    if (this.running) return;
    this.running = true;
    this.lastTime = performance.now();
    requestAnimationFrame(this.#loop.bind(this));
  }

  stop() {
    this.running = false;
  }

  #loop(now) {
    if (!this.running) return;
    const deltaMs = now - this.lastTime;
    this.lastTime = now;
    this.accumulator += deltaMs;

    while (this.accumulator >= this.fixedDelta) {
      this.update(this.fixedDelta / 1000);
      this.accumulator -= this.fixedDelta;
    }

    const alpha = this.accumulator / this.fixedDelta;
    this.render(alpha);
    requestAnimationFrame(this.#loop.bind(this));
  }

  update(dt) {
    this.input.update();
    this.scene.update(dt);
    this.camera.update(dt, this.scene);
  }

  render(alpha) {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.scene.render(ctx, this.camera, alpha);
    // simple CRT-like vignette
    const grd = ctx.createLinearGradient(0,0,0,this.canvas.height);
    grd.addColorStop(0,'rgba(0,0,0,0.10)');
    grd.addColorStop(1,'rgba(0,0,0,0.18)');
    ctx.fillStyle = grd;
    ctx.fillRect(0,0,this.canvas.width,this.canvas.height);
  }

  #fitToWindow() {
    const root = document.getElementById('game-root');
    const { clientWidth, clientHeight } = root;
    const aspect = this.canvas.width / this.canvas.height;
    let width = clientWidth;
    let height = width / aspect;
    if (height > clientHeight) {
      height = clientHeight;
      width = height * aspect;
    }
    this.canvas.style.width = `${Math.floor(width)}px`;
    this.canvas.style.height = `${Math.floor(height)}px`;
  }
}

