export class Player {
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
    this.speed = 140;
    this.jumpSpeed = 280;
    this.gravity = 920;
    this.onGround = false;
    this.facing = 1;
    this.color = '#51d1f6';
    this.dashCooldown = 0;
    this.attackTimer = 0;
    this.maxHp = 5;
    this.hp = this.maxHp;
  }

  get cx() { return this.x + this.width / 2; }
  get cy() { return this.y + this.height / 2; }

  takeDamage(amount, knockbackX = 0, knockbackY = -120) {
    this.hp = Math.max(0, this.hp - amount);
    this.vx += knockbackX;
    this.vy += knockbackY;
  }

  update(dt, scene) {
    const input = this.game.input;

    let move = 0;
    if (input.isDown('ArrowLeft') || input.isDown('KeyA') || input.isDown('KeyQ')) move -= 1;
    if (input.isDown('ArrowRight') || input.isDown('KeyD')) move += 1;
    this.vx = move * this.speed;
    if (move !== 0) this.facing = Math.sign(move);

    // Jump
    if ((input.pressed('Space') || input.pressed('ArrowUp') || input.pressed('KeyW') || input.pressed('KeyZ')) && this.onGround) {
      this.vy = -this.jumpSpeed;
      this.onGround = false;
    }

    // Dash (short burst)
    if (this.dashCooldown > 0) this.dashCooldown -= dt;
    if (input.pressed('ShiftLeft') && this.dashCooldown <= 0) {
      this.vx += this.facing * 260;
      this.dashCooldown = 0.6;
    }

    // Attack (brief timer for demo)
    if (this.attackTimer > 0) this.attackTimer -= dt;
    if (input.pressed('KeyJ')) this.attackTimer = 0.2;

    // Gravity
    this.vy += this.gravity * dt;

    // Integrate and collide with tilemap (AABB)
    const map = scene.tilemap;

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
    // Body
    ctx.fillStyle = this.color;
    ctx.fillRect(Math.floor(this.x), Math.floor(this.y), this.width, this.height);

    // Attack arc indicator
    if (this.attackTimer > 0) {
      ctx.strokeStyle = '#ffd166';
      ctx.lineWidth = 2;
      ctx.beginPath();
      const cx = this.x + this.width / 2 + this.facing * (this.width / 2 + 6);
      const cy = this.y + this.height / 2;
      ctx.arc(cx, cy, 8, -0.7, 0.7);
      ctx.stroke();
    }

    // HP pips
    for (let i = 0; i < this.maxHp; i++) {
      ctx.fillStyle = i < this.hp ? '#8fffcb' : '#2a3a33';
      ctx.fillRect(Math.floor(this.x) + i * 4, Math.floor(this.y) - 5, 3, 2);
    }
  }
}

