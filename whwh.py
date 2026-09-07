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

        /* 애니메이션 궁극기 연출 컷씬 */
        #cutscene { display: none; position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 100; justify-content: center; align-items: center; flex-direction: column; overflow: hidden; }
        #cutscene-img { width: 340px; height: 340px; border-radius: 12px; border: 5px solid #ff0033; box-shadow: 0 0 80px #ff0033; background-size: cover; background-position: center; animation: animeZoom 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        #cutscene-text { font-size: 50px; color: #ff0033; font-weight: 900; text-shadow: 0 0 40px #ff0033; margin-top: 25px; font-style: italic; animation: textPulse 0.3s infinite alternate; }
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
                <div id="p1-trans" class="transform-badge">HYBRID MODE</div>
            </div>
            <div style="font-size: 32px; font-weight: 900; color: #fff; font-style: italic; text-shadow: 0 0 10px #ff0055;">VS</div>
            <div class="player-hud p2-hud">
                <div id="p2-name" class="name">파워</div>
                <div class="bar-bg"><div id="p2-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p2-ult" class="ult-bar"></div></div>
                <div id="p2-trans" class="transform-badge">HYBRID MODE</div>
            </div>
        </div>

        <div id="main-screen" class="screen interactive">
            <h1>체인소맨 하이브리드</h1>
            <p style="color:#aaa; margin-bottom: 25px;">애니메이션 명장면 연출 대전 격투</p>
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
            <div class="ctrl-btn jump-btn" onclick="triggerAction('P1','JUMP')">점프<br>(W)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','SKILL_A')">스킬1<br>(F)</div>
            <div class="ctrl-btn" onclick="triggerAction('P1','SKILL_B')">스킬2<br>(G)</div>
            <div class="ctrl-btn trans-btn" onclick="triggerAction('P1','TRANS')">변신<br>(V)</div>
            <div class="ctrl-btn ult-btn" onclick="triggerAction('P1','ULT')">궁극기<br>(H)</div>
        </div>
        <div class="panel">
            <div class="ctrl-btn" onclick="triggerAction('P2','LEFT')">◀<br>(←)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','RIGHT')">▶<br>(→)</div>
            <div class="ctrl-btn jump-btn" onclick="triggerAction('P2','JUMP')">점프<br>(↑)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','SKILL_A')">스킬1<br>(1)</div>
            <div class="ctrl-btn" onclick="triggerAction('P2','SKILL_B')">스킬2<br>(2)</div>
            <div class="ctrl-btn trans-btn" onclick="triggerAction('P2','TRANS')">변신<br>(0)</div>
            <div class="ctrl-btn ult-btn" onclick="triggerAction('P2','ULT')">궁극기<br>(3)</div>
        </div>
    </div>

    <div id="cutscene">
        <div id="cutscene-img"></div>
        <div id="cutscene-text">필살 각성!</div>
    </div>

    <script>
        // 애니메이션 명장면 구글 이미지 링크 적용
        const CHARACTERS = {
            denji: { 
                name: '덴지', hair: '#f5d442', shirt: '#ffffff', pants: '#222222', isHybrid: true, 
                img: 'https://images.justwatch.com/poster/301548683/s718/chainsaw-man.jpg', 
                ultImg: 'https://m.media-amazon.com/images/M/MV5BODA0ZWY2NDgtYTFkMi00ZDkyLWE3MGEtNTlhY2JkNWU0MTUxXkEyXkFqcGc@._V1_.jpg',
                type: '체인소 하이브리드' 
            },
            power: { 
                name: '파워', hair: '#e0a367', shirt: '#aa2222', pants: '#111122', is
