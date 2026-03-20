import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random, os, shutil, json
from datetime import datetime

# ══════════════════════════════════════
# 페이지 설정
# ══════════════════════════════════════
st.set_page_config(
    page_title="🧚 서울 쓰레기 요정",
    page_icon="🧚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════
# CSS
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nanum Gothic', sans-serif;
    background: #F4F6FB;
}
.stApp > header                       { display: none !important; }
div[data-testid="stMain"]             { padding-top: 0 !important; }
div[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
.block-container {
    padding-top: 1rem !important;
    padding-left: 1.8rem !important;
    padding-right: 1.8rem !important;
    max-width: 100% !important;
}

/* ══ 사이드바 ══ */
section[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1.5px solid #E8ECF4 !important;
    min-width: 250px !important;
    max-width: 250px !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown div,
section[data-testid="stSidebar"] label { color: #2D3748 !important; }
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5 { color: #1A202C !important; }
section[data-testid="stSidebar"] svg { fill: #4A5568 !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #F7FAFC !important;
    border-color: #CBD5E0 !important;
    border-radius: 10px !important;
    color: #2D3748 !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    border-radius: 10px; padding: 9px 14px; display: block;
    transition: background 0.15s; cursor: pointer;
    color: #4A5568 !important; font-weight: 700; font-size: 0.9rem;
    margin-bottom: 2px;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
    background: #EBF8F3; color: #2D9A6B !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] input:checked + div {
    background: linear-gradient(90deg,#3ECF8E22,#1AA7EC11);
    border-radius: 10px;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] input:checked + div p {
    color: #2D9A6B !important; font-weight: 800 !important;
}

/* ══ 상단 헤더 ══ */
.topbar {
    background: linear-gradient(135deg, #3ECF8E, #1AA7EC);
    border-radius: 16px; padding: 20px 28px; color: white;
    margin-bottom: 22px; display: flex; align-items: center; justify-content: space-between;
}
.topbar h1 { font-size: 1.5rem; font-weight: 800; margin: 0; }
.topbar p  { font-size: 0.84rem; opacity: 0.85; margin: 3px 0 0; }
.topbar-badge {
    background: rgba(255,255,255,0.22); border-radius: 20px; padding: 8px 18px;
    font-size: 0.88rem; font-weight: 800; white-space: nowrap;
}

/* ══ 카드 ══ */
.card {
    background: white; border-radius: 16px; padding: 18px 20px;
    margin-bottom: 14px; box-shadow: 0 2px 14px rgba(0,0,0,0.07);
}
.card-title {
    font-size: 0.73rem; font-weight: 700; color: #999;
    text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;
}
.sec-title {
    font-size: 1.05rem; font-weight: 800; color: #1A1A2E;
    margin: 14px 0 10px; display: flex; align-items: center; gap: 6px;
}

/* ══ 배너 ══ */
.banner-red    { background:#FF6B6B; color:white; border-radius:12px; padding:12px 18px; margin-bottom:16px; font-size:0.88rem; font-weight:700; }
.banner-green  { background:#3ECF8E; color:white; border-radius:12px; padding:12px 18px; margin-bottom:16px; font-size:0.88rem; font-weight:700; }
.banner-orange { background:#FFB347; color:white; border-radius:12px; padding:12px 18px; margin-bottom:16px; font-size:0.88rem; font-weight:700; }

/* ══ 지표 ══ */
.metric-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:16px; }
.metric-box  { background:white; border-radius:14px; padding:16px; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.06); border-top:3px solid transparent; }
.metric-val  { font-size:1.8rem; font-weight:800; line-height:1; }
.metric-unit { font-size:0.72rem; color:#999; margin-top:4px; }
.metric-lbl  { font-size:0.72rem; font-weight:700; margin-top:4px; }

/* ══ 요일 뱃지 ══ */
.days-wrap { display:flex; gap:5px; flex-wrap:wrap; margin:8px 0; }
.day-on  { background:#3ECF8E; color:white;  padding:5px 11px; border-radius:10px; font-size:0.83rem; font-weight:700; display:inline-block; }
.day-off { background:#F0F2F5; color:#C0C7D0; padding:5px 11px; border-radius:10px; font-size:0.83rem; font-weight:700; display:inline-block; }

/* ══ 스케줄 카드 ══ */
.sched-card { background:white; border-radius:14px; padding:16px 18px; margin-bottom:12px; box-shadow:0 2px 10px rgba(0,0,0,0.06); border-left:4px solid #3ECF8E; }
.sched-header { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.sched-time { margin-left:auto; font-size:0.8rem; color:#FF6B6B; font-weight:700; background:#FFF3F3; padding:3px 10px; border-radius:8px; }

/* ══ 도감 ══ */
.waste-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(290px,1fr)); gap:14px; margin-bottom:16px; }
.waste-card { background:white; border-radius:14px; padding:16px; box-shadow:0 2px 10px rgba(0,0,0,0.06); display:flex; align-items:flex-start; gap:12px; transition:box-shadow 0.2s,transform 0.2s; }
.waste-card:hover { box-shadow:0 6px 20px rgba(0,0,0,0.12); transform:translateY(-2px); }
.waste-emoji { font-size:2.2rem; flex-shrink:0; }
.waste-info  { flex:1; min-width:0; }
.waste-name  { font-size:1rem; font-weight:800; color:#1A1A2E; }
.waste-cat   { display:inline-block; padding:2px 9px; border-radius:8px; font-size:0.72rem; font-weight:700; margin:4px 0 6px; }
.waste-step  { font-size:0.8rem; color:#555; line-height:1.6; }
.tip-chip    { background:#E8FFF5; color:#00A86B; border-radius:8px; padding:5px 10px; font-size:0.77rem; font-weight:700; margin-top:6px; display:block; }
.warn-chip   { background:#FFF8E1; color:#F57F17; border-radius:8px; padding:5px 10px; font-size:0.77rem; font-weight:700; margin-top:4px; display:block; }

/* ══ 포인트 ══ */
.pt-hero { background:linear-gradient(135deg,#FFD93D,#FF9A3C); border-radius:16px; padding:24px 28px; color:white; display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }
.pt-hero-num { font-size:3.2rem; font-weight:800; line-height:1; }
.pt-hero-sub { font-size:0.85rem; opacity:0.85; }
.char-box { background:white; border-radius:16px; padding:22px; box-shadow:0 2px 14px rgba(0,0,0,0.07); display:flex; align-items:center; gap:18px; margin-bottom:16px; }
.xp-track { height:9px; background:#F0F2F5; border-radius:5px; margin-top:8px; overflow:hidden; }
.xp-fill  { height:100%; border-radius:5px; background:linear-gradient(90deg,#3ECF8E,#1AA7EC); }
.xp-label { font-size:0.73rem; color:#999; margin-top:3px; }
.earn-pts { display:inline-block; background:linear-gradient(90deg,#FFD93D,#FF9A3C); color:white; border-radius:8px; padding:3px 10px; font-size:0.8rem; font-weight:800; margin-bottom:10px; }
.spend-box { background:white; border-radius:14px; padding:18px 12px; box-shadow:0 2px 10px rgba(0,0,0,0.06); text-align:center; transition:transform 0.15s; }
.spend-box:hover { transform:translateY(-2px); }
.spend-icon { font-size:2rem; display:block; margin-bottom:6px; }
.spend-name { font-size:0.82rem; font-weight:700; color:#333; }
.spend-pts  { font-size:0.82rem; color:#FF6B6B; font-weight:800; margin-top:3px; }
.lv-box { background:white; border-radius:14px; padding:18px 12px; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.05); border:2px solid #F0F2F5; }
.lv-box.done { border-color:#3ECF8E; background:#F0FDF6; }

/* ══ 내 현황 ══ */
.profile-hero {
    background: linear-gradient(135deg, #667EEA, #764BA2);
    border-radius: 20px; padding: 28px 32px; color: white;
    display: flex; align-items: center; gap: 24px; margin-bottom: 20px;
}
.profile-avatar { font-size: 4rem; background: rgba(255,255,255,0.2); border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.profile-name  { font-size: 1.3rem; font-weight: 800; }
.profile-sub   { font-size: 0.85rem; opacity: 0.85; margin-top: 4px; }
.profile-stats { display: flex; gap: 28px; margin-top: 12px; }
.profile-stat  { text-align: center; }
.profile-stat-val { font-size: 1.5rem; font-weight: 800; }
.profile-stat-lbl { font-size: 0.72rem; opacity: 0.8; }
.history-item {
    background: white; border-radius: 12px; padding: 12px 16px;
    margin-bottom: 8px; display: flex; align-items: center; gap: 14px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}
.history-icon { font-size: 1.4rem; flex-shrink: 0; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.history-plus  { color: #3ECF8E; font-size: 0.9rem; font-weight: 800; margin-left: auto; }
.history-minus { color: #FF6B6B; font-size: 0.9rem; font-weight: 800; margin-left: auto; }
.discharge-row {
    background: white; border-radius: 12px; padding: 14px 18px;
    margin-bottom: 8px; display: flex; align-items: center;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05); gap: 14px;
}

/* ══ 지도 ══ */
.map-wrap  { background:white; border-radius:16px; padding:18px; box-shadow:0 2px 14px rgba(0,0,0,0.07); }
.gu-path   { cursor:pointer; stroke:white; stroke-width:1.5; transition:all 0.2s; }
.gu-path:hover { stroke:#1C3F6E; stroke-width:2.5; filter:brightness(0.82); }

/* ══ 종량제 가격 카드 ══ */
.price-panel {
    background: white; border-radius: 16px; padding: 20px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.07);
}
.price-panel-title {
    font-size: 1.05rem; font-weight: 800; color: #1A1A2E;
    margin-bottom: 14px; display: flex; align-items: center; gap: 6px;
}
.price-tab-row {
    display: flex; gap: 6px; margin-bottom: 14px; flex-wrap: wrap;
}
.price-tab {
    padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;
    border: 1.5px solid #E2E8F0; background: #F7FAFC; color: #4A5568; cursor: pointer;
    transition: all 0.15s;
}
.price-tab.active { background: #3ECF8E; color: white; border-color: #3ECF8E; }
.price-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 8px;
    margin-bottom: 10px;
}
.price-cell {
    background: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 10px;
    padding: 10px 6px; text-align: center;
}
.price-cell-size { font-size: 0.72rem; color: #94A3B8; font-weight: 700; margin-bottom: 4px; }
.price-cell-val  { font-size: 1.05rem; font-weight: 800; color: #15803D; }
.price-cell-won  { font-size: 0.68rem; color: #94A3B8; margin-top: 1px; }
.price-empty {
    text-align: center; padding: 2rem; color: #A0AEC0; font-size: 0.85rem;
}

/* 순위 / 연락처 */
.rank-item { background:white; border-radius:10px; padding:9px 14px; margin:4px 0; display:flex; align-items:center; gap:10px; box-shadow:0 1px 6px rgba(0,0,0,0.05); }
.contact-box { background:white; border-radius:14px; padding:16px 18px; box-shadow:0 2px 10px rgba(0,0,0,0.06); display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.no-day-box { background:#FFF3F3; border-radius:12px; padding:10px 16px; border-left:4px solid #FF6B6B; font-size:0.83rem; color:#CC3333; margin-bottom:12px; }

div[data-testid="stButton"] > button { border-radius:12px !important; font-weight:700 !important; font-family:'Nanum Gothic',sans-serif !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# 파일 복사
# ══════════════════════════════════════
for src, dst in [
    ("/mnt/user-data/uploads/seoul_data.xlsx",   "seoul_data.xlsx"),
    ("/mnt/user-data/uploads/seoul_garbage.csv", "seoul_garbage.csv"),
    ("/mnt/user-data/uploads/trashbag.csv",      "trashbag.csv"),
]:
    if not os.path.exists(dst) and os.path.exists(src):
        shutil.copy(src, dst)


# ══════════════════════════════════════
# 데이터 로딩
# ══════════════════════════════════════
@st.cache_data
def load_amount():
    df = pd.read_excel("seoul_data.xlsx", sheet_name="데이터", header=None)
    df.columns = ["구","1인당","총량","주민수"]
    df = df.iloc[2:].copy()
    df = df[df["구"] != "계"]
    df["구"] = df["구"].str.strip()
    for c in ["1인당","총량","주민수"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    def lv(v): return "red" if v >= 2.0 else ("orange" if v >= 1.2 else "green")
    df["등급"] = df["1인당"].apply(lv)
    return df.set_index("구")

@st.cache_data
def load_schedule():
    df = pd.read_csv("seoul_garbage.csv", encoding="cp949")
    keep = [
        "시군구명","배출장소유형","배출장소",
        "생활쓰레기배출방법","음식물쓰레기배출방법","재활용품배출방법",
        "일시적다량폐기물배출방법","일시적다량폐기물배출장소",
        "생활쓰레기배출요일","음식물쓰레기배출요일","재활용품배출요일",
        "생활쓰레기배출시작시각","생활쓰레기배출종료시각",
        "음식물쓰레기배출시작시각","음식물쓰레기배출종료시각",
        "재활용품배출시작시각","재활용품배출종료시각",
        "미수거일","관리부서명","관리부서전화번호",
    ]
    df = df[keep].drop_duplicates(subset=["시군구명"], keep="first")
    return df.set_index("시군구명")

@st.cache_data
def load_trashbag():
    """종량제 봉투 가격 — 서울 전 구 로드"""
    df = pd.read_csv("trashbag.csv", encoding="cp949")
    return df[df["시도명"] == "서울특별시"].copy()

def get_bag_prices(df_bag, gu):
    """특정 구의 종량제 봉투 가격 딕셔너리 반환"""
    sub = df_bag[df_bag["시군구명"] == gu]
    result = {}

    # ① 가정용 생활쓰레기 규격봉투
    home_life = sub[
        (sub["종량제봉투용도"] == "생활쓰레기") &
        (sub["종량제봉투종류"] == "규격봉투") &
        (sub["종량제봉투사용대상"] == "가정용")
    ]
    sizes_life = ["5ℓ","10ℓ","20ℓ","30ℓ","50ℓ","75ℓ","100ℓ"]
    life_prices = {}
    if not home_life.empty:
        row = home_life.iloc[0]
        for s in sizes_life:
            col = f"{s}가격"
            if col in row and pd.notna(row[col]) and int(row[col]) > 0:
                life_prices[s] = int(row[col])
    result["생활쓰레기"] = life_prices

    # ② 가정용 음식물쓰레기
    home_food = sub[
        (sub["종량제봉투용도"] == "음식물쓰레기") &
        (sub["종량제봉투사용대상"] == "가정용")
    ]
    sizes_food = ["1ℓ","2ℓ","3ℓ","5ℓ","10ℓ","20ℓ"]
    food_prices = {}
    if not home_food.empty:
        row = home_food.iloc[0]
        for s in sizes_food:
            col = f"{s}가격"
            if col in row and pd.notna(row[col]) and int(row[col]) > 0:
                food_prices[s] = int(row[col])
    result["음식물쓰레기"] = food_prices

    # ③ 재사용규격봉투
    reuse = sub[
        (sub["종량제봉투종류"] == "재사용규격봉투") &
        (sub["종량제봉투용도"] == "생활쓰레기") &
        (sub["종량제봉투사용대상"] == "가정용")
    ]
    reuse_prices = {}
    if not reuse.empty:
        row = reuse.iloc[0]
        for s in sizes_life:
            col = f"{s}가격"
            if col in row and pd.notna(row[col]) and int(row[col]) > 0:
                reuse_prices[s] = int(row[col])
    result["재사용봉투"] = reuse_prices

    return result

try:
    df_amt  = load_amount()
    df_sch  = load_schedule()
    df_bag  = load_trashbag()
    DATA_OK = True
except Exception as e:
    DATA_OK = False; DATA_ERR = str(e)


# ══════════════════════════════════════
# 상수 & 유틸
# ══════════════════════════════════════
CLR  = {"red":"#FF6B6B","orange":"#FFB347","green":"#3ECF8E"}
EMJ  = {"red":"😰","orange":"😅","green":"😊"}
LBL  = {"red":"🔴 경고","orange":"🟠 보통","green":"🟢 우수"}
DAYS = ["일","월","화","수","목","금","토"]

GU_URLS = {
    "종로구":"https://www.jongno.go.kr","중구":"https://www.junggu.seoul.kr",
    "용산구":"https://www.yongsan.go.kr","성동구":"https://www.sd.go.kr",
    "광진구":"https://www.gwangjin.go.kr","동대문구":"https://www.ddm.go.kr",
    "중랑구":"https://www.jungnang.go.kr","성북구":"https://www.sb.go.kr",
    "강북구":"https://www.gangbuk.go.kr","도봉구":"https://www.dobong.go.kr",
    "노원구":"https://www.nowon.kr","은평구":"https://www.ep.go.kr",
    "서대문구":"https://www.sdm.go.kr","마포구":"https://www.mapo.go.kr",
    "양천구":"https://www.yangcheon.go.kr","강서구":"https://www.gangseo.seoul.kr",
    "구로구":"https://www.guro.go.kr","금천구":"https://www.geumcheon.go.kr",
    "영등포구":"https://www.ydp.go.kr","동작구":"https://www.dongjak.go.kr",
    "관악구":"https://www.gwanak.go.kr","서초구":"https://www.seocho.go.kr",
    "강남구":"https://www.gangnam.go.kr","송파구":"https://www.songpa.go.kr",
    "강동구":"https://www.gangdong.go.kr",
}

LEVEL_INFO = [
    {"min":0,   "max":200,  "emoji":"🌱","name":"LV.1 새싹 쓰요"},
    {"min":200, "max":500,  "emoji":"🌿","name":"LV.2 잎사귀 쓰요"},
    {"min":500, "max":1000, "emoji":"🌺","name":"LV.3 꽃단장 쓰요"},
    {"min":1000,"max":99999,"emoji":"🌍","name":"LV.4 지구 수호자 쓰요"},
]

WASTE_DB = [
    {"name":"우유팩","emoji":"🥛","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 종이팩","steps":"① 비우기  ② 헹구기  ③ 펼치기  ④ 따로 배출","tip":"동주민센터에 모으면 화장지/봉투 교환 가능!","warn":None},
    {"name":"라면봉지","emoji":"🍜","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 비닐류","steps":"① 오염 확인  ② 펼치기  ③ 비닐봉투에 담아 배출","tip":"딱지로 접으면 선별 ❌  꼭 펼쳐요.","warn":"국물 많이 묻었으면 → 종량제 봉투"},
    {"name":"투명 페트병","emoji":"🍼","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 투명 페트","steps":"① 비우기  ② 라벨 제거  ③ 압착  ④ 배출","tip":"색깔 병과 반드시 따로 분리!","warn":None},
    {"name":"음식물쓰레기","emoji":"🍖","cat":"food","cc":"#FFE9A0","cf":"#B8860B","ct":"🍖 음식물","steps":"① 물기 제거  ② 잘게 썰기  ③ 전용봉투  ④ 배출","tip":"물기를 꼭 짜야 냄새 ❌","warn":"뼈·껍데기·씨앗 → 일반쓰레기"},
    {"name":"깨진 유리","emoji":"🪞","cat":"special","cc":"#E8D5FF","cf":"#6B21A8","ct":"⚠️ 불연성","steps":"① 신문지로 싸기  ② '위험' 표시  ③ 불연성 전용마대","tip":"수거자 부상 방지! 꼭 싸 주세요.","warn":"일반 종량제 봉투 ❌"},
    {"name":"종이컵","emoji":"☕","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 종이팩","steps":"① 씻기  ② 펼치기  ③ 따로 모아 배출","tip":"따로 배출 시 화장지로 재활용!","warn":None},
    {"name":"스티로폼","emoji":"📦","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 발포합성수지","steps":"① 이물질 제거  ② 테이프 제거  ③ 부숴서 배출","tip":"음식 묻었으면 씻어서 배출","warn":"오염 심하면 → 일반쓰레기"},
    {"name":"헌 옷","emoji":"👕","cat":"special","cc":"#E8D5FF","cf":"#6B21A8","ct":"⚠️ 의류수거함","steps":"① 세탁  ② 묶음 포장  ③ 의류수거함 배출","tip":"수거함 위치 → 동주민센터 앱 확인","warn":"속옷·양말 → 일반쓰레기"},
    {"name":"폐건전지","emoji":"🔋","cat":"special","cc":"#E8D5FF","cf":"#6B21A8","ct":"⚠️ 폐전지","steps":"① 따로 모으기  ② 전지 수거함  ③ 배출","tip":"마트·편의점·주민센터 전지 수거함 이용","warn":"일반쓰레기 ❌  화재·환경오염 위험"},
    {"name":"치킨뼈","emoji":"🍗","cat":"general","cc":"#FFD6D6","cf":"#CC3333","ct":"🗑️ 일반쓰레기","steps":"① 종량제 봉투에 담아 배출","tip":"딱딱한 뼈 → 음식물 ❌","warn":"음식물 수거함 ❌"},
    {"name":"달걀껍데기","emoji":"🥚","cat":"general","cc":"#FFD6D6","cf":"#CC3333","ct":"🗑️ 일반쓰레기","steps":"① 종량제 봉투에 담아 배출","tip":"단단해서 음식물 처리 불가","warn":"음식물 수거함 ❌"},
    {"name":"커피찌꺼기","emoji":"☕","cat":"food","cc":"#FFE9A0","cf":"#B8860B","ct":"🍖 음식물","steps":"① 물기 제거  ② 전용봉투  ③ 배출","tip":"화분 퇴비로도 활용 가능!","warn":None},
]

QUIZZES = [
    {"q":"라면봉지는 딱지로 접어서 버려야 재활용이 잘 된다.","ans":False,"exp":"딱지로 접으면 선별 ❌  꼭 펼쳐요!"},
    {"q":"우유팩은 일반 종이와 함께 버려도 된다.","ans":False,"exp":"우유팩은 별도 재질 — 씻어서 펼친 후 따로 배출!"},
    {"q":"깨끗한 비닐은 재활용이 가능하다.","ans":True,"exp":"맞아요! 오염됐으면 일반쓰레기로."},
    {"q":"달걀껍데기는 음식물 쓰레기로 버려야 한다.","ans":False,"exp":"달걀껍데기 → 일반쓰레기!"},
    {"q":"투명 페트병은 라벨을 제거하고 배출해야 한다.","ans":True,"exp":"라벨 제거 + 압착 후 투명 페트 전용 배출!"},
    {"q":"치킨뼈는 음식물 쓰레기로 버려야 한다.","ans":False,"exp":"딱딱한 뼈 → 종량제 봉투(일반쓰레기)!"},
    {"q":"폐건전지는 일반쓰레기로 버려도 된다.","ans":False,"exp":"폐전지 → 반드시 별도 수거함에 배출!"},
]

def safe(v, d="정보 없음"):
    return d if pd.isna(v) or str(v).strip() in ("","nan","NaN") else str(v).strip()

def day_html(day_str):
    if pd.isna(day_str) or not str(day_str).strip():
        return "<span style='color:#ccc'>정보 없음</span>"
    active = set(str(day_str).replace(" ","").split("+"))
    parts = ['<div class="days-wrap">']
    for d in DAYS:
        cls = "day-on" if d in active else "day-off"
        parts.append(f'<span class="{cls}">{d}</span>')
    parts.append("</div>")
    return "".join(parts)

def get_lv(pts):
    for lv in LEVEL_INFO:
        if lv["min"] <= pts < lv["max"]: return lv
    return LEVEL_INFO[-1]

def render_waste_card(w):
    name=w["name"]; emoji=w["emoji"]; cc=w["cc"]; cf=w["cf"]; ct=w["ct"]
    steps=w["steps"]; tip=w["tip"]; warn=w["warn"]
    tip_b  = f'<span class="tip-chip">💡 {tip}</span>'   if tip  else ""
    warn_b = f'<span class="warn-chip">⚠️ {warn}</span>' if warn else ""
    return (
        '<div class="waste-card">'
          f'<div class="waste-emoji">{emoji}</div>'
          '<div class="waste-info">'
            f'<div class="waste-name">{name}</div>'
            f'<span class="waste-cat" style="background:{cc};color:{cf}">{ct}</span>'
            f'<div class="waste-step">{steps}</div>'
            + tip_b + warn_b
          + "</div>"
        + "</div>"
    )

# ══════════════════════════════════════
# 종량제 가격 패널 렌더링 (Streamlit 컴포넌트)
# ══════════════════════════════════════
def render_price_panel(gu, df_bag):
    prices = get_bag_prices(df_bag, gu)

    tab_key = f"price_tab_{gu}"
    if tab_key not in st.session_state:
        st.session_state[tab_key] = "생활쓰레기"

    # 탭 버튼
    tab_cols = st.columns(3)
    tabs = [
        ("🗑️ 생활쓰레기", "생활쓰레기"),
        ("🍖 음식물",     "음식물쓰레기"),
        ("♻️ 재사용봉투", "재사용봉투"),
    ]
    for i, (label, key) in enumerate(tabs):
        with tab_cols[i]:
            is_active = st.session_state[tab_key] == key
            btn_style = (
                "background:#3ECF8E;color:white;border:none;border-radius:20px;"
                "padding:6px 0;width:100%;font-weight:700;font-size:0.82rem;cursor:pointer;"
            ) if is_active else (
                "background:#F7FAFC;color:#4A5568;border:1.5px solid #E2E8F0;border-radius:20px;"
                "padding:6px 0;width:100%;font-weight:700;font-size:0.82rem;cursor:pointer;"
            )
            if st.button(label, key=f"ptab_{gu}_{key}", use_container_width=True):
                st.session_state[tab_key] = key
                st.rerun()

    current_tab = st.session_state[tab_key]
    price_data = prices.get(current_tab, {})

    if not price_data:
        st.markdown(
            '<div class="price-empty">📭 해당 봉투 데이터가 없어요</div>',
            unsafe_allow_html=True,
        )
    else:
        cells = ""
        for size, val in price_data.items():
            cells += (
                f'<div class="price-cell">'
                f'<div class="price-cell-size">{size}</div>'
                f'<div class="price-cell-val">{val:,}</div>'
                f'<div class="price-cell-won">원</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="price-grid">{cells}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:0.72rem;color:#A0AEC0;margin-top:4px">'
            '※ 가정용 기준 · 출처: 공공데이터포털</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════
# SVG 지도 — 클릭 시 구 선택 (구청 URL 제거)
# ══════════════════════════════════════
def build_svg_map(df_amt, sel):
    GU_PATHS = {
        "도봉구":"M270,28 L340,22 L365,55 L345,80 L300,85 L268,65 Z",
        "노원구":"M340,22 L425,26 L440,62 L405,88 L365,82 L365,55 Z",
        "강북구":"M240,62 L270,28 L268,65 L300,85 L295,108 L265,115 L242,95 Z",
        "성북구":"M265,115 L295,108 L350,108 L372,130 L348,152 L310,158 L278,148 Z",
        "중랑구":"M365,82 L405,88 L428,110 L408,140 L378,148 L372,130 L350,108 Z",
        "동대문구":"M310,158 L348,152 L372,130 L378,148 L360,170 L330,175 L308,170 Z",
        "광진구":"M378,148 L408,140 L435,162 L418,192 L388,198 L360,188 L360,170 Z",
        "성동구":"M308,170 L330,175 L360,170 L360,188 L345,210 L315,215 L292,200 Z",
        "종로구":"M198,72 L240,62 L242,95 L265,115 L278,148 L250,162 L218,155 L195,132 L188,102 Z",
        "중구":"M218,155 L250,162 L278,148 L310,158 L308,170 L292,200 L268,210 L240,200 L220,182 Z",
        "용산구":"M220,182 L240,200 L268,210 L260,238 L238,250 L210,240 L200,218 Z",
        "은평구":"M115,72 L198,72 L188,102 L195,132 L165,148 L128,140 L105,108 Z",
        "서대문구":"M165,148 L195,132 L218,155 L220,182 L200,218 L172,222 L148,202 L140,172 Z",
        "마포구":"M96,178 L140,172 L148,202 L172,222 L162,255 L130,268 L88,252 L75,218 Z",
        "강서구":"M38,248 L88,252 L130,268 L125,318 L88,340 L42,318 L28,282 Z",
        "양천구":"M88,252 L130,268 L148,315 L130,342 L88,340 L88,310 Z",
        "영등포구":"M130,268 L162,255 L188,268 L198,305 L182,342 L148,348 L130,342 L148,315 Z",
        "구로구":"M88,310 L130,342 L148,348 L140,378 L100,385 L72,362 L68,330 Z",
        "금천구":"M100,385 L140,378 L162,392 L158,422 L122,428 L98,408 Z",
        "동작구":"M182,342 L215,330 L248,348 L242,382 L208,392 L182,378 L170,358 Z",
        "관악구":"M148,348 L182,342 L170,358 L182,378 L208,392 L200,422 L162,428 L158,422 L162,392 L140,378 Z",
        "서초구":"M248,348 L295,335 L325,355 L322,400 L285,415 L252,408 L242,382 Z",
        "강남구":"M325,355 L385,348 L418,360 L422,415 L388,432 L348,440 L322,420 L322,400 Z",
        "송파구":"M418,228 L482,222 L508,268 L492,332 L448,358 L418,360 L385,348 L388,305 L405,272 Z",
        "강동구":"M482,165 L545,158 L568,200 L552,258 L508,268 L482,222 L440,205 L435,162 Z",
    }
    LABEL_POS = {
        "도봉구":(308,55),"노원구":(395,55),"강북구":(268,82),
        "성북구":(318,132),"중랑구":(395,118),"동대문구":(340,163),
        "광진구":(400,172),"성동구":(328,196),"종로구":(225,115),
        "중구":(260,178),"용산구":(232,218),"은평구":(148,108),
        "서대문구":(175,185),"마포구":(122,225),"강서구":(78,295),
        "양천구":(112,300),"영등포구":(162,308),"구로구":(108,348),
        "금천구":(130,402),"동작구":(212,362),"관악구":(175,388),
        "서초구":(282,378),"강남구":(368,400),"송파구":(448,295),
        "강동구":(498,215),
    }

    # 툴팁 데이터 (구청 URL 제거, 가격 안내 메시지로 변경)
    tip_parts = []
    for gu, row in df_amt.iterrows():
        lc = row["등급"]
        tip_parts.append(
            f'"{gu}":{{"amt":{row["1인당"]},"tot":{row["총량"]},'
            f'"pop":{int(row["주민수"])},"lbl":"{LBL[lc]}",'
            f'"clr":"{CLR[lc]}","emj":"{EMJ[lc]}"}}'
        )
    tip_json = "{" + ",".join(tip_parts) + "}"

    paths = []; labels = []
    for gu, pd_ in GU_PATHS.items():
        if gu in df_amt.index:
            lc   = df_amt.loc[gu,"등급"]
            fill = "#2563EB" if gu == sel else CLR[lc]
            sw   = "3" if gu == sel else "1.5"
        else:
            fill, sw = "#DDD","1.5"
        paths.append(
            f'<path d="{pd_}" fill="{fill}" stroke="white" stroke-width="{sw}" '
            f'class="gu-path" data-gu="{gu}" />'
        )
    for gu, (lx, ly) in LABEL_POS.items():
        labels.append(
            f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="9" '
            f'font-family="Nanum Gothic" fill="white" pointer-events="none" '
            f'font-weight="700">{gu[:3]}</text>'
        )

    svg_body = "\n".join(paths) + "\n" + "\n".join(labels)

    return f"""
<div class="map-wrap">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
    <span style="font-size:1rem">🗑️</span>
    <span style="font-size:0.82rem;color:#3ECF8E;font-weight:800">
      구를 클릭하면 해당 구의 종량제 봉투 가격을 확인할 수 있어요
    </span>
    <span style="font-size:0.75rem;color:#999;margin-left:auto">마우스를 올리면 배출량 정보 표시</span>
  </div>
  <svg id="seoulSVG" viewBox="0 0 580 460" width="100%"
       style="display:block;border-radius:10px;cursor:pointer">
    {svg_body}
  </svg>

  <!-- 툴팁 -->
  <div id="svgTip" style="display:none;position:fixed;background:white;border-radius:14px;
    padding:12px 16px;box-shadow:0 6px 28px rgba(0,0,0,0.18);z-index:9999;min-width:175px;
    border:2px solid #3ECF8E;font-family:'Nanum Gothic',sans-serif;font-size:0.83rem;
    pointer-events:none;line-height:1.8">
  </div>

  <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
    <span style="background:#3ECF8E;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🟢 우수 ~1.2 kg</span>
    <span style="background:#FFB347;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🟠 보통 1.2~2.0 kg</span>
    <span style="background:#FF6B6B;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🔴 경고 2.0+ kg</span>
    <span style="background:#2563EB;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">◼ 선택 구</span>
    <span style="background:#E2E8F0;color:#4A5568;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🗑️ 클릭 → 봉투 가격 확인</span>
  </div>
</div>

<script>
(function(){{
  var D={tip_json};
  var tt=document.getElementById('svgTip');
  var paths=document.querySelectorAll('#seoulSVG .gu-path');

  paths.forEach(function(p){{
    p.addEventListener('mousemove',function(e){{
      var g=p.getAttribute('data-gu'),i=D[g];
      if(!i)return;
      tt.innerHTML=
        '<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px">'
          +'<b style="font-size:0.95rem">'+i.emj+' '+g+'</b>'
          +'<span style="background:'+i.clr+'22;color:'+i.clr+';padding:1px 7px;border-radius:6px;font-size:0.72rem;font-weight:700">'+i.lbl+'</span>'
        +'</div>'
        +'🗑️ 1인당: <b>'+i.amt+' kg/일</b><br>'
        +'📊 총량: '+i.tot+' 톤/일<br>'
        +'👥 주민: '+i.pop.toLocaleString()+'명<br>'
        +'<div style="margin-top:6px;padding-top:6px;border-top:1px solid #eee;'
        +'font-size:0.77rem;color:#3ECF8E;font-weight:700">🗑️ 클릭하면 봉투 가격 확인</div>';
      tt.style.display='block';
      tt.style.left=(e.clientX+14)+'px';
      tt.style.top=(e.clientY-10)+'px';
    }});
    p.addEventListener('mouseleave',function(){{
      tt.style.display='none';
    }});
    /* 클릭 → Streamlit query param으로 구 전달 */
    p.addEventListener('click',function(){{
      var g=p.getAttribute('data-gu');
      if(g){{
        /* Streamlit 1.x: window.parent.postMessage로 세션 변경 불가
           대신 URL hash 방식 사용 — 페이지 새로고침 없이 감지 */
        window.location.hash='gu='+encodeURIComponent(g);
      }}
    }});
  }});
}})();
</script>
"""


# ══════════════════════════════════════
# 세션 초기화
# ══════════════════════════════════════
for k, v in [
    ("pts",0),("gu","마포구"),
    ("q_done",False),("q_idx",0),("q_user_ans",None),("q_pts_given",False),
    ("pt_history",[]),
    ("discharge_log",[]),
    ("nickname","환경 지킴이"),
    ("join_date", datetime.now().strftime("%Y.%m.%d")),
    ("map_selected_gu", None),
]:
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════
# 사이드바
# ════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:8px;padding:8px 0 4px">'
          '<span style="font-size:1.5rem">🧚</span>'
          '<span style="font-size:1.1rem;font-weight:800;color:#1A202C">서울 쓰레기 요정</span>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    menu = st.radio(
        "메뉴",
        ["🗺️ 배출량 지도", "📅 우리동네 스케줄", "📖 분리배출 도감", "⭐ 에코 마일리지", "👤 나의 현황"],
        label_visibility="collapsed",
    )
    st.markdown("---")

    st.markdown('<span style="font-size:0.8rem;font-weight:700;color:#718096">📍 내 동네 선택</span>', unsafe_allow_html=True)
    if DATA_OK:
        gu_list = sorted(df_amt.index.tolist())
        idx = gu_list.index(st.session_state.gu) if st.session_state.gu in gu_list else 0
        sel = st.selectbox("구", gu_list, index=idx, label_visibility="collapsed")
        st.session_state.gu = sel

        row_a = df_amt.loc[sel]; lv_c = row_a["등급"]
        url_gu = GU_URLS.get(sel,"#")
        st.markdown(
            f'<div style="background:#F7FAFC;border-radius:14px;padding:14px;margin-top:8px;border:1.5px solid #E2E8F0">'
              f'<div style="font-size:1rem;font-weight:800;color:#1A202C">{sel}</div>'
              f'<div style="font-size:1.9rem;font-weight:800;color:{CLR[lv_c]};margin:4px 0">'
                f'{row_a["1인당"]} <span style="font-size:0.9rem;color:#718096">kg/일</span></div>'
              f'<div style="font-size:0.75rem;color:#718096">{LBL[lv_c]}  ·  주민 {int(row_a["주민수"]):,}명</div>'
              f'<a href="{url_gu}" target="_blank" style="display:inline-block;margin-top:8px;'
              f'background:#EBF8F3;color:#2D9A6B;padding:4px 12px;border-radius:8px;'
              f'font-size:0.75rem;font-weight:700;text-decoration:none">🏛️ 구청 사이트 →</a>'
            "</div>",
            unsafe_allow_html=True,
