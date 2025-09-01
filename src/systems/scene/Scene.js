import { Player } from '../../things/Player.js';
import { Enemy } from '../../things/Enemy.js';
import { Tilemap } from '../world/Tilemap.js';
import { ParticleSystem } from '../fx/Particles.js';

export class Scene {
  constructor(game) {
    this.game = game;
    this.entities = [];
    this.player = new Player(this.game, 160, 100);
    this.entities.push(this.player);
    this.tilemap = new Tilemap(60, 16, 16);
    this.fx = new ParticleSystem();
    // Spawn a couple of enemies
    this.entities.push(new Enemy(this.game, 280, 80));
    this.entities.push(new Enemy(this.game, 520, 60));
    this.paused = false;
    window.addEventListener('keydown', (e) => {
      if (e.code === 'KeyP') this.paused = !this.paused;
    });
  }

  update(dt) {
    if (this.paused) return;
    for (const e of this.entities) e.update(dt, this);
    this.fx.update(dt);

    // Player attack hit detection vs enemies
    if (this.player.attackTimer > 0) {
      for (const e of this.entities) {
        if (e === this.player || e.dead || !e.width) continue;
        const dx = (this.player.cx + this.player.facing * (this.player.width / 2 + 8)) - e.cx;
        const dy = this.player.cy - e.cy;
        const dist = Math.hypot(dx, dy);
        if (dist < 18) {
          e.takeDamage(1, this.player.facing * 180, -160);
          this.fx.spawnBurst(e.cx, e.cy, '#ffd166', 10, 160);
        }
      }
    }
  }

  render(ctx, camera, alpha) {
    // Parallax sky
    ctx.fillStyle = '#0a0c12';
    ctx.fillRect(0, 0, this.game.canvas.width, this.game.canvas.height);

    ctx.save();
    ctx.translate(-Math.floor(camera.x), -Math.floor(camera.y));

    // Background parallax layers (simple rectangles for now)
    ctx.fillStyle = '#0e1320';
    ctx.fillRect(-200, 40, 1200, 6);
    ctx.fillStyle = '#0b1a2a';
    ctx.fillRect(-100, 80, 1200, 4);

    this.tilemap.render(ctx);

    for (const e of this.entities) e.render(ctx);
    this.fx.render(ctx);
    ctx.restore();

    // Pause overlay
    if (this.paused) {
      ctx.fillStyle = 'rgba(0,0,0,0.4)';
      ctx.fillRect(0, 0, this.game.canvas.width, this.game.canvas.height);
      ctx.fillStyle = '#e6e6e6';
      ctx.font = '16px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('PAUSE (P)', this.game.canvas.width / 2, this.game.canvas.height / 2);
      ctx.textAlign = 'left';
    }

    // HUD: player HP (top-left)
    ctx.fillStyle = '#e6e6e6';
    ctx.font = '12px monospace';
    ctx.fillText(`HP: ${this.player.hp}/${this.player.maxHp}`, 10, 16);
  }
}

