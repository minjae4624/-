import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨 하이브리드", layout="wide")

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>체인소맨 하이브리드</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #050505;
      color: #fff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      user-select: none;
    }
    #game-container {
      position: relative;
      width: 800px;
      height: 450px;
      box-shadow: 0 0 35px rgba(255, 0, 85, 0.5);
      border: 3px solid #ff0055;
      background: #111;
      overflow: hidden;
    }
    canvas { display: block; }
    
    /* HUD Overlay */
    .ui-layer {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 15px;
    }
    .hud {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }
    .health-bar-container {
      width: 300px;
      height: 22px;
      background: #222;
      border: 2px solid #fff;
      position: relative;
      border-radius: 4px;
      overflow: hidden;
      box-shadow: 0 0 10px rgba(0,0,0,0.8);
    }
    .health-bar {
      height: 100%;
      background: linear-gradient(90deg, #ff0055, #ff5500);
      width: 100%;
      transition: width 0.1s linear;
    }
    .player-name {
      font-weight: 900;
      margin-bottom: 4px;
      font-size: 16px;
      text-shadow: 0 0 10px #ff0055;
      font-style: italic;
    }
    .score-board {
      font-size: 32px;
      font-weight: 900;
      color: #ffcc00;
      text-shadow: 0 0 12px #ffcc00;
      font-style: italic;
    }

    /* Select & Result Overlays */
    .overlay {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(5, 5, 5, 0.94);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      pointer-events: auto;
      z-index: 10;
    }
    .title { 
      font-size: 42px; 
      color: #ff0055; 
      margin-bottom: 5px; 
      text-shadow: 0 0 25px #ff0055;
      font-weight: 900;
      font-style: italic;
      letter-spacing: -1px;
    }
    .subtitle {
      font-size: 14px;
      color: #aaa;
      margin-bottom: 20px;
      letter-spacing: 2px;
    }
    .select-box { display: flex; gap: 30px; margin-bottom: 15px; }
    .player-select-panel {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.03);
      padding: 12px;
      border-radius: 8px;
      border: 1px solid #333;
    }
    .char-preview {
      width: 120px;
      height: 150px;
      border: 2px solid #ff0055;
      border-radius: 6px;
      background-size: cover;
      background-position: top center;
      background-repeat: no-repeat;
      box-shadow: 0 0 15px rgba(255, 0, 85, 0.3);
      background-color: #000;
    }
    select {
      padding: 6px 12px;
      font-size: 14px;
      background: #1a1a1a;
      color: #fff;
      border: 1px solid #ff0055;
      border-radius: 4px;
      cursor: pointer;
      width: 100%;
      text-align: center;
    }
    button {
      padding: 12px 35px;
      font-size: 20px;
      font-weight: bold;
      background: #ff0055;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      box-shadow: 0 0 20px rgba(255, 0, 85, 0.6);
      transition: 0.2s;
    }
    button:hover { background: #fff; color: #ff0055; transform: scale(1.05); }
    .controls-info {
      margin-top: 15px;
      font-size: 12px;
      color: #888;
      text-align: center;
      line-height: 1.4;
    }
  </style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas" width="800" height="450"></canvas>

  <!-- HUD Overlay -->
  <div class="ui-layer">
    <div class="hud">
      <div>
        <div id="p1-name" class="player-name">1P: 덴지</div>
        <div class="health-bar-container">
          <div id="p1-health" class="health-bar"></div>
        </div>
      </div>
      <div id="score" class="score-board">0 - 0</div>
      <div style="text-align: right;">
        <div id="p2-name" class="player-name">2P: 하야카와 아키</div>
        <div class="health-bar-container">
          <div id="p2-health" class="health-bar" style="float: right;"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- Character Select Screen -->
  <div id="select-screen" class="overlay">
    <h1 class="title">체인소맨 하이브리드</h1>
    <div class="subtitle">공안 대마 특이 4과 대전 격투 (3판 2선승제)</div>
    
    <div class="select-box">
      <div class="player-select-panel">
        <label style="font-weight:bold; color:#ff0055;">1P 캐릭터</label>
        <div id="p1-preview" class="char-preview"></div>
        <select id="p1-select" onchange="updatePreview('p1')">
          <option value="denji">덴지 (특수기: 체인소 변신)</option>
          <option value="aki">하야카와 아키 (특수기: 신속 베기)</option>
          <option value="power">파워 (특수기: 피의 강타)</option>
        </select>
      </div>
      <div class="player-select-panel">
        <label style="font-weight:bold; color:#0088ff;">2P 캐릭터</label>
        <div id="p2-preview" class="char-preview"></div>
        <select id="p2-select" onchange="updatePreview('p2')">
          <option value="aki">하야카와 아키 (특수기: 신속 베기)</option>
          <option value="denji">덴지 (특수기: 체인소 변신)</option>
          <option value="power">파워 (특수기: 피의 강타)</option>
        </select>
      </div>
    </div>
    <button onclick="startGame()">전투 시작!</button>
    <div class="controls-info">
      <strong>[1P 조작]</strong> A/D: 이동 | W: 점프 | F: 일반공격 | E: 잡기술(특수기)<br>
      <strong>[2P 조작]</strong> 방향키: 이동 | Up: 점프 | K: 일반공격 | O: 잡기술(특수기)
    </div>
  </div>

  <!-- Game Over Screen -->
  <div id="game-over-screen" class="overlay" style="display: none;">
    <h1 id="winner-text" class="title">1P 최종 승리!</h1>
    <button onclick="resetFullGame()">처음으로 돌아가기</button>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const GRAVITY = 0.65;
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 450;
const GROUND_Y = 380;

const CHAR_IMAGES = {
  denji: 'https://i.ibb.co/3yk0mRk/denji.png',
  aki: 'https://static.wikia.nocookie.net/chainsaw-man/images/b/b3/Aki_Hayakawa_anime_design.png',
  power: 'https://m.media-amazon.com/images/M/MV5BNTBmNTI2ZDQtNWFlNy00ZjgwLWIzY2ItYzA3Nzc0YTY1ZmMyXkEyXkFqcGc@._V1_.jpg'
};

let p1Score = 0;
let p2Score = 0;
let gameOver = false;

const keys = {};

window.addEventListener('keydown', e => { keys[e.key] = true; });
window.addEventListener('keyup', e => { keys[e.key] = false; });

class Fighter {
  constructor({ x, y, color, isP2, character }) {
    this.x = x;
    this.y = y;
    this.width = 40;
    this.height = 70;
    this.color = color;
    this.isP2 = isP2;
    this.character = character;

    this.vx = 0;
    this.vy = 0;
    this.speed = 5.5;
    this.jumpPower = -13.5;
    this.hp = 100;
    this.isGrounded = false;

    this.isAttacking = false;
    this.attackBox = { width: 55, height: 40 };
    this.attackCooldown = false;

    this.isSpecialActive = false;
    this.specialCooldown = false;
    this.specialTimer = 0;
  }

  reset(x) {
    this.x = x;
    this.y = GROUND_Y - this.height;
    this.vx = 0;
    this.vy = 0;
    this.hp = 100;
    this.isAttacking = false;
    this.isSpecialActive = false;
    this.specialCooldown = false;
    this.speed = 5.5;
  }

  update(enemy) {
    if (this.isSpecialActive) {
      this.specialTimer--;
      if (this.specialTimer <= 0) {
        this.isSpecialActive = false;
        this.speed = 5.5;
      }
    }

    this.vy += GRAVITY;
    this.x += this.vx;
    this.y += this.vy;

    if (this.x < 0) this.x = 0;
    if (this.x + this.width > CANVAS_WIDTH) this.x = CANVAS_WIDTH - this.width;

    if (this.y + this.height >= GROUND_Y) {
      this.y = GROUND_Y - this.height;
      this.vy = 0;
      this.isGrounded = true;
    } else {
      this.isGrounded = false;
    }

    if (this.isAttacking) {
      const atkX = this.isP2 ? this.x - this.attackBox.width : this.x + this.width;
      const atkY = this.y + 10;

      if (
        atkX < enemy.x + enemy.width &&
        atkX + this.attackBox.width > enemy.x &&
        atkY < enemy.y + enemy.height &&
        atkY + this.attackBox.height > enemy.y
      ) {
        let damage = (this.character === 'denji' && this.isSpecialActive) ? 16 : 9;
        enemy.takeDamage(damage);
        this.isAttacking = false;
      }
    }
  }

  draw() {
    ctx.save();

    if (this.character === 'denji') {
      ctx.fillStyle = '#f5c542';
      ctx.fillRect(this.x - 3, this.y - 6, this.width + 6, 24);

      ctx.fillStyle = '#fce4c8';
      ctx.fillRect(this.x + 2, this.y + 10, this.width - 4, 12);

      ctx.fillStyle = '#ffffff';
      ctx.fillRect(this.x, this.y + 22, this.width, 24);
      ctx.fillStyle = '#111111';
      ctx.fillRect(this.x + (this.isP2 ? 8 : 28), this.y + 22, 4, 20);

      ctx.fillStyle = '#1c1c1e';
      ctx.fillRect(this.x, this.y + 46, this.width, this.height - 46);

      ctx.fillStyle = '#e6e6e6';
      ctx.fillRect(this.x - 2, this.y + this.height - 6, this.width + 4, 6);
    } else {
      ctx.fillStyle = this.color;
      ctx.fillRect(this.x, this.y, this.width, this.height);
    }

    if (this.character === 'denji' && this.isSpecialActive) {
      ctx.strokeStyle = (Math.floor(Date.now() / 50) % 2 === 0) ? '#ff0055' : '#ffaa00';
      ctx.lineWidth = 4;
      ctx.strokeRect(this.x - 6, this.y - 6, this.width + 12, this.height + 12);
    }

    ctx.fillStyle = '#000';
    const eyeX = this.isP2 ? this.x + 8 : this.x + 24;
    ctx.fillRect(eyeX, this.y + 12, 6, 6);

    if (this.isAttacking) {
      ctx.fillStyle = this.character === 'denji' ? 'rgba(255, 0, 85, 0.8)' : 'rgba(255, 255, 255, 0.7)';
      const atkX = this.isP2 ? this.x - this.attackBox.width : this.x + this.width;
      ctx.fillRect(atkX, this.y + 10, this.attackBox.width, this.attackBox.height);
    }

    ctx.restore();
  }

  attack() {
    if (this.attackCooldown) return;
    this.isAttacking = true;
    this.attackCooldown = true;
    setTimeout(() => { this.isAttacking = false; }, 150);
    setTimeout(() => { this.attackCooldown = false; }, 380);
  }

  useSpecial(enemy) {
    if (this.specialCooldown) return;
    this.specialCooldown = true;

    if (this.character === 'denji') {
      this.isSpecialActive = true;
      this.specialTimer = 180;
      this.speed = 8.5;
    } else {
      const dashDistance = this.isP2 ? -130 : 130;
      this.x += dashDistance;
      if (this.x < 0) this.x = 0;
      if (this.x + this.width > CANVAS_WIDTH) this.x = CANVAS_WIDTH - this.width;

      if (Math.abs(this.x - enemy.x) < 70) {
        enemy.takeDamage(18);
      }
    }

    setTimeout(() => { this.specialCooldown = false; }, 4500);
  }

  takeDamage(amount) {
    this.hp -= amount;
    if (this.hp < 0) this.hp = 0;
  }
}

let player1, player2;

function updatePreview(playerKey) {
  const selectEl = document.getElementById(playerKey + '-select');
  const previewEl = document.getElementById(playerKey + '-preview');
  const charVal = selectEl.value;

  if (CHAR_IMAGES[charVal]) {
    previewEl.style.backgroundImage = `url('${CHAR_IMAGES[charVal]}')`;
  }
}

function initGame() {
  const p1Char = document.getElementById('p1-select').value;
  const p2Char = document.getElementById('p2-select').value;

  document.getElementById('p1-name').innerText = `1P: ${getCharName(p1Char)}`;
  document.getElementById('p2-name').innerText = `2P: ${getCharName(p2Char)}`;

  player1 = new Fighter({ x: 150, y: 200, color: '#e74c3c', isP2: false, character: p1Char });
  player2 = new Fighter({ x: 610, y: 200, color: '#3498db', isP2: true, character: p2Char });
}

function getCharName(key) {
  if (key === 'denji') return '덴지';
  if (key === 'aki') return '하야카와 아키';
  if (key === 'power') return '파워';
  return key;
}

function startGame() {
  p1Score = 0;
  p2Score = 0;
  gameOver = false;
  document.getElementById('score').innerText = '0 - 0';
  document.getElementById('select-screen').style.display = 'none';
  document.getElementById('game-over-screen').style.display = 'none';

  initGame();
  requestAnimationFrame(gameLoop);
}

function resetRound() {
  player1.reset(150);
  player2.reset(610);
}

function resetFullGame() {
  document.getElementById('select-screen').style.display = 'flex';
  document.getElementById('game-over-screen').style.display = 'none';
  updatePreview('p1');
  updatePreview('p2');
}

function handleInput() {
  player1.vx = 0;
  if (keys['a'] || keys['A']) player1.vx = -player1.speed;
  if (keys['d'] || keys['D']) player1.vx = player1.speed;
  if ((keys['w'] || keys['W']) && player1.isGrounded) player1.vy = player1.jumpPower;
  if (keys['f'] || keys['F']) player1.attack();
  if (keys['e'] || keys['E']) player1.useSpecial(player2);

  player2.vx = 0;
  if (keys['ArrowLeft']) player2.vx = -player2.speed;
  if (keys['ArrowRight']) player2.vx = player2.speed;
  if (keys['ArrowUp'] && player2.isGrounded) player2.vy = player2.jumpPower;
  if (keys['k'] || keys['K']) player2.attack();
  if (keys['o'] || keys['O']) player2.useSpecial(player1);
}

function updateHUD() {
  document.getElementById('p1-health').style.width = player1.hp + '%';
  document.getElementById('p2-health').style.width = player2.hp + '%';
  document.getElementById('score').innerText = `${p1Score} - ${p2Score}`;
}

function checkRoundOver() {
  if (player1.hp <= 0 || player2.hp <= 0) {
    if (player1.hp <= 0 && player2.hp <= 0) {
      // 무승부
    } else if (player1.hp <= 0) {
      p2Score++;
    } else if (player2.hp <= 0) {
      p1Score++;
    }

    updateHUD();

    if (p1Score === 2 || p2Score === 2) {
      gameOver = true;
      const winner = p1Score === 2 ? '1P' : '2P';
      document.getElementById('winner-text').innerText = `${winner} 최종 승리!`;
      document.getElementById('game-over-screen').style.display = 'flex';
    } else {
      resetRound();
    }
  }
}

function gameLoop() {
  if (gameOver) return;

  ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  ctx.fillStyle = '#11091c';
  ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  ctx.fillStyle = '#ff0055';
  ctx.fillRect(0, GROUND_Y, CANVAS_WIDTH, CANVAS_HEIGHT - GROUND_Y);

  handleInput();
  player1.update(player2);
  player2.update(player1);

  player1.draw();
  player2.draw();

  updateHUD();
  checkRoundOver();

  requestAnimationFrame(gameLoop);
}

updatePreview('p1');
updatePreview('p2');
</script>
</body>
</html>
"""

components.html(game_html, height=500, scrolling=False)
