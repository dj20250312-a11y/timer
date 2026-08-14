import time
import streamlit as st

# 1. 페이지 기본 설정 (고양이 테마)
st.set_page_config(
    page_title="🐾 야옹이 카운트다운 냥이머",
    page_icon="🐱",
    layout="centered"  # 중앙 정렬 레이아웃
)

# 2. CSS 스타일 적용 (귀여운 고양이 파스텔 톤 & 반응형 design)
# clamp()를 활용한 폰트 크기 조절 유지
st.markdown("""
<style>
    /* 메인 background 컬러 (매우 연한 파스텔 핑크) */
    .stApp {
        background-color: #FFF5F7;
    }

    /* 메인 컨테이너 카드 스타일 (둥글고 따뜻한 느낌) */
    .timer-card {
        background-color: #ffffff;
        border-radius: 30px; /* 더 둥글게 */
        padding: 40px 30px;
        box-shadow: 0 10px 30px rgba(255, 182, 193, 0.3); /* 핑크빛 그림자 */
        text-align: center;
        margin-top: 10px;
        margin-bottom: 25px;
        border: 2px solid #FFD1DC; /* 연핑크 테두리 */
    }
    
    /* 화면 크기에 맞춰 반응형으로 크기가 변하는 타이머 텍스트 (진한 초콜릿색) */
    .timer-display {
        font-size: clamp(3.8rem, 13vw, 7rem);
        font-weight: 800;
        color: #5D4037; /* 따뜻한 초콜릿 색 */
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        line-height: 1.1;
        margin: 10px 0 20px 0;
    }
    
    /* 상태 안내 텍스트 */
    .status-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #8D6E63;
        margin-bottom: 5px;
    }

    /* 입력 창 라벨 스타일 수정 */
    .stNumberInput label {
        color: #5D4037 !important;
        font-weight: bold;
    }

    /* 버튼 스타일 커스텀 (둥글고 꽉 찬 파스텔 톤) */
    .stButton > button {
        width: 100%;
        border-radius: 20px; /* 아주 둥글게 */
        font-weight: 700;
        height: 3.2em;
        border: none;
        transition: all 0.2s ease;
    }
    
    /* "빠른 설정" 버튼 스타일 (연한 브라운) */
    div[data-testid="stColumn"]:nth-of-type(1) .stButton > button,
    div[data-testid="stColumn"]:nth-of-type(2) .stButton > button,
    div[data-testid="stColumn"]:nth-of-type(3) .stButton > button,
    div[data-testid="stColumn"]:nth-of-type(4) .stButton > button {
        background-color: #D7CCC8;
        color: #5D4037;
    }
    div[data-testid="stColumn"] .stButton > button:hover {
        background-color: #BCAAA4;
    }

    /* "시작/계속" 버튼 스타일 (코랄 핑크 - Primary) */
    .stButton > button[kind="primary"] {
        background-color: #FF8A80;
        color: white;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #FF5252;
    }

    /* "일시정지/초기화" 버튼 스타일 (연한 그레이 블루) */
    .stButton > button[kind="secondary"] {
        background-color: #CFD8DC;
        color: #37474F;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #B0BEC5;
    }

    /* 프로그레스 바 색상 변경 (코랄 핑크) */
    .stProgress > div > div > div > div {
        background-color: #FF8A80;
    }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태(st.session_state) 초기화 (변동 없음)
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "finished" not in st.session_state:
    st.session_state.finished = False
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "end_time" not in st.session_state:
    st.session_state.end_time = 0.0
if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 0
if "input_minutes" not in st.session_state:
    st.session_state.input_minutes = 3     # 기본 분 설정값
if "input_seconds" not in st.session_state:
    st.session_state.input_seconds = 0     # 기본 초 설정값

# 4. 타이머 제어 함수들 (오류 문구 수정)
def start_timer():
    total = st.session_state.input_minutes * 60 + st.session_state.input_seconds
    if total <= 0:
        st.error("🐾 냥! 0분 0초로는 집사님이 기다릴 수 없다냥! 시간을 설정해달라냥!")
        return
    st.session_state.total_seconds = total
    st.session_state.remaining_seconds = total
    st.session_state.end_time = time.monotonic() + total
    st.session_state.running = True
    st.session_state.paused = False
    st.session_state.finished = False

def pause_timer():
    if st.session_state.running and not st.session_state.paused:
        st.session_state.remaining_seconds = max(0, int(st.session_state.end_time - time.monotonic()))
        st.session_state.paused = True

def resume_timer():
    if st.session_state.running and st.session_state.paused:
        st.session_state.end_time = time.monotonic() + st.session_state.remaining_seconds
        st.session_state.paused = False

def reset_timer():
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.finished = False
    st.session_state.remaining_seconds = 0

def set_quick_time(mins):
    if not st.session_state.running:
        st.session_state.input_minutes = mins
        st.session_state.input_seconds = 0

# 5. UI 구성 - 앱 제목 (고양이 테마)
st.markdown('<h1 style="text-align: center; color: #5D4037;">🐾 야옹이 카운트다운 냥이머</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #8D6E63; margin-bottom: 25px;">집사야! 공부냥? 운동냥? 요리냥? 냥이가 재줄게냥!</p>', unsafe_allow_html=True)

# 6. 빠른 시간 설정 버튼 (실행 중이 아닐 때만 작동)
st.subheader("⚡ 냥이 속성 설정")
q_col1, q_col2, q_col3, q_col4 = st.columns(4)
disabled_inputs = st.session_state.running

with q_col1:
    if st.button("1분 냥", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(1)
with q_col2:
    if st.button("3분 냥", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(3)
with q_col3:
    if st.button("5분 냥", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(5)
with q_col4:
    if st.button("10분 냥", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(10)

# 7. 분/초 직접 입력 창
col_min, col_sec = st.columns(2)
with col_min:
    st.number_input(
        "분 (Mins 🐾)", 
        min_value=0, 
        max_value=180, 
        key="input_minutes", 
        disabled=disabled_inputs
    )
with col_sec:
    st.number_input(
        "초 (Secs 🐾)", 
        min_value=0, 
        max_value=59, 
        key="input_seconds", 
        disabled=disabled_inputs
    )

# 8. 실시간 타이머 표시 영역 (st.fragment)
@st.fragment(run_every=0.5 if st.session_state.running and not st.session_state.paused else None)
def timer_display_fragment():
    # 실행 중일 때 남은 시간 계산
    if st.session_state.running and not st.session_state.paused:
        current_time = time.monotonic()
        remaining = int(st.session_state.end_time - current_time)
        
        if remaining <= 0:
            st.session_state.remaining_seconds = 0
            st.session_state.running = False
            st.session_state.finished = True
        else:
            st.session_state.remaining_seconds = remaining

    # 표시할 분과 초 계산
    rem_sec = st.session_state.remaining_seconds
    mins, secs = divmod(rem_sec, 60)
    time_format = f"{mins:02d}:{secs:02d}"

    # 고양이 테마 카드 스타일 안에 타이머 표시
    st.markdown('<div class="timer-card">', unsafe_allow_html=True)
    
    # 상태 텍스트 출력 (고양이 말투)
    if st.session_state.finished:
        st.markdown('<div class="status-text" style="color: #FF5252; font-size: 1.4rem;">🎉 냥냥!! 시간 다 됐다냥! 🎉</div>', unsafe_allow_html=True)
    elif st.session_state.paused:
        st.markdown('<div class="status-text" style="color: #FFA726;">⏸️ 잠시 멈춤냥... 집사 어디갔냥?</div>', unsafe_allow_html=True)
    elif st.session_state.running:
        st.markdown('<div class="status-text" style="color: #FF8A80;">⏳ 냥이가 집중해서 재고 있다냥...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-text">집사야, 아래 버튼을 눌러줘냥 🐾</div>', unsafe_allow_html=True)

    # MM:SS 시간 크게 출력
    st.markdown(f'<div class="timer-display">{time_format}</div>', unsafe_allow_html=True)

    # 진행률 막대(Progress Bar) - 코랄 핑크 색상
    if st.session_state.total_seconds > 0:
        progress = st.session_state.remaining_seconds / st.session_state.total_seconds
        progress = max(0.0, min(1.0, progress))
        st.progress(progress)
    else:
        st.progress(0.0)

    st.markdown('</div>', unsafe_allow_html=True)

    # 시간이 완료되면 고양이 테마에 맞춰 함박눈 효과와 성공 메시지
    if st.session_state.finished:
        st.snow()  # 풍선 대신 눈이 내리는 효과로 변경
        st.success("🔔 집사야! 설정한 시간이 끝났다냥! 고생했다냥! 🐾")

# 타이머 부분 실행
timer_display_fragment()

# 9. 타이머 제어 버튼 (시작, 일시정지, 계속, 초기화 - 고양이 테마)
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if not st.session_state.running and not st.session_state.paused:
        st.button("▶️ 시작냥", on_click=start_timer, type="primary", use_container_width=True)
    elif st.session_state.running and not st.session_state.paused:
        # Secondary 버튼 스타일로 일시정지 표시
        st.button("⏸️ 잠시 멈춤냥", on_click=pause_timer, kind="secondary", use_container_width=True)
    elif st.session_state.paused:
        st.button("▶️ 다시 시작냥", on_click=resume_timer, type="primary", use_container_width=True)

with btn_col2:
    # Secondary 버튼 스타일로 초기화 표시
    st.button("🔄 처음부터냥", on_click=reset_timer, kind="secondary", use_container_width=True)
