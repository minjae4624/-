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
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #050505; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #fff; user-select: none; }
        #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; display: flex; justify-content: center; align-items: center; }
        canvas { background: #000; image-rendering: pixelated; border: 4px solid #ff0055; box-shadow: 0 0 35px rgba(255,0,85,0.4); }

        .ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; display: flex; flex-direction: column; justify-content: space-between; }
        .interactive { pointer-events: auto; }

        /* HUD */
        #hud { display: none; padding: 20px 40px; justify-content: space-between; align-items: flex-start; }
        .player-hud { width: 40%; }
        .p2-hud { text-align: right; }
        .name { font-size: 26px; font-weight: 900; text-shadow: 0 0 12px #ff0055; margin-bottom: 5px; font-style: italic; }
        .bar-bg { width: 100%; height: 22px; background: #111; border: 2px solid #fff; border-radius: 4px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.8); }
        .hp-bar { height: 100%; background: linear-gradient(90deg, #ff0055, #ff5500); width: 100%; transition: width 0.1s linear; }
        .ult-bar-bg { width: 100%; height: 10px; background: #111; border: 1px solid #666; margin-top: 4px; border-radius: 2px; overflow: hidden; }
        .ult-bar { height: 100%; background: linear-gradient(90deg, #00ffff, #0088ff); width: 0%; transition: width 0.2s linear; }
        .transform-badge { font-size: 13px; color: #00ffcc; font-weight: bold; display: none; margin-top: 3px; text-shadow: 0 0 8px #00ffcc; }

        /* 조작 패널 */
        #touch-controls { display: none; position: absolute; bottom: 15px; width: 100%; padding: 0 20px; box-sizing: border-box; justify-content: space-between; z-index: 20; }
        .panel { background: rgba(0,0,0,0.85); border: 2px solid #333; border-radius: 12px; padding: 8px; display: flex; gap: 6px; backdrop-filter: blur(5px); }
        .ctrl-btn { width: 48px; height: 48px; background: #1a1a1a; border: 2px solid #fff; border-radius: 6px; color: #fff; font-size: 11px; font-weight: bold; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; transition: 0.1s; }
        .ctrl-btn:active { background: #ff0033; transform: scale(0.95); }
        .jump-btn { border-color: #ffcc00; color: #ffcc00; }
        .trans-btn { border-color: #00ffcc; color: #00ffcc; }
        .ult-btn { border-color: #ff0055; background: rgba(255,0,85,0.4); }

        /* 화면 선택 메뉴 */
        .screen { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(5,5,5,0.92); }
        h1 { font-size: 52px; color: #ff0033; text-shadow: 0 0 25px #ff0033; margin-bottom: 5px; font-style: italic; letter-spacing: -2px; }
        .btn { padding: 12px 35px; font-size: 20px; font-weight: bold; background: #ff0033; color: #fff; border: none; cursor: pointer; border-radius: 5px; box-shadow: 0 0 20px #ff0033; margin: 10px; transition: 0.2s; }
        .btn:hover { background: #fff; color: #ff0033; transform: scale(1.05); }

        .select-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; max-width: 850px; margin-bottom: 15px; }
        .card { width: 105px; height: 145px; border: 3px solid #333; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; cursor: pointer; background-size: cover; background-position: center; position: relative; overflow: hidden; transition: 0.2s; }
        .card .card-info { width: 100%; background: rgba(0,0,0,0.85); text-align: center; padding: 4px 0; border-top: 1px solid #444; }
        .card.selected-p1 { border-color: #ff0055; box-shadow: 0 0 20px #ff0055; transform: scale(1.08); z-index: 2; }
        .card.selected-p2 { border-color: #0088ff; box-shadow: 0 0 20px #0088ff; transform: scale(1.08); z-index: 2; }
        .card h3 { font-size: 13px; margin: 0; color: #fff; font-weight: 800; }
        .card p { font-size: 9px; color: #ffcc00; margin: 1px 0 0 0; }

        /* 애니메이션 연출 컷씬 */
        #cutscene { display: none; position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 100; justify-content: center; align-items: center; flex-direction: column; overflow: hidden; }
        #cutscene-img { width: 340px; height: 340px; border-radius: 12px; border: 5px solid #ff0033; box-shadow: 0 0 80px #ff0033; background-size: cover; background-position: center; animation: animeZoom 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        #cutscene-text { font-size: 38px; color: #ff0033; font-weight: 900; text-shadow: 0 0 40px #ff0033; margin-top: 25px; font-style: italic; animation: textPulse 0.3s infinite alternate; text-align: center; }
        @keyframes animeZoom { from { transform: scale(0.2) rotate(-5deg); opacity: 0; } to { transform: scale(1) rotate(0deg); opacity: 1; } }
        @keyframes textPulse { from { transform: scale(1); } to { transform: scale(1.1); } }
    </style>
</head>
<body>

    <div id="canvas-container">
        <canvas id="gameCanvas" width="960" height="540"></canvas>
    </div>

    <div class="ui-layer">
        <div id="hud" class="interactive">
            <div class="player-hud p1-hud">
                <div id="p1-name" class="name">덴지</div>
                <div class="bar-bg"><div id="p1-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p1-ult" class="ult-bar"></div></div>
                <div id="p1-trans" class="transform-badge">MODE ACTIVE</div>
            </div>
            <div style="font-size: 32px; font-weight: 900; color: #fff; font-style: italic; text-shadow: 0 0 10px #ff0055;">VS</div>
            <div class="player-hud p2-hud">
                <div id="p2-name" class="name">아키</div>
                <div class="bar-bg"><div id="p2-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p2-ult" class="ult-bar"></div></div>
                <div id="p2-trans" class="transform-badge">MODE ACTIVE</div>
            </div>
        </div>

        <div id="main-screen" class="screen interactive">
            <h1>체인소맨 하이브리드</h1>
            <p style="color:#aaa; margin-bottom: 25px;">공안 대마 특이 4과 대전 격투</p>
            <button class="btn" onclick="goToModeSelect()">게임 시작</button>
        </div>

        <div id="mode-screen" class="screen interactive" style="display:none;">
            <h1>모드 선택</h1>
            <div>
                <button class="btn" onclick="selectMode('1P')">1인용 (VS AI)</button>
                <button class="btn" onclick="selectMode('2P')">2인용 (P1 vs P2)</button>
            </div>
        </div>

        <div id="select-screen" class="screen interactive" style="display:none;">
            <h2 style="margin:0 0 10px 0;">캐릭터 선택 (1P: 붉은색 / 2P: 푸른색)</h2>
            <div class="select-grid" id="char-grid"></div>

            <h2 style="margin:10px 0 5px 0;">전장 맵 선택</h2>
            <div style="display:flex; gap:15px; margin-bottom: 15px;">
                <div class="card selected-p1" id="m-city" onclick="pickMap('city')" style="width:110px; height:60px; background:#222; justify-content:center;"><h3>도쿄 옥상</h3></div>
                <div class="card" id="m-hell" onclick="pickMap('hell')" style="width:110px; height:60px; background:#400; justify-content:center;"><h3>악마의 지옥</h3></div>
                <div class="card" id="m-beach" onclick="pickMap('beach')" style="width:110px; height:60px; background:#004; justify-content:center;"><h3>신소 해변</h3></div>
            </div>

            <button class="btn" onclick="startGame()">전투 시작!</button>
        </div>
    </div>

    <div id="touch-controls" class="interactive">
        <div class="panel">
            <div class="ctrl-btn" onclick="triggerAction('P1','LEFT')">&#9664;<br>(A)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','RIGHT')">&#9654;<br>(D)</div>
            <div class="ctrl-btn jump-btn" onclick="triggerAction('P1','JUMP')">점프<br>(W)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','SKILL_A')">스킬1<br>(F)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','SKILL_B')">스킬2<br>(G)</div>
            <div class="ctrl-btn trans-btn" onclick="triggerAction('P1','TRANS')">변신/발동<br>(V)</div>
            <div class="ctrl-btn ult-btn" onclick="triggerAction('P1','ULT')">궁극기<br>(H)</div>
        </div>
        <div class="panel">
            <div class="ctrl-btn" onclick="triggerAction('P2','LEFT')">&#9664;<br>(&#8592;)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','RIGHT')">&#9654;<br>(&#8594;)</div>
            <div class="ctrl-btn jump-btn" onclick="triggerAction('P2','JUMP')">점프<br>(&#8593;)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','SKILL_A')">스킬1<br>(1)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','SKILL_B')">스킬2<br>(2)</div>
            <div class="ctrl-btn trans-btn" onclick="triggerAction('P2','TRANS')">변신/발동<br>(0)</div>
            <div class="ctrl-btn ult-btn" onclick="triggerAction('P2','ULT')">궁극기<br>(3)</div>
        </div>
    </div>

    <div id="cutscene">
        <div id="cutscene-img"></div>
        <div id="cutscene-text">필살 일격!</div>
    </div>

    <script>
        const CHARACTERS = {
            denji: { 
                name: '덴지', hair: '#f5d442', shirt: '#ffffff', pants: '#1a1a1a', isHybrid: true, 
                img: 'https://images.justwatch.com/poster/301548683/s718/chainsaw-man.jpg', 
                ultImg: 'https://m.media-amazon.com/images/M/MV5BODA0ZWY2NDgtYTFkMi00ZDkyLWE3MGEtNTlhY2JkNWU0MTUxXkEyXkFqcGc@._V1_.jpg',
                type: '체인소의 악마 하이브리드' 
            },
            aki: { 
                name: '하야카와 아키', hair: '#0a1128', shirt: '#151515', pants: '#151515', isHybrid: false, 
                img: 'https://static.wikia.nocookie.net/chainsaw-man/images/b/b3/Aki_Hayakawa_anime_design.png', 
                ultImg: 'https://static.wikia.nocookie.net/chainsaw-man/images/b/b3/Aki_Hayakawa_anime_design.png',
                type: '여우 & 커스 악마 계약' 
            },
            power: { 
                name: '파워', hair: '#e0a367', shirt: '#aa2222', pants: '#111122', isHybrid: false, 
                img: 'https://m.media-amazon.com/images/M/MV5BNTBmNTI2ZDQtNWFlNy00ZjgwLWIzY2ItYzA3Nzc0YTY1ZmMyXkEyXkFqcGc@._V1_.jpg', 
                ultImg: 'https://i.pinimg.com/736x/8f/58/09/8f5809ce86e6eb1f7b78fb7b796d1945.jpg',
                type: '혈액의 악마 마인' 
            },
            makima: { 
                name: '마키마', hair: '#d66347', shirt: '#ffffff', pants: '#111111', isHybrid: false, 
                img: 'https://static.wikia.nocookie.net/chainsaw-man/images/d/d3/Makima_anime_design.png', 
                ultImg: 'https://static.wikia.nocookie.net/chainsaw-man/images/d/d3/Makima_anime_design.png',
                type: '지배의 악마' 
            },
            reze: { 
                name: '레제', hair: '#3f3254', shirt: '#ffffff', pants: '#222233', isHybrid: true, 
                img: 'https://static.wikia.nocookie.net/chainsaw-man/images/3/36/Reze_anime_design.png', 
                ultImg: 'https://static.wikia.nocookie.net/chainsaw-man/images/3/36/Reze_anime_design.png',
                type: '폭탄의 악마 하이브리드' 
            }
        };

        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const GROUND_Y = 400;
        const GRAVITY = 0.65;

        let gameMode = '1P';
        let selectedCharP1 = 'denji', selectedCharP2 = 'aki', selectedMap = 'city';
        let isGaming = false, isCutscene = false;
        let effects = [];
        let globalTick = 0;

        function createPlayer(charKey, xPos, isAI, facingRight) {
            const data = CHARACTERS[charKey];
            return {
                key: charKey, name: data.name, data: data,
                isTransformed: false, hp: 100, ult: 0,
                x: xPos, y: GROUND_Y, vx: 0, vy: 0,
                isGrounded: true, facingRight: facingRight,
                isAttacking: false, attackType: null, isAI: isAI, img: data.img, ultImg: data.ultImg
            };
        }

        let P1, P2;
        const keysPressed = {};

        window.addEventListener('keydown', (e) => { 
            keysPressed[e.key.toLowerCase()] = true; 
            if (e.key === 'ArrowUp') keysPressed['arrowup'] = true;
            if (e.key === 'ArrowLeft') keysPressed['arrowleft'] = true;
            if (e.key === 'ArrowRight') keysPressed['arrowright'] = true;
        });
        window.addEventListener('keyup', (e) => { 
            keysPressed[e.key.toLowerCase()] = false; 
            if (e.key === 'ArrowUp') keysPressed['arrowup'] = false;
            if (e.key === 'ArrowLeft') keysPressed['arrowleft'] = false;
            if (e.key === 'ArrowRight') keysPressed['arrowright'] = false;
        });

        function triggerAction(p, act) {
            if (!isGaming || isCutscene) return;
            const target = (p === 'P1') ? P1 : P2;
            const enemy = (p === 'P1') ? P2 : P1;

            if (act === 'JUMP') playerJump(target);
            if (act === 'SKILL_A') executeSkill(target, enemy, 'SKILL_A', 8, 14);
            if (act === 'SKILL_B') executeSkill(target, enemy, 'SKILL_B', 14, 20);
            if (act === 'TRANS') transformPlayer(target);
            if (act === 'ULT') executeUltimate(target, enemy);
        }

        function playerJump(player) {
            if (player.isGrounded) {
                player.vy = -13.5;
                player.isGrounded = false;
            }
        }

        function renderCharCards() {
            const grid = document.getElementById('char-grid');
            grid.innerHTML = '';
            Object.keys(CHARACTERS).forEach(key => {
                const c = CHARACTERS[key];
                const card = document.createElement('div');
                let selClass = '';
                if (key === selectedCharP1) selClass = 'selected-p1';
                else if (key === selectedCharP2) selClass = 'selected-p2';

                card.className = 'card ' + selClass;
                card.style.backgroundImage = "url('" + c.img + "')";
                card.onclick = function() { pickChar(key); };
                card.innerHTML = '<div class="card-info"><h3>' + c.name + '</h3><p>' + c.type + '</p></div>';
                grid.appendChild(card);
            });
        }

        function goToModeSelect() { document.getElementById('main-screen').style.display = 'none'; document.getElementById('mode-screen').style.display = 'flex'; }
        function selectMode(mode) { gameMode = mode; renderCharCards(); document.getElementById('mode-screen').style.display = 'none'; document.getElementById('select-screen').style.display = 'flex'; }
        
        function pickChar(char) {
            if (selectedCharP1 !== char) selectedCharP1 = char;
            else {
                const keys = Object.keys(CHARACTERS);
                selectedCharP2 = keys[(keys.indexOf(char) + 1) % keys.length];
            }
            renderCharCards();
        }

        function pickMap(map) {
            selectedMap = map;
            document.getElementById('m-city').className = 'card ' + (map === 'city' ? 'selected-p1' : '');
            document.getElementById('m-hell').className = 'card ' + (map === 'hell' ? 'selected-p1' : '');
            document.getElementById('m-beach').className = 'card ' + (map === 'beach' ? 'selected-p1' : '');
        }

        function startGame() {
            document.getElementById('select-screen').style.display = 'none';
            document.getElementById('hud').style.display = 'flex';
            document.getElementById('touch-controls').style.display = 'flex';

            P1 = createPlayer(selectedCharP1, 200, false, true);
            P2 = createPlayer(selectedCharP2, 700, gameMode === '1P', false);

            document.getElementById('p1-name').innerText = P1.name;
            document.getElementById('p2-name').innerText = P2.name;

            isGaming = true;
            gameLoop();
        }

        function handleInput() {
            if (!isGaming || isCutscene) return;

            P1.vx = 0;
            if (keysPressed['a'] && P1.x > 50) { P1.vx = -(P1.isTransformed ? 7.5 : 5.5); P1.facingRight = false; }
            if (keysPressed['d'] && P1.x < 870) { P1.vx = (P1.isTransformed ? 7.5 : 5.5); P1.facingRight = true; }
            if (keysPressed['w']) playerJump(P1);
            if (keysPressed['f']) executeSkill(P1, P2, 'SKILL_A', 8, 14);
            if (keysPressed['g']) executeSkill(P1, P2, 'SKILL_B', 14, 20);
            if (keysPressed['v']) transformPlayer(P1);
            if (keysPressed['h']) executeUltimate(P1, P2);

            if (!P2.isAI) {
                P2.vx = 0;
                if (keysPressed['arrowleft'] && P2.x > 50) { P2.vx = -(P2.isTransformed ? 7.5 : 5.5); P2.facingRight = false; }
                if (keysPressed['arrowright'] && P2.x < 870) { P2.vx = (P2.isTransformed ? 7.5 : 5.5); P2.facingRight = true; }
                if (keysPressed['arrowup']) playerJump(P2);
                if (keysPressed['1']) executeSkill(P2, P1, 'SKILL_A', 8, 14);
                if (keysPressed['2']) executeSkill(P2, P1, 'SKILL_B', 14, 20);
                if (keysPressed['0']) transformPlayer(P2);
                if (keysPressed['3']) executeUltimate(P2, P1);
            } else {
                updateAI();
            }

            applyPhysics(P1);
            applyPhysics(P2);
        }

        function applyPhysics(player) {
            player.x += player.vx;
            player.y += player.vy;

            if (!player.isGrounded) player.vy += GRAVITY;

            if (player.y >= GROUND_Y) {
                player.y = GROUND_Y;
                player.vy = 0;
                player.isGrounded = true;
            }
        }

        function updateAI() {
            const dist = P1.x - P2.x;
            if (Math.abs(dist) > 90) {
                P2.vx = dist > 0 ? 3.5 : -3.5;
                P2.facingRight = dist > 0;
            } else {
                P2.vx = 0;
                if (Math.random() < 0.04) executeSkill(P2, P1, 'SKILL_A', 8, 14);
                if (Math.random() < 0.02) playerJump(P2);
                if (P2.data.isHybrid && !P2.isTransformed && Math.random() < 0.02) transformPlayer(P2);
                if (P2.ult >= 100) executeUltimate(P2, P1);
            }
        }

        function transformPlayer(player) {
            player.isTransformed = true;
            const badge = (player === P1) ? document.getElementById('p1-trans') : document.getElementById('p2-trans');
            badge.style.display = 'block';
            addEffect(player.x, player.y - 30, player.key === 'aki' ? '#00ffff' : '#ff0033', 60);
        }

        function addEffect(x, y, color, size, isFox) {
            effects.push({ x: x, y: y, color: color, size: size, life: 1.0, isFox: isFox || false });
        }

        function executeSkill(attacker, defender, type, damage, ultGain) {
            if (attacker.isAttacking) return;
            attacker.isAttacking = true;
            attacker.attackType = type;

            const finalDmg = attacker.isTransformed ? damage * 1.5 : damage;

            setTimeout(() => { attacker.isAttacking = false; }, 250);

            if (Math.abs(attacker.x - defender.x) < 120 && Math.abs(attacker.y - defender.y) < 60) {
                defender.hp -= finalDmg;
                attacker.ult = Math.min(100, attacker.ult + ultGain);
                defender.x += attacker.facingRight ? 35 : -35;
                
                if (attacker.key === 'aki') {
                    if (type === 'SKILL_A') {
                        addEffect(defender.x, defender.y - 40, '#e6e6e6', 70, true);
                    } else {
                        addEffect(defender.x, defender.y - 30, '#00ffff', 40);
                    }
                } else {
                    addEffect((attacker.x + defender.x)/2, defender.y - 40, attacker.key === 'denji' ? '#ff3300' : '#ff0033', 45);
                }
                updateHUD();
            }
        }

        function executeUltimate(attacker, defender) {
            if (attacker.ult < 100 || isCutscene) return;
            attacker.ult = 0; isCutscene = true;

            const cutsceneEl = document.getElementById('cutscene');
            document.getElementById('cutscene-img').style.backgroundImage = "url('" + attacker.ultImg + "')";
            
            let ultText = attacker.name + " 필살 일격!";
            if(attacker.key === 'denji') ultText = "덴지: 톱날 엔진 전개! 싹 다 베어버린다!";
            else if(attacker.key === 'aki') ultText = "하야카와 아키: ...'콘(Kon)'. 씹어삼켜라!";
            else if(attacker.key === 'power') ultText = "파워: 이 몸의 위엄에 엎드려라!";
            
            document.getElementById('cutscene-text').innerText = ultText;
            cutsceneEl.style.display = 'flex';

            setTimeout(() => {
                cutsceneEl.style.display = 'none';
                defender.hp -= 48;
                isCutscene = false;
                addEffect(defender.x, defender.y - 50, attacker.key === 'aki' ? '#ffffff' : '#ff0000', 110, attacker.key === 'aki');
                updateHUD();
            }, 2000);
        }

        function updateHUD() {
            document.getElementById('p1-hp').style.width = Math.max(0, P1.hp) + '%';
            document.getElementById('p2-hp').style.width = Math.max(0, P2.hp) + '%';
            document.getElementById('p1-ult').style.width = P1.ult + '%';
            document.getElementById('p2-ult').style.width = P2.ult + '%';
        }

        function drawAkiPixel(p) {
            ctx.save();
            ctx.translate(p.x, p.y);
            if (!p.facingRight) ctx.scale(-1, 1);

            const s = 3;

            if (p.isTransformed) {
                ctx.fillStyle = 'rgba(0, 200, 255, 0.25)';
                ctx.fillRect(-15 * s, -42 * s, 30 * s, 45 * s);
            }

            ctx.fillStyle = '#111115';
            if (!p.isGrounded) {
                ctx.fillRect(-5 * s, -10 * s, 4 * s, 7 * s);
                ctx.fillRect(1 * s, -12 * s, 4 * s, 8 * s);
            } else if (p.vx !== 0) {
                ctx.fillRect(-6 * s, -12 * s, 4 * s, 12 * s);
                ctx.fillRect(2 * s, -12 * s, 4 * s, 12 * s);
            } else {
                ctx.fillRect(-5 * s, -14 * s, 4 * s, 14 * s);
                ctx.fillRect(1 * s, -14 * s, 4 * s, 14 * s);
            }

            ctx.fillStyle = '#000000';
            ctx.fillRect(-5 * s, -2 * s, 5 * s, 2 * s);
            ctx.fillRect(1 * s, -2 * s, 5 * s, 2 * s);

            ctx.fillStyle = '#1a1a22';
            ctx.fillRect(-5 * s, -26 * s, 10 * s, 12 * s);
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(-2 * s, -26 * s, 4 * s, 5 * s);
            ctx.fillStyle = '#000000';
            ctx.fillRect(-1 * s, -25 * s, 2 * s, 7 * s);

            ctx.fillStyle = '#222';
            ctx.fillRect(-7 * s, -34 * s, 3 * s, 20 * s);
            ctx.fillStyle = '#888';
            ctx.fillRect(-8 * s, -36 * s, 5 * s, 2 * s);

            ctx.fillStyle = '#fce4c8';
            ctx.fillRect(-4 * s, -35 * s, 8 * s, 9 * s);

            ctx.fillStyle = '#111';
            ctx.fillRect(1 * s, -32 * s, 3 * s, 1 * s);

            ctx.fillStyle = '#0e182b';
            ctx.fillRect(-5 * s, -39 * s, 10 * s, 5 * s);
            ctx.fillRect(-5 * s, -36 * s, 3 * s, 8 * s);
            ctx.fillRect(-1 * s, -44 * s, 3 * s, 5 * s);
            ctx.fillRect(1 * s, -43 * s, 2 * s, 2 * s);

            ctx.fillStyle = '#1a1a22';
            if (p.isAttacking) {
                ctx.fillRect(3 * s, -26 * s, 13 * s, 4 * s);
                ctx.fillStyle = '#fce4c8';
                ctx.fillRect(14 * s, -28 * s, 4 * s, 3 * s);
            } else {
                ctx.fillRect(-2 * s, -24 * s, 4 * s, 10 * s);
            }

            ctx.restore();
        }

        function drawDenjiPixel(p) {
            ctx.save();
            ctx.translate(p.x, p.y);
            if (!p.facingRight) ctx.scale(-1, 1);

            const s = 3;

            if (p.isTransformed) {
                ctx.fillStyle = 'rgba(255, 50, 0, 0.3)';
                ctx.fillRect(-16 * s, -45 * s, 32 * s, 48 * s);
            }

            ctx.fillStyle = '#1a1a1a';
            if (!p.isGrounded) {
                ctx.fillRect(-5 * s, -10 * s, 4 * s, 7 * s);
                ctx.fillRect(1 * s, -12 * s, 4 * s, 8 * s);
            } else if (p.vx !== 0) {
                ctx.fillRect(-6 * s, -12 * s, 4 * s, 12 * s);
                ctx.fillRect(2 * s, -12 * s, 4 * s, 12 * s);
            } else {
                ctx.fillRect(-5 * s, -14 * s, 4 * s, 14 * s);
                ctx.fillRect(1 * s, -14 * s, 4 * s, 14 * s);
            }

            ctx.fillStyle = '#444';
            ctx.fillRect(-5 * s, -2 * s, 5 * s, 2 * s);
            ctx.fillRect(1 * s, -2 * s, 5 * s, 2 * s);

            ctx.fillStyle = '#ffffff';
            ctx.fillRect(-5 * s, -26 * s, 10 * s, 12 * s);
            ctx.fillStyle = '#aa0000';
            ctx.fillRect(-1 * s, -25 * s, 2 * s, 8 * s);

            if (p.isTransformed) {
                ctx.fillStyle = '#d62828';
                ctx.fillRect(-6 * s, -42 * s, 14 * s, 14 * s);
                ctx.fillStyle = '#111111';
                ctx.fillRect(-4 * s, -38 * s, 10 * s, 8 * s);

                ctx.fillStyle = '#c0c0c0';
                ctx.fillRect(4 * s, -45 * s, 16 * s, 5 * s);
                ctx.fillStyle = (globalTick % 2 === 0) ? '#ff0000' : '#ffffff';
                ctx.fillRect(6 * s, -46 * s, 12 * s, 2 * s);

                ctx.fillStyle = '#333';
                ctx.fillRect(-8 * s, -40 * s, 3 * s, 8 * s);

                ctx.fillStyle = '#c0c0c0';
                if (p.isAttacking) {
                    ctx.fillRect(5 * s, -26 * s, 22 * s, 6 * s);
                    ctx.fillStyle = '#ffcc00';
                    ctx.fillRect(20 * s, -29 * s, 6 * s, 12 * s);
                } else {
                    ctx.fillRect(3 * s, -22 * s, 14 * s, 4 * s);
                }
            } else {
                ctx.fillStyle = '#ffdbac';
                ctx.fillRect(-4 * s, -35 * s, 8 * s, 9 * s);

                ctx.fillStyle = '#222';
                ctx.fillRect(1 * s, -32 * s, 2 * s, 2 * s);

                ctx.fillStyle = p.data.hair;
                ctx.fillRect(-5 * s, -39 * s, 10 * s, 5 * s);
                ctx.fillRect(-5 * s, -36 * s, 3 * s, 8 * s);
                ctx.fillRect(2 * s, -36 * s, 3 * s, 6 * s);

                ctx.fillStyle = '#ffffff';
                if (p.isAttacking) {
                    ctx.fillRect(2 * s, -24 * s, 12 * s, 4 * s);
                } else {
                    ctx.fillRect(-2 * s, -24 * s, 4 * s, 10 * s);
                }
            }

            ctx.restore();
        }

        function drawGenericPixel(p) {
            ctx.save();
            ctx.translate(p.x, p.y);
            if (!p.facingRight) ctx.scale(-1, 1);

            const scale = 3;

            if (p.isTransformed) {
                ctx.fillStyle = 'rgba(255, 0, 85, 0.4)';
                ctx.fillRect(-14 * scale, -40 * scale, 28 * scale, 42 * scale);
            }

            ctx.fillStyle = p.data.pants;
            if (!p.isGrounded) {
                ctx.fillRect(-5 * scale, -10 * scale, 4 * scale, 7 * scale);
                ctx.fillRect(1 * scale, -12 * scale, 4 * scale, 8 * scale);
            } else if (p.vx !== 0) {
                ctx.fillRect(-6 * scale, -12 * scale, 4 * scale, 12 * scale);
                ctx.fillRect(2 * scale, -12 * scale, 4 * scale, 12 * scale);
            } else {
                ctx.fillRect(-5 * scale, -14 * scale, 4 * scale, 14 * scale);
                ctx.fillRect(1 * scale, -14 * scale, 4 * scale, 14 * scale);
            }

            ctx.fillStyle = '#111';
            ctx.fillRect(-5 * scale, -2 * scale, 5 * scale, 2 * scale);
            ctx.fillRect(1 * scale, -2 * scale, 5 * scale, 2 * scale);

            ctx.fillStyle = p.data.shirt;
            ctx.fillRect(-5 * scale, -26 * scale, 10 * scale, 12 * scale);

            ctx.fillStyle = '#ffdbac';
            ctx.fillRect(-4 * scale, -35 * scale, 8 * scale, 9 * scale);

            ctx.fillStyle = '#222';
            ctx.fillRect(1 * scale, -32 * scale, 2 * scale, 2 * scale);

            ctx.fillStyle = p.data.hair;
            ctx.fillRect(-5 * scale, -38 * scale, 10 * scale, 5 * scale);
            ctx.fillRect(-5 * scale, -35 * scale, 3 * scale, 8 * scale);

            if (p.key === 'power') {
                ctx.fillStyle = '#ff0033';
                ctx.fillRect(-1 * scale, -42 * scale, 2 * scale, 5 * scale);
                ctx.fillRect(2 * scale, -41 * scale, 2 * scale, 4 * scale);
            }

            ctx.fillStyle = p.isTransformed ? '#ff0033' : p.data.shirt;
            if (p.isAttacking) {
                ctx.fillRect(2 * scale, -24 * scale, 14 * scale, 4 * scale);
                ctx.fillStyle = p.key === 'power' ? '#ff0033' : '#ffcc00';
                ctx.fillRect(12 * scale, -32 * scale, 8 * scale, 18 * scale);
            } else {
                ctx.fillRect(-2 * scale, -24 * scale, 4 * scale, 10 * scale);
            }

            ctx.restore();
        }

        function drawEffects() {
            for (let i = effects.length - 1; i >= 0; i--) {
                let ef = effects[i];
                ctx.save();
                
                if (ef.isFox) {
                    ctx.fillStyle = 'rgba(230, 230, 230, ' + ef.life + ')';
                    ctx.beginPath();
                    ctx.arc(ef.x, ef.y, ef.size * (1.1 - ef.life * 0.3), 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#ff0000';
                    ctx.fillRect(ef.x - 10, ef.y - 10, 6, 6);
                    ctx.fillRect(ef.x + 4, ef.y - 10, 6, 6);
                } else {
                    ctx.fillStyle = ef.color;
                    ctx.globalAlpha = ef.life;
                    ctx.beginPath();
                    ctx.arc(ef.x, ef.y, ef.size * (1.2 - ef.life), 0, Math.PI * 2);
                    ctx.fill();
                }
                
                ctx.restore();

                ef.life -= 0.08;
                if (ef.life <= 0) effects.splice(i, 1);
            }
        }

        function drawBackground() {
            if (selectedMap === 'hell') {
                ctx.fillStyle = '#2b0000'; ctx.fillRect(0, 0, 960, 540);
                ctx.fillStyle = '#660000'; ctx.fillRect(0, 400, 960, 140);
                ctx.fillStyle = '#ff3333';
                for(let i=0; i<5; i++) ctx.fillRect(100 + i*180, 50, 60, 90);
            } else if (selectedMap === 'beach') {
                ctx.fillStyle = '#0a192f'; ctx.fillRect(0, 0, 960, 540);
                ctx.fillStyle = '#d2b48c'; ctx.fillRect(0, 400, 960, 140);
            } else {
                ctx.fillStyle = '#11091c'; ctx.fillRect(0, 0, 960, 540);
                ctx.fillStyle = '#ff3300'; ctx.fillRect(0, 280, 960, 120);
                ctx.fillStyle = '#222222'; ctx.fillRect(0, 400, 960, 140);
            }
        }

        function gameLoop() {
            if (!isGaming) return;
            globalTick++;
            ctx.clearRect(0, 0, 960, 540);

            drawBackground();
            handleInput();

            if (P1.key === 'denji') drawDenjiPixel(P1);
            else if (P1.key === 'aki') drawAkiPixel(P1);
            else drawGenericPixel(P1);

            if (P2.key === 'denji') drawDenjiPixel(P2);
            else if (P2.key === 'aki') drawAkiPixel(P2);
            else drawGenericPixel(P2);

            drawEffects();

            requestAnimationFrame(gameLoop);
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=False)
