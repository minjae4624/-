<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>체인소맨 하이브리드</title>
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #050505; font-family: sans-serif; color: #fff; user-select: none; }
        #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; display: flex; justify-content: center; align-items: center; }
        canvas { background: #111; image-rendering: pixelated; border: 4px solid #333; box-shadow: 0 0 30px rgba(255,0,85,0.3); }

        .ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; display: flex; flex-direction: column; justify-content: space-between; }
        .interactive { pointer-events: auto; }

        /* HUD */
        #hud { display: none; padding: 20px 40px; justify-content: space-between; align-items: flex-start; }
        .player-hud { width: 40%; }
        .p2-hud { text-align: right; }
        .name { font-size: 24px; font-weight: 900; text-shadow: 0 0 10px #ff0055; margin-bottom: 5px; }
        .bar-bg { width: 100%; height: 22px; background: #222; border: 2px solid #fff; border-radius: 4px; overflow: hidden; }
        .hp-bar { height: 100%; background: linear-gradient(90deg, #ff0055, #ff5500); width: 100%; transition: width 0.1s linear; }
        .ult-bar-bg { width: 100%; height: 10px; background: #111; border: 1px solid #666; margin-top: 4px; border-radius: 2px; overflow: hidden; }
        .ult-bar { height: 100%; background: linear-gradient(90deg, #00ffff, #0088ff); width: 0%; transition: width 0.2s linear; }
        .transform-badge { font-size: 13px; color: #00ffcc; font-weight: bold; display: none; margin-top: 3px; }

        /* 조작 패널 */
        #touch-controls { display: none; position: absolute; bottom: 15px; width: 100%; padding: 0 20px; box-sizing: border-box; justify-content: space-between; z-index: 20; }
        .panel { background: rgba(0,0,0,0.8); border: 1px solid #444; border-radius: 10px; padding: 8px; display: flex; gap: 6px; }
        .ctrl-btn { width: 50px; height: 50px; background: #222; border: 2px solid #fff; border-radius: 6px; color: #fff; font-size: 11px; font-weight: bold; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; }
        .ctrl-btn:active { background: #ff0033; }
        .trans-btn { border-color: #00ffcc; color: #00ffcc; }
        .ult-btn { border-color: #ff0055; background: rgba(255,0,85,0.4); }

        /* 화면 선택 메뉴 */
        .screen { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(0,0,0,0.9); }
        h1 { font-size: 48px; color: #ff0033; text-shadow: 0 0 20px #ff0033; margin-bottom: 5px; }
        .btn { padding: 12px 30px; font-size: 18px; font-weight: bold; background: #ff0033; color: #fff; border: none; cursor: pointer; border-radius: 5px; box-shadow: 0 0 15px #ff0033; margin: 8px; }
        .btn:hover { background: #fff; color: #ff0033; }

        .select-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; max-width: 800px; margin-bottom: 15px; }
        .card { width: 100px; height: 140px; border: 3px solid #444; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; cursor: pointer; background-size: cover; background-position: center; position: relative; overflow: hidden; }
        .card .card-info { width: 100%; background: rgba(0,0,0,0.8); text-align: center; padding: 3px 0; }
        .card.selected-p1 { border-color: #ff0055; box-shadow: 0 0 15px #ff0055; scale: 1.05; }
        .card.selected-p2 { border-color: #0088ff; box-shadow: 0 0 15px #0088ff; scale: 1.05; }
        .card h3 { font-size: 13px; margin: 0; color: #fff; }
        .card p { font-size: 9px; color: #ffcc00; margin: 1px 0 0 0; }

        /* 궁극기 연출 컷씬 */
        #cutscene { display: none; position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 100; justify-content: center; align-items: center; flex-direction: column; }
        #cutscene-img { width: 280px; height: 280px; border-radius: 50%; border: 6px solid #ff0033; box-shadow: 0 0 60px #ff0033; background-size: cover; background-position: center; animation: zoomIn 0.3s ease-out; }
        #cutscene-text { font-size: 45px; color: #ff0033; font-weight: 900; text-shadow: 0 0 30px #ff0033; margin-top: 20px; animation: pulse 0.4s infinite alternate; }
        @keyframes zoomIn { from { transform: scale(0); } to { transform: scale(1); } }
        @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }
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
                <div id="p1-trans" class="transform-badge">HYBRID MODE</div>
            </div>
            <div style="font-size: 26px; font-weight: 900; color: #fff;">VS</div>
            <div class="player-hud p2-hud">
                <div id="p2-name" class="name">파워</div>
                <div class="bar-bg"><div id="p2-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p2-ult" class="ult-bar"></div></div>
                <div id="p2-trans" class="transform-badge">HYBRID MODE</div>
            </div>
        </div>

        <div id="main-screen" class="screen interactive">
            <h1>체인소맨 하이브리드</h1>
            <p style="color:#aaa; margin-bottom: 20px;">픽셀 아트로 펼쳐지는 하이브리드 대전 격투</p>
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
            <div class="ctrl-btn" onclick="triggerAction('P1','LEFT')">◀<br>(A)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','RIGHT')">▶<br>(D)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','SKILL_A')">스킬1<br>(F)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','SKILL_B')">스킬2<br>(G)</div>
            <div class="ctrl-btn trans-btn" onclick="triggerAction('P1','TRANS')">변신<br>(V)</div>
            <div class="ctrl-btn ult-btn" onclick="triggerAction('P1','ULT')">궁극기<br>(H)</div>
        </div>
        <div class="panel">
            <div class="ctrl-btn" onclick="triggerAction('P2','LEFT')">◀<br>(←)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','RIGHT')">▶<br>(→)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','SKILL_A')">스킬1<br>(1)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','SKILL_B')">스킬2<br>(2)</div>
            <div class="ctrl-btn trans-btn" onclick="triggerAction('P2','TRANS')">변신<br>(0)</div>
            <div class="ctrl-btn ult-btn" onclick="triggerAction('P2','ULT')">궁극기<br>(3)</div>
        </div>
    </div>

    <div id="cutscene">
        <div id="cutscene-img"></div>
        <div id="cutscene-text">필살 일격!</div>
    </div>

    <script>
        const CHARACTERS = {
            denji: { name: '덴지', hair: '#f5d442', shirt: '#ffffff', pants: '#222222', isHybrid: true, img: 'http://googleusercontent.com/image_collection/image_retrieval/5284260906072440914_0', type: '체인소 하이브리드' },
            power: { name: '파워', hair: '#e0a367', shirt: '#aa2222', pants: '#111122', isHybrid: false, img: 'http://googleusercontent.com/image_collection/image_retrieval/6851370321638739379_0', type: '혈액의 악마' },
            aki: { name: '아키', hair: '#1a233a', shirt: '#151515', pants: '#151515', isHybrid: false, img: 'http://googleusercontent.com/image_collection/image_retrieval/3586354115942282614_0', type: '여우/커스 계약' },
            makima: { name: '마키마', hair: '#d66347', shirt: '#ffffff', pants: '#111111', isHybrid: false, img: 'http://googleusercontent.com/image_collection/image_retrieval/11239902871223266566_0', type: '지배의 악마' },
            reze: { name: '레제', hair: '#3f3254', shirt: '#ffffff', pants: '#222233', isHybrid: true, img: 'http://googleusercontent.com/image_collection/image_retrieval/14147712580439339747_0', type: '폭탄 하이브리드' },
            kishibe: { name: '키시베', hair: '#8a8883', shirt: '#2b2b2b', pants: '#1a1a1a', isHybrid: false, img: 'http://googleusercontent.com/image_collection/image_retrieval/15563270650040299381_0', type: '베테랑 헌터' },
            yoru: { name: '요루', hair: '#2b1b17', shirt: '#551111', pants: '#111111', isHybrid: true, img: 'http://googleusercontent.com/image_collection/image_retrieval/17499428930008820191_0', type: '전쟁 하이브리드' }
        };

        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let gameMode = '1P';
        let selectedCharP1 = 'denji', selectedCharP2 = 'power', selectedMap = 'city';
        let isGaming = false, isCutscene = false;

        function createPlayer(charKey, xPos, isAI, facingRight) {
            const data = CHARACTERS[charKey];
            return {
                key: charKey, name: data.name, data: data,
                isTransformed: false, hp: 100, ult: 0,
                x: xPos, y: 380, vx: 0, facingRight: facingRight,
                isAttacking: false, attackType: null, isAI: isAI, img: data.img
            };
        }

        let P1, P2;
        const keysPressed = {};

        window.addEventListener('keydown', (e) => { keysPressed[e.key.toLowerCase()] = true; });
        window.addEventListener('keyup', (e) => { keysPressed[e.key.toLowerCase()] = false; });

        function triggerAction(p, act) {
            if (!isGaming || isCutscene) return;
            const target = (p === 'P1') ? P1 : P2;
            const enemy = (p === 'P1') ? P2 : P1;

            if (act === 'SKILL_A') executeSkill(target, enemy, 'SKILL_A', 7, 10);
            if (act === 'SKILL_B') executeSkill(target, enemy, 'SKILL_B', 10, 15);
            if (act === 'TRANS') transformPlayer(target);
            if (act === 'ULT') executeUltimate(target, enemy);
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
            if (keysPressed['a'] && P1.x > 50) { P1.vx = -(P1.isTransformed ? 7 : 5); P1.facingRight = false; }
            if (keysPressed['d'] && P1.x < 870) { P1.vx = (P1.isTransformed ? 7 : 5); P1.facingRight = true; }
            if (keysPressed['f']) executeSkill(P1, P2, 'SKILL_A', 7, 10);
            if (keysPressed['g']) executeSkill(P1, P2, 'SKILL_B', 10, 15);
            if (keysPressed['v']) transformPlayer(P1);
            if (keysPressed['h']) executeUltimate(P1, P2);

            if (!P2.isAI) {
                P2.vx = 0;
                if (keysPressed['arrowleft'] && P2.x > 50) { P2.vx = -(P2.isTransformed ? 7 : 5); P2.facingRight = false; }
                if (keysPressed['arrowright'] && P2.x < 870) { P2.vx = (P2.isTransformed ? 7 : 5); P2.facingRight = true; }
                if (keysPressed['1']) executeSkill(P2, P1, 'SKILL_A', 7, 10);
                if (keysPressed['2']) executeSkill(P2, P1, 'SKILL_B', 10, 15);
                if (keysPressed['0']) transformPlayer(P2);
                if (keysPressed['3']) executeUltimate(P2, P1);
            } else {
                updateAI();
            }

            P1.x += P1.vx;
            P2.x += P2.vx;
        }

        function updateAI() {
            const dist = P1.x - P2.x;
            if (Math.abs(dist) > 80) {
                P2.vx = dist > 0 ? 3 : -3;
                P2.facingRight = dist > 0;
            } else {
                P2.vx = 0;
                if (Math.random() < 0.04) executeSkill(P2, P1, 'SKILL_A', 7, 10);
                if (P2.data.isHybrid && !P2.isTransformed && Math.random() < 0.02) transformPlayer(P2);
                if (P2.ult >= 100) executeUltimate(P2, P1);
            }
        }

        function transformPlayer(player) {
            if (!player.data.isHybrid || player.isTransformed) return;
            player.isTransformed = true;
            const badge = (player === P1) ? document.getElementById('p1-trans') : document.getElementById('p2-trans');
            badge.style.display = 'block';
        }

        function executeSkill(attacker, defender, type, damage, ultGain) {
            if (attacker.isAttacking) return;
            attacker.isAttacking = true;
            attacker.attackType = type;

            const finalDmg = attacker.isTransformed ? damage * 1.5 : damage;

            setTimeout(() => { attacker.isAttacking = false; }, 250);

            if (Math.abs(attacker.x - defender.x) < 90) {
                defender.hp -= finalDmg;
                attacker.ult = Math.min(100, attacker.ult + ultGain);
                defender.x += attacker.facingRight ? 30 : -30;
                updateHUD();
            }
        }

        function executeUltimate(attacker, defender) {
            if (attacker.ult < 100 || isCutscene) return;
            attacker.ult = 0; isCutscene = true;

            const cutsceneEl = document.getElementById('cutscene');
            document.getElementById('cutscene-img').style.backgroundImage = "url('" + attacker.img + "')";
            document.getElementById('cutscene-text').innerText = attacker.name + " 필살 각성 일격!";
            cutsceneEl.style.display = 'flex';

            setTimeout(() => {
                cutsceneEl.style.display = 'none';
                defender.hp -= 40;
                isCutscene = false;
                updateHUD();
            }, 1800);
        }

        function updateHUD() {
            document.getElementById('p1-hp').style.width = Math.max(0, P1.hp) + '%';
            document.getElementById('p2-hp').style.width = Math.max(0, P2.hp) + '%';
            document.getElementById('p1-ult').style.width = P1.ult + '%';
            document.getElementById('p2-ult').style.width = P2.ult + '%';
        }

        function drawPixelCharacter(p) {
            ctx.save();
            ctx.translate(p.x, p.y);
            if (!p.facingRight) ctx.scale(-1, 1);

            const scale = 4;

            if (p.isTransformed) {
                ctx.fillStyle = 'rgba(255, 0, 50, 0.4)';
                ctx.fillRect(-12 * scale, -28 * scale, 24 * scale, 30 * scale);
            }

            ctx.fillStyle = p.data.pants;
            ctx.fillRect(-5 * scale, -8 * scale, 4 * scale, 8 * scale);
            ctx.fillRect(1 * scale, -8 * scale, 4 * scale, 8 * scale);

            ctx.fillStyle = p.data.shirt;
            ctx.fillRect(-6 * scale, -18 * scale, 12 * scale, 10 * scale);

            if (p.isTransformed && p.key === 'denji') {
                ctx.fillStyle = '#444444';
                ctx.fillRect(-7 * scale, -27 * scale, 14 * scale, 9 * scale);
                ctx.fillStyle = '#ff0033';
                ctx.fillRect(-9 * scale, -25 * scale, 18 * scale, 3 * scale);
            } else {
                ctx.fillStyle = '#ffdbac';
                ctx.fillRect(-5 * scale, -25 * scale, 10 * scale, 7 * scale);
                ctx.fillStyle = p.data.hair;
                ctx.fillRect(-6 * scale, -28 * scale, 12 * scale, 5 * scale);
            }

            ctx.fillStyle = p.isTransformed ? '#ff0000' : p.data.shirt;
            if (p.isAttacking) {
                ctx.fillRect(4 * scale, -16 * scale, 16 * scale, 4 * scale);
                ctx.fillStyle = '#ffff00';
                ctx.fillRect(18 * scale, -20 * scale, 10 * scale, 12 * scale);
            } else {
                ctx.fillRect(5 * scale, -17 * scale, 4 * scale, 9 * scale);
            }

            ctx.restore();
        }

        function drawBackground() {
            if (selectedMap === 'hell') {
                ctx.fillStyle = '#2b0000'; ctx.fillRect(0, 0, 960, 540);
                ctx.fillStyle = '#660000'; ctx.fillRect(0, 420, 960, 120);
                ctx.fillStyle = '#ff3333';
                for(let i=0; i<5; i++) ctx.fillRect(100 + i*180, 50, 60, 90);
            } else if (selectedMap === 'beach') {
                ctx.fillStyle = '#0a192f'; ctx.fillRect(0, 0, 960, 540);
                ctx.fillStyle = '#d2b48c'; ctx.fillRect(0, 420, 960, 120);
            } else {
                ctx.fillStyle = '#1a0933'; ctx.fillRect(0, 0, 960, 540);
                ctx.fillStyle = '#ff5500'; ctx.fillRect(0, 300, 960, 120);
                ctx.fillStyle = '#333333'; ctx.fillRect(0, 420, 960, 120);
            }
        }

        function gameLoop() {
            if (!isGaming) return;
            ctx.clearRect(0, 0, 960, 540);

            drawBackground();
            handleInput();

            drawPixelCharacter(P1);
            drawPixelCharacter(P2);

            requestAnimationFrame(gameLoop);
        }
    </script>
</body>
</html>
