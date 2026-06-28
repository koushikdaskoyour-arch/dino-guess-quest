import random
import streamlit as st

st.set_page_config(page_title="🦖 Dino Guess Quest", page_icon="🦕", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Fredoka', sans-serif !important; }
.main-title {
    font-size: 2.5rem !important; font-weight: 700 !important; text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.dino-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 24px; padding: 1.5rem; text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 1rem 0;
}
.dino-emoji { font-size: 5rem; animation: bounce 2s infinite; }
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-15px)} }
@keyframes celebrate { 0%{transform:scale(1)rotate(0)}25%{transform:scale(1.2)rotate(-10deg)}50%{transform:scale(1)rotate(0)}75%{transform:scale(1.2)rotate(10deg)}100%{transform:scale(1)rotate(0)} }
.celebrating { animation: celebrate 0.5s ease-in-out infinite; }
.feedback-card {
    background: white; border-radius: 16px; padding: 1.5rem; margin: 1rem 0;
    text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.attempts-badge {
    display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; padding: 0.5rem 1.5rem; border-radius: 50px;
    font-size: 1.1rem; font-weight: 600;
}
.setup-card {
    background: linear-gradient(135deg, #fff1eb 0%, #ace0f9 100%);
    border-radius: 24px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}
.victory-card {
    background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
    border-radius: 24px; padding: 2rem; text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
.leaderboard-card {
    background: white; border-radius: 12px; padding: 0.8rem; margin: 0.4rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.progress-container { background: #f0f0f0; border-radius: 50px; height: 16px; overflow: hidden; margin: 1rem 0; }
.progress-bar { height: 100%; border-radius: 50px; transition: width 0.5s ease; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

DIFFICULTY_CONFIG = {
    "🟢 Normal": {
        "range": (1, 100), "dino_emoji": "🦖", "dino_name": "Fluffy",
        "dino_color": "#88d8a3", "personality": "Cheerful & Friendly",
        "description": "A fluffy green baby dinosaur who loves helping!",
        "max_range": 100
    },
    "🟠 Hard": {
        "range": (1, 250), "dino_emoji": "🦕", "dino_name": "Blaze",
        "dino_color": "#ffaaa5", "personality": "Energetic & Adventurous",
        "description": "An orange adventurous dinosaur ready for a challenge!",
        "max_range": 250
    },
    "🔴 Elite": {
        "range": (1, 500), "dino_emoji": "🐉", "dino_name": "Shadow",
        "dino_color": "#9b9bc9", "personality": "Confident & Competitive",
        "description": "A legendary dark blue dinosaur for true masters!",
        "max_range": 500
    }
}

def calculate_feedback(guess, target, max_range):
    distance = abs(guess - target)
    percentage = (distance / max_range) * 100
    if guess == target:
        return {"emoji": "🎯", "text": "Perfect!", "color": "#00b894", "face": "🎉", "mood": "celebrating", "level": "perfect"}
    elif percentage <= 1:
        return {"emoji": "🤩", "text": "Almost There!", "color": "#fdcb6e", "face": "🤩", "mood": "excited", "level": "almost"}
    elif percentage <= 3:
        return {"emoji": "😲", "text": "Very Close!", "color": "#e17055", "face": "😲", "mood": "surprised", "level": "very_close"}
    elif percentage <= 7:
        return {"emoji": "😊", "text": "Close!", "color": "#fd79a8", "face": "😊", "mood": "happy", "level": "close"}
    elif percentage <= 15:
        return {"emoji": "🔥", "text": "Getting Warmer!", "color": "#e84393", "face": "🙂", "mood": "pleased", "level": "warmer"}
    elif percentage <= 30:
        return {"emoji": "🌤", "text": "Far", "color": "#74b9ff", "face": "😐", "mood": "neutral", "level": "far"}
    else:
        return {"emoji": "❄️", "text": "Very Far Away", "color": "#0984e3", "face": "😞", "mood": "sad", "level": "very_far"}

def init_state():
    defaults = {
        'game_initialized': False, 'player_name': "", 'difficulty': None,
        'target_number': None, 'attempts': 0, 'game_won': False,
        'guess_history': [], 'leaderboard': [], 'setup_complete': False,
        'current_guess': None, 'feedback': None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def start_game(difficulty_key, player_name):
    config = DIFFICULTY_CONFIG[difficulty_key]
    st.session_state.difficulty = difficulty_key
    st.session_state.target_number = random.randint(*config["range"])
    st.session_state.attempts = 0
    st.session_state.game_won = False
    st.session_state.guess_history = []
    st.session_state.player_name = player_name
    st.session_state.setup_complete = True
    st.session_state.current_guess = None
    st.session_state.feedback = None

def check_guess(guess):
    if guess is None: return
    st.session_state.attempts += 1
    st.session_state.current_guess = guess
    st.session_state.guess_history.append(guess)
    config = DIFFICULTY_CONFIG[st.session_state.difficulty]
    fb = calculate_feedback(guess, st.session_state.target_number, config["max_range"])
    if guess == st.session_state.target_number:
        st.session_state.game_won = True
        entry = {'player': st.session_state.player_name, 'difficulty': st.session_state.difficulty,
                 'attempts': st.session_state.attempts, 'target': st.session_state.target_number}
        st.session_state.leaderboard.append(entry)
        st.session_state.leaderboard.sort(key=lambda x: x['attempts'])
        st.balloons()
    st.session_state.feedback = fb

def restart_game():
    config = DIFFICULTY_CONFIG[st.session_state.difficulty]
    st.session_state.target_number = random.randint(*config["range"])
    st.session_state.attempts = 0; st.session_state.game_won = False
    st.session_state.guess_history = []; st.session_state.current_guess = None
    st.session_state.feedback = None

def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()

def get_best():
    if not st.session_state.leaderboard: return None
    entries = [e for e in st.session_state.leaderboard if e['difficulty'] == st.session_state.difficulty]
    return min(entries, key=lambda x: x['attempts']) if entries else None

def render_setup():
    st.markdown('<h1 class="main-title">🦖 Dino Guess Quest</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Can you find the hidden number?</p>', unsafe_allow_html=True)
    st.markdown('<div class="setup-card">', unsafe_allow_html=True)
    st.markdown("### 👤 Enter Your Name")
    player_name = st.text_input("Your Name", placeholder="e.g., Dino Hunter", label_visibility="collapsed")
    st.markdown("### 🎮 Choose Your Difficulty")
    cols = st.columns(3)
    diff_choice = None
    for idx, (key, cfg) in enumerate(DIFFICULTY_CONFIG.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align:center;padding:0.8rem;">
            <div style="font-size:3.5rem;">{cfg['dino_emoji']}</div>
            <div style="font-weight:700;font-size:1.1rem;color:{cfg['dino_color']};">{cfg['dino_name']}</div>
            <div style="font-size:0.85rem;color:#666;margin:0.3rem 0;">{cfg['description']}</div>
            <div style="background:#f0f0f0;border-radius:8px;padding:0.4rem;font-size:0.9rem;">
            <strong>Range:</strong> 1-{cfg['max_range']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Play {key}", key=f"btn_{key}", use_container_width=True):
                diff_choice = key
    st.markdown('</div>', unsafe_allow_html=True)
    if diff_choice and player_name.strip():
        start_game(diff_choice, player_name.strip()); st.rerun()
    elif diff_choice and not player_name.strip():
        st.error("⚠️ Please enter your name first!")

def render_game():
    cfg = DIFFICULTY_CONFIG[st.session_state.difficulty]
    st.markdown('<h1 class="main-title">🦖 Dino Guess Quest</h1>', unsafe_allow_html=True)
    anim = "celebrating" if st.session_state.game_won else ""
    st.markdown(f"""
    <div class="dino-card">
    <div class="dino-emoji {anim}">{cfg['dino_emoji']}</div>
    <h2 style="color:{cfg['dino_color']};margin:0.3rem 0;">{cfg['dino_name']}</h2>
    <p style="color:#666;margin:0;">{cfg['personality']}</p>
    </div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="feedback-card"><div style="font-size:0.85rem;color:#888;">Player</div><div style="font-size:1.2rem;font-weight:700;">{st.session_state.player_name}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="feedback-card"><div style="font-size:0.85rem;color:#888;">Difficulty</div><div style="font-size:1.2rem;font-weight:700;">{st.session_state.difficulty}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="feedback-card"><div style="font-size:0.85rem;color:#888;">Attempts</div><div class="attempts-badge">{st.session_state.attempts}</div></div>', unsafe_allow_html=True)
    if st.session_state.game_won:
        render_victory()
    else:
        render_guess_input(); render_feedback(); render_history()

def render_guess_input():
    cfg = DIFFICULTY_CONFIG[st.session_state.difficulty]
    mn, mx = cfg["range"]
    st.markdown("### 🔢 Enter Your Guess")
    c1, c2 = st.columns([3, 1])
    with c1:
        guess = st.number_input(f"Guess {mn}-{mx}", min_value=mn, max_value=mx, value=mn, step=1, label_visibility="collapsed")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Guess!", use_container_width=True, type="primary"):
            check_guess(guess); st.rerun()

def render_feedback():
    if st.session_state.feedback is None:
        cfg = DIFFICULTY_CONFIG[st.session_state.difficulty]
        st.markdown(f"""
        <div class="feedback-card">
        <div style="font-size:2.5rem;margin-bottom:0.3rem;">🤔</div>
        <div style="font-size:1.2rem;font-weight:600;color:#667eea;">
        I'm thinking of a number between 1 and {cfg['max_range']}...</div>
        <div style="color:#888;">Can you guess it?</div>
        </div>""", unsafe_allow_html=True)
        return
    fb = st.session_state.feedback
    guess = st.session_state.current_guess
    target = st.session_state.target_number
    if not st.session_state.game_won:
        direction = "📈 Too Low! Go Higher!" if guess < target else "📉 Too High! Go Lower!"
        st.markdown(f"""
        <div class="feedback-card" style="border-left:5px solid {fb['color']};">
        <div style="font-size:2.5rem;margin-bottom:0.3rem;">{fb['face']}</div>
        <div style="font-size:1.3rem;font-weight:600;color:{fb['color']};">
        {fb['emoji']} {fb['text']}</div>
        <div style="font-size:1.3rem;font-weight:700;color:#2d3436;margin:0.3rem 0;">{direction}</div>
        <div style="color:#888;font-size:0.9rem;">Your guess: <strong>{guess}</strong></div>
        </div>""", unsafe_allow_html=True)
        max_r = DIFFICULTY_CONFIG[st.session_state.difficulty]['max_range']
        dist = abs(guess - target)
        prog = max(0, 100 - (dist / max_r * 100))
        st.markdown(f"""
        <div style="margin:0.8rem 0;">
        <div style="display:flex;justify-content:space-between;font-size:0.85rem;color:#888;">
        <span>Cold</span><span>Hot</span></div>
        <div class="progress-container">
        <div class="progress-bar" style="width:{prog}%;background:linear-gradient(90deg,#74b9ff,#fd79a8,#e17055);"></div>
        </div></div>""", unsafe_allow_html=True)

def render_history():
    if st.session_state.guess_history:
        with st.expander("📜 Guess History", expanded=False):
            html = "<div style='display:flex;flex-wrap:wrap;gap:0.4rem;'>"
            for i, g in enumerate(st.session_state.guess_history, 1):
                t = st.session_state.target_number
                ind = "🎯" if g == t else "📈" if g < t else "📉"
                col = "#00b894" if g == t else "#74b9ff" if g < t else "#e17055"
                html += f"""
                <div style="background:{col}20;border:2px solid {col};border-radius:12px;padding:0.4rem 0.8rem;">
                <span style="font-size:0.75rem;color:#888;">#{i}</span>
                <span style="font-weight:700;color:{col};margin-left:0.3rem;">{g}</span>
                <span style="margin-left:0.2rem;">{ind}</span>
                </div>"""
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

def render_victory():
    cfg = DIFFICULTY_CONFIG[st.session_state.difficulty]
    st.markdown(f"""
    <div class="victory-card">
    <div style="font-size:4rem;margin-bottom:0.5rem;" class="celebrating">🎉</div>
    <h2 style="color:#2d3436;margin:0.3rem 0;">Congratulations, {st.session_state.player_name}!</h2>
    <div style="font-size:1.2rem;color:#636e72;margin:0.8rem 0;">
    You found <strong style="color:#e17055;font-size:1.8rem;">{st.session_state.target_number}</strong>!</div>
    <div class="attempts-badge" style="font-size:1.3rem;">🏆 Attempts: {st.session_state.attempts}</div>
    <div style="font-size:3.5rem;margin:0.8rem 0;" class="celebrating">{cfg['dino_emoji']}</div>
    <div style="color:#636e72;">{cfg['dino_name']} is so proud! 🌟</div>
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Play Again", use_container_width=True, type="primary"):
            restart_game(); st.rerun()
    with c2:
        if st.button("🏠 Main Menu", use_container_width=True):
            reset_all(); st.rerun()

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🦕 Dino Guess Quest"); st.markdown("---")
        with st.expander("📖 Game Rules", expanded=True):
            st.markdown("1. 🎯 **Guess** the hidden number\n2. 📈 Get **Too High / Too Low** hints\n3. 🔥 Watch the **warmth meter**\n4. 🏆 **Lower attempts = Better score!**")
        with st.expander("⚡ Difficulties", expanded=False):
            for key, cfg in DIFFICULTY_CONFIG.items():
                st.markdown(f"**{key}**  \n🦖 {cfg['dino_name']}  \n📊 Range: 1-{cfg['max_range']}  \n🎭 {cfg['personality']}")
        if st.session_state.setup_complete:
            st.markdown("---"); st.markdown("### 👤 Current Player")
            st.markdown(f"""
            <div style="background:#f8f9fa;border-radius:12px;padding:0.8rem;margin:0.4rem 0;">
            <strong>Name:</strong> {st.session_state.player_name}<br>
            <strong>Difficulty:</strong> {st.session_state.difficulty}<br>
            <strong>Attempts:</strong> {st.session_state.attempts}
            </div>""", unsafe_allow_html=True)
            best = get_best()
            if best:
                st.markdown(f"""
                <div style="background:#fff3cd;border-radius:12px;padding:0.8rem;">
                🏆 <strong>Best Score:</strong> {best['attempts']} attempts
                </div>""", unsafe_allow_html=True)
        if st.session_state.leaderboard:
            st.markdown("---"); st.markdown("### 🏅 Leaderboard")
            for i, e in enumerate(st.session_state.leaderboard[:10], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "•"
                st.markdown(f"""
                <div class="leaderboard-card">
                <div style="display:flex;justify-content:space-between;">
                <span>{medal} <strong>{e['player']}</strong></span>
                <span style="color:#e17055;font-weight:700;">{e['attempts']}</span>
                </div>
                <div style="font-size:0.75rem;color:#888;">{e['difficulty']} • Hidden: {e['target']}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("---")
        if st.session_state.setup_complete:
            if st.button("🔄 Restart Game", use_container_width=True):
                restart_game(); st.rerun()
        if st.button("🏠 Back to Menu", use_container_width=True):
            reset_all(); st.rerun()

def main():
    init_state(); render_sidebar()
    if not st.session_state.setup_complete:
        render_setup()
    else:
        render_game()

if __name__ == "__main__":
    main()
