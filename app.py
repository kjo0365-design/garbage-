import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import os
import shutil

# ══════════════════════════════════════
# 페이지 설정
# ══════════════════════════════════════
st.set_page_config(
    page_title="쓰레기 요정 🧚",
    page_icon="🧚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════
# CSS  (상단 잘림 수정 + 앱 스타일)
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nanum Gothic', sans-serif;
    background: #F4F6FB;
}

/* ── 상단 잘림 수정: Streamlit 기본 여백 제거 ── */
#root > div:first-child { margin-top: 0 !important; }
.stApp > header { display: none !important; }
.stApp { margin-top: 0 !important; padding-top: 0 !important; }
div[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
div[data-testid="stMain"] { padding-top: 0 !important; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 520px !important;
}

/* ── 앱바 ── */
.appbar {
    background: linear-gradient(135deg, #3ECF8E 0%, #1AA7EC 100%);
    border-radius: 0 0 28px 28px;
    padding: 28px 24px 34px;
    color: white;
    position: relative;
    margin-bottom: 0;
}
.appbar-title { font-size: 1.35rem; font-weight: 800; }
.appbar-sub   { font-size: 0.82rem; opacity: 0.85; margin-top: 3px; }
.appbar-badge {
    position: absolute; top: 22px; right: 20px;
    background: rgba(255,255,255,0.25);
    border-radius: 20px; padding: 6px 14px;
    font-size: 0.85rem; font-weight: 800; color: white;
}

/* ── 카드 ── */
.card {
    background: white;
    border-radius: 20px;
    padding: 16px 18px;
    margin: 10px 14px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
}
.card-title {
    font-size: 0.74rem; font-weight: 700;
    color: #888; text-transform: uppercase;
    letter-spacing: 0.5px; margin-bottom: 8px;
}
.sec-header {
    font-size: 1rem; font-weight: 800; color: #1A1A2E;
    padding: 8px 14px 4px; margin-top: 6px;
}

/* ── 요일 뱃지 ── */
.days-wrap { display:flex; gap:5px; flex-wrap:wrap; margin:8px 0; }
.day-on  { background:#3ECF8E; color:white;  padding:5px 10px; border-radius:10px; font-size:0.82rem; font-weight:700; display:inline-block; }
.day-off { background:#F0F2F5; color:#C0C7D0; padding:5px 10px; border-radius:10px; font-size:0.82rem; font-weight:700; display:inline-block; }

/* ── 배너 ── */
.banner-red    { background:#FF6B6B; color:white; border-radius:14px; padding:12px 16px; margin:8px 14px; font-size:0.85rem; font-weight:700; }
.banner-green  { background:#3ECF8E; color:white; border-radius:14px; padding:12px 16px; margin:8px 14px; font-size:0.85rem; font-weight:700; }
.banner-orange { background:#FFB347; color:white; border-radius:14px; padding:12px 16px; margin:8px 14px; font-size:0.85rem; font-weight:700; }

/* ── 쓰레기 아이템 ── */
.waste-item {
    background: white;
    border-radius: 16px;
    padding: 14px 16px;
    margin: 8px 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.waste-emoji { font-size:2rem; flex-shrink:0; margin-top:2px; }
.waste-info  { flex:1; min-width:0; }
.waste-name  { font-size:0.97rem; font-weight:800; color:#1A1A2E; }
.waste-cat   {
    display:inline-block; padding:2px 9px;
    border-radius:8px; font-size:0.72rem; font-weight:700;
    margin:3px 0 6px;
}
.waste-step  { font-size:0.79rem; color:#555; line-height:1.6; }
.tip-chip  {
    background:#E8FFF5; color:#00A86B;
    border-radius:8px; padding:5px 10px;
    font-size:0.76rem; font-weight:700;
    margin-top:6px; display:block;
}
.warn-chip {
    background:#FFF8E1; color:#F57F17;
    border-radius:8px; padding:5px 10px;
    font-size:0.76rem; font-weight:700;
    margin-top:4px; display:block;
}

/* ── 포인트 히어로 ── */
.pt-hero {
    background: linear-gradient(135deg,#FFD93D,#FF9A3C);
    border-radius:20px; margin:10px 14px;
    padding:22px; color:white; text-align:center;
}
.pt-hero-num { font-size:3rem; font-weight:800; line-height:1; }
.pt-hero-sub { font-size:0.82rem; opacity:0.85; margin-top:4px; }

/* ── 캐릭터 ── */
.char-box {
    background:white; border-radius:20px; margin:10px 14px;
    padding:18px; box-shadow:0 2px 16px rgba(0,0,0,0.07);
    display:flex; align-items:center; gap:14px;
}
.xp-track { height:8px; background:#F0F2F5; border-radius:4px; margin-top:6px; overflow:hidden; }
.xp-fill  { height:100%; border-radius:4px; background:linear-gradient(90deg,#3ECF8E,#1AA7EC); }
.xp-label { font-size:0.72rem; color:#999; margin-top:3px; }

/* ── 순위 ── */
.rank-item {
    background:white; border-radius:12px; padding:10px 14px;
    margin:5px 14px; display:flex; align-items:center; gap:10px;
    box-shadow:0 1px 8px rgba(0,0,0,0.05);
}

/* ── 연락처 ── */
.contact-box {
    background:white; border-radius:16px; padding:14px 16px;
    margin:8px 14px; box-shadow:0 2px 12px rgba(0,0,0,0.06);
    display:flex; align-items:center; justify-content:space-between;
}
.no-day-box {
    background:#FFF3F3; border-radius:12px; padding:10px 14px;
    margin:6px 14px; border-left:4px solid #FF6B6B;
    font-size:0.82rem; color:#CC3333;
}
.lv-box {
    background:white; border-radius:14px; padding:14px 12px;
    text-align:center; box-shadow:0 2px 10px rgba(0,0,0,0.05);
    border:2px solid #F0F2F5; margin-bottom:8px;
}
.lv-box.done { border-color:#3ECF8E; background:#F0FDF6; }

/* ── 서울 SVG 지도 스타일 ── */
.map-wrap {
    background: white; border-radius: 20px;
    margin: 10px 14px; padding: 16px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    position: relative;
}
.gu-path { cursor: pointer; stroke: white; stroke-width: 1.5; transition: all 0.2s; }
.gu-path:hover { stroke: #333; stroke-width: 2.5; filter: brightness(0.88); }

/* ── 맵 툴팁 ── */
.map-tooltip {
    position: absolute;
    background: white;
    border-radius: 14px;
    padding: 10px 14px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.15);
    pointer-events: none;
    display: none;
    z-index: 999;
    min-width: 160px;
    border: 2px solid #3ECF8E;
    font-size: 0.82rem;
}

/* ── Streamlit 요소 패딩 ── */
div[data-testid="stSelectbox"] { padding: 0 14px; }
div[data-testid="stTextInput"] { padding: 0 14px; }
div[data-testid="stFileUploader"] { padding: 0 14px; }
div[data-testid="stButton"] > button {
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-family: 'Nanum Gothic', sans-serif !important;
}
button[data-baseweb="tab"] {
    font-family: 'Nanum Gothic', sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# 파일 경로 자동 처리
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
    df.columns = ["구", "1인당", "총량", "주민수"]
    df = df.iloc[2:].copy()
    df = df[df["구"] != "계"]
    df["구"] = df["구"].str.strip()
    for c in ["1인당", "총량", "주민수"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    def lv(v):
        return "red" if v >= 2.0 else ("orange" if v >= 1.2 else "green")
    df["등급"] = df["1인당"].apply(lv)
    return df.set_index("구")

@st.cache_data
def load_schedule():
    df = pd.read_csv("seoul_garbage.csv", encoding="cp949")
    keep = [
        "시군구명", "배출장소유형", "배출장소",
        "생활쓰레기배출방법", "음식물쓰레기배출방법", "재활용품배출방법",
        "일시적다량폐기물배출방법", "일시적다량폐기물배출장소",
        "생활쓰레기배출요일", "음식물쓰레기배출요일", "재활용품배출요일",
        "생활쓰레기배출시작시각", "생활쓰레기배출종료시각",
        "음식물쓰레기배출시작시각", "음식물쓰레기배출종료시각",
        "재활용품배출시작시각", "재활용품배출종료시각",
        "미수거일", "관리부서명", "관리부서전화번호",
    ]
    df = df[keep].drop_duplicates(subset=["시군구명"], keep="first")
    return df.set_index("시군구명")

try:
    df_amt  = load_amount()
    df_sch  = load_schedule()
    DATA_OK = True
except Exception as e:
    DATA_OK  = False
    DATA_ERR = str(e)


# ══════════════════════════════════════
# 상수 & 유틸
# ══════════════════════════════════════
CLR  = {"red": "#FF6B6B", "orange": "#FFB347", "green": "#3ECF8E"}
EMJ  = {"red": "😰",       "orange": "😅",       "green": "😊"}
LBL  = {"red": "🔴 경고",  "orange": "🟠 보통",  "green": "🟢 우수"}
DAYS = ["일", "월", "화", "수", "목", "금", "토"]

LEVEL_INFO = [
    {"min": 0,    "max": 200,   "emoji": "🌱", "name": "LV.1 새싹 쓰요"},
    {"min": 200,  "max": 500,   "emoji": "🌿", "name": "LV.2 잎사귀 쓰요"},
    {"min": 500,  "max": 1000,  "emoji": "🌺", "name": "LV.3 꽃단장 쓰요"},
    {"min": 1000, "max": 99999, "emoji": "🌍", "name": "LV.4 지구 수호자 쓰요"},
]

# ── 분리배출 도감 데이터 ──
# HTML f-string 따옴표 충돌 방지: 딕셔너리 값을 변수로 꺼내서 사용
WASTE_DB = [
    {
        "name": "우유팩", "emoji": "🥛", "cat": "recycle",
        "cc": "#B7F0D5", "cf": "#00A86B", "ct": "♻️ 종이팩",
        "steps": "① 비우기  ② 헹구기  ③ 펼치기  ④ 따로 배출",
        "tip": "동주민센터에 모으면 화장지/봉투 교환 가능!",
        "warn": None,
    },
    {
        "name": "라면봉지", "emoji": "🍜", "cat": "recycle",
        "cc": "#B7F0D5", "cf": "#00A86B", "ct": "♻️ 비닐류",
        "steps": "① 오염 확인  ② 펼치기  ③ 비닐봉투에 담아 배출",
        "tip": "딱지로 접으면 선별 ❌  꼭 펼쳐요.",
        "warn": "국물 많이 묻었으면 → 종량제 봉투",
    },
    {
        "name": "투명 페트병", "emoji": "🍼", "cat": "recycle",
        "cc": "#B7F0D5", "cf": "#00A86B", "ct": "♻️ 투명 페트",
        "steps": "① 비우기  ② 라벨 제거  ③ 압착  ④ 배출",
        "tip": "색깔 병과 반드시 따로 분리!",
        "warn": None,
    },
    {
        "name": "음식물쓰레기", "emoji": "🍖", "cat": "food",
        "cc": "#FFE9A0", "cf": "#B8860B", "ct": "🍖 음식물",
        "steps": "① 물기 제거  ② 잘게 썰기  ③ 전용봉투  ④ 배출",
        "tip": "물기를 꼭 짜야 냄새 ❌",
        "warn": "뼈·껍데기·씨앗 → 일반쓰레기",
    },
    {
        "name": "깨진 유리", "emoji": "🪞", "cat": "special",
        "cc": "#E8D5FF", "cf": "#6B21A8", "ct": "⚠️ 불연성",
        "steps": "① 신문지로 싸기  ② '위험' 표시  ③ 불연성 전용마대",
        "tip": "수거자 부상 방지! 꼭 싸 주세요.",
        "warn": "일반 종량제 봉투 ❌",
    },
    {
        "name": "종이컵", "emoji": "☕", "cat": "recycle",
        "cc": "#B7F0D5", "cf": "#00A86B", "ct": "♻️ 종이팩",
        "steps": "① 씻기  ② 펼치기  ③ 따로 모아 배출",
        "tip": "따로 배출 시 화장지로 재활용!",
        "warn": None,
    },
    {
        "name": "스티로폼", "emoji": "📦", "cat": "recycle",
        "cc": "#B7F0D5", "cf": "#00A86B", "ct": "♻️ 발포합성수지",
        "steps": "① 이물질 제거  ② 테이프 제거  ③ 부숴서 배출",
        "tip": "음식 묻었으면 씻어서 배출",
        "warn": "오염 심하면 → 일반쓰레기",
    },
    {
        "name": "헌 옷", "emoji": "👕", "cat": "special",
        "cc": "#E8D5FF", "cf": "#6B21A8", "ct": "⚠️ 의류수거함",
        "steps": "① 세탁  ② 묶음 포장  ③ 의류수거함 배출",
        "tip": "수거함 위치 → 동주민센터 앱 확인",
        "warn": "속옷·양말 → 일반쓰레기",
    },
    {
        "name": "폐건전지", "emoji": "🔋", "cat": "special",
        "cc": "#E8D5FF", "cf": "#6B21A8", "ct": "⚠️ 폐전지",
        "steps": "① 따로 모으기  ② 전지 수거함  ③ 배출",
        "tip": "마트·편의점·주민센터 전지 수거함 이용",
        "warn": "일반쓰레기 ❌  화재·환경오염 위험",
    },
    {
        "name": "치킨뼈", "emoji": "🍗", "cat": "general",
        "cc": "#FFD6D6", "cf": "#CC3333", "ct": "🗑️ 일반쓰레기",
        "steps": "① 종량제 봉투에 담아 배출",
        "tip": "딱딱한 뼈 → 음식물 ❌",
        "warn": "음식물 수거함 ❌",
    },
    {
        "name": "달걀껍데기", "emoji": "🥚", "cat": "general",
        "cc": "#FFD6D6", "cf": "#CC3333", "ct": "🗑️ 일반쓰레기",
        "steps": "① 종량제 봉투에 담아 배출",
        "tip": "단단해서 음식물 처리 불가",
        "warn": "음식물 수거함 ❌",
    },
    {
        "name": "커피찌꺼기", "emoji": "☕", "cat": "food",
        "cc": "#FFE9A0", "cf": "#B8860B", "ct": "🍖 음식물",
        "steps": "① 물기 제거  ② 전용봉투  ③ 배출",
        "tip": "화분 퇴비로도 활용 가능!",
        "warn": None,
    },
]

QUIZZES = [
    {"q": "라면봉지는 딱지로 접어서 버려야 재활용이 잘 된다.", "ans": False,
     "exp": "딱지로 접으면 선별 ❌  꼭 펼쳐요!"},
    {"q": "우유팩은 일반 종이와 함께 버려도 된다.", "ans": False,
     "exp": "우유팩은 별도 재질 — 씻어서 펼친 후 따로 배출!"},
    {"q": "깨끗한 비닐은 재활용이 가능하다.", "ans": True,
     "exp": "맞아요! 오염됐으면 일반쓰레기로."},
    {"q": "달걀껍데기는 음식물 쓰레기로 버려야 한다.", "ans": False,
     "exp": "달걀껍데기 → 일반쓰레기!"},
    {"q": "투명 페트병은 라벨을 제거하고 배출해야 한다.", "ans": True,
     "exp": "라벨 제거 + 압착 후 투명 페트 전용 배출!"},
    {"q": "치킨뼈는 음식물 쓰레기로 버려야 한다.", "ans": False,
     "exp": "딱딱한 뼈 → 종량제 봉투(일반쓰레기)!"},
    {"q": "폐건전지는 일반쓰레기로 버려도 된다.", "ans": False,
     "exp": "폐전지 → 반드시 별도 수거함에 배출!"},
]


def safe(v, d="정보 없음"):
    return d if pd.isna(v) or str(v).strip() in ("", "nan", "NaN") else str(v).strip()


def day_html(day_str):
    if pd.isna(day_str) or not str(day_str).strip():
        return "<span style='color:#ccc'>정보 없음</span>"
    active = set(str(day_str).replace(" ", "").split("+"))
    parts = []
    for d in DAYS:
        cls = "day-on" if d in active else "day-off"
        parts.append(f'<span class="{cls}">{d}</span>')
    return '<div class="days-wrap">' + "".join(parts) + "</div>"


def get_lv(pts):
    for lv in LEVEL_INFO:
        if lv["min"] <= pts < lv["max"]:
            return lv
    return LEVEL_INFO[-1]


def render_waste_item(w):
    """HTML 태그 쌍이 정확히 맞도록 변수로 분리해서 조립"""
    name    = w["name"]
    emoji   = w["emoji"]
    cc      = w["cc"]
    cf      = w["cf"]
    ct      = w["ct"]
    steps   = w["steps"]
    tip     = w["tip"]
    warn    = w["warn"]

    tip_block  = f'<span class="tip-chip">💡 {tip}</span>'   if tip  else ""
    warn_block = f'<span class="warn-chip">⚠️ {warn}</span>' if warn else ""

    html = (
        '<div class="waste-item">'
          f'<div class="waste-emoji">{emoji}</div>'
          '<div class="waste-info">'
            f'<div class="waste-name">{name}</div>'
            f'<span class="waste-cat" style="background:{cc};color:{cf}">{ct}</span>'
            f'<div class="waste-step">{steps}</div>'
            + tip_block
            + warn_block
          + "</div>"
        + "</div>"
    )
    return html


# ══════════════════════════════════════
# 서울시 SVG 지도 (Plotly Choropleth)
# ══════════════════════════════════════
def build_map_chart(df_amt, selected_gu):
    """Plotly scatter geo 대신 bar를 쓰되, 실제 지도는 Plotly의 geojson 방식 사용"""
    df_c = df_amt.reset_index().sort_values("1인당", ascending=True)

    bar_colors = [
        "#1A1A2E" if r["구"] == selected_gu else CLR[r["등급"]]
        for _, r in df_c.iterrows()
    ]

    fig = go.Figure()
    for i, row in df_c.iterrows():
        is_sel = row["구"] == selected_gu
        amt = row["1인당"]
        lv  = row["등급"]
        gu  = row["구"]
        pop = int(row["주민수"])
        tot = row["총량"]
        fig.add_trace(go.Bar(
            x=[amt], y=[gu],
            orientation="h",
            marker_color="#1A1A2E" if is_sel else CLR[lv],
            marker_line_width=0,
            text=f" {amt}" if is_sel else "",
            textposition="outside",
            textfont=dict(size=10),
            showlegend=False,
            hovertemplate=(
                f"<b>{EMJ[lv]} {gu}</b><br>"
                f"1인당: <b>{amt} kg/일</b><br>"
                f"총량: {tot} 톤/일<br>"
                f"주민: {pop:,}명<br>"
                f"등급: {LBL[lv]}<extra></extra>"
            ),
        ))

    fig.add_vline(x=1.2, line_dash="dot", line_color="#3ECF8E", line_width=1.5,
                  annotation_text="우수 기준", annotation_font_color="#3ECF8E",
                  annotation_font_size=10)
    fig.add_vline(x=2.0, line_dash="dot", line_color="#FF6B6B", line_width=1.5,
                  annotation_text="경고 기준", annotation_font_color="#FF6B6B",
                  annotation_font_size=10)

    fig.update_layout(
        height=600,
        margin=dict(l=0, r=48, t=16, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(gridcolor="#F0F2F5", range=[0, 3.4], title="kg/일"),
        yaxis=dict(gridcolor="white"),
        font=dict(family="Nanum Gothic", size=11),
        bargap=0.28,
        title=dict(text=f"서울 25개구 1인당 배출량 (2024)  ◼ = {selected_gu}",
                   x=0.5, font=dict(size=12, color="#1A1A2E")),
    )
    return fig


# ══════════════════════════════════════
# 서울시 인터랙티브 SVG 지도 (HTML)
# ══════════════════════════════════════
def build_svg_map(df_amt, selected_gu):
    """실제 서울 구 SVG + 마우스오버 툴팁"""

    # 각 구 GeoJSON 근사 polygon (SVG viewBox 560×480 기준)
    GU_PATHS = {
        "도봉구":   "M270,28 L340,22 L365,55 L345,80 L300,85 L268,65 Z",
        "노원구":   "M340,22 L425,26 L440,62 L405,88 L365,82 L365,55 Z",
        "강북구":   "M240,62 L270,28 L268,65 L300,85 L295,108 L265,115 L242,95 Z",
        "성북구":   "M265,115 L295,108 L350,108 L372,130 L348,152 L310,158 L278,148 Z",
        "중랑구":   "M365,82 L405,88 L428,110 L408,140 L378,148 L372,130 L350,108 Z",
        "동대문구": "M310,158 L348,152 L372,130 L378,148 L360,170 L330,175 L308,170 Z",
        "광진구":   "M378,148 L408,140 L435,162 L418,192 L388,198 L360,188 L360,170 Z",
        "성동구":   "M308,170 L330,175 L360,170 L360,188 L345,210 L315,215 L292,200 Z",
        "종로구":   "M198,72 L240,62 L242,95 L265,115 L278,148 L250,162 L218,155 L195,132 L188,102 Z",
        "중구":     "M218,155 L250,162 L278,148 L310,158 L308,170 L292,200 L268,210 L240,200 L220,182 Z",
        "용산구":   "M220,182 L240,200 L268,210 L260,238 L238,250 L210,240 L200,218 Z",
        "은평구":   "M115,72 L198,72 L188,102 L195,132 L165,148 L128,140 L105,108 Z",
        "서대문구": "M165,148 L195,132 L218,155 L220,182 L200,218 L172,222 L148,202 L140,172 Z",
        "마포구":   "M96,178 L140,172 L148,202 L172,222 L162,255 L130,268 L88,252 L75,218 Z",
        "강서구":   "M38,248 L88,252 L130,268 L125,318 L88,340 L42,318 L28,282 Z",
        "양천구":   "M88,252 L130,268 L148,315 L130,342 L88,340 L88,310 Z",
        "영등포구": "M130,268 L162,255 L188,268 L198,305 L182,342 L148,348 L130,342 L148,315 Z",
        "구로구":   "M88,310 L130,342 L148,348 L140,378 L100,385 L72,362 L68,330 Z",
        "금천구":   "M100,385 L140,378 L162,392 L158,422 L122,428 L98,408 Z",
        "동작구":   "M182,342 L215,330 L248,348 L242,382 L208,392 L182,378 L170,358 Z",
        "관악구":   "M148,348 L182,342 L170,358 L182,378 L208,392 L200,422 L162,428 L158,422 L162,392 L140,378 Z",
        "서초구":   "M248,348 L295,335 L325,355 L322,400 L285,415 L252,408 L242,382 Z",
        "강남구":   "M325,355 L385,348 L418,360 L422,415 L388,432 L348,440 L322,420 L322,400 Z",
        "송파구":   "M418,228 L482,222 L508,268 L492,332 L448,358 L418,360 L385,348 L388,305 L405,272 Z",
        "강동구":   "M482,165 L545,158 L568,200 L552,258 L508,268 L482,222 L440,205 L435,162 Z",
    }

    # 툴팁용 데이터 JSON 문자열 생성
    tooltip_data_parts = []
    for gu, row in df_amt.iterrows():
        lv_c  = row["등급"]
        amt   = row["1인당"]
        tot   = row["총량"]
        pop   = int(row["주민수"])
        lbl   = LBL[lv_c]
        clr   = CLR[lv_c]
        emj   = EMJ[lv_c]
        tooltip_data_parts.append(
            f'"{gu}":{{"amt":{amt},"tot":{tot},"pop":{pop},"lbl":"{lbl}","clr":"{clr}","emj":"{emj}"}}'
        )
    tooltip_json = "{" + ",".join(tooltip_data_parts) + "}"

    # SVG path 생성
    path_parts = []
    for gu, path_d in GU_PATHS.items():
        if gu in df_amt.index:
            lv_c = df_amt.loc[gu, "등급"]
            fill = "#2D2D5E" if gu == selected_gu else CLR[lv_c]
            stroke_w = "2.5" if gu == selected_gu else "1.5"
            path_parts.append(
                f'<path d="{path_d}" fill="{fill}" stroke="white" stroke-width="{stroke_w}" '
                f'class="gu-path" data-gu="{gu}" />'
            )
        else:
            path_parts.append(
                f'<path d="{path_d}" fill="#DDD" stroke="white" stroke-width="1.5" '
                f'class="gu-path" data-gu="{gu}" />'
            )

    # 구 이름 라벨 (중심 좌표 근사)
    LABEL_POS = {
        "도봉구": (308, 55), "노원구": (395, 55), "강북구": (268, 82),
        "성북구": (318, 132), "중랑구": (395, 118), "동대문구": (340, 163),
        "광진구": (400, 172), "성동구": (328, 196), "종로구": (225, 115),
        "중구": (260, 178), "용산구": (232, 218), "은평구": (148, 108),
        "서대문구": (175, 185), "마포구": (122, 225), "강서구": (78, 295),
        "양천구": (112, 300), "영등포구": (162, 308), "구로구": (108, 348),
        "금천구": (130, 402), "동작구": (212, 362), "관악구": (175, 388),
        "서초구": (282, 378), "강남구": (368, 400), "송파구": (448, 295),
        "강동구": (498, 215),
    }
    label_parts = []
    for gu, (lx, ly) in LABEL_POS.items():
        color = "white" if gu == selected_gu else "#fff"
        label_parts.append(
            f'<text x="{lx}" y="{ly}" text-anchor="middle" '
            f'font-size="9" font-family="Nanum Gothic" fill="{color}" '
            f'pointer-events="none" font-weight="700">{gu[:3]}</text>'
        )

    svg_paths  = "\n".join(path_parts)
    svg_labels = "\n".join(label_parts)

    html = f"""
<div class="map-wrap" id="mapWrap" style="position:relative">
  <div style="font-size:0.78rem;color:#888;margin-bottom:8px;font-weight:700">
    🗺️ 구에 마우스를 올리면 정보가 표시돼요  ·  클릭하면 선택
  </div>
  <svg id="seoulMap" viewBox="0 0 580 460" width="100%" style="display:block">
    {svg_paths}
    {svg_labels}
  </svg>

  <div id="mapTooltip" style="
    display:none; position:fixed;
    background:white; border-radius:14px; padding:10px 14px;
    box-shadow:0 6px 28px rgba(0,0,0,0.18); z-index:9999;
    min-width:160px; border:2px solid #3ECF8E;
    font-family:'Nanum Gothic',sans-serif; font-size:0.82rem;
    pointer-events:none;">
  </div>

  <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">
    <span style="background:#3ECF8E;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🟢 우수 ~1.2 kg</span>
    <span style="background:#FFB347;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🟠 보통 1.2~2.0 kg</span>
    <span style="background:#FF6B6B;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">🔴 경고 2.0+ kg</span>
    <span style="background:#2D2D5E;color:white;padding:3px 10px;border-radius:8px;font-size:0.7rem;font-weight:700">◼ 선택</span>
  </div>
</div>

<script>
(function() {{
  var DATA = {tooltip_json};
  var tooltip = document.getElementById('mapTooltip');
  var paths   = document.querySelectorAll('#seoulMap .gu-path');

  paths.forEach(function(p) {{
    p.addEventListener('mousemove', function(e) {{
      var gu   = p.getAttribute('data-gu');
      var info = DATA[gu];
      if (!info) return;
      tooltip.innerHTML =
        '<b style="font-size:0.9rem">' + info.emj + ' ' + gu + '</b><br>' +
        '<span style="color:' + info.clr + ';font-weight:700">' + info.lbl + '</span><br>' +
        '1인당: <b>' + info.amt + ' kg/일</b><br>' +
        '총량: ' + info.tot + ' 톤/일<br>' +
        '주민: ' + info.pop.toLocaleString() + '명';
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 14) + 'px';
      tooltip.style.top  = (e.clientY - 10) + 'px';
    }});
    p.addEventListener('mouseleave', function() {{
      tooltip.style.display = 'none';
    }});
  }});
}})();
</script>
"""
    return html


# ══════════════════════════════════════
# 세션 초기화
# ══════════════════════════════════════
for k, v in [
    ("pts", 0), ("gu", "마포구"),
    ("q_done", False), ("q_idx", 0),
    ("q_user_ans", None), ("q_pts_given", False),
]:
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════
# 앱바 (상단 잘림 해결: padding-top:0)
# ══════════════════════════════════════
lv_now = get_lv(st.session_state.pts)
st.markdown(
    '<div class="appbar">'
      '<div class="appbar-title">🧚 서울 쓰레기 요정</div>'
      '<div class="appbar-sub">우리 동네 분리배출 가이드 · 2024</div>'
      f'<div class="appbar-badge">{lv_now["emoji"]} {st.session_state.pts}P</div>'
    "</div>",
    unsafe_allow_html=True,
)


# ══════════════════════════════════════
# 구 선택
# ══════════════════════════════════════
if DATA_OK:
    gu_list = sorted(df_amt.index.tolist())
    idx = gu_list.index(st.session_state.gu) if st.session_state.gu in gu_list else 0
    sel = st.selectbox("📍 내 동네 선택", gu_list, index=idx)
    st.session_state.gu = sel
else:
    sel = "마포구"


# ══════════════════════════════════════
# 탭
# ══════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ 배출 지도", "📅 우리동네", "📖 도감", "⭐ 포인트"])


# ════════════════════════════════════════════════
# TAB 1 — 배출량 지도
# ════════════════════════════════════════════════
with tab1:
    if not DATA_OK:
        st.error(f"데이터 오류: {DATA_ERR}")
        st.stop()

    row_a = df_amt.loc[sel]
    lv_c  = row_a["등급"]

    # 배너
    banner_html = {
        "red":    f'<div class="banner-red">🚨 {sel}은 배출량 경고! 서울 평균보다 높아요</div>',
        "green":  f'<div class="banner-green">🌿 {sel}은 배출량 우수 지역! 👍</div>',
        "orange": f'<div class="banner-orange">🟠 {sel}은 보통 수준. 조금만 더!</div>',
    }
    st.markdown(banner_html[lv_c], unsafe_allow_html=True)

    # 지표
    st.markdown('<div class="sec-header">📊 내 동네 배출 현황</div>', unsafe_allow_html=True)
    amt_val = row_a["1인당"]
    tot_val = row_a["총량"]
    pop_val = int(row_a["주민수"])
    clr_val = CLR[lv_c]
    lbl_val = LBL[lv_c]
    st.markdown(
        '<div class="card">'
          '<div class="card-title">2024년 실제 데이터 기반</div>'
          '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;text-align:center">'
            f'<div><div style="font-size:1.6rem;font-weight:800;color:{clr_val}">{amt_val}</div>'
            f'<div style="font-size:0.7rem;color:#888">kg/일 · 1인당</div>'
            f'<div style="font-size:0.7rem;font-weight:700;color:{clr_val};margin-top:2px">{lbl_val}</div></div>'
            f'<div><div style="font-size:1.4rem;font-weight:800;color:#1AA7EC">{tot_val}</div>'
            '<div style="font-size:0.7rem;color:#888">톤/일 · 총배출</div></div>'
            f'<div><div style="font-size:1.2rem;font-weight:800;color:#555">{pop_val:,}</div>'
            '<div style="font-size:0.7rem;color:#888">명 · 주민수</div></div>'
          "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── SVG 인터랙티브 지도 ──
    st.markdown('<div class="sec-header">🗺️ 서울시 구별 배출량 지도</div>', unsafe_allow_html=True)
    st.markdown(build_svg_map(df_amt, sel), unsafe_allow_html=True)

    # ── 바 차트 ──
    st.markdown('<div class="sec-header">📈 배출량 수치 비교</div>', unsafe_allow_html=True)
    fig = build_map_chart(df_amt, sel)
    st.plotly_chart(fig, use_container_width=True)

    # 순위
    st.markdown('<div class="sec-header">🏆 배출량 순위</div>', unsafe_allow_html=True)
    df_rank = df_amt.reset_index().sort_values("1인당")
    cb, cw = st.columns(2)

    with cb:
        st.markdown("**🌿 적은 TOP 5**")
        for i, (_, r) in enumerate(df_rank.head(5).iterrows(), 1):
            mark  = " ⬅" if r["구"] == sel else ""
            color = CLR[r["등급"]]
            gu_n  = r["구"]
            amt_n = r["1인당"]
            st.markdown(
                f'<div class="rank-item">'
                  f'<div style="width:22px;height:22px;border-radius:50%;'
                  f'background:{color}22;color:{color};display:flex;align-items:center;'
                  f'justify-content:center;font-size:0.72rem;font-weight:800;flex-shrink:0">{i}</div>'
                  f'<div style="flex:1;font-size:0.87rem;font-weight:700">{gu_n}'
                  f'<span style="color:#3ECF8E;font-size:0.68rem">{mark}</span></div>'
                  f'<div style="font-size:0.82rem;color:#666;font-weight:700">{amt_n}</div>'
                "</div>",
                unsafe_allow_html=True,
            )

    with cw:
        st.markdown("**🔴 많은 TOP 5**")
        for i, (_, r) in enumerate(df_rank.tail(5).iloc[::-1].iterrows(), 1):
            mark  = " ⬅" if r["구"] == sel else ""
            color = CLR[r["등급"]]
            gu_n  = r["구"]
            amt_n = r["1인당"]
            st.markdown(
                f'<div class="rank-item">'
                  f'<div style="width:22px;height:22px;border-radius:50%;'
                  f'background:{color}22;color:{color};display:flex;align-items:center;'
                  f'justify-content:center;font-size:0.72rem;font-weight:800;flex-shrink:0">{i}</div>'
                  f'<div style="flex:1;font-size:0.87rem;font-weight:700">{gu_n}'
                  f'<span style="color:#3ECF8E;font-size:0.68rem">{mark}</span></div>'
                  f'<div style="font-size:0.82rem;color:#666;font-weight:700">{amt_n}</div>'
                "</div>",
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════
# TAB 2 — 우리 동네 스케줄
# ════════════════════════════════════════════════
with tab2:
    if not DATA_OK:
        st.error("데이터 오류")
        st.stop()

    row_s = df_sch.loc[sel] if sel in df_sch.index else None
    st.markdown(f'<div class="sec-header">📍 {sel} 배출 스케줄</div>', unsafe_allow_html=True)

    if row_s is not None:
        for icon, label, d_col, s_col, e_col in [
            ("🗑️", "일반쓰레기",
             "생활쓰레기배출요일", "생활쓰레기배출시작시각", "생활쓰레기배출종료시각"),
            ("♻️", "재활용품",
             "재활용품배출요일", "재활용품배출시작시각", "재활용품배출종료시각"),
            ("🍖", "음식물",
             "음식물쓰레기배출요일", "음식물쓰레기배출시작시각", "음식물쓰레기배출종료시각"),
        ]:
            t_s = safe(row_s[s_col])
            t_e = safe(row_s[e_col])
            days_str = row_s[d_col]
            st.markdown(
                '<div class="card" style="margin-bottom:8px">'
                  f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">'
                    f'<span style="font-size:1.4rem">{icon}</span>'
                    f'<span style="font-size:0.95rem;font-weight:800">{label}</span>'
                    f'<span style="margin-left:auto;font-size:0.78rem;color:#FF6B6B;font-weight:700">⏰ {t_s} ~ {t_e}</span>'
                  "</div>"
                  + day_html(days_str)
                + "</div>",
                unsafe_allow_html=True,
            )

        # 배출 방법
        st.markdown('<div class="sec-header">📋 배출 방법</div>', unsafe_allow_html=True)
        for icon, label, col in [
            ("🗑️", "일반쓰레기", "생활쓰레기배출방법"),
            ("♻️", "재활용품",   "재활용품배출방법"),
            ("🍖", "음식물",     "음식물쓰레기배출방법"),
        ]:
            txt = safe(row_s[col])
            if txt != "정보 없음":
                st.markdown(
                    '<div class="card" style="margin-bottom:8px">'
                      f'<div style="font-size:0.8rem;font-weight:800;color:#555;margin-bottom:4px">'
                        f'{icon} {label}'
                      "</div>"
                      f'<div style="font-size:0.82rem;color:#444;line-height:1.6">{txt}</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )

        # 미수거일
        no_day = safe(row_s["미수거일"])
        if no_day not in ("정보 없음", ""):
            st.markdown(
                f'<div class="no-day-box">🚫 <b>미수거일:</b> {no_day}</div>',
                unsafe_allow_html=True,
            )

        # 대형폐기물
        bulky       = safe(row_s["일시적다량폐기물배출방법"])
        bulky_place = safe(row_s["일시적다량폐기물배출장소"])
        skip_set    = {"정보 없음", "미운영", "없음", "-", "해당없음", "해당사항없음", "별도안내", "처리업체와협의"}
        if bulky not in skip_set:
            st.markdown('<div class="sec-header">🛻 대형폐기물</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="card">'
                  f'<div style="font-size:0.82rem;color:#444;line-height:1.6">{bulky}</div>'
                  f'<div style="font-size:0.78rem;color:#888;margin-top:5px">📍 {bulky_place}</div>'
                "</div>",
                unsafe_allow_html=True,
            )

        # 배출 장소
        place_type = safe(row_s["배출장소유형"])
        place      = safe(row_s["배출장소"])
        st.markdown('<div class="sec-header">🏠 배출 장소</div>', unsafe_allow_html=True)
        bg_p   = "#F0FDF6" if place_type == "문전수거" else "#FFFBF0"
        icon_p = "🏠" if place_type == "문전수거" else "🗂️"
        st.markdown(
            f'<div class="card" style="background:{bg_p}">'
              f'<div style="font-size:0.9rem;font-weight:800">{icon_p} {place_type}</div>'
              f'<div style="font-size:0.82rem;color:#555;margin-top:4px">{place}</div>'
            "</div>",
            unsafe_allow_html=True,
        )

        # 연락처
        phone = safe(row_s["관리부서전화번호"])
        dept  = safe(row_s["관리부서명"])
        st.markdown('<div class="sec-header">📞 관할 부서</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="contact-box">'
              "<div>"
                f'<div style="font-size:0.75rem;color:#888">{dept}</div>'
                f'<div style="font-size:1.15rem;font-weight:800;color:#1AA7EC;margin-top:2px">{phone}</div>'
              "</div>"
              '<span style="font-size:1.5rem">📲</span>'
            "</div>",
            unsafe_allow_html=True,
        )
        phone_clean = phone.replace("-", "")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;[📞 전화 걸기](tel:{phone_clean})")
    else:
        st.info(f"{sel} 상세 정보가 없어요.")


# ════════════════════════════════════════════════
# TAB 3 — 분리배출 도감  (HTML 태그 버그 수정)
# ════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-header">📖 알쏭달쏭 분리배출 도감</div>', unsafe_allow_html=True)

    search  = st.text_input("🔍 검색", placeholder="우유팩, 라면봉지, 페트병…",
                            label_visibility="collapsed")
    cat_sel = st.selectbox(
        "카테고리",
        ["전체", "♻️ 재활용", "🗑️ 일반쓰레기", "🍖 음식물", "⚠️ 특수"],
        label_visibility="collapsed",
    )
    cat_map = {
        "전체": "all", "♻️ 재활용": "recycle",
        "🗑️ 일반쓰레기": "general", "🍖 음식물": "food", "⚠️ 특수": "special",
    }
    cat_key = cat_map[cat_sel]

    filtered = [
        w for w in WASTE_DB
        if (not search.strip() or search in w["name"] or search in w["ct"])
        and (cat_key == "all" or w["cat"] == cat_key)
    ]

    if not filtered:
        st.info("검색 결과가 없어요 🔍")
    else:
        for w in filtered:
            # ★ render_waste_item() 함수로 HTML 조립 — 따옴표 충돌 완전 방지
            st.markdown(render_waste_item(w), unsafe_allow_html=True)

    # 내 동네 연동
    if DATA_OK and sel in df_sch.index:
        row_s2 = df_sch.loc[sel]
        rd = safe(row_s2["재활용품배출요일"])
        rt = safe(row_s2["재활용품배출시작시각"]) + "~" + safe(row_s2["재활용품배출종료시각"])
        fd = safe(row_s2["음식물쓰레기배출요일"])
        ft = safe(row_s2["음식물쓰레기배출시작시각"]) + "~" + safe(row_s2["음식물쓰레기배출종료시각"])
        st.markdown(
            '<div class="card" style="margin-top:10px;'
            'background:linear-gradient(135deg,#E8FFF5,#EEF9FF)">'
              f'<div style="font-weight:800;margin-bottom:6px">📍 {sel} 배출 일정 연동</div>'
              '<div style="font-size:0.82rem;line-height:1.9">'
                f'♻️ 재활용: <b>{rd}요일</b> {rt}<br>'
                f'🍖 음식물: <b>{fd}요일</b> {ft}'
              "</div>"
            "</div>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════
# TAB 4 — 에코 마일리지
# ════════════════════════════════════════════════
with tab4:
    lv      = get_lv(st.session_state.pts)
    next_lv = next((l for l in LEVEL_INFO if l["min"] > lv["min"]), None)
    pct     = int(((st.session_state.pts - lv["min"]) / (next_lv["min"] - lv["min"])) * 100) if next_lv else 100
    next_min = next_lv["min"] if next_lv else "MAX"
    remain   = (next_lv["min"] - st.session_state.pts) if next_lv else 0

    # 포인트 히어로
    st.markdown(
        '<div class="pt-hero">'
          '<div style="font-size:0.85rem;opacity:0.85">나의 에코 마일리지</div>'
          f'<div class="pt-hero-num">{st.session_state.pts}</div>'
          '<div class="pt-hero-sub">포인트 보유 중 ✨</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # 캐릭터
    lv_emoji = lv["emoji"]
    lv_name  = lv["name"]
    pts_now  = st.session_state.pts
    xp_suffix = f"다음까지 {remain}P" if next_lv else "🏆 최고 레벨!"
    st.markdown(
        '<div class="char-box">'
          f'<span style="font-size:3rem;flex-shrink:0">{lv_emoji}</span>'
          "<div style='flex:1'>"
            f'<div style="font-size:0.75rem;font-weight:700;color:#3ECF8E">{lv_name}</div>'
            '<div style="font-size:1rem;font-weight:800;margin:2px 0">나의 쓰레기 요정</div>'
            '<div class="xp-track">'
              f'<div class="xp-fill" style="width:{pct}%"></div>'
            "</div>"
            f'<div class="xp-label">{pts_now} / {next_min} P  ·  {xp_suffix}</div>'
          "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec-header">💰 포인트 적립</div>', unsafe_allow_html=True)

    with st.expander("📸 분리배출 AI 인증  +50P"):
        st.caption("올바르게 분리한 쓰레기 사진을 업로드하세요!")
        uploaded = st.file_uploader("사진", type=["jpg", "jpeg", "png"],
                                    label_visibility="collapsed")
        if uploaded:
            st.image(uploaded, width=200)
        if st.button("✅ AI 인증하기 (+50P)", use_container_width=True):
            if uploaded:
                st.session_state.pts += 50
                st.success("🎉 인증 완료! +50P 적립!")
                st.balloons()
                st.rerun()
            else:
                st.warning("사진을 먼저 올려 주세요!")

    with st.expander("❓ 오늘의 OX 퀴즈  +10P"):
        quiz = QUIZZES[st.session_state.q_idx]
        st.markdown(f'**"{quiz["q"]}"**')
        if not st.session_state.q_done:
            qa, qb = st.columns(2)
            with qa:
                if st.button("⭕ O", use_container_width=True, key="qO"):
                    st.session_state.q_done     = True
                    st.session_state.q_user_ans = True
                    st.rerun()
            with qb:
                if st.button("❌ X", use_container_width=True, key="qX"):
                    st.session_state.q_done     = True
                    st.session_state.q_user_ans = False
                    st.rerun()
        else:
            correct = st.session_state.q_user_ans == quiz["ans"]
            if correct:
                st.success(f"🎉 정답! {quiz['exp']}")
                if not st.session_state.q_pts_given:
                    st.session_state.pts       += 10
                    st.session_state.q_pts_given = True
            else:
                st.error(f"😢 오답!  {quiz['exp']}")
            if st.button("🔄 다음 퀴즈", use_container_width=True):
                st.session_state.q_idx       = random.randint(0, len(QUIZZES) - 1)
                st.session_state.q_done      = False
                st.session_state.q_user_ans  = None
                st.session_state.q_pts_given = False
                st.rerun()

    with st.expander("📱 SNS 숏폼 챌린지  +500P"):
        st.caption("분리배출 노하우 영상을 SNS에 올리고 링크를 인증하세요!")
        link = st.text_input("링크", placeholder="https://instagram.com/...",
                             label_visibility="collapsed")
        if st.button("📣 챌린지 인증 (+500P)", use_container_width=True):
            if link.strip():
                st.session_state.pts += 500
                st.success("🎬 +500P 적립!")
                st.balloons()
                st.rerun()
            else:
                st.warning("링크를 입력해 주세요!")

    with st.expander("🏘️ 우리 동네 녹색 달성  +200P"):
        if DATA_OK and sel in df_amt.index:
            g = df_amt.loc[sel, "등급"]
            if g == "green":
                st.success(f"🌿 {sel}는 녹색 달성 중이에요!")
                if st.button("🎁 보너스 받기 (+200P)", use_container_width=True):
                    st.session_state.pts += 200
                    st.success("+200P 적립!")
                    st.rerun()
            elif g == "orange":
                st.warning("🟠 조금만 더 노력해요!")
            else:
                st.error("🔴 배출량을 줄여 보아요!")

    # 포인트 사용
    st.markdown('<div class="sec-header">🛍️ 포인트 사용</div>', unsafe_allow_html=True)
    spend_list = [
        ("🛒", "종량제 봉투", 100), ("☕", "카페 쿠폰",   300),
        ("🧻", "재생 화장지", 150), ("🥛", "편의점 쿠폰", 200),
        ("🌱", "환경단체 기부", 50), ("🐾", "유기동물 기부", 50),
    ]
    sa, sb = st.columns(2)
    for i, (icon, name, cost) in enumerate(spend_list):
        tgt = sa if i % 2 == 0 else sb
        with tgt:
            st.markdown(
                f'<div style="background:white;border-radius:14px;padding:14px 10px;'
                f'text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:8px">'
                  f'<span style="font-size:1.8rem;display:block;margin-bottom:5px">{icon}</span>'
                  f'<div style="font-size:0.8rem;font-weight:700;color:#333">{name}</div>'
                  f'<div style="font-size:0.8rem;color:#FF6B6B;font-weight:800;margin-top:2px">{cost} P</div>'
                "</div>",
                unsafe_allow_html=True,
            )
            if st.button("교환", key=f"sp_{i}", use_container_width=True):
                if st.session_state.pts >= cost:
                    st.session_state.pts -= cost
                    st.success(f"✅ {name} 교환!")
                    st.rerun()
                else:
                    st.error("포인트 부족 😢")

    # 레벨 가이드
    st.markdown('<div class="sec-header">🌱 캐릭터 성장 가이드</div>', unsafe_allow_html=True)
    la, lb = st.columns(2)
    for i, li in enumerate(LEVEL_INFO):
        done  = st.session_state.pts >= li["min"]
        tgt   = la if i % 2 == 0 else lb
        li_e  = li["emoji"]
        li_n  = li["name"]
        li_m  = li["min"]
        done_badge = '<div style="color:#3ECF8E;font-size:0.72rem;font-weight:700;margin-top:3px">✅ 달성!</div>' if done else ""
        with tgt:
            st.markdown(
                f'<div class="lv-box {"done" if done else ""}">'
                  f'<span style="font-size:2rem;display:block;margin-bottom:4px">{li_e}</span>'
                  f'<div style="font-size:0.75rem;font-weight:800">{li_n}</div>'
                  f'<div style="font-size:0.7rem;color:#AAB;margin-top:2px">{li_m}P~</div>'
                  + done_badge
                + "</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
