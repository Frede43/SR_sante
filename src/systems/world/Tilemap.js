export class Tilemap {
  constructor(cols, rows, tileSize) {
    this.cols = cols;
    this.rows = rows;
    this.tileSize = tileSize;
    this.solid = 1;

    // Simple demo level: ground and some platforms
    this.grid = new Array(rows).fill(0).map(() => new Array(cols).fill(0));
    const groundY = rows - 2;
    for (let x = 0; x < cols; x++) this.grid[groundY][x] = this.solid;
    // some platforms
    for (let x = 6; x < 12; x++) this.grid[groundY - 4][x] = this.solid;
    for (let x = 18; x < 26; x++) this.grid[groundY - 7][x] = this.solid;
    for (let x = 30; x < 38; x++) this.grid[groundY - 10][x] = this.solid;

    // Make some pillars/obstacles
    for (let y = groundY - 1; y > groundY - 5; y--) this.grid[y][14] = this.solid;
    for (let y = groundY - 1; y > groundY - 4; y--) this.grid[y][28] = this.solid;
  }

  worldToTile(x, y) {
    return { cx: Math.floor(x / this.tileSize), cy: Math.floor(y / this.tileSize) };
  }

  isSolidAt(x, y) {
    const { cx, cy } = this.worldToTile(x, y);
    if (cy < 0 || cy >= this.rows || cx < 0 || cx >= this.cols) return true; // out of bounds solid
    return this.grid[cy][cx] === this.solid;
  }

  rectCollides(x, y, w, h) {
    const left = Math.floor(x / this.tileSize);
    const right = Math.floor((x + w - 1) / this.tileSize);
    const top = Math.floor(y / this.tileSize);
    const bottom = Math.floor((y + h - 1) / this.tileSize);
    for (let cy = top; cy <= bottom; cy++) {
      for (let cx = left; cx <= right; cx++) {
        if (cy < 0 || cy >= this.rows || cx < 0 || cx >= this.cols) return true;
        if (this.grid[cy][cx] === this.solid) return true;
      }
    }
    return false;
  }

  render(ctx) {
    ctx.fillStyle = '#1b2233';
    for (let y = 0; y < this.rows; y++) {
      for (let x = 0; x < this.cols; x++) {
        if (this.grid[y][x] !== this.solid) continue;
        ctx.fillRect(x * this.tileSize, y * this.tileSize, this.tileSize, this.tileSize);
      }
    }
  }
}

