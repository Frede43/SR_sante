export class Input {
  constructor() {
    this.keysDown = new Set();
    this.keysPressed = new Set();
    this.keysReleased = new Set();
    this.locked = false;

    window.addEventListener('keydown', (e) => {
      if (this.locked) return;
      if (!this.keysDown.has(e.code)) this.keysPressed.add(e.code);
      this.keysDown.add(e.code);
    });

    window.addEventListener('keyup', (e) => {
      if (this.locked) return;
      this.keysDown.delete(e.code);
      this.keysReleased.add(e.code);
    });
  }

  update() {
    this.keysPressed.clear();
    this.keysReleased.clear();
  }

  isDown(code) { return this.keysDown.has(code); }
  pressed(code) { return this.keysPressed.has(code); }
  released(code) { return this.keysReleased.has(code); }
}

