<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pixel Action Game</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #050505;
            font-family: 'Courier New', Courier, monospace;
        }

        #game-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* 메인 게임 캔버스 */
        canvas {
            background: #111318;
            image-rendering: pixelated; /* 픽셀 선명도 강화 */
            box-shadow: 0 0 30px rgba(0,0,0,0.8);
        }

        /* 스타트 화면 오버레이 */
        #start-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.4);
        }

        /* 유튜브 배경 영상 */
        #video-background {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100vw;
            height: 56.25vw; /* 16:9 비율 유지 */
            min-height: 100vh;
            min-width: 177.77vh;
            transform: translate(-50%, -50%);
            z-index: 1;
            pointer-events: none;
            filter: brightness(0.6) contrast(1.1);
        }

        /* UI 엘리먼트 */
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 5;
            pointer-events: none;
        }

        .start-btn {
            pointer-events: auto;
            position: relative;
            z-index: 11;
            padding: 18px 45px;
            font-size: 28px;
            font-weight: bold;
            color: #fff;
            background: linear-gradient(45deg, #ff0055, #ff5500);
            border: 4px solid #fff;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(255, 85, 0, 0.6);
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .start-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.9);
            background: linear-gradient(45deg, #ff2277, #ff7722);
        }

        .title-text {
            position: relative;
            z-index: 11;
            color: #fff;
            font-size: 48px;
            font-weight: 900;
            text-shadow: 3px 3px 0px #ff0055, -3px -3px 0px #00e5ff;
            margin-bottom: 30px;
            text-align: center;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <!-- 배경 유튜브 영상 (요청 영상) -->
        <iframe id="video-background" 
            src="https://www.youtube.com/embed/l9E-dh9kf_0?autoplay=1&mute=1&controls=0&loop=1&playlist=l9E-dh9kf_0&enablejsapi=1" 
            frameborder="0" 
            allow="autoplay; encrypted-media">
        </iframe>

        <!-- 스타트 UI 오버레이 -->
        <div id="start-screen">
            <h1 class="title-text">PIXEL ACTION</h1>
            <button class="start-btn" id="start-btn">GAME START</button>
        </div>

        <!-- 게임 캔버스 -->
        <canvas id="gameCanvas" width="960" height="540"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const startScreen = document.getElementById('start-screen');
        const startBtn = document.getElementById('start-btn');

        let gameRunning = false;
        let keys = {};
        let particles = [];
        let screenShakeTime = 0;

        // 플레이어 객체 (디테일 픽셀 표현 및 화려한 이펙트 추가)
        const player = {
            x: 100,
            y: 380,
            width: 32,
            height: 48,
            vx: 0,
            vy: 0,
            speed: 5,
            isGrounded: false,
            facing: 'right',
            ultGauge: 0,       // 궁극기 게이지 (0 ~ 100)
            maxUltGauge: 100,
            isChargingSkill: false,
            afterImages: []    // 잔상 이펙트용
        };

        // 입력 처리
        window.addEventListener('keydown', e => keys[e.code] = true);
        window.addEventListener('keyup', e => keys[e.code] = false);

        startBtn.addEventListener('click', () => {
            startScreen.style.display = 'none';
            document.getElementById('video-background').style.display = 'none'; // 시작 시 비디오 숨김
            gameRunning = true;
            gameLoop();
        });

        // 화려한 파티클 생성 함수
        function createParticles(x, y, color, count, speedMultiplier = 1) {
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 8 * speedMultiplier,
                    vy: (Math.random() - 0.5) * 8 * speedMultiplier,
                    size: Math.random() * 6 + 2,
                    color: color,
                    life: 1.0,
                    decay: Math.random() * 0.03 + 0.02
                });
            }
        }

        // 스킬 사용 함수
        function triggerSkill() {
            createParticles(player.x + player.width / 2, player.y + player.height / 2, '#00e5ff', 30, 1.5);
            screenShakeTime = 10;
            
            // 궁극기 게이지 차오름
            player.ultGauge = Math.min(player.maxUltGauge, player.ultGauge + 25);
        }

        // 궁극기 발동 함수
        function triggerUltimate() {
            if (player.ultGauge >= player.maxUltGauge) {
                player.ultGauge = 0;
                screenShakeTime = 25;
                createParticles(player.x + player.width / 2, player.y + player.height / 2, '#ff0055', 100, 3);
                createParticles(player.x + player.width / 2, player.y + player.height / 2, '#ffcc00', 80, 2);
            }
        }

        // 키 입력에 따른 스킬 및 동작 처리
        window.addEventListener('keydown', (e) => {
            if (!gameRunning) return;

            if (e.code === 'KeyZ') triggerSkill();      // Z키: 화려한 기본 스킬
            if (e.code === 'KeyX') triggerUltimate();   // X키: 궁극기
        });

        function update() {
            // 이동 로직
            if (keys['ArrowLeft'] || keys['KeyA']) {
                player.vx = -player.speed;
                player.facing = 'left';
            } else if (keys['ArrowRight'] || keys['KeyD']) {
                player.vx = player.speed;
                player.facing = 'right';
            } else {
                player.vx = 0;
            }

            // 점프
            if ((keys['ArrowUp'] || keys['KeyW'] || keys['Space']) && player.isGrounded) {
                player.vy = -12;
                player.isGrounded = false;
                createParticles(player.x + player.width / 2, player.y + player.height, '#ffffff', 10);
            }

            // 중력
            player.vy += 0.6;
            player.x += player.vx;
            player.y += player.vy;

            // 바닥 충돌
            if (player.y >= 380) {
                player.y = 380;
                player.vy = 0;
                player.isGrounded = true;
            }

            // 잔상 이펙트 추가 (이동 시)
            if (Math.abs(player.vx) > 0) {
                player.afterImages.push({
                    x: player.x,
                    y: player.y,
                    alpha: 0.6,
                    color: player.facing === 'right' ? '#00e5ff' : '#ff0055'
                });
            }

            // 잔상 업데이트
            player.afterImages.forEach((img, index) => {
                img.alpha -= 0.05;
                if (img.alpha <= 0) player.afterImages.splice(index, 1);
            });

            // 파티클 업데이트
            particles.forEach((p, index) => {
                p.x += p.vx;
                p.y += p.vy;
                p.life -= p.decay;
                if (p.life <= 0) particles.splice(index, 1);
            });

            // 화면 흔들림 감쇠
            if (screenShakeTime > 0) screenShakeTime--;
        }

        function drawPixelPlayer(x, y, facing) {
            // 디테일한 픽셀 캐릭터 표현 (레이어별 픽셀 그리기)
            ctx.fillStyle = '#ffcc99'; // 피부
            ctx.fillRect(x + 8, y + 4, 16, 12);

            ctx.fillStyle = '#333333'; // 머리카락
            ctx.fillRect(x + 6, y, 20, 8);

            ctx.fillStyle = '#0055ff'; // 상의
            ctx.fillRect(x + 4, y + 16, 24, 18);

            ctx.fillStyle = '#111111'; // 하의
            ctx.fillRect(x + 6, y + 34, 20, 14);

            // 눈 (방향)
            ctx.fillStyle = '#ffffff';
            let eyeOffset = facing === 'right' ? 16 : 8;
            ctx.fillRect(x + eyeOffset, y + 8, 4, 4);
            ctx.fillStyle = '#000000';
            ctx.fillRect(x + eyeOffset + (facing === 'right' ? 2 : 0), y + 9, 2, 2);
        }

        function drawUI() {
            // UI: 궁극기 게이지 바 복원
            const barX = 30;
            const barY = 30;
            const barWidth = 200;
            const barHeight = 20;

            // 테두리 및 배경
            ctx.fillStyle = '#222';
            ctx.fillRect(barX - 4, barY - 4, barWidth + 8, barHeight + 8);
            ctx.fillStyle = '#444';
            ctx.fillRect(barX, barY, barWidth, barHeight);

            // 채워지는 게이지
            const currentWidth = (player.ultGauge / player.maxUltGauge) * barWidth;
            const gaugeColor = player.ultGauge >= player.maxUltGauge ? '#ff0055' : '#00e5ff';
            ctx.fillStyle = gaugeColor;
            ctx.fillRect(barX, barY, currentWidth, barHeight);

            // 텍스트 UI
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 12px Courier New';
            ctx.fillText(`ULTIMATE [X]: ${player.ultGauge}%`, barX, barY - 8);

            if (player.ultGauge >= player.maxUltGauge) {
                ctx.fillStyle = '#ff0055';
                ctx.font = 'bold 14px Courier New';
                ctx.fillText('READY!', barX + barWidth + 12, barY + 15);
            }
        }

        function render() {
            ctx.save();

            // 화면 흔들림 효과 적용
            if (screenShakeTime > 0) {
                let dx = (Math.random() - 0.5) * screenShakeTime;
                let dy = (Math.random() - 0.5) * screenShakeTime;
                ctx.translate(dx, dy);
            }

            // 배경 클리어
            ctx.fillStyle = '#1a1d24';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 바닥 그리드 픽셀 연출
            ctx.fillStyle = '#2c313d';
            ctx.fillRect(0, 428, canvas.width, 112);
            ctx.fillStyle = '#00e5ff';
            ctx.fillRect(0, 428, canvas.width, 2); // 네온 라인

            // 잔상 표현
            player.afterImages.forEach(img => {
                ctx.globalAlpha = img.alpha;
                ctx.fillStyle = img.color;
                ctx.fillRect(img.x, img.y, player.width, player.height);
            });
            ctx.globalAlpha = 1.0;

            // 디테일 픽셀 플레이어 그리기
            drawPixelPlayer(player.x, player.y, player.facing);

            // 파티클 그리기 (화려한 스킬 이펙트)
            particles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.life;
                ctx.fillRect(p.x, p.y, p.size, p.size);
            });
            ctx.globalAlpha = 1.0;

            ctx.restore();

            // UI 그리기는 화면 흔들림 영향 없이 고정
            drawUI();
        }

        function gameLoop() {
            if (!gameRunning) return;
            update();
            render();
            requestAnimationFrame(gameLoop);
        }
    </script>
</body>
</html>
