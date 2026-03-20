import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import os
import shutil

# ── 페이지 설정 ──
st.set_page_config(
    page_title="🧚 서울 쓰레기 요정",
    page_icon="🧚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Nanum Gothic', sans-serif; }

.main-header {
    background: linear-gradient(135deg, #e8faf8 0%, #fff9e6 100%);
    border-radius: 20px; padding: 1.8rem 2rem; text-align: center;
    margin-bottom: 1.5rem; border: 2px solid #5ECFC1;
}
.main-header h1 { font-size: 2rem; color: #5ECFC1; margin-bottom: 0.3rem; }
.main-header p  { color: #777; font-size: 0.95rem; }

.info-card {
    background: white; border-radius: 14px; padding: 1.1rem;
    box-shadow: 0 4px 18px rgba(0,0,0,0.07); margin-bottom: 0.8rem;
    border-left: 4px solid #5ECFC1;
}
.day-badge-row { display:flex; gap:5px; flex-wrap:wrap; margin:7px 0; }
.day-active   { background:#5ECFC1; color:white; padding:3px 11px;
                border-radius:20px; font-size:0.82rem; font-weight:700; display:inline-block; }
.day-inactive { background:#e9ecef; color:#aaa; padding:3px 11px;
                border-radius:20px; font-size:0.82rem; font-weight:700; display:inline-block; }

.waste-card {
    background:white; border-radius:14px; padding:1rem;
    box-shadow:0 3px 14px rgba(0,0,0,0.07); margin-bottom:0.8rem;
    border:2px solid #f0f0f0;
}
.steps-row { display:flex; gap:5px; margin:8px 0; }
.step-box  { flex:1; background:#f8f9fa; border-radius:9px; padding:7px 4px;
             text-align:center; font-size:0.75rem; position:relative; }
.step-box:not(:last-child)::after {
    content:'▶'; position:absolute; right:-6px; top:50%; transform:translateY(-50%);
    font-size:0.55rem; color:#ccc;
}
.tip-box  { background:#f0fdf4; border-left:3px solid #7ED957;
            padding:7px 11px; border-radius:0 8px 8px 0;
            font-size:0.82rem; color:#444; margin-top:7px; }
.warn-box { background:#fff9e6; border-left:3px solid #FFD93D;
            padding:7px 11px; border-radius:0 8px 8px 0;
            font-size:0.82rem; color:#444; margin-top:5px; }

.point-card {
    background: linear-gradient(135deg, #FFD93D, #FFB347);
    border-radius:16px; padding:1.4rem; color:white; text-align:center; margin-bottom:1rem;
}
.point-card h2 { font-size:2.4rem; margin:0; }

.no-collect {
    background:#fff0f0; border:1.5px solid #FF6B6B; border-radius:10px;
    padding:9px 13px; margin:5px 0; font-size:0.87rem;
}
.green-box {
    background:#f0fff4; border:1.5px solid #7ED957; border-radius:10px;
    padding:9px 13px; margin:5px 0; font-size:0.87rem;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════
# 파일 경로 자동 탐색
# ══════════════════════════════
CSV_NAME = "생활쓰레기배출정보_서울특별시.csv"
XLS_NAME = "서울시배출량.xlsx"

for fname in [CSV_NAME, XLS_NAME]:
    if not os.path.exists(fname):
        candidate = "/mnt/user-data/uploads/" + fname
        if os.path.exists(candidate):
            shutil.copy(candidate, fname)


# ══════════════════════════════
# 데이터 로딩 (캐시)
# ══════════════════════════════
@st.cache_data
def load_data():
    # ── CSV 배출정보 ──
    df_raw = pd.read_csv(CSV_NAME, encoding="cp949")

    keep = [
        "시군구명", "배출장소유형", "배출장소",
        "생활쓰레기배출방법", "음식물쓰레기배출방법", "재활용품배출방법",
        "일시적다량폐기물배출방법", "일시적다량폐기물배출장소",
        "생활쓰레기배출요일", "음식물쓰레기배출요일", "재활용품배출요일",
        "생활쓰레기배출시작시각", "생활쓰레기배출종료시각",
        "음식물쓰레기배출시작시각", "음식물쓰레기배출종료시각",
        "재활용품배출시작시각", "재활용품배출종료시각",
        "미수거일", "관리부서명", "관리부서전화번호"
    ]
    df_info = df_raw[keep].drop_duplicates(subset=["시군구명"], keep="first").set_index("시군구명")

    # ── XLSX 배출량 ──
    df_amount_raw = pd.read_excel(XLS_NAME, sheet_name="데이터", header=None)
    df_amount_raw.columns = ["구", "1인당배출량", "총배출량", "주민수"]
    df_amount = df_amount_raw.iloc[2:].copy()
    df_amount = df_amount[df_amount["구"] != "계"].copy()
    df_amount["구"] = df_amount["구"].str.strip()
    for col in ["1인당배출량", "총배출량", "주민수"]:
        df_amount[col] = pd.to_numeric(df_amount[col], errors="coerce")

    def level(val):
        if val >= 2.0: return "red"
        if val >= 1.2: return "orange"
        return "green"

    df_amount["등급"] = df_amount["1인당배출량"].apply(level)
    df_amount = df_amount.set_index("구")

    return df_info, df_amount


try:
    df_info, df_amount = load_data()
    DATA_OK = True
except Exception as e:
    DATA_OK = False
    DATA_ERR = str(e)


# ══════════════════════════════
# 상수 / 유틸
# ══════════════════════════════
COLOR_MAP = {"red": "#FF6B6B", "orange": "#FFB347", "green": "#7ED957"}
EMOJI_MAP = {"red": "😰",      "orange": "😅",       "green": "😊"}
LABEL_MAP = {"red": "🔴 경고 (많음)", "orange": "🟠 보통", "green": "🟢 우수 (적음)"}
ALL_DAYS  = ["일", "월", "화", "수", "목", "금", "토"]

def day_badges(day_str: str) -> str:
    if pd.isna(day_str) or str(day_str).strip() == "":
        return "<span style='color:#aaa'>정보 없음</span>"
    active = set(str(day_str).replace(" ", "").split("+"))
    badges = "".join(
        f'<span class="{"day-active" if d in active else "day-inactive"}">{d}</span>'
        for d in ALL_DAYS
    )
    return f'<div class="day-badge-row">{badges}</div>'

def safe(val, default="정보 없음"):
    if pd.isna(val) or str(val).strip() in ("", "nan", "NaN"):
        return default
    return str(val).strip()

LEVEL_INFO = [
    {"min": 0,    "max": 200,   "emoji": "🌱", "name": "LV.1 새싹 쓰요"},
    {"min": 200,  "max": 500,   "emoji": "🌿", "name": "LV.2 잎사귀 쓰요"},
    {"min": 500,  "max": 1000,  "emoji": "🌺", "name": "LV.3 꽃단장 쓰요"},
    {"min": 1000, "max": 99999, "emoji": "🌍", "name": "LV.4 지구 수호자 쓰요"},
]

def get_level(pts):
    for lv in LEVEL_INFO:
        if lv["min"] <= pts < lv["max"]:
            return lv
    return LEVEL_INFO[-1]

WASTE_ITEMS = [
    {"name":"우유팩","emoji":"🥛","cat":"recycle","cat_label":"♻️ 재활용 (종이팩)",
     "steps":[("💧","비우기"),("🚿","헹구기"),("✂️","펼치기"),("📦","모아두기")],
     "tip":"동주민센터에 모아 가면 화장지/봉투로 교환 가능!","warning":None,
     "detail":"우유팩은 일반 종이와 다른 재질이에요. 씻어서 펼친 후 따로 배출해 주세요!"},
    {"name":"라면봉지","emoji":"🍜","cat":"recycle","cat_label":"♻️ 재활용 (비닐류)",
     "steps":[("🔍","오염확인"),("📃","펼치기"),("🛍️","비닐봉투"),("♻️","배출")],
     "tip":"딱지로 접으면 선별 안 돼요! 꼭 펼쳐서 버려요.",
     "warning":"국물이 심하게 묻었으면 → 종량제 봉투에 넣어요",
     "detail":"깨끗한 비닐은 재활용! 씻어도 오염이 남으면 일반쓰레기로 버려 주세요."},
    {"name":"투명 페트병","emoji":"🍼","cat":"recycle","cat_label":"♻️ 재활용 (투명 페트)",
     "steps":[("💧","비우기"),("🏷️","라벨제거"),("👟","압착"),("♻️","배출")],
     "tip":"투명 페트병은 색깔 병과 따로 분리해요!","warning":None,
     "detail":"무색 투명 페트병은 고품질 재활용이 가능해요. 라벨을 반드시 제거해 주세요!"},
    {"name":"음식물쓰레기","emoji":"🍖","cat":"food","cat_label":"🍖 음식물쓰레기",
     "steps":[("💧","물기제거"),("✂️","잘게썰기"),("🛒","전용봉투"),("🗑️","배출")],
     "tip":"물기를 꼭 짜서 버려야 냄새가 안 나요!",
     "warning":"뼈·껍데기·씨앗은 일반쓰레기예요!",
     "detail":"과일 씨앗, 복숭아뼈, 조개·게껍데기는 음식물이 아니에요!"},
    {"name":"깨진 유리","emoji":"🪞","cat":"special","cat_label":"⚠️ 특수 (불연성)",
     "steps":[("📰","신문지 싸기"),("✏️","위험 표시"),("🛍️","전용마대"),("🗑️","배출")],
     "tip":"수거 분들이 다치지 않게 꼭 신문지로 싸 주세요!",
     "warning":"일반 종량제 봉투 ❌ → 불연성 전용 마대 사용!",
     "detail":"편의점·마트에서 불연성 전용 마대를 구입해 사용해 주세요."},
    {"name":"종이컵","emoji":"☕","cat":"recycle","cat_label":"♻️ 재활용 (종이팩)",
     "steps":[("💧","씻기"),("🔄","펼치기"),("📦","모으기"),("♻️","배출")],
     "tip":"종이팩처럼 씻어서 따로 모아 배출해요!","warning":None,
     "detail":"종이컵도 씻어서 따로 배출하면 화장지로 재활용 돼요."},
    {"name":"스티로폼","emoji":"📦","cat":"recycle","cat_label":"♻️ 재활용 (발포합성수지)",
     "steps":[("🧹","이물질제거"),("🏷️","테이프제거"),("✂️","부수기"),("♻️","배출")],
     "tip":"음식물이 묻었다면 깨끗이 씻어서 배출해요",
     "warning":"오염이 심하면 → 일반쓰레기",
     "detail":"테이프·라벨을 제거하고 최대한 작게 부숴 주세요."},
    {"name":"헌 옷","emoji":"👕","cat":"special","cat_label":"⚠️ 특수 (의류수거함)",
     "steps":[("🧹","세탁"),("👜","묶음포장"),("📍","수거함확인"),("🗑️","배출")],
     "tip":"의류 수거함 위치는 동주민센터 앱에서 확인!",
     "warning":"속옷·양말은 일반쓰레기로 버려요",
     "detail":"입을 수 있는 옷은 의류 수거함에! 너무 낡은 옷은 일반쓰레기로."},
    {"name":"폐건전지","emoji":"🔋","cat":"special","cat_label":"⚠️ 특수 (폐전지)",
     "steps":[("📦","따로모으기"),("🏪","마트·편의점"),("📮","전지수거함"),("✅","배출")],
     "tip":"대형마트·편의점·주민센터에 전지 수거함 있어요!",
     "warning":"절대 일반쓰레기 ❌ → 화재·환경오염 위험!",
     "detail":"건전지·충전지 모두 폐전지 수거함에 배출해야 해요."},
    {"name":"치킨뼈","emoji":"🍗","cat":"general","cat_label":"🗑️ 일반쓰레기",
     "steps":[("🍽️","음식제거"),("🛒","종량제봉투"),("🗑️","배출"),("✅","완료")],
     "tip":"뼈는 음식물이 아닌 일반쓰레기예요!",
     "warning":"음식물 수거함 ❌ → 종량제 봉투에!",
     "detail":"닭뼈·돼지뼈 등 딱딱한 뼈는 일반쓰레기로 버려요."},
    {"name":"달걀껍데기","emoji":"🥚","cat":"general","cat_label":"🗑️ 일반쓰레기",
     "steps":[("🧹","이물제거"),("🛒","종량제봉투"),("🗑️","배출"),("✅","완료")],
     "tip":"달걀껍데기는 일반쓰레기예요!","warning":"음식물 수거함 ❌",
     "detail":"달걀껍데기는 단단해 음식물 처리가 어려워 일반쓰레기로 분류해요."},
    {"name":"커피찌꺼기","emoji":"☕","cat":"food","cat_label":"🍖 음식물쓰레기",
     "steps":[("💧","물기제거"),("🛒","전용봉투"),("🗑️","배출"),("✅","완료")],
     "tip":"화분 퇴비로 활용해도 좋아요!","warning":None,
     "detail":"커피찌꺼기는 음식물쓰레기로 분류돼요."},
]

QUIZZES = [
    {"q":"라면봉지는 딱지로 접어서 버려야 재활용이 잘 된다.","ans":False,
     "exp":"딱지로 접으면 선별장에서 날아가 재활용이 안 돼요! 꼭 펼쳐서 버려요."},
    {"q":"우유팩은 일반 종이류와 함께 버려도 된다.","ans":False,
     "exp":"우유팩은 일반 종이와 다른 재질이에요. 씻어서 펼친 후 따로 배출해요."},
    {"q":"음식물이 없는 깨끗한 비닐은 재활용이 가능하다.","ans":True,
     "exp":"맞아요! 깨끗한 비닐은 재활용 가능해요. 오염됐으면 일반쓰레기로."},
    {"q":"달걀껍데기는 음식물 쓰레기로 버려야 한다.","ans":False,
     "exp":"달걀껍데기는 일반쓰레기예요! 음식물 수거함에 넣으면 안 돼요."},
    {"q":"투명 페트병은 라벨을 제거하고 배출해야 한다.","ans":True,
     "exp":"정확해요! 라벨 제거 후 압착해서 투명 페트 전용으로 배출해요."},
    {"q":"치킨뼈는 음식물 쓰레기로 버려야 한다.","ans":False,
     "exp":"딱딱한 뼈는 일반쓰레기예요! 종량제 봉투에 넣어 주세요."},
    {"q":"폐건전지는 일반쓰레기로 버려도 된다.","ans":False,
     "exp":"폐건전지는 절대 일반쓰레기 금지! 전지 수거함에 별도 배출해요."},
]


# ══════════════════════════════
# 세션 초기화
# ══════════════════════════════
if "points"        not in st.session_state: st.session_state.points = 0
if "quiz_answered" not in st.session_state: st.session_state.quiz_answered = False
if "quiz_idx"      not in st.session_state: st.session_state.quiz_idx = 0
if "selected_gu"   not in st.session_state: st.session_state.selected_gu = "마포구"


# ══════════════════════════════
# 사이드바
# ══════════════════════════════
with st.sidebar:
    st.markdown("## 🧚 서울 쓰레기 요정")
    st.markdown("---")
    page = st.radio(
        "메뉴",
        ["🗺️ 배출량 지도", "📖 분리배출 도감", "⭐ 에코 마일리지"],
        label_visibility="collapsed"
    )
    st.markdown("---")

    lv = get_level(st.session_state.points)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#FFD93D,#FFB347);border-radius:12px;
                padding:11px;text-align:center;color:white;margin-bottom:1rem">
        <div style="font-size:1.7rem">{lv['emoji']}</div>
        <div style="font-weight:800;font-size:0.88rem">{lv['name']}</div>
        <div style="font-size:1.4rem;font-weight:800;margin-top:3px">{st.session_state.points} P</div>
    </div>
    """, unsafe_allow_html=True)

    if DATA_OK:
        gu_list = sorted(df_amount.index.tolist())
        st.markdown("#### 🏘️ 내 동네 선택")
        sel = st.selectbox(
            "구",
            gu_list,
            index=gu_list.index(st.session_state.selected_gu)
                  if st.session_state.selected_gu in gu_list else 0,
            label_visibility="collapsed"
        )
        st.session_state.selected_gu = sel
        row_a = df_amount.loc[sel]
        lv_c  = row_a["등급"]
        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:10px;
                    border-left:4px solid {COLOR_MAP[lv_c]};font-size:0.84rem">
            <b>{sel}</b><br>
            1인당 {row_a['1인당배출량']} kg/일<br>
            {LABEL_MAP[lv_c]}
        </div>
        """, unsafe_allow_html=True)


# 데이터 오류 처리
if not DATA_OK:
    st.error(f"⚠️ 데이터 파일 로딩 오류\n\n{DATA_ERR}\n\n`app.py`와 같은 폴더에 CSV, XLSX 파일을 넣어 주세요.")
    st.stop()

sel = st.session_state.selected_gu


# ══════════════════════════════════════════════
# PAGE 1 : 배출량 지도
# ══════════════════════════════════════════════
if page == "🗺️ 배출량 지도":

    st.markdown("""
    <div class="main-header">
        <h1>🗺️ 서울시 쓰레기 배출량 현황</h1>
        <p>2024년 실제 데이터 기반 · 구별 배출 요일 · 시간 · 방법을 한눈에 ✨</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 가로 바 차트 ──
    df_chart = df_amount.reset_index().sort_values("1인당배출량", ascending=True)
    df_chart["색상"]  = df_chart["등급"].map(COLOR_MAP)
    df_chart["이모지"] = df_chart["등급"].map(EMOJI_MAP)
    df_chart["라벨"]  = df_chart["등급"].map(LABEL_MAP)

    fig = go.Figure()
    for _, row in df_chart.iterrows():
        fig.add_trace(go.Bar(
            x=[row["1인당배출량"]],
            y=[row["구"]],
            orientation="h",
            marker_color=row["색상"],
            text=f"  {row['1인당배출량']} kg",
            textposition="outside",
            showlegend=False,
            hovertemplate=(
                f"<b>{row['이모지']} {row['구']}</b><br>"
                f"1인당 배출량: <b>{row['1인당배출량']} kg/일</b><br>"
                f"총 배출량: {row['총배출량']} 톤/일<br>"
                f"주민수: {int(row['주민수']):,} 명<br>"
                f"등급: {row['라벨']}<extra></extra>"
            ),
        ))

    fig.update_layout(
        height=660, margin=dict(l=10, r=70, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="1인당 생활폐기물 배출량 (kg/일)",
                   gridcolor="#f0f0f0", range=[0, 3.4]),
        yaxis=dict(gridcolor="#f0f0f0"),
        font=dict(family="Nanum Gothic"),
        bargap=0.22,
        title=dict(text="서울시 25개구 1인당 생활폐기물 배출량 (2024)", x=0.5,
                   font=dict(size=14))
    )
    fig.add_vline(x=1.2, line_dash="dash", line_color="#7ED957",
                  annotation_text="우수 기준 1.2kg", annotation_position="top right",
                  annotation_font_color="#7ED957")
    fig.add_vline(x=2.0, line_dash="dash", line_color="#FF6B6B",
                  annotation_text="경고 기준 2.0kg", annotation_position="top right",
                  annotation_font_color="#FF6B6B")

    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="green-box">🟢 <b>우수</b> — 1.2 kg 미만</div>', unsafe_allow_html=True)
    c2.markdown('<div style="background:#fff8ee;border:1.5px solid #FFB347;border-radius:10px;padding:9px 13px;margin:5px 0;font-size:0.87rem">🟠 <b>보통</b> — 1.2 ~ 2.0 kg</div>', unsafe_allow_html=True)
    c3.markdown('<div class="no-collect">🔴 <b>경고</b> — 2.0 kg 이상</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── 선택 구 상세 스케줄 ──
    st.markdown(f"### 📍 {sel} 배출 스케줄")

    row_a = df_amount.loc[sel]
    lv_c  = row_a["등급"]

    m1, m2, m3 = st.columns(3)
    m1.metric("1인당 배출량", f"{row_a['1인당배출량']} kg/일",
              delta="⚠️ 경고" if lv_c == "red" else ("✅ 우수" if lv_c == "green" else "🔶 보통"))
    m2.metric("총 배출량",    f"{row_a['총배출량']} 톤/일")
    m3.metric("주민수",        f"{int(row_a['주민수']):,} 명")

    if sel in df_info.index:
        row_i = df_info.loc[sel]

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="info-card">
                <b>🗑️ 일반 생활쓰레기</b>
                {day_badges(row_i['생활쓰레기배출요일'])}
                <div style="color:#FF6B6B;font-size:0.85rem;font-weight:700;margin-top:4px">
                    ⏰ {safe(row_i['생활쓰레기배출시작시각'])} ~ {safe(row_i['생활쓰레기배출종료시각'])}
                </div>
                <div style="font-size:0.79rem;color:#666;margin-top:5px">
                    📌 {safe(row_i['생활쓰레기배출방법'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="info-card" style="border-left-color:#7ED957">
                <b>♻️ 재활용품</b>
                {day_badges(row_i['재활용품배출요일'])}
                <div style="color:#FF6B6B;font-size:0.85rem;font-weight:700;margin-top:4px">
                    ⏰ {safe(row_i['재활용품배출시작시각'])} ~ {safe(row_i['재활용품배출종료시각'])}
                </div>
                <div style="font-size:0.79rem;color:#666;margin-top:5px">
                    📌 {safe(row_i['재활용품배출방법'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="info-card" style="border-left-color:#FFB347">
                <b>🍖 음식물쓰레기</b>
                {day_badges(row_i['음식물쓰레기배출요일'])}
                <div style="color:#FF6B6B;font-size:0.85rem;font-weight:700;margin-top:4px">
                    ⏰ {safe(row_i['음식물쓰레기배출시작시각'])} ~ {safe(row_i['음식물쓰레기배출종료시각'])}
                </div>
                <div style="font-size:0.79rem;color:#666;margin-top:5px">
                    📌 {safe(row_i['음식물쓰레기배출방법'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            noncol = safe(row_i["미수거일"])
            if noncol != "정보 없음":
                st.markdown(f'<div class="no-collect">🚫 <b>미수거일</b>: {noncol}</div>', unsafe_allow_html=True)
            bulky = safe(row_i["일시적다량폐기물배출방법"])
            bulky_place = safe(row_i["일시적다량폐기물배출장소"])
            if bulky not in ("미운영", "정보 없음"):
                st.markdown(f"""
                <div class="info-card" style="border-left-color:#74C0FC;margin-top:8px">
                    🛻 <b>대형폐기물</b><br>
                    <span style="font-size:0.8rem;color:#555">{bulky}</span><br>
                    <span style="font-size:0.77rem;color:#aaa">배출장소: {bulky_place}</span>
                </div>
                """, unsafe_allow_html=True)
        with cb:
            phone = safe(row_i["관리부서전화번호"])
            dept  = safe(row_i["관리부서명"])
            place_type = safe(row_i["배출장소유형"])
            place      = safe(row_i["배출장소"])
            st.markdown(f"""
            <div class="info-card" style="border-left-color:#74C0FC">
                📞 <b>{dept}</b><br>
                <span style="font-size:1.15rem;font-weight:800;color:#74C0FC">{phone}</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"📲 [전화 걸기](tel:{phone.replace('-','')})")
            if place_type == "문전수거":
                st.markdown(f'<div class="green-box">🏠 <b>문전수거</b> — {place}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="info-card" style="border-left-color:#FFB347">🗂️ <b>거점수거</b> — {place}</div>', unsafe_allow_html=True)

    if lv_c == "red":
        st.error(f"🚨 {sel}은 서울 평균보다 배출량이 많아요! 올바른 분리배출로 우리 동네를 녹색으로 만들어요 💚")
    elif lv_c == "green":
        st.success(f"🌿 {sel}은 배출량 우수 지역이에요! 앞으로도 올바른 분리배출로 유지해 주세요 👍")
    else:
        st.warning(f"🟠 {sel}은 보통 수준이에요. 조금만 더 노력하면 녹색이 될 수 있어요!")

    # 순위표
    st.markdown("---")
    st.markdown("### 🏆 구별 배출량 순위 (2024)")
    df_rank = df_amount.reset_index().sort_values("1인당배출량")
    rb, rw = st.columns(2)
    with rb:
        st.markdown("#### 🌿 배출량 상위 5 (적은 순)")
        for _, r in df_rank.head(5).iterrows():
            mark = " ⬅ 내 동네!" if r["구"] == sel else ""
            st.markdown(f"""
            <div style="background:white;border-radius:9px;padding:7px 13px;margin:3px 0;
                        box-shadow:0 2px 7px rgba(0,0,0,0.05);
                        border-left:4px solid {COLOR_MAP[r['등급']]}">
                {EMOJI_MAP[r['등급']]} <b>{r['구']}</b>
                <span style="float:right;color:#555">{r['1인당배출량']} kg/일</span>
                <span style="color:#5ECFC1;font-size:0.77rem">{mark}</span>
            </div>
            """, unsafe_allow_html=True)
    with rw:
        st.markdown("#### 🔴 배출량 하위 5 (많은 순)")
        for _, r in df_rank.tail(5).iloc[::-1].iterrows():
            mark = " ⬅ 내 동네!" if r["구"] == sel else ""
            st.markdown(f"""
            <div style="background:white;border-radius:9px;padding:7px 13px;margin:3px 0;
                        box-shadow:0 2px 7px rgba(0,0,0,0.05);
                        border-left:4px solid {COLOR_MAP[r['등급']]}">
                {EMOJI_MAP[r['등급']]} <b>{r['구']}</b>
                <span style="float:right;color:#555">{r['1인당배출량']} kg/일</span>
                <span style="color:#5ECFC1;font-size:0.77rem">{mark}</span>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE 2 : 분리배출 도감
# ══════════════════════════════════════════════
elif page == "📖 분리배출 도감":

    st.markdown("""
    <div class="main-header">
        <h1>📖 알쏭달쏭 분리배출 도감</h1>
        <p>헷갈리는 쓰레기, 어떻게 버려야 할지 바로 찾아보세요! 🔍</p>
    </div>
    """, unsafe_allow_html=True)

    cs, cf = st.columns([3, 1])
    with cs:
        search = st.text_input("🔍 품목 검색", placeholder="우유팩, 라면봉지, 페트병...", label_visibility="collapsed")
    with cf:
        cat_sel = st.selectbox("카테고리",
            ["전체","♻️ 재활용","🗑️ 일반쓰레기","🍖 음식물","⚠️ 특수"],
            label_visibility="collapsed")

    cat_map = {"전체":"all","♻️ 재활용":"recycle","🗑️ 일반쓰레기":"general","🍖 음식물":"food","⚠️ 특수":"special"}
    cat_key = cat_map[cat_sel]

    filtered = [
        w for w in WASTE_ITEMS
        if (not search.strip() or search in w["name"] or search in w["cat_label"])
        and (cat_key == "all" or w["cat"] == cat_key)
    ]

    cat_colors = {
        "recycle": ("#e8f5e9","#2e7d32"),
        "general": ("#fce4ec","#c62828"),
        "food":    ("#fff8e1","#f57f17"),
        "special": ("#e8eaf6","#283593"),
    }

    if not filtered:
        st.info("검색 결과가 없어요. 다른 키워드로 찾아보세요! 🔍")
    else:
        cols = st.columns(3)
        for i, w in enumerate(filtered):
            bg, fg = cat_colors.get(w["cat"], ("#f5f5f5","#333"))
            steps_html = "".join(
                f'<div class="step-box"><span style="font-size:1.1rem">{ic}</span><br>{lb}</div>'
                for ic, lb in w["steps"]
            )
            tip_html  = f'<div class="tip-box">💡 {w["tip"]}</div>'       if w["tip"]     else ""
            warn_html = f'<div class="warn-box">⚠️ {w["warning"]}</div>'  if w["warning"] else ""
            with cols[i % 3]:
                st.markdown(f"""
                <div class="waste-card">
                    <div style="display:flex;align-items:center;gap:9px;margin-bottom:7px">
                        <span style="font-size:1.9rem">{w['emoji']}</span>
                        <div>
                            <b style="font-size:0.97rem">{w['name']}</b><br>
                            <span style="background:{bg};color:{fg};padding:2px 7px;
                                         border-radius:7px;font-size:0.73rem;font-weight:700">
                                {w['cat_label']}
                            </span>
                        </div>
                    </div>
                    <p style="font-size:0.8rem;color:#666;margin-bottom:5px">{w['detail']}</p>
                    <div class="steps-row">{steps_html}</div>
                    {tip_html}{warn_html}
                </div>
                """, unsafe_allow_html=True)

    # 내 동네 연동
    st.markdown("---")
    if sel in df_info.index:
        row_i = df_info.loc[sel]
        rec_days = safe(row_i["재활용품배출요일"])
        rec_time = f"{safe(row_i['재활용품배출시작시각'])} ~ {safe(row_i['재활용품배출종료시각'])}"
        food_days = safe(row_i["음식물쓰레기배출요일"])
        food_time = f"{safe(row_i['음식물쓰레기배출시작시각'])} ~ {safe(row_i['음식물쓰레기배출종료시각'])}"
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#e8faf8,#fff9e6);border-radius:14px;
                    padding:1.1rem 1.3rem;border:2px solid #5ECFC1">
            <b>📍 {sel} 주민이시군요!</b><br>
            ♻️ 재활용품: <b>{rec_days}요일</b> · {rec_time}<br>
            🍖 음식물쓰레기: <b>{food_days}요일</b> · {food_time}
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE 3 : 에코 마일리지
# ══════════════════════════════════════════════
elif page == "⭐ 에코 마일리지":

    st.markdown("""
    <div class="main-header">
        <h1>⭐ 쓰요 에코 마일리지</h1>
        <p>올바른 분리배출로 포인트를 모아 캐릭터를 키워요! 🌱</p>
    </div>
    """, unsafe_allow_html=True)

    lv = get_level(st.session_state.points)
    next_lv = next((l for l in LEVEL_INFO if l["min"] > lv["min"]), None)
    pct = int(((st.session_state.points - lv["min"]) / (next_lv["min"] - lv["min"])) * 100) if next_lv else 100

    cp, cc = st.columns([1, 2])
    with cp:
        st.markdown(f"""
        <div class="point-card">
            <div style="font-size:0.88rem;opacity:0.9">보유 포인트</div>
            <h2>{st.session_state.points}</h2>
            <div style="font-size:0.82rem;opacity:0.85">P</div>
        </div>
        """, unsafe_allow_html=True)
    with cc:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:1.1rem;
                    box-shadow:0 4px 18px rgba(0,0,0,0.07);display:flex;
                    align-items:center;gap:1rem">
            <span style="font-size:3.2rem">{lv['emoji']}</span>
            <div style="flex:1">
                <div style="color:#5ECFC1;font-weight:800;font-size:0.9rem">{lv['name']}</div>
                <div style="font-size:1rem;font-weight:800;margin:3px 0">나의 쓰레기 요정</div>
                <div style="background:#e9ecef;height:9px;border-radius:5px;overflow:hidden;margin-top:5px">
                    <div style="width:{pct}%;height:100%;
                                background:linear-gradient(90deg,#5ECFC1,#7ED957);border-radius:5px"></div>
                </div>
                <div style="font-size:0.77rem;color:#888;margin-top:3px">
                    {st.session_state.points} / {next_lv['min'] if next_lv else 'MAX'} P
                    {'· 다음 레벨까지 ' + str(next_lv['min'] - st.session_state.points) + 'P' if next_lv else '· 🏆 최고 레벨!'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💰 포인트 적립")

    ea1, ea2 = st.columns(2)
    with ea1:
        with st.container(border=True):
            st.markdown("#### 📸 분리배출 AI 인증 (+50P)")
            st.caption("올바르게 분리한 쓰레기 사진을 업로드하세요!")
            uploaded = st.file_uploader("사진 업로드", type=["jpg","jpeg","png"], label_visibility="collapsed")
            if uploaded:
                st.image(uploaded, width=180)
            if st.button("✅ AI 인증하기", use_container_width=True, key="ai_btn"):
                if uploaded:
                    st.session_state.points += 50
                    st.success("🎉 올바른 배출로 인증! +50P 적립!")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("사진을 먼저 업로드해 주세요!")

    with ea2:
        with st.container(border=True):
            st.markdown("#### ❓ 오늘의 OX 퀴즈 (+10P)")
            quiz = QUIZZES[st.session_state.quiz_idx]
            st.markdown(f'**"{quiz["q"]}"**')
            if not st.session_state.quiz_answered:
                q1, q2 = st.columns(2)
                with q1:
                    if st.button("⭕ O", use_container_width=True, key="qo"):
                        st.session_state.quiz_answered = True
                        st.session_state.quiz_user_ans = True
                        st.rerun()
                with q2:
                    if st.button("❌ X", use_container_width=True, key="qx"):
                        st.session_state.quiz_answered = True
                        st.session_state.quiz_user_ans = False
                        st.rerun()
            else:
                correct = st.session_state.quiz_user_ans == quiz["ans"]
                if correct:
                    st.success(f"🎉 정답! +10P\n\n{quiz['exp']}")
                    if "quiz_pts_given" not in st.session_state:
                        st.session_state.points += 10
                        st.session_state.quiz_pts_given = True
                else:
                    st.error(f"😢 오답!\n\n{quiz['exp']}")
                if st.button("🔄 다음 퀴즈", use_container_width=True):
                    st.session_state.quiz_idx = random.randint(0, len(QUIZZES)-1)
                    st.session_state.quiz_answered = False
                    st.session_state.pop("quiz_pts_given", None)
                    st.rerun()

    ea3, ea4 = st.columns(2)
    with ea3:
        with st.container(border=True):
            st.markdown("#### 📱 SNS 숏폼 챌린지 (+500P)")
            st.caption("분리배출 노하우 영상을 올리고 링크를 인증하세요!")
            link = st.text_input("SNS 링크", placeholder="https://instagram.com/...", label_visibility="collapsed")
            if st.button("📣 챌린지 인증", use_container_width=True):
                if link.strip():
                    st.session_state.points += 500
                    st.success("🎬 챌린지 인증 완료! +500P!")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("링크를 입력해 주세요!")

    with ea4:
        with st.container(border=True):
            st.markdown("#### 🏘️ 우리 동네 녹색 달성 (+200P)")
            if sel in df_amount.index:
                lv_c = df_amount.loc[sel, "등급"]
                if lv_c == "green":
                    st.success(f"🌿 {sel}는 녹색 달성 중이에요!")
                    if st.button("🎁 보너스 받기", use_container_width=True):
                        st.session_state.points += 200
                        st.success("+200P 적립!")
                        st.rerun()
                elif lv_c == "orange":
                    st.warning(f"🟠 {sel}는 아직 보통이에요. 조금만 더!")
                else:
                    st.error(f"🔴 {sel}는 배출량이 많아요. 함께 줄여요!")

    st.markdown("---")
    st.markdown("### 🛍️ 포인트 사용")

    spend_items = [
        ("🛒","종량제 봉투",100), ("☕","카페 쿠폰",300),
        ("🧻","재생 화장지",150), ("🥛","편의점 쿠폰",200),
        ("🌱","환경단체 기부",50), ("🐾","유기동물 기부",50),
    ]
    sc = st.columns(3)
    for i, (icon, name, pts) in enumerate(spend_items):
        with sc[i % 3]:
            with st.container(border=True):
                st.markdown(f"""
                <div style="text-align:center;padding:6px 0">
                    <div style="font-size:1.9rem">{icon}</div>
                    <div style="font-weight:700;margin:3px 0;font-size:0.9rem">{name}</div>
                    <div style="color:#FF6B6B;font-weight:800;font-size:0.85rem">{pts} P</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("교환하기", key=f"spend_{i}", use_container_width=True):
                    if st.session_state.points >= pts:
                        st.session_state.points -= pts
                        st.success(f"✅ {name} 교환 완료!")
                        st.rerun()
                    else:
                        st.error("포인트가 부족해요 😢")

    st.markdown("---")
    st.markdown("### 🌱 캐릭터 성장 가이드")
    lv_cols = st.columns(4)
    for i, lv_info in enumerate(LEVEL_INFO):
        achieved = st.session_state.points >= lv_info["min"]
        border = "#5ECFC1" if achieved else "#e9ecef"
        bg     = "#e8faf8" if achieved else "white"
        with lv_cols[i]:
            st.markdown(f"""
            <div style="background:{bg};border:2px solid {border};border-radius:11px;
                        padding:0.9rem;text-align:center">
                <div style="font-size:1.9rem">{lv_info['emoji']}</div>
                <div style="font-weight:800;font-size:0.85rem;margin:3px 0">{lv_info['name']}</div>
                <div style="font-size:0.75rem;color:#888">{lv_info['min']}P~</div>
                {'<div style="color:#5ECFC1;font-size:0.78rem;font-weight:700">✅ 달성!</div>' if achieved else ''}
            </div>
            """, unsafe_allow_html=True)
