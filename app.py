import random
import streamlit as st

# 1. 페이지 기본 설정 (반응형 레이아웃 및 타이틀)
st.set_page_config(
    page_title="🎵 나만의 멜론 차트 노래 추천기",
    page_icon="🎵",
    layout="centered"  # 중앙 정렬 레이아웃
)

# 2. CSS 스타일 적용 (반응형 카드 디자인, clamp()를 활용한 폰트 크기 조절)
st.markdown("""
<style>
    /* 메인 음악 카드 스타일 */
    .song-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin-top: 15px;
        margin-bottom: 25px;
        border: 1px solid #e0e0e0;
    }
    
    /* 화면 크기에 맞춰 반응형으로 크기가 변하는 노래 제목 텍스트 */
    .song-title-display {
        font-size: clamp(1.8rem, 6vw, 3.2rem);
        font-weight: 800;
        color: #00cd3c; /* 멜론 대표 초록색 */
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        line-height: 1.2;
        margin: 15px 0 5px 0;
        word-break: keep-all;
    }

    /* 가수명 텍스트 */
    .artist-display {
        font-size: clamp(1.1rem, 3.5vw, 1.8rem);
        font-weight: 600;
        color: #2E3A59;
        margin-bottom: 15px;
    }
    
    /* 카테고리 뱃지 */
    .chart-badge {
        display: inline-block;
        background-color: #e6f9ed;
        color: #00cd3c;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
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

# 3. 데이터베이스 샘플 (외부 API 대신 내장 모의 멜론 차트 데이터 사용)
MELON_DATABASE = {
    "🔥 멜론 TOP100": [
        {"title": "Accendio", "artist": "IVE (아이브)", "genre": "댄스", "album": "IVE SWITCH", "year": 2024},
        {"title": "Supernova", "artist": "aespa", "genre": "댄스", "album": "Armageddon", "year": 2024},
        {"title": "How Sweet", "artist": "NewJeans", "genre": "댄스", "album": "How Sweet", "year": 2024},
        {"title": "Spot! (feat. JENNIE)", "artist": "지코 (ZICO)", "genre": "랩/힙합", "album": "SPOT!", "year": 2024},
        {"title": "주저하는 연인들을 위해", "artist": "잔나비", "genre": "인디/록", "album": "전설", "year": 2019},
    ],
    "☀️ 일간 핫트렌드": [
        {"title": "Small girl (feat. 도경수)", "artist": "이영지", "genre": "랩/힙합", "album": "16 FANTASY", "year": 2024},
        {"title": "Magnetic", "artist": "ILLIT (아일릿)", "genre": "댄스", "album": "SUPER REAL ME", "year": 2024},
        {"title": "첫 만남은 계획대로 되지 않아", "artist": "TWS (투어스)", "genre": "댄스", "album": "Sparkling Blue", "year": 2024},
        {"title": "Bam Yang Gang (밤양갱)", "artist": "비비 (BIBI)", "genre": "R&B/Soul", "album": "밤양갱", "year": 2024},
    ],
    "🎸 장르별 랭킹": [
        {"title": " 사건의 지평선", "artist": "윤하 (YOUNHA)", "genre": "록/메탈", "album": "END THEORY", "year": 2022},
        {"title": "Love wins all", "artist": "아이유 (IU)", "genre": "발라드", "album": "The Winning", "year": 2024},
        {"title": "에피소드", "artist": "이무진", "genre": "발라드", "album": "에피소드", "year": 2023},
        {"title": "To. X", "artist": "태연 (TAEYEON)", "genre": "R&B/Soul", "album": "To. X", "year": 2023},
    ],
    "📼 추억의 차트": [
        {"title": "Dynamite", "artist": "방탄소년단", "genre": "댄스", "album": "Dynamite", "year": 2020},
        {"title": "Rollin' (롤린)", "artist": "브레이브걸스", "genre": "댄스", "album": "Rollin'", "year": 2017},
        {"title": "아모르 파티", "artist": "김연자", "genre": "트롯", "album": "아모르 파티", "year": 2013},
        {"title": "시든 꽃에 물을 주듯", "artist": "HYNN (박혜원)", "genre": "발라드", "album": "LET ME OUT", "year": 2019},
    ]
}

# 4. 세션 상태(st.session_state) 초기화 (변수가 없으면 새로 생성)
if "selected_chart" not in st.session_state:
    st.session_state.selected_chart = "🔥 멜론 TOP100"   # 기본 เลือก 차트
if "current_song" not in st.session_state:
    st.session_state.current_song = None                # 현재 추천된 노래
if "favorites" not in st.session_state:
    st.session_state.favorites = []                     # 즐겨찾기 리스트
if "recommend_count" not in st.session_state:
    st.session_state.recommend_count = 0                # 추천 횟수 카운터

# 5. 제어 함수들 (버튼 클릭 시 실행)
def recommend_song():
    """선택한 차트 카테고리에서 무작위 노래 추천"""
    chart_list = MELON_DATABASE.get(st.session_state.selected_chart, [])
    if chart_list:
        st.session_state.current_song = random.choice(chart_list)
        st.session_state.recommend_count += 1

def add_to_favorites():
    """현재 추천된 노래를 즐겨찾기에 추가"""
    if st.session_state.current_song:
        song = st.session_state.current_song
        # 중복 저장 방지
        if song not in st.session_state.favorites:
            st.session_state.favorites.append(song)
            st.toast(f"❤️ [{song['title']}] 곡이 보관함에 담겼습니다!", icon="🎵")
        else:
            st.warning("이미 즐겨찾기에 추가된 노래입니다!")

def clear_favorites():
    """즐겨찾기 보관함 초기화"""
    st.session_state.favorites = []

# 6. UI 구성 - 앱 제목
st.title("🎵 나만의 멜론 차트 노래 추천기")
st.write("지금 당신의 기분에 딱 맞는 노래를 멜론 차트별로 추천해 드립니다!")

# 7. 차트 테마 빠른 선택 버튼
st.subheader("⚡ 멜론 차트 선택")
chart_keys = list(MELON_DATABASE.keys())
q_col1, q_col2, q_col3, q_col4 = st.columns(4)

with q_col1:
    if st.button("🔥 TOP100", use_container_width=True):
        st.session_state.selected_chart = chart_keys[0]
        recommend_song()
with q_col2:
    if st.button("☀️ 핫트렌드", use_container_width=True):
        st.session_state.selected_chart = chart_keys[1]
        recommend_song()
with q_col3:
    if st.button("🎸 장르별", use_container_width=True):
        st.session_state.selected_chart = chart_keys[2]
        recommend_song()
with q_col4:
    if st.button("📼 추억차트", use_container_width=True):
        st.session_state.selected_chart = chart_keys[3]
        recommend_song()

# 8. 검색 및 필터 옵션
st.markdown("---")
selected_category = st.selectbox(
    "🎧 현재 탐색 중인 차트",
    options=chart_keys,
    index=chart_keys.index(st.session_state.selected_chart),
    key="chart_selector"
)
st.session_state.selected_chart = selected_category

# 최초 진입 시 기본 추천 곡 설정
if st.session_state.current_song is None:
    recommend_song()

# 9. 실시간 노래 추천 카드 표시 영역 (st.fragment로 리프레시 관리)
@st.fragment
def song_display_fragment():
    song = st.session_state.current_song
    
    st.markdown('<div class="song-card">', unsafe_allow_html=True)
    
    if song:
        st.markdown(f'<span class="chart-badge">{st.session_state.selected_chart}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="song-title-display">{song["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="artist-display">🎤 {song["artist"]}</div>', unsafe_allow_html=True)
        
        # 상세 정보 표시 (앨범, 장르, 발매년도)
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.caption("💿 앨범")
            st.write(f"**{song['album']}**")
        with info_col2:
            st.caption("🎶 장르")
            st.write(f"**{song['genre']}**")
        with info_col3:
            st.caption("📅 발매년도")
            st.write(f"**{song['year']}년**")
    else:
        st.write("버튼을 눌러 노래를 추천받아 보세요!")
        
    st.markdown('</div>', unsafe_allow_html=True)

    # 추천을 5번 이상 받을 때마다 축하 풍선 효과
    if st.session_state.recommend_count > 0 and st.session_state.recommend_count % 5 == 0:
        st.balloons()
        st.success(f"🎉 음악 탐험가! 벌써 {st.session_state.recommend_count}번째 곡을 추천받으셨어요!")

# 노래 디스플레이 출력
song_display_fragment()

# 10. 추천 제어 버튼 (다시 추천받기 / 즐겨찾기)
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    st.button("🎲 다른 노래 추천받기", on_click=recommend_song, type="primary", use_container_width=True)

with btn_col2:
    st.button("❤️ 내 보관함에 담기", on_click=add_to_favorites, use_container_width=True)

# 11. 내 즐겨찾기 보관함
st.markdown("---")
st.subheader("📁 내가 담은 노래 보관함")

if st.session_state.favorites:
    for idx, fav in enumerate(st.session_state.favorites, 1):
        st.text(f"{idx}. {fav['title']} - {fav['artist']} ({fav['genre']})")
    
    if st.button("🗑️ 보관함 비우기"):
        clear_favorites()
        st.rerun()
else:
    st.info("아직 보관함에 담긴 노래가 없습니다. 마음에 드는 곡을 담아보세요!")
