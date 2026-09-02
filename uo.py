import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="체인소맨: 하이브리드 클래시", layout="wide")

game_html = """<!DOCTYPE html>
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

        /* 메뉴
