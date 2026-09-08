import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨 하이브리드 - 픽셀 액션", layout="wide")

# HTML / CSS / JS 코드를 파이썬 문자열 변수(r""")로 안전하게 포장합니다.
game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>체인소맨 하이브리드</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body {
      background: #050505;
      color: #fff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      overflow: hidden;
    }
    #game-container {
      position: relative;
      width: 800px;
      height: 450px;
      box-shadow: 0 0 35px rgba(255, 0, 85, 0.5);
      border: 3px solid #ff0055;
      background: #000;
      overflow: hidden;
    }
    canvas { display: block; image-rendering: pixelated; }

    /* 스타트 화면 배경 유튜브 영상 오버레이 */
    #start-screen {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      z-index: 20;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.5);
    }
    #video-background {
      position: absolute;
      top: 50%; left: 50%;
      width: 100%; height: 100%;
      transform: translate(-50%, -50%);
      z-index: 1;
      pointer-events: none;
      filter: brightness(0.7) contrast(1.1);
      object-fit: cover;
    }
    .title { 
      position: relative; z-index: 2;
      font-size: 38px; color: #fff; margin-bottom: 10px; 
      text-shadow: 3px 3px 0px #ff0055, -3px -3px 0px #00e5ff;
      font-weight: 900; font-style: italic; letter-spacing: -1px;
    }
    .start-btn {
      position: relative; z-index: 2;
      padding: 14px 40px;
      font-size: 22px; font-weight: bold;
      color: #fff;
      background: linear-gradient(45deg, #ff0055, #ff5500);
      border: 3px solid #fff; border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 0 25px rgba(255, 0, 85, 0.8);
      transition: all 0.2s ease;
      letter-spacing: 2px;
    }
    .start-btn:hover {
      transform: scale(1.08);
      background: linear-gradient(45deg, #fff, #ff0055);
      color: #ff0055;
    }

    /* HUD Overlay & 게이지 바 */
    .ui-layer {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 12px;
      z-index: 5;
    }
    .hud { display: flex; justify-content: space-between; align-items: flex-start; width: 100%; }
    .bar-container {
      width: 250px; height: 18px;
      background: #222; border: 2px solid #fff;
      position: relative; border-radius: 3px; overflow: hidden;
      margin-bottom: 4px;
    }
    .health-bar { height: 100%; background: linear-gradient(90deg, #ff0055, #ff5500); width: 100%; }
    .ult-bar { height: 100%; background: linear-gradient(90deg, #00e5ff, #0055ff); width: 0%; transition: width 0.1s; }
    .player-name { font-weight: 900; font-size: 14px; text-shadow: 0 0 8px #ff0055; }
    .ult-text { font-size: 11px; font-weight: bold; color: #00e5ff; text-transform: uppercase; }

    /* 캐릭터 선택 오버레이 */
    .overlay {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(5, 5, 5, 0.94);
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      pointer-events: auto; z-index: 10;
    }
    .select-box { display: flex; gap: 20px; margin-bottom: 15px; }
    .player-select-panel {
      display: flex; flex-direction: column; align-items: center; gap: 6px;
      background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; border: 1px solid #333;
    }
    .char-preview {
      width: 100px; height: 120px; border: 2px solid #ff0055; border-radius: 6px;
      background-size: cover; background-position: center; background-color: #000;
    }
    select {
      padding: 5px 10px; font-size: 13px; background: #1a1a1a; color: #fff;
      border: 1px solid #ff0055; border-radius: 4px; cursor: pointer; text-align: center;
    }
    .game-btn {
      padding: 10px 30px; font-size: 18px; font-weight: bold;
      background: #ff0055; color: #fff; border: none; border-radius: 4px; cursor: pointer;
      box-shadow: 0 0 15px rgba(255, 0, 85, 0.6); transition: 0.2s;
    }
    .game-btn:hover { background: #fff; color: #ff0055; transform: scale(1.05); }

    /* 마키마 궁극기 컷씬 오버레이 */
    #makima-cutscene {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.95); display: none;
      flex-direction: column; align-items: center; justify-content: center;
      z-index: 15; pointer-events: none;
    }
    #makima-cutscene img {
      width: 200px; height: auto; border: 3px solid #ff0055;
      box-shadow: 0 0 30px #ff0055; border-radius: 8px; margin-bottom: 10px;
    }
    #makima-cutscene .text {
      font-size: 24px; font-weight: 900; color: #ff0055;
      text-shadow: 0 0 15px #ff0055; font-style: italic;
    }
  </style>
</head>
<body>

<div id="game-container">
  <!-- 1. 스타트 메인 화면 (요청하신 IRIS OUT 배경 음악 영상) -->
  <div id="start-screen">
    <iframe id="video-background" 
      src="https://www.youtube.com/embed/l9E-dh9kf_0?autoplay=1&mute=1&controls=0&loop=1&playlist=l9E-dh9kf_0&enablejsapi=1" 
      frameborder="0" allow="autoplay; encrypted-media">
    </iframe>
    <h1 class="title">CHAINSAW HYBRID</h1>
    <button class="start-btn" onclick="enterCharSelect()">GAME START</button>
  </div>

  <canvas id="gameCanvas" width="800" height="450"></canvas>

  <!-- 마키마 궁극기 연출 컷씬 -->
  <div id="makima-cutscene">
    <img src="https://i.ibb.co/L5Q2w4X/makima.png" alt="Makima Ritual">
    <div class="text">"이름을 복창해라... (압착)"</div>
  </div>

  <!-- 게임 HUD (체력바 + 복원된 궁극기 게이지) -->
  <div class="ui-layer">
    <div class="hud">
      <div>
        <div id="p1-name" class="player-name">1P: 하야카와 아키</div>
        <div class="bar-container"><div id="p1-health" class="health-bar"></div></div>
        <div class="bar-container"><div id="p1-ult" class="ult-bar"></div></div>
        <div id="p1-ult-text" class="ult-text">ULT GAUGE: 0%</div>
      </div>
      <div id="score" style="font-size:28px; font-weight:900; color:#ffcc00;">0 - 0</div>
      <div style="text-align: right;">
        <div id="p2-name" class="player-name">2P: 마키마</div>
        <div class="bar-container"><div id="p2-health" class="health-bar" style="float:right;"></div></div>
        <div class="bar-container"><div id="p2-ult" class="ult-bar" style="float:right;"></div></div>
        <div id="p2-ult-text" class="ult-text">ULT GAUGE: 0%</div>
      </div>
    </div>
  </div>

  <!-- 캐릭터 선택 화면 -->
  <div id="select-screen" class="overlay" style="display: none;">
    <h1 class="title" style="font-size:32px;">캐릭터 선택</h1>
    <div class="select-box">
      <div class="player-select-panel">
        <label style="font-weight:bold; color:#ff0055;">1P 캐릭터</label>
        <div id="p1-preview" class="char-preview"></div>
        <select id="p1-select" onchange="updatePreview('p1')">
          <option value="aki">하야카와 아키</option>
          <option value="makima">마키마 (신사 의식)</option>
          <option value="denji">덴지 (체인소)</option>
          <option value="power">파워 (피의 악마)</option>
        </select>
      </div>
      <div class="player-select-panel">
        <label style="font-weight:bold; color:#0088ff;">2P 캐릭터</label>
        <div id="p2-preview" class="char-preview"></div>
        <select id="p2-select" onchange="updatePreview('p2')">
          <option value="makima">마키마 (신사 의식)</option>
          <option value="aki">하야카와 아키</option>
          <option value="denji">덴지 (체인소)</option>
          <option value="power">파워 (피의 악마)</option>
        </select>
      </div>
    </div>
    <button class="game-btn" onclick="startGame()">전투 시작!</button>
    <div style="margin-top:10px; font-size:11px; color:#aaa; text-align:center;">
      [1P] A/D: 이동 | W: 점프 | F: 일반공격 | E: 궁극기(100%)<br>
      [2P] 방향키: 이동 | Up: 점프 | K: 일반공격 | O: 궁극기(100%)
    </div>
  </div>

  <!-- 승리 화면 -->
  <div id="game-over-screen" class="overlay" style="display: none;">
    <h1 id="winner-text" class="title">1P 최종 승리!</h1>
    <button class="game-btn" onclick="resetFullGame()">처음으로 돌아가기</button>
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
  aki: 'https://i.ibb.co/b3yK49Z/aki.png',
  power: 'https://i.ibb.co/6y4TjT1/power.png',
  makima: 'https://i.ibb.co/L5Q2w4X/makima.png'
};

let p1Score = 0, p2Score = 0;
let gameOver = false;
let screenShake = 0;
let particles = [];
let afterImages = [];

const keys = {};
window.addEventListener('keydown', e => { keys[e.key] = true; });
window.addEventListener('keyup', e => { keys[e.key] = false; });

function enterCharSelect() {
  document.getElementById('start-screen').style.display = 'none';
  document.getElementById('select-screen').style.display = 'flex';
  updatePreview('p1');
  updatePreview('p2');
}

class Fighter {
  constructor({ x, y, color, isP2, character }) {
    this.x = x; this.y = y;
    this.width = 40; this.height = 70;
    this.isP2 = isP2;
    this.character = character;

    this.vx = 0; this.vy = 0;
    this.speed = 5.5; this.jumpPower = -13.5;
    this.hp = 100;
    this.ultGauge = 0; // 복원된 궁극기 게이지 (0 ~ 100)
    this.isGrounded = false;

    this.isAttacking = false;
    this.attackBox = { width: 55, height: 40 };
    this.attackCooldown = false;
  }

  reset(x) {
    this.x = x; this.y = GROUND_Y - this.height;
    this.vx = 0; this.vy = 0;
    this.hp = 100; this.ultGauge = 0;
    this.isAttacking = false;
  }

  update(enemy) {
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

    // 이동 시 디테일 픽셀 잔상 이펙트
    if (Math.abs(this.vx) > 0 && Math.random() < 0.4) {
      afterImages.push({
        x: this.x, y: this.y, width: this.width, height: this.height,
        color: this.isP2 ? '#00e5ff' : '#ff0055', alpha: 0.5
      });
    }

    // 피격 판정
    if (this.isAttacking) {
      const atkX = this.isP2 ? this.x - this.attackBox.width : this.x + this.width;
      const atkY = this.y + 10;

      if (
        atkX < enemy.x + enemy.width &&
        atkX + this.attackBox.width > enemy.x &&
        atkY < enemy.y + enemy.height &&
        atkY + this.attackBox.height > enemy.y
      ) {
        enemy.takeDamage(8);
        this.ultGauge = Math.min(100, this.ultGauge + 15); // 공격 성공 시 궁극기 게이지 상승
        createParticles(enemy.x + 20, enemy.y + 30, '#ff0055', 12);
        screenShake = 6;
        this.isAttacking = false;
      }
    }
  }

  // 더욱 디테일해진 픽셀 표현
  draw() {
    ctx.save();

    if (this.character === 'denji') {
      ctx.fillStyle = '#f5c542'; ctx.fillRect(this.x - 2, this.y - 6, this.width + 4, 20); // 머리
      ctx.fillStyle = '#fce4c8'; ctx.fillRect(this.x + 4, y = this.y + 10, this.width - 8, 12); // 얼굴
      ctx.fillStyle = '#ffffff'; ctx.fillRect(this.x, this.y + 22, this.width, 24); // 셔츠
      ctx.fillStyle = '#1c1c1e'; ctx.fillRect(this.x, this.y + 46, this.width, this.height - 46); // 바지
    } 
    else if (this.character === 'makima') {
      ctx.fillStyle = '#d94e34'; ctx.fillRect(this.x - 2, this.y - 6, this.width + 4, 24); // 땋은 머리
      ctx.fillStyle = '#fce4c8'; ctx.fillRect(this.x + 4, this.y + 10, this.width - 8, 10);
      ctx.fillStyle = '#111115'; ctx.fillRect(this.x - 2, this.y + 20, this.width + 4, 45); // 긴 코트
      ctx.fillStyle = '#800000'; ctx.fillRect(this.x + 18, this.y + 20, 4, 15); // 넥타이
    }
    else {
      ctx.fillStyle = '#1e2749'; ctx.fillRect(this.x - 2, this.y - 4, this.width + 4, 22);
      ctx.fillStyle = '#fce4c8'; ctx.fillRect(this.x + 4, this.y + 10, this.width - 8, 10);
      ctx.fillStyle = '#15161a'; ctx.fillRect(this.x, this.y + 20, this.width, this.height - 20);
    }

    // 눈 픽셀
    ctx.fillStyle = '#000';
    const eyeX = this.isP2 ? this.x + 8 : this.x + 24;
    ctx.fillRect(eyeX, this.y + 12, 5, 5);

    // 화려한 공격 스킬 픽셀 이펙트
    if (this.isAttacking) {
      ctx.fillStyle = '#ff0055';
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
    setTimeout(() => { this.attackCooldown = false; }, 350);
  }

  useSpecial(enemy) {
    // 게이지가 100% 찼을 때만 발동
    if (this.ultGauge < 100) return;
    this.ultGauge = 0; // 게이지 소모

    if (this.character === 'makima') {
      const cutsceneEl = document.getElementById('makima-cutscene');
      cutsceneEl.style.display = 'flex';

      setTimeout(() => {
        cutsceneEl.style.display = 'none';
        triggerMakimaSqueezeEffect(enemy);
        enemy.takeDamage(40);
        screenShake = 20;
      }, 1200);
    } else {
      createParticles(enemy.x + 20, enemy.y + 30, '#00e5ff', 40);
      enemy.takeDamage(30);
      screenShake = 15;
    }
  }

  takeDamage(amount) {
    this.hp = Math.max(0, this.hp - amount);
  }
}

// 화려한 파티클 이펙트
function createParticles(x, y, color, count) {
  for (let i = 0; i < count; i++) {
    particles.push({
      x, y,
      vx: (Math.random() - 0.5) * 10,
      vy: (Math.random() - 0.5) * 10,
      size: Math.random() * 6 + 2,
      color, life: 1.0
    });
  }
}

let makimaEffects = [];
function triggerMakimaSqueezeEffect(target) {
  makimaEffects.push({ x: target.x + 20, y: target.y + 35, size: 140, alpha: 1.0 });
}

let player1, player2;

function updatePreview(playerKey) {
  const selectEl = document.getElementById(playerKey + '-select');
  const previewEl = document.getElementById(playerKey + '-preview');
  previewEl.style.backgroundImage = `url('${CHAR_IMAGES[selectEl.value]}')`;
}

function initGame() {
  const p1Char = document.getElementById('p1-select').value;
  const p2Char = document.getElementById('p2-select').value;

  document.getElementById('p1-name').innerText = `1P: ${p1Char.toUpperCase()}`;
  document.getElementById('p2-name').innerText = `2P: ${p2Char.toUpperCase()}`;

  player1 = new Fighter({ x: 150, y: 200, isP2: false, character: p1Char });
  player2 = new Fighter({ x: 610, y: 200, isP2: true, character: p2Char });
}

function startGame() {
  p1Score = 0; p2Score = 0; gameOver = false;
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

  // 궁극기 게이지 업데이트
  document.getElementById('p1-ult').style.width = player1.ultGauge + '%';
  document.getElementById('p2-ult').style.width = player2.ultGauge + '%';
  document.getElementById('p1-ult-text').innerText = player1.ultGauge >= 100 ? 'ULT READY! (E)' : `ULT: ${player1.ultGauge}%`;
  document.getElementById('p2-ult-text').innerText = player2.ultGauge >= 100 ? 'ULT READY! (O)' : `ULT: ${player2.ultGauge}%`;

  document.getElementById('score').innerText = `${p1Score} - ${p2Score}`;
}

function gameLoop() {
  if (gameOver) return;

  ctx.save();
  if (screenShake > 0) {
    ctx.translate((Math.random() - 0.5) * screenShake, (Math.random() - 0.5) * screenShake);
    screenShake--;
  }

  ctx.fillStyle = '#11091c'; ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  ctx.fillStyle = '#ff0055'; ctx.fillRect(0, GROUND_Y, CANVAS_WIDTH, CANVAS_HEIGHT - GROUND_Y);

  handleInput();
  player1.update(player2);
  player2.update(player1);

  // 잔상 렌더링
  afterImages.forEach((img, idx) => {
    ctx.globalAlpha = img.alpha;
    ctx.fillStyle = img.color;
    ctx.fillRect(img.x, img.y, img.width, img.height);
    img.alpha -= 0.08;
    if (img.alpha <= 0) afterImages.splice(idx, 1);
  });
  ctx.globalAlpha = 1.0;

  player1.draw();
  player2.draw();

  // 파티클 연출
  particles.forEach((p, idx) => {
    ctx.fillStyle = p.color;
    ctx.fillRect(p.x, p.y, p.size, p.size);
    p.x += p.vx; p.y += p.vy; p.life -= 0.04;
    if (p.life <= 0) particles.splice(idx, 1);
  });

  // 마키마 압착 연출
  makimaEffects.forEach((eff, idx) => {
    ctx.fillStyle = `rgba(255, 0, 55, ${eff.alpha})`;
    ctx.beginPath(); ctx.arc(eff.x, eff.y, eff.size, 0, Math.PI * 2); ctx.fill();
    eff.alpha -= 0.05;
    if (eff.alpha <= 0) makimaEffects.splice(idx, 1);
  });

  ctx.restore();

  updateHUD();

  if (player1.hp <= 0 || player2.hp <= 0) {
    if (player1.hp <= 0) p2Score++;
    else if (player2.hp <= 0) p1Score++;

    if (p1Score === 2 || p2Score === 2) {
      gameOver = true;
      document.getElementById('winner-text').innerText = `${p1Score === 2 ? '1P' : '2P'} 최종 승리!`;
      document.getElementById('game-over-screen').style.display = 'flex';
    } else {
      resetRound();
    }
  }

  requestAnimationFrame(gameLoop);
}
</script>
</body>
</html>
"""

components.html(game_html, height=500, scrolling=False)
