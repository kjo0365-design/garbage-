import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random, os, shutil

# ══════════════════════════════════════
# 페이지 설정  —  가로형 Wide
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

/* Streamlit 기본 여백/헤더 제거 */
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
    background: linear-gradient(180deg, #1C3F6E 0%, #0F2645 100%) !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown div { color: rgba(255,255,255,0.85) !important; }
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5 { color: white !important; }
section[data-testid="stSidebar"] label { color: rgba(255,255,255,0.75) !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    color: white !important;
}
section[data-testid="stSidebar"] svg { fill: rgba(255,255,255,0.7) !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    border-radius: 10px;
    padding: 8px 12px;
    display: block;
    transition: background 0.15s;
    color: rgba(255,255,255,0.75) !important;
    font-weight: 700;
    font-size: 0.9rem;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.1);
    color: white !important;
}

/* ══ 상단 헤더 ══ */
.topbar {
    background: linear-gradient(135deg, #3ECF8E, #1AA7EC);
    border-radius: 16px;
    padding: 20px 28px;
    color: white;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.topbar h1 { font-size: 1.5rem; font-weight: 800; margin: 0; }
.topbar p  { font-size: 0.84rem; opacity: 0.85; margin: 3px 0 0; }
.topbar-badge {
    background: rgba(255,255,255,0.22);
    border-radius: 20px; padding: 8px 18px;
    font-size: 0.88rem; font-weight: 800;
    white-space: nowrap;
}

/* ══ 카드 ══ */
.card {
    background: white;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.07);
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

/* ══ 지표 3개 ══ */
.metric-grid {
    display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-bottom: 16px;
}
.metric-box {
    background: white; border-radius: 14px; padding: 16px;
    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border-top: 3px solid transparent;
}
.metric-val  { font-size: 1.8rem; font-weight: 800; line-height: 1; }
.metric-unit { font-size: 0.72rem; color: #999; margin-top: 4px; }
.metric-lbl  { font-size: 0.72rem; font-weight: 700; margin-top: 4px; }

/* ══ 요일 뱃지 ══ */
.days-wrap { display:flex; gap:5px; flex-wrap:wrap; margin:8px 0; }
.day-on  { background:#3ECF8E; color:white;  padding:5px 11px; border-radius:10px; font-size:0.83rem; font-weight:700; display:inline-block; }
.day-off { background:#F0F2F5; color:#C0C7D0; padding:5px 11px; border-radius:10px; font-size:0.83rem; font-weight:700; display:inline-block; }

/* ══ 스케줄 카드 ══ */
.sched-card {
    background: white; border-radius: 14px; padding: 16px 18px;
    margin-bottom: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border-left: 4px solid #3ECF8E;
}
.sched-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.sched-time   { margin-left: auto; font-size: 0.8rem; color: #FF6B6B; font-weight: 700; background: #FFF3F3; padding: 3px 10px; border-radius: 8px; }

/* ══ 도감 그리드 ══ */
.waste-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    gap: 14px;
    margin-bottom: 16px;
}
.waste-card {
    background: white; border-radius: 14px; padding: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    display: flex; align-items: flex-start; gap: 12px;
    transition: box-shadow 0.2s, transform 0.2s;
}
.waste-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.12); transform: translateY(-2px); }
.waste-emoji { font-size: 2.2rem; flex-shrink: 0; }
.waste-info  { flex: 1; min-width: 0; }
.waste-name  { font-size: 1rem; font-weight: 800; color: #1A1A2E; }
.waste-cat   { display:inline-block; padding:2px 9px; border-radius:8px; font-size:0.72rem; font-weight:700; margin:4px 0 6px; }
.waste-step  { font-size: 0.8rem; color: #555; line-height: 1.6; }
.tip-chip    { background:#E8FFF5; color:#00A86B; border-radius:8px; padding:5px 10px; font-size:0.77rem; font-weight:700; margin-top:6px; display:block; }
.warn-chip   { background:#FFF8E1; color:#F57F17; border-radius:8px; padding:5px 10px; font-size:0.77rem; font-weight:700; margin-top:4px; display:block; }

/* ══ 포인트 히어로 ══ */
.pt-hero {
    background: linear-gradient(135deg,#FFD93D,#FF9A3C);
    border-radius: 16px; padding: 24px 28px; color: white;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px;
}
.pt-hero-num { font-size: 3.2rem; font-weight: 800; line-height: 1; }
.pt-hero-sub { font-size: 0.85rem; opacity: 0.85; }

/* 캐릭터 */
.char-box {
    background: white; border-radius: 16px; padding: 22px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.07);
    display: flex; align-items: center; gap: 18px;
    margin-bottom: 16px;
}
.xp-track { height: 9px; background: #F0F2F5; border-radius: 5px; margin-top: 8px; overflow: hidden; }
.xp-fill  { height: 100%; border-radius: 5px; background: linear-gradient(90deg,#3ECF8E,#1AA7EC); }
.xp-label { font-size: 0.73rem; color: #999; margin-top: 3px; }

/* 적립 카드 */
.earn-card {
    background: white; border-radius: 14px; padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    height: 100%;
}
.earn-pts { display:inline-block; background:linear-gradient(90deg,#FFD93D,#FF9A3C); color:white; border-radius:8px; padding:3px 10px; font-size:0.8rem; font-weight:800; margin-bottom:10px; }

/* 사용 아이템 */
.spend-box {
    background: white; border-radius: 14px; padding: 18px 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06); text-align: center;
    transition: transform 0.15s;
}
.spend-box:hover { transform: translateY(-2px); }
.spend-icon { font-size: 2rem; display: block; margin-bottom: 6px; }
.spend-name { font-size: 0.82rem; font-weight: 700; color: #333; }
.spend-pts  { font-size: 0.82rem; color: #FF6B6B; font-weight: 800; margin-top: 3px; }

/* 레벨 */
.lv-box {
    background:white; border-radius:14px; padding:18px 12px;
    text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.05);
    border:2px solid #F0F2F5;
}
.lv-box.done { border-color:#3ECF8E; background:#F0FDF6; }

/* 순위 */
.rank-item {
    background:white; border-radius:10px; padding:9px 14px;
    margin:4px 0; display:flex; align-items:center; gap:10px;
    box-shadow:0 1px 6px rgba(0,0,0,0.05);
}

/* 연락처 */
.contact-box {
    background:white; border-radius:14px; padding:16px 18px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:12px;
}
.no-day-box {
    background:#FFF3F3; border-radius:12px; padding:10px 16px;
    border-left:4px solid #FF6B6B; font-size:0.83rem; color:#CC3333;
    margin-bottom:12px;
}

/* SVG 지도 */
.map-wrap { background:white; border-radius:16px; padding:18px; box-shadow:0 2px 14px rgba(0,0,0,0.07); }
.gu-path  { cursor:pointer; stroke:white; stroke-width:1.5; transition:all 0.2s; }
.gu-path:hover { stroke:#333; stroke-width:2.5; filter:brightness(0.85); }

/* Streamlit 버튼 */
div[data-testid="stButton"] > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Nanum Gothic', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# 파일 복사
# ══════════════════════════════════════
for src, dst in [
    ("/mnt/user-data/uploads/seoul_data.xlsx",   "seoul_data.xlsx"),
    ("/mnt/user-data/uploads/seoul_garbage.csv", "seoul_garbage.csv"),
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

try:
    df_amt  = load_amount()
    df_sch  = load_schedule()
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

LEVEL_INFO = [
    {"min":0,   "max":200,  "emoji":"🌱","name":"LV.1 새싹 쓰요"},
    {"min":200, "max":500,  "emoji":"🌿","name":"LV.2 잎사귀 쓰요"},
    {"min":500, "max":1000, "emoji":"🌺","name":"LV.3 꽃단장 쓰요"},
    {"min":1000,"max":99999,"emoji":"🌍","name":"LV.4 지구 수호자 쓰요"},
]

WASTE_DB = [
    {"name":"우유팩","emoji":"🥛","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 종이팩",
     "steps":"① 비우기  ② 헹구기  ③ 펼치기  ④ 따로 배출","tip":"동주민센터에 모으면 화장지/봉투 교환 가능!","warn":None},
    {"name":"라면봉지","emoji":"🍜","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 비닐류",
     "steps":"① 오염 확인  ② 펼치기  ③ 비닐봉투에 담아 배출","tip":"딱지로 접으면 선별 ❌  꼭 펼쳐요.","warn":"국물 많이 묻었으면 → 종량제 봉투"},
    {"name":"투명 페트병","emoji":"🍼","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 투명 페트",
     "steps":"① 비우기  ② 라벨 제거  ③ 압착  ④ 배출","tip":"색깔 병과 반드시 따로 분리!","warn":None},
    {"name":"음식물쓰레기","emoji":"🍖","cat":"food","cc":"#FFE9A0","cf":"#B8860B","ct":"🍖 음식물",
     "steps":"① 물기 제거  ② 잘게 썰기  ③ 전용봉투  ④ 배출","tip":"물기를 꼭 짜야 냄새 ❌","warn":"뼈·껍데기·씨앗 → 일반쓰레기"},
    {"name":"깨진 유리","emoji":"🪞","cat":"special","cc":"#E8D5FF","cf":"#6B21A8","ct":"⚠️ 불연성",
     "steps":"① 신문지로 싸기  ② '위험' 표시  ③ 불연성 전용마대","tip":"수거자 부상 방지! 꼭 싸 주세요.","warn":"일반 종량제 봉투 ❌"},
    {"name":"종이컵","emoji":"☕","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 종이팩",
     "steps":"① 씻기  ② 펼치기  ③ 따로 모아 배출","tip":"따로 배출 시 화장지로 재활용!","warn":None},
    {"name":"스티로폼","emoji":"📦","cat":"recycle","cc":"#B7F0D5","cf":"#00A86B","ct":"♻️ 발포합성수지",
     "steps":"① 이물질 제거  ② 테이프 제거  ③ 부숴서 배출","tip":"음식 묻었으면 씻어서 배출","warn":"오염 심하면 → 일반쓰레기"},
    {"name":"헌 옷","emoji":"👕","cat":"special","cc":"#E8D5FF","cf":"#6B21A8","ct":"⚠️ 의류수거함",
     "steps":"① 세탁  ② 묶음 포장  ③ 의류수거함 배출","tip":"수거함 위치 → 동주민센터 앱 확인","warn":"속옷·양말 → 일반쓰레기"},
    {"name":"폐건전지","emoji":"🔋","cat":"special","cc":"#E8D5FF","cf":"#6B21A8","ct":"⚠️ 폐전지",
     "steps":"① 따로 모으기  ② 전지 수거함  ③ 배출","tip":"마트·편의점·주민센터 전지 수거함 이용","warn":"일반쓰레기 ❌  화재·환경오염 위험"},
    {"name":"치킨뼈","emoji":"🍗","cat":"general","cc":"#FFD6D6","cf":"#CC3333","ct":"🗑️ 일반쓰레기",
     "steps":"① 종량제 봉투에 담아 배출","tip":"딱딱한 뼈 → 음식물 ❌","warn":"음식물 수거함 ❌"},
    {"name":"달걀껍데기","emoji":"🥚","cat":"general","cc":"#FFD6D6","cf":"#CC3333","ct":"🗑️ 일반쓰레기",
     "steps":"① 종량제 봉투에 담아 배출","tip":"단단해서 음식물 처리 불가","warn":"음식물 수거함 ❌"},
    {"name":"커피찌꺼기","emoji":"☕","cat":"food","cc":"#FFE9A0","cf":"#B8860B","ct":"🍖 음식물",
     "steps":"① 물기 제거  ② 전용봉투  ③ 배출","tip":"화분 퇴비로도 활용 가능!","warn":None},
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
# SVG 인터랙티브 지도
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
            fill = "#1C3F6E" if gu == sel else CLR[lc]
            sw   = "3" if gu == sel else "1.5"
        else:
            fill, sw = "#DDD", "1.5"
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
  <div style="font-size:0.78rem;color:#888;font-weight:700;margin-bottom:10px">
    🗺️ 구에 마우스를 올리면 정보가 표시돼요
  </div>
  <svg id="seoulSVG" viewBox="0 0 580 460" width="100%" style="display:block;border-radius:10px">
    {svg_body}
  </svg>
  <div id="svgTip" style="display:none;position:fixed;background:white;border-radius:14px;
    padding:10px 14px;box-shadow:0 6px 28px rgba(0,0,0,0.18);z-index:9999;min-width:165px;
    border:2px solid #3ECF8E;font-family:'Nanum Gothic',sans-serif;font-size:0.83rem;
    pointer-events:none;line-height:1.7"></div>
  <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
    <span style="background:#3ECF8E;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🟢 우수 ~1.2 kg</span>
    <span style="background:#FFB347;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🟠 보통 1.2~2.0 kg</span>
    <span style="background:#FF6B6B;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🔴 경고 2.0+ kg</span>
    <span style="background:#1C3F6E;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">◼ 선택 구</span>
  </div>
</div>
<script>
(function(){{
  var D={tip_json};
  var tt=document.getElementById('svgTip');
  document.querySelectorAll('#seoulSVG .gu-path').forEach(function(p){{
    p.addEventListener('mousemove',function(e){{
      var g=p.getAttribute('data-gu'),i=D[g];
      if(!i)return;
      tt.innerHTML='<b style="font-size:0.92rem">'+i.emj+' '+g+'</b><br>'
        +'<span style="color:'+i.clr+';font-weight:700">'+i.lbl+'</span><br>'
        +'1인당: <b>'+i.amt+' kg/일</b><br>'
        +'총량: '+i.tot+' 톤/일<br>'
        +'주민: '+i.pop.toLocaleString()+'명';
      tt.style.display='block';
      tt.style.left=(e.clientX+14)+'px';
      tt.style.top=(e.clientY-10)+'px';
    }});
    p.addEventListener('mouseleave',function(){{tt.style.display='none';}});
  }});
}})();
</script>
"""


# ══════════════════════════════════════
# 세션 초기화
# ══════════════════════════════════════
for k, v in [("pts",0),("gu","마포구"),("q_done",False),
              ("q_idx",0),("q_user_ans",None),("q_pts_given",False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════
# 사이드바
# ════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧚 서울 쓰레기 요정")
    st.markdown("---")

    menu = st.radio(
        "메뉴",
        ["🗺️ 배출량 지도", "📅 우리동네 스케줄", "📖 분리배출 도감", "⭐ 에코 마일리지"],
        label_visibility="collapsed",
    )
    st.markdown("---")

    st.markdown("##### 📍 내 동네 선택")
    if DATA_OK:
        gu_list = sorted(df_amt.index.tolist())
        idx = gu_list.index(st.session_state.gu) if st.session_state.gu in gu_list else 0
        sel = st.selectbox("구", gu_list, index=idx, label_visibility="collapsed")
        st.session_state.gu = sel

        row_a = df_amt.loc[sel]; lv_c = row_a["등급"]
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.1);border-radius:14px;padding:14px;margin-top:10px">'
              f'<div style="font-size:1rem;font-weight:800;color:white">{sel}</div>'
              f'<div style="font-size:1.9rem;font-weight:800;color:{CLR[lv_c]};margin:4px 0">'
                f'{row_a["1인당"]} <span style="font-size:0.9rem;color:rgba(255,255,255,0.7)">kg/일</span></div>'
              f'<div style="font-size:0.75rem;color:rgba(255,255,255,0.65)">'
                f'{LBL[lv_c]}  ·  주민 {int(row_a["주민수"]):,}명</div>'
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        sel = "마포구"
        st.error(f"데이터 오류: {DATA_ERR}")

    st.markdown("---")
    lv_now = get_lv(st.session_state.pts)
    st.markdown(
        '<div style="background:linear-gradient(135deg,#FFD93D,#FF9A3C);'
        'border-radius:14px;padding:14px;text-align:center">'
          f'<div style="font-size:2rem">{lv_now["emoji"]}</div>'
          f'<div style="font-size:0.8rem;font-weight:800;color:white">{lv_now["name"]}</div>'
          f'<div style="font-size:2rem;font-weight:800;color:white;margin-top:4px">'
            f'{st.session_state.pts} P</div>'
        "</div>",
        unsafe_allow_html=True,
    )


# ════════════════════════════════════════════════════
# 상단 헤더바
# ════════════════════════════════════════════════════
if DATA_OK:
    row_a  = df_amt.loc[sel]; lv_c = row_a["등급"]
    lv_now = get_lv(st.session_state.pts)
    st.markdown(
        '<div class="topbar">'
          "<div>"
            '<h1>🧚 서울 쓰레기 요정</h1>'
            '<p>2024년 실제 데이터 기반 · 서울 25개 자치구 분리배출 가이드</p>'
          "</div>"
          '<div style="display:flex;align-items:center;gap:12px">'
            f'<div class="topbar-badge">{EMJ[lv_c]} {sel} · {row_a["1인당"]} kg/일 · {LBL[lv_c]}</div>'
            f'<div class="topbar-badge">{lv_now["emoji"]} {st.session_state.pts} P</div>'
          "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# ════════════════════════════════════════════════════
# PAGE 1 — 배출량 지도
# ════════════════════════════════════════════════════
if menu == "🗺️ 배출량 지도":
    if not DATA_OK: st.error(f"데이터 오류: {DATA_ERR}"); st.stop()

    lv_c = df_amt.loc[sel,"등급"]
    banners = {
        "red":    f'<div class="banner-red">🚨 {sel}은 배출량 경고 지역! 서울 평균보다 높아요. 분리배출을 실천해요.</div>',
        "green":  f'<div class="banner-green">🌿 {sel}은 배출량 우수 지역! 앞으로도 올바른 분리배출로 유지해요. 👍</div>',
        "orange": f'<div class="banner-orange">🟠 {sel}은 보통 수준. 조금만 더 노력하면 녹색 지역이 될 수 있어요!</div>',
    }
    st.markdown(banners[lv_c], unsafe_allow_html=True)

    # 2컬럼: 왼쪽=SVG지도, 오른쪽=지표+바차트
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown('<div class="sec-title">🗺️ 서울시 구별 배출량 지도</div>', unsafe_allow_html=True)
        st.markdown(build_svg_map(df_amt, sel), unsafe_allow_html=True)

        # 순위 (지도 아래)
        st.markdown('<div class="sec-title">🏆 배출량 순위</div>', unsafe_allow_html=True)
        df_rank = df_amt.reset_index().sort_values("1인당")
        rb, rw = st.columns(2, gap="medium")
        with rb:
            st.markdown("**🌿 적은 TOP 5**")
            for i, (_, r) in enumerate(df_rank.head(5).iterrows(), 1):
                mark = " ⬅" if r["구"] == sel else ""
                clr  = CLR[r["등급"]]
                st.markdown(
                    '<div class="rank-item">'
                      f'<div style="width:22px;height:22px;border-radius:50%;background:{clr}22;'
                      f'color:{clr};display:flex;align-items:center;justify-content:center;'
                      f'font-size:0.72rem;font-weight:800;flex-shrink:0">{i}</div>'
                      f'<div style="flex:1;font-size:0.88rem;font-weight:700">{r["구"]}'
                      f'<span style="color:#3ECF8E;font-size:0.7rem">{mark}</span></div>'
                      f'<div style="font-weight:700;color:{clr}">{r["1인당"]}kg</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )
        with rw:
            st.markdown("**🔴 많은 TOP 5**")
            for i, (_, r) in enumerate(df_rank.tail(5).iloc[::-1].iterrows(), 1):
                mark = " ⬅" if r["구"] == sel else ""
                clr  = CLR[r["등급"]]
                st.markdown(
                    '<div class="rank-item">'
                      f'<div style="width:22px;height:22px;border-radius:50%;background:{clr}22;'
                      f'color:{clr};display:flex;align-items:center;justify-content:center;'
                      f'font-size:0.72rem;font-weight:800;flex-shrink:0">{i}</div>'
                      f'<div style="flex:1;font-size:0.88rem;font-weight:700">{r["구"]}'
                      f'<span style="color:#3ECF8E;font-size:0.7rem">{mark}</span></div>'
                      f'<div style="font-weight:700;color:{clr}">{r["1인당"]}kg</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )

    with col_r:
        # 지표
        st.markdown('<div class="sec-title">📊 내 동네 현황</div>', unsafe_allow_html=True)
        row_a = df_amt.loc[sel]
        amt_v = row_a["1인당"]; tot_v = row_a["총량"]; pop_v = int(row_a["주민수"])
        clr_v = CLR[lv_c]
        st.markdown(
            '<div class="metric-grid">'
              f'<div class="metric-box" style="border-top-color:{clr_v}">'
                f'<div class="metric-val" style="color:{clr_v}">{amt_v}</div>'
                '<div class="metric-unit">kg/일 · 1인당</div>'
                f'<div class="metric-lbl" style="color:{clr_v}">{LBL[lv_c]}</div>'
              "</div>"
              '<div class="metric-box" style="border-top-color:#1AA7EC">'
                f'<div class="metric-val" style="color:#1AA7EC">{tot_v}</div>'
                '<div class="metric-unit">톤/일 · 총배출</div>'
              "</div>"
              '<div class="metric-box" style="border-top-color:#888">'
                f'<div class="metric-val" style="color:#555;font-size:1.3rem">{pop_v:,}</div>'
                '<div class="metric-unit">명 · 주민수</div>'
              "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        # 바차트
        st.markdown('<div class="sec-title">📈 25개구 배출량 비교</div>', unsafe_allow_html=True)
        df_c = df_amt.reset_index().sort_values("1인당", ascending=True)
        fig  = go.Figure()
        for _, r in df_c.iterrows():
            is_sel = r["구"] == sel
            fig.add_trace(go.Bar(
                x=[r["1인당"]], y=[r["구"]], orientation="h",
                marker_color="#1C3F6E" if is_sel else CLR[r["등급"]],
                marker_line_width=0,
                text=f" {r['1인당']}" if is_sel else "",
                textposition="outside", textfont=dict(size=9),
                showlegend=False,
                hovertemplate=(
                    f"<b>{EMJ[r['등급']]} {r['구']}</b><br>"
                    f"1인당: <b>{r['1인당']} kg/일</b><br>"
                    f"총량: {r['총량']} 톤/일<br>"
                    f"주민: {int(r['주민수']):,}명<extra></extra>"
                ),
            ))
        fig.add_vline(x=1.2, line_dash="dot", line_color="#3ECF8E", line_width=1.5)
        fig.add_vline(x=2.0, line_dash="dot", line_color="#FF6B6B", line_width=1.5)
        fig.update_layout(
            height=540, margin=dict(l=0,r=44,t=10,b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(gridcolor="#F0F2F5", range=[0,3.4], title="kg/일"),
            yaxis=dict(gridcolor="white"),
            font=dict(family="Nanum Gothic", size=11),
            bargap=0.26,
        )
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════
# PAGE 2 — 우리동네 스케줄
# ════════════════════════════════════════════════════
elif menu == "📅 우리동네 스케줄":
    if not DATA_OK: st.error("데이터 오류"); st.stop()

    st.markdown(f'<div class="sec-title">📍 {sel} 배출 스케줄</div>', unsafe_allow_html=True)
    row_s = df_sch.loc[sel] if sel in df_sch.index else None

    if row_s is not None:
        # 3컬럼 스케줄 카드
        sc1, sc2, sc3 = st.columns(3, gap="large")
        for col, icon, label, color, d_col, s_col, e_col, m_col in [
            (sc1,"🗑️","일반쓰레기","#FF6B6B","생활쓰레기배출요일","생활쓰레기배출시작시각","생활쓰레기배출종료시각","생활쓰레기배출방법"),
            (sc2,"♻️","재활용품","#3ECF8E","재활용품배출요일","재활용품배출시작시각","재활용품배출종료시각","재활용품배출방법"),
            (sc3,"🍖","음식물쓰레기","#FFB347","음식물쓰레기배출요일","음식물쓰레기배출시작시각","음식물쓰레기배출종료시각","음식물쓰레기배출방법"),
        ]:
            with col:
                t_s=safe(row_s[s_col]); t_e=safe(row_s[e_col]); method=safe(row_s[m_col])
                st.markdown(
                    f'<div class="sched-card" style="border-left-color:{color}">'
                      '<div class="sched-header">'
                        f'<span style="font-size:1.5rem">{icon}</span>'
                        f'<span style="font-size:0.95rem;font-weight:800">{label}</span>'
                        f'<div class="sched-time">⏰ {t_s}~{t_e}</div>'
                      "</div>"
                      + day_html(row_s[d_col])
                      + f'<div style="font-size:0.8rem;color:#555;margin-top:10px;'
                        f'background:#F8F9FA;border-radius:10px;padding:10px;line-height:1.6">{method}</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        info_l, info_r = st.columns([2, 1], gap="large")

        with info_l:
            no_day = safe(row_s["미수거일"])
            if no_day not in ("정보 없음",""):
                st.markdown(f'<div class="no-day-box">🚫 <b>미수거일:</b> {no_day}</div>', unsafe_allow_html=True)
            bulky = safe(row_s["일시적다량폐기물배출방법"])
            bulky_place = safe(row_s["일시적다량폐기물배출장소"])
            skip_set = {"정보 없음","미운영","없음","-","해당없음","해당사항없음","별도안내","처리업체와협의"}
            if bulky not in skip_set:
                st.markdown('<div class="sec-title">🛻 대형폐기물 배출</div>', unsafe_allow_html=True)
                st.markdown(
                    '<div class="card">'
                      f'<div style="font-size:0.85rem;color:#444;line-height:1.7">{bulky}</div>'
                      f'<div style="font-size:0.8rem;color:#888;margin-top:8px">📍 배출장소: {bulky_place}</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )
            place_type=safe(row_s["배출장소유형"]); place=safe(row_s["배출장소"])
            bg_p="#F0FDF6" if place_type=="문전수거" else "#FFFBF0"
            icon_p="🏠" if place_type=="문전수거" else "🗂️"
            st.markdown(
                f'<div class="card" style="background:{bg_p}">'
                  f'<div style="font-size:0.9rem;font-weight:800">{icon_p} {place_type}</div>'
                  f'<div style="font-size:0.82rem;color:#555;margin-top:5px">{place}</div>'
                "</div>",
                unsafe_allow_html=True,
            )

        with info_r:
            phone=safe(row_s["관리부서전화번호"]); dept=safe(row_s["관리부서명"])
            st.markdown('<div class="sec-title">📞 관할 부서</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="contact-box">'
                  "<div>"
                    f'<div style="font-size:0.75rem;color:#888">{dept}</div>'
                    f'<div style="font-size:1.2rem;font-weight:800;color:#1AA7EC;margin-top:3px">{phone}</div>'
                  "</div>"
                  '<span style="font-size:1.8rem">📲</span>'
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"[📞 전화 걸기](tel:{phone.replace('-','')})")
    else:
        st.info(f"{sel} 상세 정보가 없어요.")


# ════════════════════════════════════════════════════
# PAGE 3 — 분리배출 도감
# ════════════════════════════════════════════════════
elif menu == "📖 분리배출 도감":
    st.markdown('<div class="sec-title">📖 알쏭달쏭 분리배출 도감</div>', unsafe_allow_html=True)

    sf1, sf2, sf3 = st.columns([3,1.5,1], gap="medium")
    with sf1:
        search = st.text_input("🔍 검색", placeholder="우유팩, 라면봉지, 페트병…", label_visibility="collapsed")
    with sf2:
        cat_sel = st.selectbox("카테고리",
            ["전체","♻️ 재활용","🗑️ 일반쓰레기","🍖 음식물","⚠️ 특수"],
            label_visibility="collapsed")
    with sf3:
        st.markdown('<div style="padding-top:8px;font-size:0.8rem;color:#888">총 12개 품목</div>', unsafe_allow_html=True)

    cat_map = {"전체":"all","♻️ 재활용":"recycle","🗑️ 일반쓰레기":"general","🍖 음식물":"food","⚠️ 특수":"special"}
    filtered = [w for w in WASTE_DB
                if (not search.strip() or search in w["name"] or search in w["ct"])
                and (cat_map[cat_sel]=="all" or w["cat"]==cat_map[cat_sel])]

    if not filtered:
        st.info("검색 결과가 없어요 🔍")
    else:
        cards_html = '<div class="waste-grid">' + "".join(render_waste_card(w) for w in filtered) + "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

    if DATA_OK and sel in df_sch.index:
        row_s2 = df_sch.loc[sel]
        rd = safe(row_s2["재활용품배출요일"])
        rt = safe(row_s2["재활용품배출시작시각"])+"~"+safe(row_s2["재활용품배출종료시각"])
        fd = safe(row_s2["음식물쓰레기배출요일"])
        ft = safe(row_s2["음식물쓰레기배출시작시각"])+"~"+safe(row_s2["음식물쓰레기배출종료시각"])
        st.markdown(
            '<div class="card" style="margin-top:16px;background:linear-gradient(135deg,#E8FFF5,#EEF9FF)">'
              f'<div style="font-weight:800;font-size:1rem;margin-bottom:8px">📍 {sel} 배출 일정 연동</div>'
              '<div style="font-size:0.85rem;line-height:2">'
                f'♻️ 재활용품: <b>{rd}요일</b> &nbsp; {rt}<br>'
                f'🍖 음식물쓰레기: <b>{fd}요일</b> &nbsp; {ft}'
              "</div>"
            "</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════
# PAGE 4 — 에코 마일리지
# ════════════════════════════════════════════════════
elif menu == "⭐ 에코 마일리지":
    lv      = get_lv(st.session_state.pts)
    next_lv = next((l for l in LEVEL_INFO if l["min"] > lv["min"]), None)
    pct     = int(((st.session_state.pts-lv["min"])/(next_lv["min"]-lv["min"]))*100) if next_lv else 100
    next_min = next_lv["min"] if next_lv else "MAX"
    remain   = (next_lv["min"]-st.session_state.pts) if next_lv else 0
    xp_suf   = f"다음 레벨까지 {remain}P" if next_lv else "🏆 최고 레벨 달성!"

    # 포인트 히어로 + 캐릭터 (2컬럼)
    ph, ch = st.columns([1, 2], gap="large")
    with ph:
        st.markdown(
            '<div class="pt-hero">'
              "<div>"
                '<div style="font-size:0.88rem;opacity:0.85">나의 에코 마일리지</div>'
                f'<div class="pt-hero-num">{st.session_state.pts}</div>'
                '<div class="pt-hero-sub">포인트 보유 중 ✨</div>'
              "</div>"
              f'<div style="font-size:4rem">{lv["emoji"]}</div>'
            "</div>",
            unsafe_allow_html=True,
        )
    with ch:
        st.markdown(
            '<div class="char-box">'
              f'<span style="font-size:3.5rem;flex-shrink:0">{lv["emoji"]}</span>'
              "<div style='flex:1'>"
                f'<div style="font-size:0.8rem;font-weight:700;color:#3ECF8E">{lv["name"]}</div>'
                '<div style="font-size:1.1rem;font-weight:800;margin:3px 0">나의 쓰레기 요정</div>'
                '<div class="xp-track">'
                  f'<div class="xp-fill" style="width:{pct}%"></div>'
                "</div>"
                f'<div class="xp-label">{st.session_state.pts} / {next_min} P  ·  {xp_suf}</div>'
              "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<div class="sec-title">💰 포인트 적립하기</div>', unsafe_allow_html=True)

    e1, e2, e3, e4 = st.columns(4, gap="large")

    with e1:
        with st.container(border=True):
            st.markdown("#### 📸 분리배출 AI 인증")
            st.markdown('<span class="earn-pts">+50P</span>', unsafe_allow_html=True)
            st.caption("올바르게 분리한 쓰레기 사진을 업로드하세요!")
            uploaded = st.file_uploader("사진", type=["jpg","jpeg","png"], label_visibility="collapsed")
            if uploaded: st.image(uploaded, width=160)
            if st.button("✅ AI 인증하기", use_container_width=True, key="ai"):
                if uploaded:
                    st.session_state.pts+=50; st.success("🎉 +50P!"); st.balloons(); st.rerun()
                else: st.warning("사진을 먼저 올려 주세요!")

    with e2:
        with st.container(border=True):
            st.markdown("#### ❓ OX 퀴즈")
            st.markdown('<span class="earn-pts">+10P</span>', unsafe_allow_html=True)
            quiz = QUIZZES[st.session_state.q_idx]
            st.markdown(f'**"{quiz["q"]}"**')
            if not st.session_state.q_done:
                qa, qb = st.columns(2)
                with qa:
                    if st.button("⭕ O", use_container_width=True, key="qO"):
                        st.session_state.q_done=True; st.session_state.q_user_ans=True; st.rerun()
                with qb:
                    if st.button("❌ X", use_container_width=True, key="qX"):
                        st.session_state.q_done=True; st.session_state.q_user_ans=False; st.rerun()
            else:
                correct = st.session_state.q_user_ans==quiz["ans"]
                if correct:
                    st.success(f"🎉 정답! {quiz['exp']}")
                    if not st.session_state.q_pts_given:
                        st.session_state.pts+=10; st.session_state.q_pts_given=True
                else: st.error(f"😢 오답! {quiz['exp']}")
                if st.button("🔄 다음 퀴즈", use_container_width=True):
                    st.session_state.q_idx=random.randint(0,len(QUIZZES)-1)
                    st.session_state.q_done=False; st.session_state.q_user_ans=None
                    st.session_state.q_pts_given=False; st.rerun()

    with e3:
        with st.container(border=True):
            st.markdown("#### 📱 SNS 챌린지")
            st.markdown('<span class="earn-pts">+500P</span>', unsafe_allow_html=True)
            st.caption("분리배출 영상을 SNS에 올리고 링크 인증!")
            link = st.text_input("링크", placeholder="https://instagram.com/...", label_visibility="collapsed")
            if st.button("📣 인증하기", use_container_width=True):
                if link.strip():
                    st.session_state.pts+=500; st.success("🎬 +500P!"); st.balloons(); st.rerun()
                else: st.warning("링크를 입력해 주세요!")

    with e4:
        with st.container(border=True):
            st.markdown("#### 🏘️ 동네 녹색 달성")
            st.markdown('<span class="earn-pts">+200P</span>', unsafe_allow_html=True)
            if DATA_OK and sel in df_amt.index:
                g = df_amt.loc[sel,"등급"]
                if g=="green":
                    st.success(f"🌿 {sel} 녹색 달성!")
                    if st.button("🎁 보너스", use_container_width=True):
                        st.session_state.pts+=200; st.success("+200P!"); st.rerun()
                elif g=="orange": st.warning("🟠 조금만 더!")
                else: st.error("🔴 배출량을 줄여요!")

    st.markdown("---")
    st.markdown('<div class="sec-title">🛍️ 포인트 사용하기</div>', unsafe_allow_html=True)
    spend_list = [
        ("🛒","종량제 봉투",100),("☕","카페 쿠폰",300),("🧻","재생 화장지",150),
        ("🥛","편의점 쿠폰",200),("🌱","환경단체 기부",50),("🐾","유기동물 기부",50),
    ]
    sp_cols = st.columns(6, gap="medium")
    for i,(icon,name,cost) in enumerate(spend_list):
        with sp_cols[i]:
            st.markdown(
                f'<div class="spend-box">'
                  f'<span class="spend-icon">{icon}</span>'
                  f'<div class="spend-name">{name}</div>'
                  f'<div class="spend-pts">{cost} P</div>'
                "</div>",
                unsafe_allow_html=True,
            )
            if st.button("교환", key=f"sp_{i}", use_container_width=True):
                if st.session_state.pts>=cost:
                    st.session_state.pts-=cost; st.success(f"✅ {name} 교환!"); st.rerun()
                else: st.error("포인트 부족 😢")

    st.markdown("---")
    st.markdown('<div class="sec-title">🌱 캐릭터 성장 가이드</div>', unsafe_allow_html=True)
    lv_cols = st.columns(4, gap="large")
    for i, li in enumerate(LEVEL_INFO):
        done = st.session_state.pts >= li["min"]
        with lv_cols[i]:
            st.markdown(
                f'<div class="lv-box {"done" if done else ""}">'
                  f'<span style="font-size:2.5rem;display:block;margin-bottom:6px">{li["emoji"]}</span>'
                  f'<div style="font-size:0.85rem;font-weight:800">{li["name"]}</div>'
                  f'<div style="font-size:0.73rem;color:#AAB;margin-top:3px">{li["min"]}P~</div>'
                  + ('<div style="color:#3ECF8E;font-size:0.75rem;font-weight:700;margin-top:4px">✅ 달성!</div>' if done else "")
                + "</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
