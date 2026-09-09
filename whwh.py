import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨 하이브리드 - BGM 포함", layout="wide")

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>체인소맨 하이브리드 - BGM 포함</title>
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
    canvas { display: block; image-rendering: pixelated; }

    #start-screen {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 20;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      background: rgba(0, 0, 0, 0.5);
    }
    #video-background {
      position: absolute; top: 50%; left: 50%; width: 100%; height: 100%;
      transform: translate(-50%, -50%); z-index: 1; pointer-events: auto;
      filter: brightness(0.7) contrast(1.1); object-fit: cover;
    }
    .title { 
      position: relative; z-index: 2; font-size: 38px; color: #fff; margin-bottom: 10px; 
      text-shadow: 3px 3px 0px #ff0055, -3px -3px 0px #00e5ff; font-weight: 900; font-style: italic;
    }
    .sound-btn {
      position: absolute; top: 15px; right: 15px; z-index: 25;
      padding: 8px 16px; font-size: 14px; font-weight: bold; color: #fff;
      background: rgba(0, 0, 0, 0.7); border: 2px solid #ff0055; border-radius: 20px;
      cursor: pointer; transition: all 0.2s; box-shadow: 0 0 10px rgba(255, 0, 85, 0.5);
    }
    .sound-btn:hover { background: #ff0055; color: #fff; }

    .start-btn {
      position: relative; z-index: 2; padding: 14px 40px; font-size: 22px; font-weight: bold;
      color: #fff; background: linear-gradient(45deg, #ff0055, #ff5500);
      border: 3px solid #fff; border-radius: 6px; cursor: pointer;
      box-shadow: 0 0 25px rgba(255, 0, 85, 0.8); transition: all 0.2s;
    }
    .start-btn:hover { transform: scale(1.08); background: linear-gradient(45deg, #fff, #ff0055); color: #ff0055; }

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
    .player-name { font-weight: 900; font-size: 13px; text-shadow: 0 0 8px #ff0055; }
    .ult-text { font-size: 10px; font-weight: bold; color: #00e5ff; }

    .overlay {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(5, 5, 5, 0.94); display: flex; flex-direction: column;
      align-items: center; justify-content: center; pointer-events: auto; z-index: 10;
    }
    .select-box { display: flex; gap: 20px; margin-bottom: 12px; }
    .player-select-panel {
      display: flex; flex-direction: column; align-items: center; gap: 6px;
      background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; border: 1px solid #333;
    }
    .char-preview-canvas {
      width: 100px; height: 110px; border: 2px solid #ff0055; border-radius: 6px;
      background-color: #050508;
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

    #makima-cutscene {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.95); display: none;
      flex-direction: column; align-items: center; justify-content: center;
      z-index: 15; pointer-events: none;
    }
    #makima-cutscene .text { font-size: 24px; font-weight: 900; color: #ff0055; text-shadow: 0 0 15px #ff0055; font-style: italic; }
  </style>
</head>
<body>

<div id="game-container">
  <button id="sound-btn" class="sound-btn" onclick="toggleAudio()">🔊 BGM 켜기</button>

  <div id="start-screen">
    <!-- 유튜브 플레이어 iframe (YouTube API 연동) -->
    <iframe id="video-background" 
      src="https://www.youtube.com/embed/l9E-dh9kf_0?enablejsapi=1&autoplay=1&mute=0&controls=0&loop=1&playlist=l9E-dh9kf_0" 
      frameborder="0" allow="autoplay; encrypted-media">
    </iframe>
    <h1 class="title">CHAINSAW HYBRID</h1>
    <button class="start-btn" onclick="enterCharSelect()">GAME START</button>
  </div>

  <canvas id="gameCanvas" width="800" height="450"></canvas>

  <div id="makima-cutscene">
    <div class="text">"이름을 복창해라... (압착)"</div>
  </div>

  <div class="ui-layer">
    <div class="hud">
      <div>
        <div id="p1-name" class="player-name">1P: 덴지 (체인소 악마)</div>
        <div class="bar-container"><div id="p1-health" class="health-bar"></div></div>
        <div class="bar-container"><div id="p1-ult" class="ult-bar"></div></div>
        <div id="p1-ult-text" class="ult-text">ULT: 0%</div>
      </div>
      <div id="score" style="font-size:26px; font-weight:900; color:#ffcc00;">0 - 0</div>
      <div style="text-align: right;">
        <div id="p2-name" class="player-name">2P: 마키마</div>
        <div class="bar-container"><div id="p2-health" class="health-bar" style="float:right;"></div></div>
        <div class="bar-container"><div id="p2-ult" class="ult-bar" style="float:right;"></div></div>
        <div id="p2-ult-text" class="ult-text">ULT: 0%</div>
      </div>
    </div>
  </div>

  <div id="select-screen" class="overlay" style="display: none;">
    <h1 class="title" style="font-size:32px;">캐릭터 선택</h1>
    <div class="select-box">
      <div class="player-select-panel">
        <label style="font-weight:bold; color:#ff0055;">1P 캐릭터</label>
        <canvas id="p1-prev-cv" class="char-preview-canvas" width="100" height="110"></canvas>
        <select id="p1-select" onchange="updatePreview('p1')">
          <option value="denji">덴지 (체인소 악마)</option>
          <option value="aki">하야카와 아키</option>
          <option value="makima">마키마 (신사 의식)</option>
          <option value="power">파워 (피의 악마)</option>
        </select>
      </div>
      <div class="player-select-panel">
        <label style="font-weight:bold; color:#0088ff;">2P 캐릭터</label>
        <canvas id="p2-prev-cv" class="char-preview-canvas" width="100" height="110"></canvas>
        <select id="p2-select" onchange="updatePreview('p2')">
          <option value="makima">마키마 (신사 의식)</option>
          <option value="denji">덴지 (체인소 악마)</option>
          <option value="aki">하야카와 아키</option>
          <option value="power">파워 (피의 악마)</option>
        </select>
      </div>
    </div>
    <button class="game-btn" onclick="startGame()">전투 시작!</button>
    <div style="margin-top:8px; font-size:11px; color:#aaa; text-align:center;">
      [1P] A/D:이동 | W:점프 | F:일반공격 | Z:스킬1 | X:스킬2 | C:사슬포획 | E:궁극기<br>
      [2P] 방향키:이동 | Up:점프 | K:일반공격 | J:스킬1 | I:스킬2 | U:사슬포획 | O:궁극기
    </div>
  </div>

  <div id="game-over-screen" class="overlay" style="display: none;">
    <h1 id="winner-text" class="title">1P 최종 승리!</h1>
    <button class="game-btn" onclick="resetFullGame()">처음으로 돌아가기</button>
  </div>
</div>

<script>
// YouTube API 제어 연동
let ytPlayer = null;
let isMuted = true;

const tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
const firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onYouTubeIframeAPIReady() {
  ytPlayer = new YT.Player('video-background', {
    events: {
      'onReady': (e) => {
        e.target.unMute();
        e.target.setVolume(80);
        e.target.playVideo();
      }
    }
  });
}

function toggleAudio() {
  const btn = document.getElementById('sound-btn');
  if (ytPlayer && ytPlayer.unMute) {
    if (isMuted) {
      ytPlayer.unMute();
      ytPlayer.setVolume(80);
      ytPlayer.playVideo();
      btn.innerText = "🔇 BGM 끄기";
      isMuted = false;
    } else {
      ytPlayer.mute();
      btn.innerText = "🔊 BGM 켜기";
      isMuted = true;
    }
  }
}

function enterCharSelect() {
  // 사용자가 GAME START를 누를 때 소리 락을 풀어 즉시 재생
  if (ytPlayer && ytPlayer.unMute) {
    ytPlayer.unMute();
    ytPlayer.setVolume(80);
    ytPlayer.playVideo();
    document.getElementById('sound-btn').innerText = "🔇 BGM 끄기";
    isMuted = false;
  }
  document.getElementById('start-screen').style.display = 'none';
  document.getElementById('select-screen').style.display = 'flex';
  updatePreview('p1');
  updatePreview('p2');
}

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const GRAVITY = 0.65;
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 450;
const GROUND_Y = 380;

let p1Score = 0, p2Score = 0;
let gameOver = false;
let screenShake = 0;
let particles = [];
let afterImages = [];
let activeChains = [];

const keys = {};
window.addEventListener('keydown', e => { keys[e.key] = true; });
window.addEventListener('keyup', e => { keys[e.key] = false; });

function renderPixelChar(targetCtx, charType, width, height) {
  targetCtx.save();

  if (charType === 'denji') {
    targetCtx.fillStyle = '#ff3300';
    targetCtx.fillRect(-width/2 + 10, -height/2 + 10, width - 20, 20);
    
    targetCtx.fillStyle = '#cccccc';
    targetCtx.fillRect(-width/2 + 22, -height/2 - 25, 16, 35);
    targetCtx.fillStyle = '#ff0000';
    targetCtx.fillRect(-width/2 + 24, -height/2 - 20, 12, 10);

    targetCtx.fillStyle = '#ffffff'; targetCtx.fillRect(-width/2 + 12, -height/2 + 30, width - 24, 25);
    targetCtx.fillStyle = '#222222'; targetCtx.fillRect(-width/2 + 12, -height/2 + 55, width - 24, 30);

    targetCtx.fillStyle = '#aaaaaa';
    targetCtx.fillRect(width/2 - 12, -height/2 + 20, 10, 45);
    targetCtx.fillRect(-width/2 + 2, -height/2 + 20, 10, 45);
  } else if (charType === 'makima') {
    targetCtx.fillStyle = '#e65c00';
    targetCtx.fillRect(-width/2 + 12, -height/2 + 5, width - 24, 25);
    targetCtx.fillStyle = '#ffdbac';
    targetCtx.fillRect(-width/2 + 16, -height/2 + 18, width - 32, 12);
    targetCtx.fillStyle = '#111115';
    targetCtx.fillRect(-width/2 + 10, -height/2 + 30, width - 20, 55);
    targetCtx.fillStyle = '#800000';
    targetCtx.fillRect(-2, -height/2 + 30, 4, 20);
  } else if (charType === 'power') {
    targetCtx.fillStyle = '#ffcc00';
    targetCtx.fillRect(-width/2 + 8, -height/2 + 5, width - 16, 30);
    targetCtx.fillStyle = '#ff0000';
    targetCtx.fillRect(-12, -height/2 - 5, 6, 12); targetCtx.fillRect(6, -height/2 - 5, 6, 12);
    targetCtx.fillStyle = '#003366';
    targetCtx.fillRect(-width/2 + 10, -height/2 + 35, width - 20, 50);
  } else {
    targetCtx.fillStyle = '#0f172a';
    targetCtx.fillRect(-width/2 + 12, -height/2 + 5, width - 24, 25);
    targetCtx.fillRect(-4, -height/2 - 8, 8, 10);
    targetCtx.fillStyle = '#1e293b';
    targetCtx.fillRect(-width/2 + 10, -height/2 + 30, width - 20, 55);
  }

  targetCtx.restore();
}

class Fighter {
  constructor({ x, y, isP2, character }) {
    this.x = x; this.y = y;
    this.width = 60; this.height = 90;
    this.isP2 = isP2;
    this.character = character;
    this.facing = isP2 ? 'left' : 'right';

    this.vx = 0; this.vy = 0;
    this.speed = 5.5; this.jumpPower = -13.5;
    this.hp = 100;
    this.ultGauge = 0;
    this.isGrounded = false;

    this.isAttacking = false;
    this.attackBox = { width: 55, height: 45 };
    
    this.cdSkill1 = false;
    this.cdSkill2 = false;
    this.cdSkill3 = false;
  }

  reset(x) {
    this.x = x; this.y = GROUND_Y - this.height;
    this.vx = 0; this.vy = 0;
    this.hp = 100; this.ultGauge = 0;
    this.isAttacking = false;
    this.facing = this.isP2 ? 'left' : 'right';
    this.cdSkill1 = false; this.cdSkill2 = false; this.cdSkill3 = false;
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

    if (Math.abs(this.vx) > 0 && Math.random() < 0.3) {
      afterImages.push({
        x: this.x, y: this.y, width: this.width, height: this.height,
        facing: this.facing, character: this.character, alpha: 0.4
      });
    }

    if (this.isAttacking) {
      const atkX = this.facing === 'right' ? this.x + this.width : this.x - this.attackBox.width;
      const atkY = this.y + 10;

      if (
        atkX < enemy.x + enemy.width &&
        atkX + this.attackBox.width > enemy.x &&
        atkY < enemy.y + enemy.height &&
        atkY + this.attackBox.height > enemy.y
      ) {
        enemy.takeDamage(7);
        this.ultGauge = Math.min(100, this.ultGauge + 12);
        createParticles(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2, '#ff0055', 10);
        screenShake = 5;
        this.isAttacking = false;
      }
    }
  }

  draw() {
    ctx.save();
    ctx.translate(this.x + this.width / 2, this.y + this.height / 2);

    if (this.facing === 'left') {
      ctx.scale(-1, 1);
    }

    renderPixelChar(ctx, this.character, this.width, this.height);
    ctx.restore();

    if (this.isAttacking) {
      ctx.fillStyle = 'rgba(255, 0, 85, 0.5)';
      const atkX = this.facing === 'right' ? this.x + this.width : this.x - this.attackBox.width;
      ctx.fillRect(atkX, this.y + 10, this.attackBox.width, this.attackBox.height);
    }
  }

  attack() {
    if (this.isAttacking) return;
    this.isAttacking = true;
    setTimeout(() => { this.isAttacking = false; }, 120);
  }

  useSkill1(enemy) {
    if (this.cdSkill1) return;
    this.cdSkill1 = true;

    const dir = this.facing === 'right' ? 1 : -1;
    createParticles(this.x + this.width/2 + (dir * 40), this.y + 30, '#ff5500', 25);

    const hitRange = 90;
    if (Math.abs(this.x - enemy.x) < hitRange && Math.abs(this.y - enemy.y) < 60) {
      enemy.takeDamage(16);
      this.ultGauge = Math.min(100, this.ultGauge + 20);
      screenShake = 12;
    }

    setTimeout(() => { this.cdSkill1 = false; }, 3000);
  }

  useSkill2(enemy) {
    if (this.cdSkill2) return;
    this.cdSkill2 = true;

    const dir = this.facing === 'right' ? 1 : -1;
    this.vx = dir * 18;
    createParticles(this.x + this.width/2, this.y + this.height - 10, '#00e5ff', 20);

    setTimeout(() => {
      if (Math.abs(this.x - enemy.x) < 70 && Math.abs(this.y - enemy.y) < 60) {
        enemy.takeDamage(18);
        this.ultGauge = Math.min(100, this.ultGauge + 20);
        screenShake = 10;
      }
    }, 100);

    setTimeout(() => { this.cdSkill2 = false; }, 4000);
  }

  useSkill3(enemy) {
    if (this.cdSkill3) return;
    this.cdSkill3 = true;

    const startX = this.x + this.width / 2;
    const startY = this.y + 30;
    const targetX = enemy.x + enemy.width / 2;

    activeChains.push({
      x1: startX, y1: startY,
      x2: targetX, y2: startY,
      life: 1.0
    });

    if (Math.abs(startX - targetX) < 380) {
      enemy.x = this.facing === 'right' ? this.x + 50 : this.x - 50;
      enemy.takeDamage(10);
      this.ultGauge = Math.min(100, this.ultGauge + 15);
      screenShake = 8;
      createParticles(enemy.x + enemy.width/2, enemy.y + 30, '#ffffff', 20);
    }

    setTimeout(() => { this.cdSkill3 = false; }, 6000);
  }

  useUltimate(enemy) {
    if (this.ultGauge < 100) return;
    this.ultGauge = 0;

    if (this.character === 'makima') {
      const cutsceneEl = document.getElementById('makima-cutscene');
      cutsceneEl.style.display = 'flex';
      setTimeout(() => {
        cutsceneEl.style.display = 'none';
        triggerMakimaSqueezeEffect(enemy);
        enemy.takeDamage(50);
        screenShake = 25;
      }, 1200);
    } else {
      const dir = this.facing === 'right' ? 1 : -1;
      this.vx = dir * 25;
      createParticles(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2, '#ff0055', 80);
      createParticles(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2, '#ffcc00', 60);
      enemy.takeDamage(45);
      screenShake = 25;
    }
  }

  takeDamage(amount) {
    this.hp = Math.max(0, this.hp - amount);
  }
}

function createParticles(x, y, color, count) {
  for (let i = 0; i < count; i++) {
    particles.push({
      x, y,
      vx: (Math.random() - 0.5) * 12,
      vy: (Math.random() - 0.5) * 12,
      size: Math.random() * 6 + 2,
      color, life: 1.0
    });
  }
}

let makimaEffects = [];
function triggerMakimaSqueezeEffect(target) {
  makimaEffects.push({ x: target.x + target.width / 2, y: target.y + target.height / 2, size: 150, alpha: 1.0 });
}

let player1, player2;

function updatePreview(playerKey) {
  const selectEl = document.getElementById(playerKey + '-select');
  const cv = document.getElementById(playerKey + '-prev-cv');
  const pCtx = cv.getContext('2d');
  
  pCtx.clearRect(0, 0, cv.width, cv.height);
  pCtx.save();
  pCtx.translate(cv.width / 2, cv.height / 2 + 5);
  renderPixelChar(pCtx, selectEl.value, 50, 75);
  pCtx.restore();
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
  if (keys['z'] || keys['Z']) player1.useSkill1(player2);
  if (keys['x'] || keys['X']) player1.useSkill2(player2);
  if (keys['c'] || keys['C']) player1.useSkill3(player2);
  if (keys['e'] || keys['E']) player1.useUltimate(player2);

  player2.vx = 0;
  if (keys['ArrowLeft']) player2.vx = -player2.speed;
  if (keys['ArrowRight']) player2.vx = player2.speed;
  if (keys['ArrowUp'] && player2.isGrounded) player2.vy = player2.jumpPower;
  if (keys['k'] || keys['K']) player2.attack();
  if (keys['j'] || keys['J']) player2.useSkill1(player1);
  if (keys['i'] || keys['I']) player2.useSkill2(player1);
  if (keys['u'] || keys['U']) player2.useSkill3(player1);
  if (keys['o'] || keys['O']) player2.useUltimate(player1);
}

function updateHUD() {
  document.getElementById('p1-health').style.width = player1.hp + '%';
  document.getElementById('p2-health').style.width = player2.hp + '%';

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

  afterImages.forEach((img, idx) => {
    ctx.save();
    ctx.globalAlpha = img.alpha;
    ctx.translate(img.x + img.width / 2, img.y + img.height / 2);
    if (img.facing === 'left') ctx.scale(-1, 1);

    renderPixelChar(ctx, img.character, img.width, img.height);
    ctx.restore();

    img.alpha -= 0.08;
    if (img.alpha <= 0) afterImages.splice(idx, 1);
  });
  ctx.globalAlpha = 1.0;

  player1.draw();
  player2.draw();

  activeChains.forEach((chain, idx) => {
    ctx.strokeStyle = '#ff0055';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(chain.x1, chain.y1);
    ctx.lineTo(chain.x2, chain.y2);
    ctx.stroke();
    chain.life -= 0.1;
    if (chain.life <= 0) activeChains.splice(idx, 1);
  });

  particles.forEach((p, idx) => {
    ctx.fillStyle = p.color;
    ctx.fillRect(p.x, p.y, p.size, p.size);
    p.x += p.vx; p.y += p.vy; p.life -= 0.04;
    if (p.life <= 0) particles.splice(idx, 1);
  });

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
