import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨 하이브리드 게임", layout="wide")

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>체인소맨 하이브리드 - 풀버전</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body {
      background: #050505; color: #fff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      min-height: 100vh; overflow: hidden;
    }
    #game-container {
      position: relative; width: 800px; height: 450px;
      box-shadow: 0 0 35px rgba(255, 0, 85, 0.5);
      border: 3px solid #ff0055; background: #000; overflow: hidden;
    }
    canvas { display: block; position: relative; z-index: 2; }

    /* 메인화면 동영상 배경 */
    .bg-video {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover; opacity: 0.6; z-index: 1; pointer-events: none;
    }

    .title { 
      position: relative; z-index: 2; font-size: 32px; color: #fff; margin-bottom: 10px; 
      text-shadow: 3px 3px 0px #ff0055, -3px -3px 0px #00e5ff; font-weight: 900; font-style: italic;
    }
    .overlay {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(5, 5, 5, 0.75); display: flex; flex-direction: column;
      align-items: center; justify-content: center; pointer-events: auto; z-index: 10;
    }
    .input-box {
      display: flex; flex-direction: column; gap: 6px; margin-bottom: 15px; width: 75%;
      background: rgba(0, 0, 0, 0.6); padding: 12px; border-radius: 8px; border: 1px solid #ff0055;
    }
    input[type="text"] {
      width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ff0055;
      background: #111; color: #fff; font-size: 12px;
    }
    .btn-group { display: flex; gap: 15px; }
    .game-btn {
      padding: 10px 22px; font-size: 16px; font-weight: bold;
      background: #ff0055; color: #fff; border: none; border-radius: 4px; cursor: pointer;
      box-shadow: 0 0 15px rgba(255, 0, 85, 0.6); transition: 0.2s;
    }
    .game-btn.blue { background: #00e5ff; color: #000; box-shadow: 0 0 15px rgba(0, 229, 255, 0.6); }
    .game-btn:hover { transform: scale(1.05); filter: brightness(1.2); }

    .ui-layer {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none; display: flex; flex-direction: column; justify-content: space-between;
      padding: 10px; z-index: 5;
    }
    .hud { display: flex; justify-content: space-between; align-items: flex-start; width: 100%; }
    .bar-container {
      width: 220px; height: 16px; background: #222; border: 2px solid #fff;
      position: relative; border-radius: 3px; overflow: hidden; margin-bottom: 3px;
    }
    .health-bar { height: 100%; background: linear-gradient(90deg, #ff0055, #ff5500); width: 100%; }
    .ult-bar { height: 100%; background: linear-gradient(90deg, #00e5ff, #0055ff); width: 0%; transition: width 0.1s; }
  </style>
</head>
<body>

<div id="game-container">
  <!-- 메인화면 루프 동영상 -->
  <video class="bg-video" autoplay loop muted playsinline id="main-bg-video">
    <source src="https://assets.mixkit.co/videos/preview/mixkit-red-abstract-particle-motion-41525-large.mp4" type="video/mp4">
  </video>

  <canvas id="gameCanvas" width="800" height="450"></canvas>

  <div class="ui-layer">
    <div class="hud">
      <div>
        <div style="font-weight:900; font-size:13px; text-shadow:0 0 8px #ff0055;">1P: PLAYER</div>
        <div class="bar-container"><div id="p1-health" class="health-bar"></div></div>
        <div class="bar-container"><div id="p1-ult" class="ult-bar"></div></div>
      </div>
      <div id="score" style="font-size:20px; font-weight:900; color:#ffcc00;">READY</div>
      <div style="text-align: right;">
        <div id="p2-label" style="font-weight:900; font-size:13px; text-shadow:0 0 8px #00e5ff;">2P: ENEMY</div>
        <div class="bar-container"><div id="p2-health" class="health-bar" style="float:right;"></div></div>
        <div class="bar-container"><div id="p2-ult" class="ult-bar" style="float:right;"></div></div>
      </div>
    </div>
  </div>

  <div id="select-screen" class="overlay">
    <h1 class="title">체인소맨 하이브리드</h1>
    
    <div class="input-box">
      <label style="font-size:12px; color:#00e5ff; font-weight:bold;">1P 커스텀 캐릭터 이미지 URL:</label>
      <input type="text" id="img-url-input" placeholder="이미지 URL을 입력하세요" value="https://raw.githubusercontent.com/pokeapi/sprites/master/sprites/pokemon/other/official-artwork/25.png">
    </div>

    <div class="btn-group">
      <button class="game-btn" onclick="startGame(true)">1P vs AI (싱글)</button>
      <button class="game-btn blue" onclick="startGame(false)">1P vs 2P (대전)</button>
    </div>

    <div style="margin-top:12px; font-size:11px; color:#ccc; text-align:center; line-height:1.4;">
      [1P] A/D: 이동 | W: 점프 | F: 공격 | Z,X: 특수스킬 | E: 궁극기<br>
      [2P] 방향키: 이동 | Up: 점프 | K: 공격 | J,I: 특수스킬 | O: 궁극기
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

ctx.imageSmoothingEnabled = true;

const GRAVITY = 0.65;
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 450;
const GROUND_Y = 380;

let customImage = new Image();
let isImageLoaded = false;
let isAiMode = false;
let particles = [];

class Fighter {
  constructor({ x, y, isP2, imageObj }) {
    this.x = x; this.y = y;
    this.width = 65; this.height = 85;
    this.isP2 = isP2;
    this.facing = isP2 ? 'left' : 'right';
    this.imageObj = imageObj;

    this.vx = 0; this.vy = 0;
    this.speed = 6; this.jumpPower = -13.5;
    this.hp = 100;
    this.ultGauge = 0;
    this.isGrounded = false;
    this.isAttacking = false;
  }

  update(enemy) {
    this.vy += GRAVITY;
    this.x += this.vx;
    this.y += this.vy;

    if (this.vx > 0) this.facing = 'right';
    else if (this.vx < 0) this.facing = 'left';

    if (this.x < 0) this.x = 0;
    if (this.x + this.width > CANVAS_WIDTH) this.x = CANVAS_WIDTH - this.width;

    if (this.y + this.height >= GROUND_Y) {
      this.y = GROUND_Y - this.height;
      this.vy = 0;
      this.isGrounded = true;
    } else {
      this.isGrounded = false;
    }
  }

  draw() {
    ctx.save();
    ctx.translate(this.x + this.width / 2, this.y + this.height / 2);

    if (this.facing === 'left') ctx.scale(-1, 1);

    if (this.imageObj && isImageLoaded) {
      ctx.drawImage(this.imageObj, -this.width / 2, -this.height / 2, this.width, this.height);
    } else {
      ctx.fillStyle = this.isP2 ? '#00e5ff' : '#ff0055';
      ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
    }

    ctx.restore();

    if (this.isAttacking) {
      ctx.fillStyle = this.isP2 ? 'rgba(0, 229, 255, 0.7)' : 'rgba(255, 0, 85, 0.7)';
      const atkX = this.facing === 'right' ? this.x + this.width : this.x - 45;
      ctx.fillRect(atkX, this.y + 15, 45, 35);
    }
  }

  attack(enemy, dmg = 8, range = 45) {
    if (this.isAttacking) return;
    this.isAttacking = true;
    
    const atkX = this.facing === 'right' ? this.x + this.width : this.x - range;
    if (atkX < enemy.x + enemy.width && atkX + range > enemy.x && this.y < enemy.y + enemy.height) {
      enemy.hp = Math.max(0, enemy.hp - dmg);
      this.ultGauge = Math.min(100, this.ultGauge + 12);
      createParticles(enemy.x + enemy.width/2, enemy.y + enemy.height/2, this.isP2 ? '#00e5ff' : '#ff0055');
    }

    setTimeout(() => { this.isAttacking = false; }, 150);
  }

  useUlt(enemy) {
    if (this.ultGauge >= 100) {
      this.ultGauge = 0;
      this.attack(enemy, 35, 100);
      createParticles(enemy.x + enemy.width/2, enemy.y + enemy.height/2, '#ffcc00', 30);
    }
  }
}

function createParticles(x, y, color, count = 10) {
  for (let i = 0; i < count; i++) {
    particles.push({
      x: x, y: y,
      vx: (Math.random() - 0.5) * 8,
      vy: (Math.random() - 0.5) * 8,
      life: 20, color: color
    });
  }
}

let player1, player2;
const keys = {};

window.addEventListener('keydown', e => keys[e.key] = true);
window.addEventListener('keyup', e => keys[e.key] = false);

function startGame(aiMode) {
  isAiMode = aiMode;
  const url = document.getElementById('img-url-input').value;
  if(url) {
    customImage.crossOrigin = "Anonymous";
    customImage.src = url;
    customImage.onload = () => { isImageLoaded = true; };
  }

  document.getElementById('select-screen').style.display = 'none';
  document.getElementById('p2-label').innerText = isAiMode ? "2P: AI BOT" : "2P: PLAYER 2";

  player1 = new Fighter({ x: 150, y: 200, isP2: false, imageObj: customImage });
  player2 = new Fighter({ x: 600, y: 200, isP2: true, imageObj: null });

  requestAnimationFrame(gameLoop);
}

function updateAI() {
  player2.vx = 0;
  const dist = player1.x - player2.x;

  if (Math.abs(dist) > 50) {
    player2.vx = dist > 0 ? player2.speed * 0.7 : -player2.speed * 0.7;
  } else {
    if (Math.random() < 0.06) player2.attack(player1);
    if (player2.ultGauge >= 100) player2.useUlt(player1);
  }

  if (Math.random() < 0.01 && player2.isGrounded) player2.vy = player2.jumpPower;
}

function handleInput() {
  // 1P 조작
  player1.vx = 0;
  if (keys['a'] || keys['A']) player1.vx = -player1.speed;
  if (keys['d'] || keys['D']) player1.vx = player1.speed;
  if ((keys['w'] || keys['W']) && player1.isGrounded) player1.vy = player1.jumpPower;
  if (keys['f'] || keys['F']) player1.attack(player2);
  if (keys['z'] || keys['Z'] || keys['x'] || keys['X']) player1.attack(player2, 12, 60);
  if (keys['e'] || keys['E']) player1.useUlt(player2);

  // 2P 조작 또는 AI
  if (isAiMode) {
    updateAI();
  } else {
    player2.vx = 0;
    if (keys['ArrowLeft']) player2.vx = -player2.speed;
    if (keys['ArrowRight']) player2.vx = player2.speed;
    if (keys['ArrowUp'] && player2.isGrounded) player2.vy = player2.jumpPower;
    if (keys['k'] || keys['K']) player2.attack(player1);
    if (keys['j'] || keys['J'] || keys['i'] || keys['I']) player2.attack(player1, 12, 60);
    if (keys['o'] || keys['O']) player2.useUlt(player1);
  }
}

function gameLoop() {
  ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  // 배경 그래픽
  let grad = ctx.createLinearGradient(0, 0, 0, CANVAS_HEIGHT);
  grad.addColorStop(0, '#05050d'); grad.addColorStop(1, '#1a0b2e');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  // 스테이지 바닥
  ctx.fillStyle = '#1e1e24';
  ctx.fillRect(0, GROUND_Y, CANVAS_WIDTH, CANVAS_HEIGHT - GROUND_Y);
  ctx.fillStyle = '#ff0055';
  ctx.fillRect(0, GROUND_Y, CANVAS_WIDTH, 3);

  handleInput();
  player1.update(player2);
  player2.update(player1);

  player1.draw();
  player2.draw();

  // 파티클 렌더링
  particles.forEach((p, idx) => {
    p.x += p.vx; p.y += p.vy; p.life--;
    ctx.fillStyle = p.color;
    ctx.fillRect(p.x, p.y, 4, 4);
    if (p.life <= 0) particles.splice(idx, 1);
  });

  document.getElementById('p1-health').style.width = player1.hp + '%';
  document.getElementById('p2-health').style.width = player2.hp + '%';
  document.getElementById('p1-ult').style.width = player1.ultGauge + '%';
  document.getElementById('p2-ult').style.width = player2.ultGauge + '%';

  requestAnimationFrame(gameLoop);
}
</script>
</body>
</html>
"""

components.html(game_html, height=500, scrolling=False)
