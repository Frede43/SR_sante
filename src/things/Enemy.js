export class Enemy {
  constructor(game, x, y) {
    this.game = game;
    this.x = x;
    this.y = y;
    this.prevX = x;
    this.prevY = y;
    this.width = 14;
    this.height = 18;
    this.vx = 0;
    this.vy = 0;
    this.speed = 90;
    this.gravity = 920;
    this.onGround = false;
    this.facing = -1;

    this.state = 'patrol';
    this.patrolTimer = 0;
    this.attackCooldown = 0;
    this.attackRange = 18;

    this.maxHp = 3;
    this.hp = this.maxHp;
    this.stunTimer = 0;
    this.dead = false;
    this.color = '#f65a83';
  }

  get cx() { return this.x + this.width / 2; }
  get cy() { return this.y + this.height / 2; }

  takeDamage(amount, knockbackX = 0, knockbackY = -120) {
    if (this.dead) return;
    this.hp -= amount;
    this.stunTimer = 0.25;
    this.vx += knockbackX;
    this.vy += knockbackY;
    if (this.hp <= 0) {
      this.dead = true;
    }
  }

  #distanceTo(target) {
    const dx = target.cx - this.cx;
    const dy = target.cy - this.cy;
    return Math.hypot(dx, dy);
  }

  update(dt, scene) {
    if (this.dead) return;

    const player = scene.player;
    const map = scene.tilemap;

    if (this.stunTimer > 0) this.stunTimer -= dt;
    if (this.attackCooldown > 0) this.attackCooldown -= dt;

    // Simple state machine
    const distance = this.#distanceTo(player);
    if (distance < 140 && this.stunTimer <= 0) {
      this.state = 'chase';
    } else if (this.stunTimer <= 0) {
      this.state = 'patrol';
    }

    if (this.state === 'patrol') {
      this.patrolTimer -= dt;
      if (this.patrolTimer <= 0) {
        this.facing = Math.random() < 0.5 ? -1 : 1;
        this.patrolTimer = 1.2 + Math.random() * 1.6;
      }
      this.vx = this.facing * this.speed * 0.5;
    } else if (this.state === 'chase') {
      this.facing = player.cx < this.cx ? -1 : 1;
      this.vx = this.facing * this.speed;
      if (distance < this.attackRange + 8 && this.onGround && this.attackCooldown <= 0) {
        // Attack: brief lunge
        this.vx += this.facing * 220;
        this.attackCooldown = 0.9;
        // If close enough, apply damage to player
        const overlapX = Math.max(0, Math.min(this.x + this.width, player.x + player.width) - Math.max(this.x, player.x));
        const overlapY = Math.max(0, Math.min(this.y + this.height, player.y + player.height) - Math.max(this.y, player.y));
        if (overlapX > 4 && overlapY > 6) {
          player.takeDamage(1, this.facing * 160, -140);
        }
      }
    }

    if (this.stunTimer > 0) {
      this.vx *= 0.6;
    }

    // Gravity
    this.vy += this.gravity * dt;

    // Integrate + collide (AABB similar to Player)
    this.prevX = this.x;
    this.prevY = this.y;

    // Horizontal
    this.x += this.vx * dt;
    if (map.rectCollides(this.x, this.y, this.width, this.height)) {
      if (this.vx > 0) {
        this.x = Math.floor((this.x + this.width) / map.tileSize) * map.tileSize - this.width - 0.001;
      } else if (this.vx < 0) {
        this.x = Math.floor(this.x / map.tileSize + 1) * map.tileSize + 0.001;
      }
      this.vx = 0;
      // flip on wall while patrolling
      if (this.state === 'patrol') this.facing *= -1;
    }

    // Vertical
    this.y += this.vy * dt;
    this.onGround = false;
    if (map.rectCollides(this.x, this.y, this.width, this.height)) {
      if (this.vy > 0) {
        this.y = Math.floor((this.y + this.height) / map.tileSize) * map.tileSize - this.height - 0.001;
        this.onGround = true;
      } else if (this.vy < 0) {
        this.y = Math.floor(this.y / map.tileSize + 1) * map.tileSize + 0.001;
      }
      this.vy = 0;
    }
  }

  render(ctx) {
    if (this.dead) return;
    ctx.fillStyle = this.color;
    ctx.fillRect(Math.floor(this.x), Math.floor(this.y), this.width, this.height);
    // HP pips
    for (let i = 0; i < this.maxHp; i++) {
      ctx.fillStyle = i < this.hp ? '#ff9a9e' : '#3a2b32';
      ctx.fillRect(Math.floor(this.x) + i * 4, Math.floor(this.y) - 4, 3, 2);
    }
  }
}

