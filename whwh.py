import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨 - 커스텀 이미지 캐릭터 게임", layout="wide")

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>체인소맨 하이브리드 - 커스텀 캐릭터</title>
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
    canvas { display: block; }

    .title { 
      position: relative; z-index: 2; font-size: 32px; color: #fff; margin-bottom: 10px; 
      text-shadow: 3px 3px 0px #ff0055, -3px -3px 0px #00e5ff; font-weight: 900; font-style: italic;
    }
    .overlay {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(5, 5, 5, 0.94); display: flex; flex-direction: column;
      align-items: center; justify-content: center; pointer-events: auto; z-index: 10;
    }
    .input-box {
      display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; width: 80%;
      background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; border: 1px solid #ff0055;
    }
    input[type="text"] {
      width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ff0055;
      background: #111; color: #fff; font-size: 13px;
    }
    .game-btn {
      padding: 10px 30px; font-size: 18px; font-weight: bold;
      background: #ff0055; color: #fff; border: none; border-radius: 4px; cursor: pointer;
      box-shadow: 0 0 15px rgba(255, 0, 85, 0.6); transition: 0.2s;
    }
    .game-btn:hover { background: #fff; color: #ff0055; transform: scale(1.05); }

    .ui-layer {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none; display: flex; flex-direction: column; justify-content: space-between;
      padding: 10px; z-index: 5;
    }
    .hud { display: flex; justify-content: space-between; align-items: flex-start; width: 100%; }
    .bar-container {
      width: 230px; height: 16px; background: #222; border: 2px solid #fff;
      position: relative; border-radius: 3px; overflow: hidden; margin-bottom: 3px;
    }
    .health-bar { height: 100%; background: linear-gradient(90deg, #ff0055, #ff5500); width: 100%; }
    .ult-bar { height: 100%; background: linear-gradient(90deg, #00e5ff, #0055ff); width: 0%; transition: width 0.1s; }
  </style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas" width="800" height="450"></canvas>

  <div class="ui-layer">
    <div class="hud">
      <div>
        <div style="font-weight:900; font-size:13px; text-shadow:0 0 8px #ff0055;">1P: MY CHARACTER</div>
        <div class="bar-container"><div id="p1-health" class="health-bar"></div></div>
        <div class="bar-container"><div id="p1-ult" class="ult-bar"></div></div>
      </div>
      <div id="score" style="font-size:26px; font-weight:900; color:#ffcc00;">0 - 0</div>
      <div style="text-align: right;">
        <div style="font-weight:900; font-size:13px; text-shadow:0 0 8px #00e5ff;">2P: ENEMY</div>
        <div class="bar-container"><div id="p2-health" class="health-bar" style="float:right;"></div></div>
        <div class="bar-container"><div id="p2-ult" class="ult-bar" style="float:right;"></div></div>
      </div>
    </div>
  </div>

  <div id="select-screen" class="overlay">
    <h1 class="title">커스텀 캐릭터 설정</h1>
    
    <div class="input-box">
      <label style="font-size:13px; color:#00e5ff; font-weight:bold;">1P 캐릭터 이미지 URL 입력:</label>
      <input type="text" id="img-url-input" placeholder="https://example.com/character.png" value="https://raw.githubusercontent.com/pokeapi/sprites/master/sprites/pokemon/other/official-artwork/25.png">
      <span style="font-size:11px; color:#aaa;">* 원하시는 이미지의 웹 주소(PNG, JPG)를 넣으시면 캐릭터로 적용되어 조종할 수 있습니다.</span>
    </div>

    <button class="game-btn" onclick="startGame()">게임 시작!</button>
    <div style="margin-top:12px; font-size:11px; color:#aaa; text-align:center;">
      [1P] A/D: 이동 | W: 점프 | F: 기본공격 | Z/X: 특수스킬 | E: 궁극기<br>
      [2P] 방향키: 이동 | Up: 점프 | K: 기본공격 | J/I: 특수스킬 | O: 궁극기
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 그래픽 향상 옵션
ctx.imageSmoothingEnabled = true;

const GRAVITY = 0.65;
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 450;
const GROUND_Y = 380;

let customImage = new Image();
let isImageLoaded = false;

class Fighter {
  constructor({ x, y, isP2, imageObj }) {
    this.x = x; this.y = y;
    this.width = 70; this.height = 90;
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

    if (this.facing === 'left') {
      ctx.scale(-1, 1);
    }

    if (this.imageObj && isImageLoaded) {
      // 고화질 캐릭터 이미지 랜더링
      ctx.drawImage(this.imageObj, -this.width / 2, -this.height / 2, this.width, this.height);
    } else {
      // 이미지 미로드시 대체 그래픽
      ctx.fillStyle = this.isP2 ? '#00e5ff' : '#ff0055';
      ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
    }

    ctx.restore();

    if (this.isAttacking) {
      ctx.fillStyle = 'rgba(255, 0, 85, 0.6)';
      const atkX = this.facing === 'right' ? this.x + this.width : this.x - 50;
      ctx.fillRect(atkX, this.y + 20, 50, 40);
    }
  }

  attack(enemy) {
    if (this.isAttacking) return;
    this.isAttacking = true;
    
    const atkX = this.facing === 'right' ? this.x + this.width : this.x - 50;
    if (atkX < enemy.x + enemy.width && atkX + 50 > enemy.x && this.y < enemy.y + enemy.height) {
      enemy.hp = Math.max(0, enemy.hp - 10);
      this.ultGauge = Math.min(100, this.ultGauge + 15);
    }

    setTimeout(() => { this.isAttacking = false; }, 150);
  }
}

let player1, player2;
const keys = {};

window.addEventListener('keydown', e => keys[e.key] = true);
window.addEventListener('keyup', e => keys[e.key] = false);

function startGame() {
  const url = document.getElementById('img-url-input').value;
  customImage.crossOrigin = "Anonymous";
  customImage.src = url;
  customImage.onload = () => { isImageLoaded = true; };

  document.getElementById('select-screen').style.display = 'none';

  player1 = new Fighter({ x: 150, y: 200, isP2: false, imageObj: customImage });
  player2 = new Fighter({ x: 600, y: 200, isP2: true, imageObj: null });

  requestAnimationFrame(gameLoop);
}

function handleInput() {
  player1.vx = 0;
  if (keys['a'] || keys['A']) player1.vx = -player1.speed;
  if (keys['d'] || keys['D']) player1.vx = player1.speed;
  if ((keys['w'] || keys['W']) && player1.isGrounded) player1.vy = player1.jumpPower;
  if (keys['f'] || keys['F']) player1.attack(player2);

  player2.vx = 0;
  if (keys['ArrowLeft']) player2.vx = -player2.speed;
  if (keys['ArrowRight']) player2.vx = player2.speed;
  if (keys['ArrowUp'] && player2.isGrounded) player2.vy = player2.jumpPower;
  if (keys['k'] || keys['K']) player2.attack(player1);
}

function gameLoop() {
  ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  // 배경 그래픽 (신주쿠 백화점 옥상 야경)
  let grad = ctx.createLinearGradient(0, 0, 0, CANVAS_HEIGHT);
  grad.addColorStop(0, '#020208'); grad.addColorStop(1, '#1a0b2e');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  // 바닥
  ctx.fillStyle = '#22222b';
  ctx.fillRect(0, GROUND_Y, CANVAS_WIDTH, CANVAS_HEIGHT - GROUND_Y);
  ctx.fillStyle = '#ff0055';
  ctx.fillRect(0, GROUND_Y, CANVAS_WIDTH, 4);

  handleInput();
  player1.update(player2);
  player2.update(player1);

  player1.draw();
  player2.draw();

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
