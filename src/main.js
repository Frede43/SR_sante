import { Game } from './systems/Game.js';

const canvas = document.getElementById('game');
const game = new Game(canvas);

// Start game loop
game.start();

