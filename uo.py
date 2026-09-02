import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨 3D 격투 게임", layout="wide")

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>체인소맨 3D 격투 게임</title>
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #050505; font-family: 'Noto Sans KR', sans-serif; color: #fff; user-select: none; }
        #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1; }
        
        .ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; display: flex; flex-direction: column; justify-content: space-between; }
        .interactive { pointer-events: auto; }
        
        /* HUD */
        #hud { display: none; padding: 15px 30px; justify-content: space-between; align-items: flex-start; }
        .player-hud { width: 42%; }
        .p2-hud { text-align: right; }
        .name { font-size: 26px; font-weight: 900; text-shadow: 0 0 10px #ff0055; margin-bottom: 5px; text-transform: uppercase; }
        .bar-bg { width: 100%; height: 24px; background: rgba(255,255,255,0.15); border: 2px solid #fff; box-shadow: 0 0 15px rgba(0,0,0,0.8); border-radius: 4px; overflow: hidden; }
        .hp-bar { height: 100%; background: linear-gradient(90deg, #ff0055, #ff5500); width: 100%; transition: width 0.1s linear; }
        .ult-bar-bg { width: 100%; height: 12px; background: rgba(0,0,0,0.6); border: 1px solid #777; margin-top: 6px; border-radius: 2px; overflow: hidden; }
        .ult-bar { height: 100%; background: linear-gradient(90deg, #00ffff, #0088ff); width: 0%; transition: width 0.2s linear; }
        .score { font-size: 18px; color: #ffd700; margin-top: 5px; font-weight: bold; }

        /* 화면 가상 컨트롤러 */
        #touch-controls { display: none; position: absolute; bottom: 20px; width: 100%; padding: 0 30px; box-sizing: border-box; justify-content: space-between; align-items: flex-end; z-index: 20; }
        .control-group { display: flex; gap: 10px; }
        .ctrl-btn { width: 65px; height: 65px; background: rgba(0,0,0,0.6); border: 2px solid #fff; border-radius: 12px; color: #fff; font-size: 15px; font-weight: bold; display: flex; justify-content: center; align-items: center; cursor: pointer; backdrop-filter: blur(4px); box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .ctrl-btn:active { background: #ff0033; transform: scale(0.95); }
        .ult-btn { background: rgba(255,0,85,0.8); border-color: #ff0055; width: 85px; }

        /* 메뉴 레이아웃 */
        .screen { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); }
        h1 { font-size: 56px; color: #ff0033; text-shadow: 0 0 20px #ff0033, 4px 4px 0px #000; margin-bottom: 10px; font-weight: 900; }
        .btn { padding: 15px 40px; font-size: 22px; font-weight: bold; background: #ff0033; color: #fff; border: none; cursor: pointer; border-radius: 6px; box-shadow: 0 0 15px #ff0033; transition: all 0.2s; margin: 10px; }
        .btn:hover { background: #fff; color: #ff0033; transform: scale(1.05); }
        
        /* 7명 캐릭터 선택 그리드 (이미지 카드 적용) */
        .select-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; max-width: 1000px; margin-bottom: 20px; max-height: 50vh; overflow-y: auto; padding: 10px; }
        .card { width: 120px; height: 180px; border: 3px solid #444; border-radius: 10px; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; cursor: pointer; background-size: cover; background-position: center; transition: 0.2s; position: relative; overflow: hidden; }
        .card .card-info { width: 100%; background: rgba(0,0,0,0.75); text-align: center; padding: 5px 0; border-top: 1px solid rgba(255,255,255,0.2); }
        .card.selected { border-color: #ff0033; box-shadow: 0 0 20px #ff0033; transform: scale(1.05); }
        .card h3 { font-size: 16px; margin: 0; color: #fff; text-shadow: 0 0 5px #000; }
        .card p { font-size: 11px; color: #ffcc00; margin: 2px 0 0 0; }

        /* 궁극기 컷씬 오버레이 */
        #cutscene { display: none; position: absolute; width: 100%; height: 100%; background: #000; z-index: 100; justify-content: center; align-items: center; flex-direction: column; }
        #cutscene-text { font-size: 64px; color: #ff0033; font-weight: 900; text-shadow: 0 0 30px #ff0033; animation: pulse 0.4s infinite alternate; }
        @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.15); } }
    </style>
    <!-- Three.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="canvas-container"></div>

    <div class="ui-layer">
        <!-- HUD -->
        <div id="hud" class="interactive">
            <div class="player-hud p1-hud">
                <div id="p1-name" class="name">덴지</div>
                <div class="bar-bg"><div id="p1-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p1-ult" class="ult-bar"></div></div>
                <div id="p1-score" class="score">라운드 승리: 0</div>
            </div>
            <div style="font-size: 32px; font-weight: 900; color: #fff;">VS</div>
            <div class="player-hud p2-hud">
                <div id="p2-name" class="name">파워</div>
                <div class="bar-bg"><div id="p2-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p2-ult" class="ult-bar"></div></div>
                <div id="p2-score" class="score">라운드 승리: 0</div>
            </div>
        </div>

        <!-- 메인 화면 -->
        <div id="main-screen" class="screen interactive">
            <h1>체인소맨 3D 격투</h1>
            <p style="color:#aaa; margin-bottom: 30px;">7인의 데빌 헌터 & 악마 대결</p>
            <button class="btn" onclick="goToModeSelect()">게임 시작</button>
        </div>

        <!-- 모드 선택 -->
        <div id="mode-screen" class="screen interactive" style="display:none;">
            <h1>모드 선택</h1>
            <div>
                <button class="btn" onclick="selectMode('1P')">1인용 (VS AI)</button>
                <button class="btn" onclick="selectMode('2P')">2인용 (대전)</button>
            </div>
        </div>

        <!-- 캐릭터 7명 & 맵 선택 -->
        <div id="select-screen" class="screen interactive" style="display:none;">
            <h2 style="margin-top:0;">캐릭터 선택 (7인)</h2>
            <div class="select-grid" id="char-grid"></div>

            <h2>전장 맵 선택</h2>
            <div style="display:flex; gap:20px; margin-bottom: 15px;">
                <div class="card selected" id="m-city" onclick="pickMap('city')" style="width:140px; height:80px; background:#222; justify-content:center;">
                    <h3>도시 옥상</h3>
                </div>
                <div class="card" id="m-hell" onclick="pickMap('hell')" style="width:140px; height:80px; background:#400; justify-content:center;">
                    <h3>악마의 영역</h3>
                </div>
            </div>

            <button class="btn" onclick="startGame()">전투 시작!</button>
        </div>
    </div>

    <!-- 가상 조작 버튼 -->
    <div id="touch-controls" class="interactive">
        <div class="control-group">
            <div class="ctrl-btn" onmousedown="setVirtualKey('a', true)" onmouseup="setVirtualKey('a', false)">◀</div>
            <div class="ctrl-btn" onmousedown="setVirtualKey('d', true)" onmouseup="setVirtualKey('d', false)">▶</div>
        </div>
        <div class="control-group">
            <div class="ctrl-btn" onclick="triggerSkill('SKILL_A')">스킬1 (F)</div>
            <div class="ctrl-btn" onclick="triggerSkill('SKILL_B')">스킬2 (G)</div>
            <div class="ctrl-btn" onclick="triggerSkill('FUSION')">조합 (F+G)</div>
            <div class="ctrl-btn ult-btn" onclick="triggerSkill('ULT')">궁극기 (H)</div>
        </div>
    </div>

    <!-- 연출 컷씬 -->
    <div id="cutscene">
        <div id="cutscene-text">필살 악마 일격!</div>
    </div>

    <script>
        // 7명 캐릭터 정보 및 구글 찾기 기반 일러스트 URL 등록
        const CHARACTERS = {
            denji: { name: '덴지', color: 0xff0055, img: 'http://googleusercontent.com/image_collection/image_retrieval/5284260906072440914_0', type: '체인소' },
            power: { name: '파워', color: 0xff5500, img: 'http://googleusercontent.com/image_collection/image_retrieval/11872592120298979664_0', type: '혈액 망치' },
            aki: { name: '아키', color: 0x0088ff, img: 'http://googleusercontent.com/image_collection/image_retrieval/3586354115942282614_0', type: '여우의 악마' },
            makima: { name: '마키마', color: 0xff00aa, img: 'http://googleusercontent.com/image_collection/image_retrieval/2167677592680287183_0', type: '지배의 악마' },
            reze: { name: '레제', color: 0xaa00ff, img: 'http://googleusercontent.com/image_collection/image_retrieval/2170920114765024793_0', type: '폭탄의 악마' },
            kishibe: { name: '키시베', color: 0x888888, img: 'http://googleusercontent.com/image_collection/image_retrieval/15563270650040299381_0', type: '베테랑 헌터' },
            yoru: { name: '요루', color: 0xcc0000, img: 'http://googleusercontent.com/image_collection/image_retrieval/17499428930008820191_0', type: '전쟁의 악마' }
        };

        // Web Audio API 사운드 효과음
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        let audioCtx;

        function initAudio() {
            if (!audioCtx) audioCtx = new AudioCtx();
        }

        function playSound(type) {
            initAudio();
            if (!audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            const now = audioCtx.currentTime;

            if (type === 'hit') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(160, now);
                osc.frequency.exponentialRampToValueAtTime(40, now + 0.15);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.15);
                osc.start(now); osc.stop(now + 0.15);
            } else if (type === 'fusion') {
                osc.type = 'square';
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.exponentialRampToValueAtTime(650, now + 0.25);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
                osc.start(now); osc.stop(now + 0.25);
            } else if (type === 'ult') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(100, now);
                osc.frequency.linearRampToValueAtTime(900, now + 0.6);
                gain.gain.setValueAtTime(0.6, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.6);
                osc.start(now); osc.stop(now + 0.6);
            }
        }

        let gameMode = '1P';
        let selectedCharP1 = 'denji';
        let selectedCharP2 = 'power';
        let selectedMap = 'city';
        
        let p1Score = 0, p2Score = 0;
        let isGaming = false;
        let isCutscene = false;

        function createPlayer(charKey, xPos, isAI) {
            const data = CHARACTERS[charKey];
            return {
                key: charKey,
                name: data.name,
                color: data.color,
                hp: 100,
                ult: 0,
                comboCount: 0,
                isAttacking: false,
                isAI: isAI,
                position: { x: xPos, y: 1, z: 0 },
                mesh: null
            };
        }

        let P1, P2;
        const keysPressed = {};

        window.addEventListener('keydown', (e) => {
            keysPressed[e.key.toLowerCase()] = true;
            handleSkillCombinations();
        });

        window.addEventListener('keyup', (e) => {
            keysPressed[e.key.toLowerCase()] = false;
        });

        function setVirtualKey(key, pressed) {
            keysPressed[key] = pressed;
        }

        function triggerSkill(type) {
            if (!isGaming || isCutscene) return;
            if (type === 'SKILL_A') executeSkill(P1, P2, 'SKILL_A', 6, 10);
            if (type === 'SKILL_B') executeSkill(P1, P2, 'SKILL_B', 8, 12);
            if (type === 'FUSION') executeSkill(P1, P2, 'FUSION_COMBO', 18, 25);
            if (type === 'ULT') executeUltimate(P1, P2);
        }

        // 일러스트 카드 동적 생성
        function renderCharCards() {
            const grid = document.getElementById('char-grid');
            grid.innerHTML = '';
            
            Object.keys(CHARACTERS).forEach(key => {
                const c = CHARACTERS[key];
                const card = document.createElement('div');
                card.className = `card ${key === selectedCharP1 ? 'selected' : ''}`;
                card.style.backgroundImage = `url('${c.img}')`;
                card.onclick = () => pickChar(key);
                
                card.innerHTML = `
                    <div class="card-info">
                        <h3>${c.name}</h3>
                        <p>${c.type}</p>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function goToModeSelect() {
            initAudio();
            document.getElementById('main-screen').style.display = 'none';
            document.getElementById('mode-screen').style.display = 'flex';
        }

        function selectMode(mode) {
            gameMode = mode;
            renderCharCards();
            document.getElementById('mode-screen').style.display = 'none';
            document.getElementById('select-screen').style.display = 'flex';
        }

        function pickChar(char) {
            selectedCharP1 = char;
            const keys = Object.keys(CHARACTERS);
            selectedCharP2 = keys[(keys.indexOf(char) + 1) % keys.length];
            renderCharCards();
        }

        function pickMap(map) {
            selectedMap = map;
            document.getElementById('m-city').classList.toggle('selected', map === 'city');
            document.getElementById('m-hell').classList.toggle('selected', map === 'hell');
        }

        // 3D 엔진
        let scene, camera, renderer, stageFloor, light;

        function init3D() {
            const container = document.getElementById('canvas-container');
            scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x050505, 0.015);

            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 5, 15);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);

            light = new THREE.DirectionalLight(0xffffff, 1.2);
            light.position.set(5, 20, 10);
            light.castShadow = true;
            scene.add(light);

            window.addEventListener('resize', onWindowResize, false);
        }

        function setupStage(mapType) {
            if (stageFloor) scene.remove(stageFloor);
            
            let floorColor = mapType === 'city' ? 0x222222 : 0x550000;
            const geo = new THREE.BoxGeometry(30, 1, 10);
            const mat = new THREE.MeshStandardMaterial({ color: floorColor, roughness: 0.3 });
            stageFloor = new THREE.Mesh(geo, mat);
            stageFloor.position.y = -0.5;
            stageFloor.receiveShadow = true;
            scene.add(stageFloor);

            scene.background = new THREE.Color(mapType === 'city' ? 0x050510 : 0x1a0000);
        }

        function createCharacterMesh(color) {
            const group = new THREE.Group();
            
            const bodyGeo = new THREE.BoxGeometry(1, 2, 0.6);
            const bodyMat = new THREE.MeshStandardMaterial({ color: color, metalness: 0.5, roughness: 0.2 });
            const body = new THREE.Mesh(bodyGeo, bodyMat);
            body.castShadow = true;
            group.add(body);

            const headGeo = new THREE.BoxGeometry(0.6, 0.6, 0.6);
            const headMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: color, emissiveIntensity: 0.5 });
            const head = new THREE.Mesh(headGeo, headMat);
            head.position.y = 1.4;
            group.add(head);

            return group;
        }

        function startGame() {
            document.getElementById('select-screen').style.display = 'none';
            document.getElementById('hud').style.display = 'flex';
            document.getElementById('touch-controls').style.display = 'flex';

            setupStage(selectedMap);

            P1 = createPlayer(selectedCharP1, -4, false);
            P2 = createPlayer(selectedCharP2, 4, gameMode === '1P');

            document.getElementById('p1-name').innerText = P1.name;
            document.getElementById('p2-name').innerText = P2.name;

            if (P1.mesh) scene.remove(P1.mesh);
            if (P2.mesh) scene.remove(P2.mesh);

            P1.mesh = createCharacterMesh(P1.color);
            P2.mesh = createCharacterMesh(P2.color);

            scene.add(P1.mesh);
            scene.add(P2.mesh);

            resetRound();
            isGaming = true;
            animate();
        }

        function resetRound() {
            P1.hp = 100; P2.hp = 100;
            P1.position.x = -4; P2.position.x = 4;
            P1.comboCount = 0; P2.comboCount = 0;
            updateHUD();
        }

        function handleInput() {
            if (!isGaming || isCutscene) return;

            if (keysPressed['a'] && P1.position.x > -13) P1.position.x -= 0.12;
            if (keysPressed['d'] && P1.position.x < 13) P1.position.x += 0.12;
            
            if (keysPressed['f']) executeSkill(P1, P2, 'SKILL_A', 6, 10);
            if (keysPressed['g']) executeSkill(P1, P2, 'SKILL_B', 8, 12);
            if (keysPressed['h']) executeUltimate(P1, P2);

            if (!P2.isAI) {
                if (keysPressed['arrowleft'] && P2.position.x > -13) P2.position.x -= 0.12;
                if (keysPressed['arrowright'] && P2.position.x < 13) P2.position.x += 0.12;
                if (keysPressed['1']) executeSkill(P2, P1, 'SKILL_A', 6, 10);
                if (keysPressed['2']) executeSkill(P2, P1, 'SKILL_B', 8, 12);
                if (keysPressed['3']) executeUltimate(P2, P1);
            } else {
                updateAI();
            }
        }

        function handleSkillCombinations() {
            if (!isGaming || isCutscene) return;
            if (keysPressed['f'] && keysPressed['g']) executeSkill(P1, P2, 'FUSION_COMBO', 18, 25);
            if (!P2.isAI && keysPressed['1'] && keysPressed['2']) executeSkill(P2, P1, 'FUSION_COMBO', 18, 25);
        }

        function updateAI() {
            const dist = P1.position.x - P2.position.x;
            if (Math.abs(dist) > 2.2) {
                P2.position.x += dist > 0 ? 0.08 : -0.08;
            } else {
                if (Math.random() < 0.05) executeSkill(P2, P1, 'SKILL_A', 6, 10);
                if (P2.ult >= 100) executeUltimate(P2, P1);
            }
        }

        function executeSkill(attacker, defender, skillType, damage, ultGain) {
            if (attacker.isAttacking) return;
            attacker.isAttacking = true;

            const distance = Math.abs(attacker.position.x - defender.position.x);
            
            attacker.mesh.position.z = 0.5;
            setTimeout(() => { attacker.mesh.position.z = 0; attacker.isAttacking = false; }, 200);

            if (distance < 2.5) {
                if (skillType === 'FUSION_COMBO') playSound('fusion');
                else playSound('hit');

                defender.hp -= damage;
                defender.comboCount++;
                attacker.ult = Math.min(100, attacker.ult + ultGain);

                if (defender.comboCount >= 3) {
                    defender.position.x += (defender.position.x > attacker.position.x ? 2.5 : -2.5);
                    defender.comboCount = 0;
                }

                if (defender.hp <= 0) handleRoundEnd(attacker);
                updateHUD();
            }
        }

        function executeUltimate(attacker, defender) {
            if (attacker.ult < 100 || isCutscene) return;
            
            attacker.ult = 0;
            isCutscene = true;
            playSound('ult');

            const cutsceneEl = document.getElementById('cutscene');
            const cutsceneText = document.getElementById('cutscene-text');
            cutsceneText.innerText = attacker.name + " 필살 악마 일격!";
            cutsceneEl.style.display = 'flex';

            camera.position.set(attacker.position.x, 3, 4);

            setTimeout(() => {
                cutsceneEl.style.display = 'none';
                camera.position.set(0, 5, 15);
                
                defender.hp -= 40;
                isCutscene = false;
                
                if (defender.hp <= 0) handleRoundEnd(attacker);
                updateHUD();
            }, 1800);
        }

        function handleRoundEnd(winner) {
            if (winner === P1) p1Score++;
            else p2Score++;

            document.getElementById('p1-score').innerText = `라운드 승리: ${p1Score}`;
            document.getElementById('p2-score').innerText = `라운드 승리: ${p2Score}`;

            if (p1Score >= 2 || p2Score >= 2) {
                alert(`${winner.name} 최종 승리!`);
                p1Score = 0; p2Score = 0;
                document.getElementById('hud').style.display = 'none';
                document.getElementById('touch-controls').style.display = 'none';
                document.getElementById('main-screen').style.display = 'flex';
                isGaming = false;
            } else {
                resetRound();
            }
        }

        function updateHUD() {
            document.getElementById('p1-hp').style.width = Math.max(0, P1.hp) + '%';
            document.getElementById('p2-hp').style.width = Math.max(0, P2.hp) + '%';
            document.getElementById('p1-ult').style.width = P1.ult + '%';
            document.getElementById('p2-ult').style.width = P2.ult + '%';
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function animate() {
            if (!isGaming) return;
            requestAnimationFrame(animate);

            handleInput();

            if (P1.mesh) P1.mesh.position.x = P1.position.x;
            if (P2.mesh) P2.mesh.position.x = P2.position.x;

            if (!isCutscene) {
                const midPoint = (P1.position.x + P2.position.x) / 2;
                camera.position.x += (midPoint - camera.position.x) * 0.05;
            }

            renderer.render(scene, camera);
        }

        init3D();
    </script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=False)
