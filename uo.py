import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="Chainsaw Man 3D Fight", layout="wide")

# 게임 전체 HTML / Three.js / JS 코드
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Chainsaw Man 3D Fighter</title>
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #050505; font-family: 'Impact', sans-serif; color: #fff; }
        #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1; }
        
        /* UI overlay */
        .ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; display: flex; flex-direction: column; justify-content: space-between; }
        .interactive { pointer-events: auto; }
        
        /* HUD */
        #hud { display: none; padding: 20px 40px; justify-content: space-between; align-items: flex-start; }
        .player-hud { width: 42%; }
        .p2-hud { text-align: right; }
        .name { font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #ff0055; margin-bottom: 5px; text-transform: uppercase; }
        .bar-bg { width: 100%; height: 26px; background: rgba(255,255,255,0.1); border: 2px solid #fff; box-shadow: 0 0 15px rgba(0,0,0,0.8); position: relative; }
        .hp-bar { height: 100%; background: linear-gradient(90deg, #ff0055, #ff5500); width: 100%; transition: width 0.1s linear; }
        .ult-bar-bg { width: 100%; height: 12px; background: rgba(0,0,0,0.5); border: 1px solid #777; margin-top: 6px; }
        .ult-bar { height: 100%; background: linear-gradient(90deg, #00ffff, #0088ff); width: 0%; transition: width 0.2s linear; }
        .score { font-size: 20px; color: #ffd700; margin-top: 5px; }

        /* Screens */
        .screen { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); }
        h1 { font-size: 72px; color: #ff0033; text-shadow: 0 0 20px #ff0033, 4px 4px 0px #000; margin-bottom: 20px; letter-spacing: 2px; }
        .btn { padding: 15px 40px; font-size: 24px; font-weight: bold; background: #ff0033; color: #fff; border: none; cursor: pointer; border-radius: 4px; box-shadow: 0 0 15px #ff0033; transition: all 0.2s; margin: 10px; }
        .btn:hover { background: #fff; color: #ff0033; transform: scale(1.05); }
        
        .select-container { display: flex; gap: 20px; margin-bottom: 20px; }
        .card { width: 180px; height: 220px; border: 3px solid #444; border-radius: 8px; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; background: rgba(255,255,255,0.05); transition: 0.2s; }
        .card.selected { border-color: #ff0033; box-shadow: 0 0 20px #ff0033; background: rgba(255,0,51,0.2); }
        .card h3 { font-size: 22px; margin: 10px 0; }

        /* Ultimate Cutscene Overlay */
        #cutscene { display: none; position: absolute; width: 100%; height: 100%; background: #000; z-index: 100; justify-content: center; align-items: center; flex-direction: column; }
        #cutscene-text { font-size: 80px; color: #ff0033; text-shadow: 0 0 30px #ff0033; animation: pulse 0.5s infinite alternate; }
        @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.15); } }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="canvas-container"></div>

    <div class="ui-layer">
        <div id="hud" class="interactive">
            <div class="player-hud p1-hud">
                <div id="p1-name" class="name">DENJI</div>
                <div class="bar-bg"><div id="p1-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p1-ult" class="ult-bar"></div></div>
                <div id="p1-score" class="score">ROUND WINS: 0</div>
            </div>
            <div style="font-size: 36px; font-weight: bold; color: #fff;">VS</div>
            <div class="player-hud p2-hud">
                <div id="p2-name" class="name">POWER</div>
                <div class="bar-bg"><div id="p2-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p2-ult" class="ult-bar"></div></div>
                <div id="p2-score" class="score">ROUND WINS: 0</div>
            </div>
        </div>

        <div id="main-screen" class="screen interactive">
            <h1>CHAINSAW MAN 3D</h1>
            <p style="color:#aaa; margin-bottom: 30px;">ULTIMATE 3D FIGHTING EXPERIENCE</p>
            <button class="btn" onclick="goToModeSelect()">START GAME</button>
        </div>

        <div id="mode-screen" class="screen interactive" style="display:none;">
            <h1>SELECT MODE</h1>
            <div>
                <button class="btn" onclick="selectMode('1P')">1 PLAYER (VS AI)</button>
                <button class="btn" onclick="selectMode('2P')">2 PLAYERS (LOCAL)</button>
            </div>
        </div>

        <div id="select-screen" class="screen interactive" style="display:none;">
            <h2>SELECT CHARACTER</h2>
            <div class="select-container">
                <div class="card selected" id="c-denji" onclick="pickChar('denji')">
                    <h3>DENJI</h3>
                    <p style="font-size:12px; color:#aaa;">Chainsaw / Aggressive</p>
                </div>
                <div class="card" id="c-power" onclick="pickChar('power')">
                    <h3>POWER</h3>
                    <p style="font-size:12px; color:#aaa;">Blood Hammer / Range</p>
                </div>
                <div class="card" id="c-aki" onclick="pickChar('aki')">
                    <h3>AKI</h3>
                    <p style="font-size:12px; color:#aaa;">Fox Devil / Balanced</p>
                </div>
            </div>

            <h2>SELECT MAP</h2>
            <div class="select-container">
                <div class="card selected" id="m-city" onclick="pickMap('city')">
                    <h3>ROOFTOP</h3>
                </div>
                <div class="card" id="m-hell" onclick="pickMap('hell')">
                    <h3>DEVIL REALM</h3>
                </div>
            </div>

            <button class="btn" onclick="startGame()">FIGHT!</button>
        </div>
    </div>

    <div id="cutscene">
        <div id="cutscene-text">ULTIMATE DEVIL ATTACK!</div>
    </div>

    <script>
        // --- Game State Variables ---
        let gameMode = '1P';
        let selectedCharP1 = 'denji';
        let selectedCharP2 = 'power';
        let selectedMap = 'city';
        
        let p1Score = 0, p2Score = 0;
        let isGaming = false;
        let isCutscene = false;

        // Player Data Object Template
        function createPlayer(name, color, xPos, isAI) {
            return {
                name: name,
                hp: 100,
                ult: 0,
                comboCount: 0,
                isHit: false,
                isAttacking: false,
                isAI: isAI,
                position: { x: xPos, y: 1, z: 0 },
                mesh: null,
                color: color,
                keys: {}
            };
        }

        let P1, P2;

        // Key Configs
        const keysPressed = {};

        window.addEventListener('keydown', (e) => {
            keysPressed[e.key.toLowerCase()] = true;
            handleSkillCombinations();
        });

        window.addEventListener('keyup', (e) => {
            keysPressed[e.key.toLowerCase()] = false;
        });

        // --- UI Navigation ---
        function goToModeSelect() {
            document.getElementById('main-screen').style.display = 'none';
            document.getElementById('mode-screen').style.display = 'flex';
        }

        function selectMode(mode) {
            gameMode = mode;
            document.getElementById('mode-screen').style.display = 'none';
            document.getElementById('select-screen').style.display = 'flex';
        }

        function pickChar(char) {
            selectedCharP1 = char;
            selectedCharP2 = char === 'denji' ? 'power' : 'denji';
            document.querySelectorAll('.select-container')[0].querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
            document.getElementById('c-' + char).classList.add('selected');
        }

        function pickMap(map) {
            selectedMap = map;
            document.querySelectorAll('.select-container')[1].querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
            document.getElementById('m-' + map).classList.add('selected');
        }

        // --- 3D Engine Setup (Three.js) ---
        let scene, camera, renderer;
        let p1Mesh, p2Mesh, stageFloor, light;

        function init3D() {
            const container = document.getElementById('canvas-container');
            scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x050505, 0.015);

            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 5, 15);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
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
            
            // Body
            const bodyGeo = new THREE.BoxGeometry(1, 2, 0.6);
            const bodyMat = new THREE.MeshStandardMaterial({ color: color, metalness: 0.5, roughness: 0.2 });
            const body = new THREE.Mesh(bodyGeo, bodyMat);
            body.castShadow = true;
            group.add(body);

            // Head / Glowing Accents
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

            setupStage(selectedMap);

            P1 = createPlayer(selectedCharP1.toUpperCase(), 0xff0055, -4, false);
            P2 = createPlayer(selectedCharP2.toUpperCase(), 0x0088ff, 4, gameMode === '1P');

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

        // --- Logic & Control Mechanics ---
        function handleInput() {
            if (!isGaming || isCutscene) return;

            // Player 1 Control (WASD)
            if (keysPressed['a'] && P1.position.x > -13) P1.position.x -= 0.12;
            if (keysPressed['d'] && P1.position.x < 13) P1.position.x += 0.12;
            
            // Basic Attack
            if (keysPressed['f']) executeSkill(P1, P2, 'SKILL_A', 5, 8);
            if (keysPressed['g']) executeSkill(P1, P2, 'SKILL_B', 7, 10);
            if (keysPressed['h']) executeUltimate(P1, P2);

            // Player 2 Control (Arrow Keys) / AI Mode
            if (!P2.isAI) {
                if (keysPressed['arrowleft'] && P2.position.x > -13) P2.position.x -= 0.12;
                if (keysPressed['arrowright'] && P2.position.x < 13) P2.position.x += 0.12;
                if (keysPressed['1']) executeSkill(P2, P1, 'SKILL_A', 5, 8);
                if (keysPressed['2']) executeSkill(P2, P1, 'SKILL_B', 7, 10);
                if (keysPressed['3']) executeUltimate(P2, P1);
            } else {
                updateAI();
            }
        }

        // Skill Combination Logic (Dual key press creates Combo Fusion Skill)
        function handleSkillCombinations() {
            if (!isGaming || isCutscene) return;
            
            // P1 Combination: F + G
            if (keysPressed['f'] && keysPressed['g']) {
                executeSkill(P1, P2, 'FUSION_COMBO', 18, 25);
            }
            // P2 Combination: 1 + 2
            if (!P2.isAI && keysPressed['1'] && keysPressed['2']) {
                executeSkill(P2, P1, 'FUSION_COMBO', 18, 25);
            }
        }

        // Simple Smart AI System
        function updateAI() {
            const dist = P1.position.x - P2.position.x;
            if (Math.abs(dist) > 2) {
                P2.position.x += dist > 0 ? 0.08 : -0.08;
            } else {
                if (Math.random() < 0.05) executeSkill(P2, P1, 'SKILL_A', 5, 8);
                if (P2.ult >= 100) executeUltimate(P2, P1);
            }
        }

        // Combat Mechanics & Combo Escape System
        function executeSkill(attacker, defender, skillType, damage, ultGain) {
            if (attacker.isAttacking) return;
            attacker.isAttacking = true;

            const distance = Math.abs(attacker.position.x - defender.position.x);
            
            // Trigger Visual FX Mesh Movement
            attacker.mesh.position.z = 0.5;
            setTimeout(() => { attacker.mesh.position.z = 0; attacker.isAttacking = false; }, 200);

            if (distance < 2.5) {
                // Damage Logic
                defender.hp -= damage;
                defender.comboCount++;
                attacker.ult = Math.min(100, attacker.ult + ultGain);

                // Anti-Infinite Combo System (Automated Escape Mechanism)
                if (defender.comboCount >= 3) {
                    defender.position.x += (defender.position.x > attacker.position.x ? 3 : -3); // Evade Backwards
                    defender.comboCount = 0; // Reset Combo Break
                }

                if (defender.hp <= 0) handleRoundEnd(attacker);
                updateHUD();
            }
        }

        // Cinematic Ultimate System
        function executeUltimate(attacker, defender) {
            if (attacker.ult < 100 || isCutscene) return;
            
            attacker.ult = 0;
            isCutscene = true;

            const cutsceneEl = document.getElementById('cutscene');
            const cutsceneText = document.getElementById('cutscene-text');
            cutsceneText.innerText = attacker.name + " ULTIMATE EXECUTION!";
            cutsceneEl.style.display = 'flex';

            // Dynamic Camera Dramatic Move
            camera.position.set(attacker.position.x, 3, 4);

            setTimeout(() => {
                cutsceneEl.style.display = 'none';
                camera.position.set(0, 5, 15);
                
                // Massive Ultimate Damage & Dual Combo Attack Execution
                defender.hp -= 40;
                isCutscene = false;
                
                if (defender.hp <= 0) handleRoundEnd(attacker);
                updateHUD();
            }, 1800);
        }

        function handleRoundEnd(winner) {
            if (winner === P1) p1Score++;
            else p2Score++;

            document.getElementById('p1-score').innerText = `ROUND WINS: ${p1Score}`;
            document.getElementById('p2-score').innerText = `ROUND WINS: ${p2Score}`;

            if (p1Score >= 2 || p2Score >= 2) {
                alert(`${winner.name} WINS THE MATCH!`);
                p1Score = 0; p2Score = 0;
                document.getElementById('hud').style.display = 'none';
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

        // Main Game Render Loop (60 FPS)
        function animate() {
            if (!isGaming) return;
            requestAnimationFrame(animate);

            handleInput();

            // Synchronize Mesh Positions with Game Engine State
            if (P1.mesh) P1.mesh.position.x = P1.position.x;
            if (P2.mesh) P2.mesh.position.x = P2.position.x;

            // Camera Tracking Smoothly
            if (!isCutscene) {
                const midPoint = (P1.position.x + P2.position.x) / 2;
                camera.position.x += (midPoint - camera.position.x) * 0.05;
            }

            renderer.render(scene, camera);
        }

        // Initialize 3D Engine on load
        init3D();
    </script>
</body>
</html>
"""

# Streamlit 내부에 렌더링 (전체 화면 높이 설정)
components.html(game_html, height=850, scrolling=False)
