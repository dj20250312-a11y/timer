import random
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🎵 2026 멜론 차트 & 밴드·인디 추천기",
    page_icon="🎵",
    layout="centered"
)

# 2. CSS 스타일 적용
st.markdown("""
<style>
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
    
    .song-title-display {
        font-size: clamp(1.8rem, 6vw, 3.2rem);
        font-weight: 800;
        color: #00cd3c;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        line-height: 1.2;
        margin: 15px 0 5px 0;
        word-break: keep-all;
    }

    .artist-display {
        font-size: clamp(1.1rem, 3.5vw, 1.8rem);
        font-weight: 600;
        color: #2E3A59;
        margin-bottom: 15px;
    }
    
    .chart-badge {
        display: inline-block;
        background-color: #e6f9ed;
        color: #00cd3c;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# 3. 신뢰할 수 있는 데이터베이스 (2026년 7~8월 차트 및 실제 발매 곡 기준)
MELON_DATABASE = {
    "☀️ 2026 7~8월 핫트렌드": [
        {"title": "REDRED", "artist": "CORTIS (코르티스)", "genre": "댄스/팝", "album": "REDRED", "year": 2026},
        {"title": "BANG BANG", "artist": "IVE (아이브)", "genre": "댄스", "album": "BANG BANG", "year": 2026},
        {"title": "SWIM", "artist": "방탄소년단 (BTS)", "genre": "R&B/Pop", "album": "SWIM", "year": 2026},
        {"title": "It's Me", "artist": "ILLIT (아일릿)", "genre": "댄스", "album": "It's Me", "year": 2026},
        {"title": "갑자기 (Suddenly)", "artist": "I.O.I (아이오아이)", "genre": "댄스/발라드", "album": "Re:UNION", "year": 2026},
        {"title": "소문의 낙원", "artist": "AKMU (악뮤)", "genre": "인디/포크", "album": "낙원", "year": 2026},
        {"title": "캐치 캐치 (Catch Catch)", "artist": "YENA (최예나)", "genre": "댄스", "album": "Catch Catch", "year": 2026},
        {"title": "기쁨, 슬픔, 아름다운 마음", "artist": "AKMU (악뮤)", "genre": "발라드", "album": "낙원", "year": 2026},
    ],
    "🎸 밴드 & 인디": [
        {"title": "입춘", "artist": "한로로", "genre": "인디 록", "album": "입춘", "year": 2022},
        {"title": "사랑하게 될 거야", "artist": "한로로", "genre": "인디 록", "album": "이상비행", "year": 2023},
        {"title": "자처", "artist": "한로로", "genre": "인디 록", "album": "자처", "year": 2023},
        {"title": "고민중독", "artist": "QWER", "genre": "밴드/록", "album": "MANITO", "year": 2024},
        {"title": "주저하는 연인들을 위해", "artist": "잔나비", "genre": "인디/록", "album": "전설", "year": 2019},
        {"title": "Tik Tak Tok (feat. So!YoON!)", "artist": "실리카겔", "genre": "사이키델릭 록", "album": "POWER AND BANE", "year": 2023},
        {"title": "Bad", "artist": "wave to earth", "genre": "인디 팝/록", "album": "0.1 flaws and all.", "year": 2023},
        {"title": "개화 (Flowering)", "artist": "LUCY (루시)", "genre": "인디 팝", "album": "PANORAMA", "year": 2020},
    ],
    "🔥 대중적인 인기 가요": [
        {"title": "Supernova", "artist": "aespa", "genre": "댄스", "album": "Armageddon", "year": 2024},
        {"title": "How Sweet", "artist": "NewJeans", "genre": "댄스", "album": "How Sweet", "year": 2024},
        {"title": "Magnetic", "artist": "ILLIT (아일릿)", "genre": "댄스", "album": "SUPER REAL ME", "year": 2024},
        {"title": "Spot! (feat. JENNIE)", "artist": "지코 (ZICO)", "genre": "랩/힙합", "album": "SPOT!", "year": 2024},
        {"title": "Small girl (feat. 도경수)", "artist": "이영지", "genre": "랩/힙합", "album": "16 FANTASY", "year": 2024},
        {"title": "Bam Yang Gang (밤양갱)", "artist": "비비 (BIBI)", "genre": "R&B/Soul", "album": "밤양갱", "year": 2024},
    ],
    "📼 스테디셀러 명곡": [
        {"title": "Dynamite", "artist": "방탄소년단", "genre": "댄스/팝", "album": "Dynamite", "year": 2020},
        {"title": "Love wins all", "artist": "아이유 (IU)", "genre": "발라드", "album": "The Winning", "year": 2024},
        {"title": "사건의 지평선", "artist": "윤하 (YOUNHA)", "genre": "록/메탈", "album": "END THEORY", "year": 2022},
        {"title": "신호등", "artist": "이무진", "genre": "포크/인디", "album": "신호등", "year": 2021},
        {"title": "Hype Boy", "artist": "NewJeans", "genre": "댄스", "album": "New Jeans", "year": 2022},
    ]
}

# 4. 세션 상태 초기화
if "selected_chart" not in st.session_state:
    st.session_state.selected_chart = "☀️ 2026 7~8월 핫트렌드"
if "current_song" not in st.session_state:
    st.session_state.current_song = None
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "recommend_count" not in st.session_state:
    st.session_state.recommend_count = 0

# 5. 제어 함수
def recommend_song():
    chart_list = MELON_DATABASE.get(st.session_state.selected_chart, [])
    if chart_list:
        st.session_state.current_song = random.choice(chart_list)
        st.session_state.recommend_count += 1

def add_to_favorites():
    if st.session_state.current_song:
        song = st.session_state.current_song
        if song not in st.session_state.favorites:
            st.session_state.favorites.append(song)
            st.toast(f"❤️ [{song['title']}] 곡이 보관함에 담겼습니다!", icon="🎵")
        else:
            st.warning("이미 즐겨찾기에 추가된 노래입니다!")

def clear_favorites():
    st.session_state.favorites = []

# 6. UI 구성
st.title("🎵 멜론 차트 & 밴드·인디 추천기")
st.write("2026년 7~8월 최신 차트부터 인디/밴드 명곡까지 추천해 드립니다!")

# 7. 차트 빠른 선택 버튼
st.subheader("⚡ 음악 장르/차트 선택")
chart_keys = list(MELON_DATABASE.keys())
q_col1, q_col2, q_col3, q_col4 = st.columns(4)

with q_col1:
    if st.button("☀️ 7~8월 차트", use_container_width=True):
        st.session_state.selected_chart = chart_keys[0]
        recommend_song()
with q_col2:
    if st.button("🎸 밴드 & 인디", use_container_width=True):
        st.session_state.selected_chart = chart_keys[1]
        recommend_song()
with q_col3:
    if st.button("🔥 인기 가요", use_container_width=True):
        st.session_state.selected_chart = chart_keys[2]
        recommend_song()
with q_col4:
    if st.button("📼 명곡 레전드", use_container_width=True):
        st.session_state.selected_chart = chart_keys[3]
        recommend_song()

# 8. 셀렉트 박스
st.markdown("---")
selected_category = st.selectbox(
    "🎧 현재 탐색 중인 장르/차트",
    options=chart_keys,
    index=chart_keys.index(st.session_state.selected_chart),
    key="chart_selector"
)
st.session_state.selected_chart = selected_category

if st.session_state.current_song is None:
    recommend_song()

# 9. 실시간 노래 추천 카드
@st.fragment
def song_display_fragment():
    song = st.session_state.current_song
    
    st.markdown('<div class="song-card">', unsafe_allow_html=True)
    
    if song:
        st.markdown(f'<span class="chart-badge">{st.session_state.selected_chart}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="song-title-display">{song["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="artist-display">🎤 {song["artist"]}</div>', unsafe_allow_html=True)
        
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

    if st.session_state.recommend_count > 0 and st.session_state.recommend_count % 5 == 0:
        st.balloons()
        st.success(f"🎉 음악 탐험가! 벌써 {st.session_state.recommend_count}번째 곡을 추천받으셨어요!")

song_display_fragment()

# 10. 추천 제어 버튼
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    st.button("🎲 다른 노래 추천받기", on_click=recommend_song, type="primary", use_container_width=True)

with btn_col2:
    st.button("❤️ 내 보관함에 담기", on_click=add_to_favorites, use_container_width=True)

# 11. 즐겨찾기 보관함
st.markdown("---")
st.subheader("📁 내가 담은 추천 곡 보관함")

if st.session_state.favorites:
    for idx, fav in enumerate(st.session_state.favorites, 1):
        st.text(f"{idx}. {fav['title']} - {fav['artist']} ({fav['year']}년 / {fav['genre']})")
    
    if st.button("🗑️ 보관함 비우기"):
        clear_favorites()
        st.rerun()
else:
    st.info("아직 보관함에 담긴 노래가 없습니다. 마음에 드는 곡을 담아보세요!")
