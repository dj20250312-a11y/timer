import time
import streamlit as st

# 1. 페이지 기본 설정 (반응형 레이아웃 및 타이틀)
st.set_page_config(
    page_title="⏱️ 나만의 반응형 타이머",
    page_icon="⏱️",
    layout="centered"  # 중앙 정렬 레이아웃
)

# 2. CSS 스타일 적용 (반응형 카드 design, clamp()를 활용한 폰트 크기 조절)
st.markdown("""
<style>
    /* 메인 컨테이너 카드 스타일 */
    .timer-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin-top: 10px;
        margin-bottom: 25px;
    }
    
    /* 화면 크기에 맞춰 반응형으로 크기가 변하는 타이머 텍스트 */
    .timer-display {
        font-size: clamp(3.5rem, 12vw, 6.5rem);
        font-weight: 800;
        color: #2E3A59;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        line-height: 1.1;
        margin: 15px 0;
    }
    
    /* 상태 안내 텍스트 */
    .status-text {
        font-size: 1.1rem;
        font-weight: 600;
        color: #5C6A79;
        margin-bottom: 10px;
    }

    /* 버튼 모바일 최적화 및 스타일 개선 */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태(st.session_state) 초기화 (변수가 없으면 새로 생성)
if "running" not in st.session_state:
    st.session_state.running = False      # 타이머 실행 여부
if "paused" not in st.session_state:
    st.session_state.paused = False        # 일시정지 여부
if "finished" not in st.session_state:
    st.session_state.finished = False      # 완료 여부
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0     # 총 설정 시간 (초)
if "end_time" not in st.session_state:
    st.session_state.end_time = 0.0        # 목표 종료 시각 (monotonic 타임)
if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 0 # 남은 시간 (초)
if "input_minutes" not in st.session_state:
    st.session_state.input_minutes = 3     # 기본 분 설정값
if "input_seconds" not in st.session_state:
    st.session_state.input_seconds = 0     # 기본 초 설정값

# 4. 타이머 제어 함수들 (버튼 클릭 시 실행)
def start_timer():
    """타이머 시작"""
    total = st.session_state.input_minutes * 60 + st.session_state.input_seconds
    if total <= 0:
        st.error("0분 0초 이상으로 시간을 설정해 주세요!")
        return
    st.session_state.total_seconds = total
    st.session_state.remaining_seconds = total
    # 정확한 시간 계산을 위해 현재 고정밀 시각에 설정 시간을 더함
    st.session_state.end_time = time.monotonic() + total
    st.session_state.running = True
    st.session_state.paused = False
    st.session_state.finished = False

def pause_timer():
    """타이머 일시정지"""
    if st.session_state.running and not st.session_state.paused:
        # 일시정지 시점의 남은 시간을 정확히 계산하여 저장
        st.session_state.remaining_seconds = max(0, int(st.session_state.end_time - time.monotonic()))
        st.session_state.paused = True

def resume_timer():
    """타이머 계속 실행"""
    if st.session_state.running and st.session_state.paused:
        # 남은 시간을 기준으로 새 목표 종료 시각 재설정
        st.session_state.end_time = time.monotonic() + st.session_state.remaining_seconds
        st.session_state.paused = False

def reset_timer():
    """타이머 초기화"""
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.finished = False
    st.session_state.remaining_seconds = 0

def set_quick_time(mins):
    """빠른 설정 버튼용 함수"""
    if not st.session_state.running:
        st.session_state.input_minutes = mins
        st.session_state.input_seconds = 0

# 5. UI 구성 - 앱 제목
st.title("⏱️ 나만의 반응형 타이머")
st.write("공부, 운동, 요리에 활용할 수 있는 정확한 타이머입니다.")

# 6. 빠른 시간 설정 버튼 (1분, 3분, 5분, 10분, 1시간 버튼 구성)
st.subheader("⚡ 빠른 시간 설정")
q_col1, q_col2, q_col3, q_col4, q_col5 = st.columns(5)
disabled_inputs = st.session_state.running

with q_col1:
    if st.button("1분", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(1)
with q_col2:
    if st.button("3분", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(3)
with q_col3:
    if st.button("5분", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(5)
with q_col4:
    if st.button("10분", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(10)
with q_col5:
    if st.button("1시간", disabled=disabled_inputs, use_container_width=True):
        set_quick_time(60)

# 7. 분/초 직접 입력 창
col_min, col_sec = st.columns(2)
with col_min:
    st.number_input(
        "분 (Minutes)", 
        min_value=0, 
        max_value=180, 
        key="input_minutes", 
        disabled=disabled_inputs
    )
with col_sec:
    st.number_input(
        "초 (Seconds)", 
        min_value=0, 
        max_value=59, 
        key="input_seconds", 
        disabled=disabled_inputs
    )

# 8. 실시간 타이머 표시 영역 (st.fragment로 0.5초마다 부분 새로고침)
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

    # 카드 스타일 안에 타이머 표시
    st.markdown('<div class="timer-card">', unsafe_allow_html=True)
    
    # 상태 텍스트 출력
    if st.session_state.finished:
        st.markdown('<div class="status-text" style="color: #4CAF50;">🎉 시간이 완료되었습니다!</div>', unsafe_allow_html=True)
    elif st.session_state.paused:
        st.markdown('<div class="status-text" style="color: #FF9800;">⏸️ 일시 정지됨</div>', unsafe_allow_html=True)
    elif st.session_state.running:
        st.markdown('<div class="status-text" style="color: #2196F3;">⏳ 타이머 작동 중...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-text">시작 버튼을 눌러주세요</div>', unsafe_allow_html=True)

    # MM:SS 시간 크게 출력
    st.markdown(f'<div class="timer-display">{time_format}</div>', unsafe_allow_html=True)

    # 진행률 막대(Progress Bar) 계산 및 표시
    if st.session_state.total_seconds > 0:
        progress = st.session_state.remaining_seconds / st.session_state.total_seconds
        # progress가 0~1 사이를 벗어나지 않도록 방어 코드
        progress = max(0.0, min(1.0, progress))
        st.progress(progress)
    else:
        st.progress(0.0)

    st.markdown('</div>', unsafe_allow_html=True)

    # 시간이 완료되면 풍선 효과 및 성공 메시지 출력
    if st.session_state.finished:
        st.balloons()
        st.success("🔔 설정한 시간이 종료되었습니다! 수고하셨습니다.")

# 타이머 부분 실행
timer_display_fragment()

# 9. 타이머 제어 버튼 (시작, 일시정지, 계속, 초기화)
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if not st.session_state.running and not st.session_state.paused:
        st.button("▶️ 시작", on_click=start_timer, type="primary", use_container_width=True)
    elif st.session_state.running and not st.session_state.paused:
        st.button("⏸️ 일시정지", on_click=pause_timer, use_container_width=True)
    elif st.session_state.paused:
        st.button("▶️ 계속", on_click=resume_timer, type="primary", use_container_width=True)

with btn_col2:
    st.button("🔄 초기화", on_click=reset_timer, use_container_width=True)
