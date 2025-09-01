export class ParticleSystem {
  constructor() {
    this.particles = [];
  }

  spawnBurst(x, y, color = '#ffffff', count = 8, speed = 120) {
    for (let i = 0; i < count; i++) {
      const a = Math.random() * Math.PI * 2;
      const s = speed * (0.4 + Math.random() * 0.8);
      this.particles.push({
        x,
        y,
        vx: Math.cos(a) * s,
        vy: Math.sin(a) * s,
        life: 0.4 + Math.random() * 0.5,
        size: 1 + Math.random() * 2,
        color,
      });
    }
  }

  update(dt) {
    for (const p of this.particles) {
      p.life -= dt;
      p.vy += 600 * dt; // gravity-like for particles
      p.x += p.vx * dt;
      p.y += p.vy * dt;
    }
    this.particles = this.particles.filter(p => p.life > 0);
  }

  render(ctx) {
    for (const p of this.particles) {
      ctx.fillStyle = p.color;
      ctx.fillRect(Math.floor(p.x), Math.floor(p.y), p.size, p.size);
    }
  }
}

