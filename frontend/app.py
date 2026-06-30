import threading
import time
import httpx
import streamlit as st

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="MedRoute AI",
    page_icon="🏥",
    layout="centered",
)

st.markdown("""
<style>
.emergency-banner {
    background: #ff4444;
    color: white;
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 16px;
}
.dept-card {
    background: #1e2a3a;
    border-left: 5px solid #4fa3e0;
    padding: 16px 20px;
    border-radius: 8px;
    margin-bottom: 12px;
}
.dept-card.emergency {
    border-left-color: #ff4444;
}
.priority-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: bold;
    margin-left: 8px;
}
.badge-emergency { background: #ff4444; color: white; }
.badge-urgent    { background: #ff9900; color: white; }
.badge-routine   { background: #28a745; color: white; }
.confidence-bar  { height: 8px; border-radius: 4px; background: #e9ecef; margin-top: 4px; }
.confidence-fill { height: 8px; border-radius: 4px; background: #4fa3e0; }
.status-dot      { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
.status-ok  { background: #28a745; }
.status-err { background: #ff4444; }
</style>
""", unsafe_allow_html=True)


def check_backend() -> bool:
    try:
        r = httpx.get(f"{BACKEND_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def call_triage(message: str, language: str) -> dict:
    with httpx.Client(timeout=120) as client:
        r = client.post(
            f"{BACKEND_URL}/triage",
            json={"message": message, "language": language},
        )
        r.raise_for_status()
        return r.json()


def priority_badge(priority: str) -> str:
    cls = {
        "Emergency": "badge-emergency",
        "Urgent": "badge-urgent",
        "Routine": "badge-routine",
    }.get(priority, "badge-routine")
    return f'<span class="priority-badge {cls}">{priority}</span>'


# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏥 MedRoute AI")
st.caption("Multilingual Medical Triage — Powered by Sarvam-2B + LoRA")

# Backend status
ok = check_backend()
dot = "status-ok" if ok else "status-err"
label = "Backend connected" if ok else "Backend offline — start the FastAPI server"
st.markdown(
    f'<span class="status-dot {dot}"></span><small>{label}</small>',
    unsafe_allow_html=True,
)
st.divider()

# ── Input ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    message = st.text_area(
        "Describe your symptoms",
        placeholder="e.g. I have chest pain radiating to my left arm...",
        height=120,
        label_visibility="collapsed",
    )
with col2:
    language = st.selectbox(
        "Language",
        ["auto", "english", "hindi", "marathi", "tamil", "telugu", "bengali"],
    )

submitted = st.button("Analyse Symptoms", type="primary", disabled=not ok)

# ── Session history ───────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Triage ────────────────────────────────────────────────────────────────────
STAGES = [
    "🩺 Receiving symptoms...",
    "🌐 Detecting language...",
    "🧠 Analysing symptoms...",
    "🏥 Selecting department...",
    "🤖 Consulting Sarvam AI...",
    "📋 Preparing recommendation...",
]

if submitted and message.strip():
    t0 = time.perf_counter()
    result_box: dict = {}
    error_box: dict = {}

    def _fetch():
        try:
            result_box["data"] = call_triage(message.strip(), language)
        except Exception as exc:
            error_box["err"] = str(exc)

    thread = threading.Thread(target=_fetch, daemon=True)
    thread.start()

    status = st.empty()
    stage_idx = 0
    while thread.is_alive():
        status.markdown(f"**{STAGES[min(stage_idx, len(STAGES)-1)]}**")
        time.sleep(1.1)
        stage_idx += 1
    thread.join()
    status.empty()

    if error_box:
        # Graceful fallback instead of a raw error
        st.warning(
            "⚠️ **AI service temporarily unavailable.** Using emergency fallback protocol.\n\n"
            "If symptoms are severe, please seek immediate medical attention."
        )
        st.caption(f"Technical detail: {error_box['err']}")
    elif result_box:
        latency = int((time.perf_counter() - t0) * 1000)
        st.session_state.history.insert(0, {
            "message": message,
            "result": result_box["data"],
            "latency": latency,
        })

elif submitted and not message.strip():
    st.warning("Please describe your symptoms first.")

# ── Results ───────────────────────────────────────────────────────────────────
for entry in st.session_state.history:
    r = entry["result"]
    msg = entry["message"]
    ms = entry["latency"]

    # Emergency banner — text comes from backend (already translated)
    if r.get("emergency"):
        lang_code = r.get("language", "en")
        _BANNERS = {
            "hi": "🚨 आपातकाल — तुरंत चिकित्सकीय सहायता लें",
            "mr": "🚨 आपत्कालीन — त्वरित वैद्यकीय मदत घ्या",
        }
        banner_text = _BANNERS.get(lang_code, "🚨 EMERGENCY — Seek immediate medical attention")
        st.markdown(
            f'<div class="emergency-banner">{banner_text}</div>',
            unsafe_allow_html=True,
        )

    # Main card
    dept = r.get("department", "Unknown")
    priority = r.get("priority", "Routine")
    confidence = r.get("confidence", 0.0)
    card_cls = "dept-card emergency" if r.get("emergency") else "dept-card"

    st.markdown(
        f"""<div class="{card_cls}">
        <strong style="font-size:1.2rem">{dept}</strong>
        {priority_badge(priority)}
        <br><small style="color:#aaa">Confidence</small>
        <div class="confidence-bar">
          <div class="confidence-fill" style="width:{int(confidence*100)}%"></div>
        </div>
        <small>{int(confidence*100)}%</small>
        </div>""",
        unsafe_allow_html=True,
    )

    # Advice
    advice = r.get("advice", "")
    if advice:
        st.info(f"**Advice:** {advice}")

    # Details
    with st.expander("Details", expanded=True):
        col_a, col_b = st.columns(2)

        with col_a:
            reasoning = r.get("reasoning", [])
            if reasoning:
                st.markdown("**Reasoning**")
                for item in reasoning:
                    st.markdown(f"- {item}")

        with col_b:
            tests = r.get("recommended_tests", [])
            if tests:
                st.markdown("**Recommended Tests**")
                for t in tests:
                    st.markdown(f"- {t}")

        st.caption(f"Language: {r.get('language', 'unknown')} · Response time: {ms} ms")

    st.markdown(f"<small style='color:#666'>*{msg[:80]}{'…' if len(msg)>80 else ''}*</small>", unsafe_allow_html=True)
    st.divider()
