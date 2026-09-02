import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨: 하이브리드 클래시", layout="wide")

# r"""...""" (Raw String)을 사용하여 파이썬 이스케이프 문자 오류를 해결했습니다.
game_html = r"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>체인소맨 3D 격투</title>
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
        .transform-badge { font-size: 14px; color: #00ffcc; font-weight: bold; display: none; margin-top: 3px; }

        /* 조작 가이드 패널 */
        #touch-controls { display: none; position: absolute; bottom: 15px; width: 100%; padding: 0 20px; box-sizing: border-box; justify-content: space-between; align-items: flex-end; z-index: 20; }
        .panel { background: rgba(0,0,0,0.7); border: 1px solid #444; border-radius: 12px; padding: 10px; display: flex; gap: 8px; backdrop-filter: blur(5px); }
        .ctrl-btn { width: 55px; height: 55px; background: rgba(255,255,255,0.1); border: 2px solid #fff; border-radius: 8px; color: #fff; font-size: 13px; font-weight: bold; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; text-align: center; }
        .ctrl-btn:active { background: #ff0033; transform: scale(0.95); }
        .trans-btn { border-color: #00ffcc; color: #00ffcc; }
        .ult-btn { border-color: #ff0055; background: rgba(255,0,85,0.5); }

        /* 메뉴 레이아웃 */
        .screen { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); }
        h1 { font-size: 52px; color: #ff0033; text-shadow: 0 0 20px #ff0033; margin-bottom: 5px; font-weight: 900; }
        .btn { padding: 12px 35px; font-size: 20px; font-weight: bold; background: #ff0033; color: #fff; border: none; cursor: pointer; border-radius: 6px; box-shadow: 0 0 15px #ff0033; transition: all 0.2s; margin: 8px; }
        .btn:hover { background: #fff; color: #ff0033; transform: scale(1.05); }
        
        .select-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; max-width: 900px; margin-bottom: 15px; }
        .card { width: 110px; height: 160px; border: 3px solid #444; border-radius: 10px; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; cursor: pointer; background-size: cover; background-position: center; transition: 0.2s; position: relative; overflow: hidden; }
        .card .card-info { width: 100%; background: rgba(0,0,0,0.8); text-align: center; padding: 4px 0; border-top: 1px solid rgba(255,255,255,0.2); }
        .card.selected-p1 { border-color: #ff0055; box-shadow: 0 0 15px #ff0055; transform: scale(1.05); }
        .card.selected-p2 { border-color: #0088ff; box-shadow: 0 0 15px #0088ff; transform: scale(1.05); }
        .card h3 { font-size: 15px; margin: 0; color: #fff; }
        .card p { font-size: 10px; color: #ffcc00; margin: 1px 0 0 0; }

        /* 궁극기 컷씬 연출 */
        #cutscene { display: none; position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 100; justify-content: center; align-items: center; flex-direction: column; }
        #cutscene-img { width: 320px; height: 320px; border-radius: 50%; border: 5px solid #ff0033; box-shadow: 0 0 50px #ff0033; background-size: cover; background-position: center; animation: zoomIn 0.3s ease-out; }
        #cutscene-text { font-size: 50px; color: #ff0033; font-weight: 900; text-shadow: 0 0 30px #ff0033; margin-top: 20px; animation: pulse 0.4s infinite alternate; }
        @keyframes zoomIn { from { transform: scale(0); } to { transform: scale(1); } }
        @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.1); } }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="canvas-container"></div>

    <div class="ui-layer">
        <div id="hud" class="interactive">
            <div class="player-hud p1-hud">
                <div id="p1-name" class="name">덴지</div>
                <div class="bar-bg"><div id="p1-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p1-ult" class="ult-bar"></div></div>
                <div id="p1-trans" class="transform-badge">HYBRID MODE</div>
            </div>
            <div style="font-size: 28px; font-weight: 900; color: #fff;">VS</div>
            <div class="player-hud p2-hud">
                <div id="p2-name" class="name">파워</div>
                <div class="bar-bg"><div id="p2-hp" class="hp-bar"></div></div>
                <div class="ult-bar-bg"><div id="p2-ult" class="ult-bar"></div></div>
                <div id="p2-trans" class="transform-badge">HYBRID MODE</div>
            </div>
        </div>

        <div id="main-screen" class="screen interactive">
            <h1>체인소맨 3D</h1>
            <p style="color:#aaa; margin-bottom: 20px;">하이브리드 악마들의 난투격투</p>
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
                <div class="card selected-p1" id="m-city" onclick="pickMap('city')" style="width:120px; height:70px; background:#222; justify-content:center;">
                    <h3>도쿄 옥상</h3>
                </div>
                <div class="card" id="m-hell" onclick="pickMap('hell')" style="width:120px; height:70px; background:#400; justify-content:center;">
                    <h3>악마의 지옥</h3>
                </div>
                <div class="card" id="m-beach" onclick="pickMap('beach')" style="width:120px; height:70px; background:#004; justify-content:center;">
                    <h3>신소 해변</h3>
                </div>
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
            <div class="ctrl-btn" onclick="triggerAction('P2','SKILL_A')">스킬1
