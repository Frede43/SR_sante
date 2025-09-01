export class Camera {
  constructor(x, y, width, height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.lerp = 0.12;
    this.target = { x: 0, y: 0 };
    this.bounds = { x: 0, y: 0, width: 4000, height: 2000 };
  }

  follow(target) {
    this.target = target;
  }

  update(dt, scene) {
    if (scene && scene.player) {
      this.follow(scene.player);
    }
    const desiredX = this.target.x - this.width / 2;
    const desiredY = this.target.y - this.height / 2;
    this.x += (desiredX - this.x) * this.lerp;
    this.y += (desiredY - this.y) * this.lerp;
    // Clamp to bounds
    this.x = Math.max(this.bounds.x, Math.min(this.x, this.bounds.x + this.bounds.width - this.width));
    this.y = Math.max(this.bounds.y, Math.min(this.y, this.bounds.y + this.bounds.height - this.height));
  }
}

