import streamlit as st
import tensorflow as tf
import numpy as np
import textwrap
import math
from PIL import Image
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SafeRoad AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("SafeRoad_AI_Model.keras")


model = load_model()


# ============================================================
# HTML HELPER — always dedent so Markdown never mistakes
# indented lines for a code block.
# ============================================================

def html(markup: str) -> str:
    return textwrap.dedent(markup).strip()


def render(markup: str):
    st.markdown(html(markup), unsafe_allow_html=True)


# ============================================================
# CUSTOM CSS
# ============================================================

render("""
<style>

.stApp {
    background: radial-gradient(circle at top left, #263746 0%, #18232d 35%, #101820 100%);
    color: #e8eef2;
}

#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }

.main .block-container {
    max-width: 1300px;
    margin: 25px auto;
    padding: 30px 34px;
    background: rgba(39, 52, 63, 0.88);
    border: 1px solid rgba(130, 150, 165, 0.45);
    border-radius: 18px;
    box-shadow: 0 0 35px rgba(0, 0, 0, 0.45), inset 0 0 20px rgba(255, 255, 255, 0.02);
}

.logo-title { font-size: 35px; font-weight: 700; letter-spacing: 0.3px; color: #f0f5f8; }
.subtitle { margin-top: 4px; margin-bottom: 28px; color: #aab8c2; font-size: 16px; }
.section-title { font-size: 18px; font-weight: 600; color: #edf3f6; margin-bottom: 12px; }

/* Card containers (targeted via st.container(key=...)) */
.st-key-upload_card, .st-key-image_card, .st-key-detect_card, .st-key-risk_card {
    background: rgba(28, 40, 49, 0.92) !important;
    border: 1px solid #52616c;
    border-radius: 14px;
    padding: 18px 20px 20px 20px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.25), inset 0 0 10px rgba(255, 255, 255, 0.015);
    margin-bottom: 15px;
}
.st-key-detect_card, .st-key-risk_card {
    background: linear-gradient(145deg, #202e38, #18232b) !important;
    border: 1px solid #566772;
}
.st-key-image_card { padding: 10px; }

[data-testid="stFileUploader"] {
    background: #293640;
    border: 1px dashed #657581;
    border-radius: 12px;
    padding: 12px;
    margin-top: 6px;
}
[data-testid="stFileUploader"] button {
    background: #f0f4f6 !important;
    color: #1d2932 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.image-caption { text-align: center; color: #9baab4; font-size: 12px; margin-top: 8px; letter-spacing: 0.5px; }

.card-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}
.card-title { font-size: 17px; font-weight: 600; color: #eef4f7; }

.status-pill-ok {
    background: rgba(55, 190, 120, 0.18);
    border: 1px solid rgba(70, 210, 135, 0.5);
    color: #65d79a;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
}
.status-pill-alert {
    background: rgba(245, 90, 75, 0.18);
    border: 1px solid rgba(245, 100, 85, 0.55);
    color: #ff8074;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.condition-row { display: flex; align-items: center; gap: 10px; margin-top: 14px; }
.condition-icon-ok, .condition-icon-alert {
    width: 26px; height: 26px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 700;
}
.condition-icon-ok { background: rgba(55, 190, 120, 0.2); color: #65d79a; }
.condition-icon-alert { background: rgba(245, 90, 75, 0.2); color: #ff8074; }
.condition-label-ok { font-size: 21px; font-weight: 700; color: #65d79a; }
.condition-label-alert { font-size: 21px; font-weight: 700; color: #ff8074; }
.mini-label { color: #aebbc5; font-size: 13px; }

.confidence-container { display: flex; justify-content: center; align-items: center; margin: 4px 0; }
.confidence-circle {
    width: 105px; height: 105px; border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    position: relative;
    background: conic-gradient(#dce7ec 0deg, #dce7ec var(--percentage), #394852 var(--percentage), #394852 360deg);
    box-shadow: 0 0 20px rgba(180, 210, 225, 0.15);
}
.confidence-circle::before {
    content: ""; position: absolute; width: 80px; height: 80px;
    background: #202c35; border-radius: 50%;
}
.confidence-text { position: relative; font-size: 16px; font-weight: 700; color: #e9f0f4; }

.section-divider { background: #53616c; height: 1px; margin: 10px 0 15px 0; }

.info-row {
    display: flex; align-items: center; gap: 10px;
    background: rgba(255,255,255,0.035);
    border-radius: 8px; padding: 10px; margin-top: 7px; font-size: 14px;
}
.info-icon {
    width: 25px; height: 25px; display: flex; justify-content: center; align-items: center;
    background: #43525d; border-radius: 6px; flex-shrink: 0;
}

.recommendation-wrap {
    border-radius: 12px; overflow: hidden; margin-top: 15px;
    border: 1px solid #78bde0; box-shadow: 0 0 18px rgba(100, 190, 230, 0.12);
}
.recommendation-header { background: #a9d8f2; color: #10202b; padding: 10px 16px; font-size: 15px; font-weight: 700; }
.recommendation-body { background: linear-gradient(135deg, #2e4350, #20303a); padding: 16px; color: #d9e3e8; font-size: 14px; }
.recommendation-timestamp { margin-top: 12px; font-size: 11px; color: #7f909a; text-align: right; }

.footer { text-align: center; color: #758691; font-size: 12px; margin-top: 25px; }

</style>
""")


# ============================================================
# HELPERS
# ============================================================

def run_inference(pil_image):
    resized = pil_image.resize((224, 224))
    arr = np.expand_dims(np.array(resized), axis=0)
    pred = model.predict(arr, verbose=0)[0][0]

    if pred >= 0.5:
        label = "Pothole"
        confidence = pred * 100
    else:
        label = "Normal"
        confidence = (1 - pred) * 100

    # Severity — prototype rule, not learned by the CNN
    if label == "Normal":
        severity = "Low"
    else:
        severity = "Medium" if confidence >= 98 else "Low"

    risk = {"Low": "Low", "Medium": "Medium"}.get(severity, "High")

    recommendation = {
        "Low": "Proceed with normal caution.",
        "Medium": "Reduce speed and proceed carefully.",
        "High": "Reduce speed and avoid the pothole if safe.",
    }[risk]

    return label, confidence, severity, risk, recommendation


def risk_gauge_svg(risk_level: str) -> str:
    needle_angle = {"Low": 145, "Medium": 90, "High": 35}[risk_level]
    needle_color = {"Low": "#65d79a", "Medium": "#f0d15a", "High": "#ff8074"}[risk_level]
    rad = math.radians(needle_angle)
    nx = 130 + 72 * math.cos(rad)
    ny = 140 - 72 * math.sin(rad)

    # NOTE: kept on tight single-purpose lines, no blank lines inside —
    # blank/indented lines inside an SVG string make Markdown treat the
    # rest of it as a code block instead of rendering it as HTML.
    return (
        '<svg viewBox="0 0 260 165" xmlns="http://www.w3.org/2000/svg" '
        'style="display:block;margin:0 auto;width:100%;max-width:280px;height:auto;">'
        '<path d="M30,140 A100,100 0 0 1 80,53.4" fill="none" stroke="#4fc58a" stroke-width="22" stroke-linecap="round"/>'
        '<path d="M80,53.4 A100,100 0 0 1 180,53.4" fill="none" stroke="#f0d15a" stroke-width="22" stroke-linecap="round"/>'
        '<path d="M180,53.4 A100,100 0 0 1 230,140" fill="none" stroke="#ed6868" stroke-width="22" stroke-linecap="round"/>'
        '<text x="35" y="118" fill="#c9d4da" font-size="13" font-weight="600" transform="rotate(-55 35 118)">Low</text>'
        '<text x="118" y="30" fill="#c9d4da" font-size="13" font-weight="600">Medium</text>'
        '<text x="200" y="118" fill="#c9d4da" font-size="13" font-weight="600" transform="rotate(55 218 118)">High</text>'
        f'<line x1="130" y1="140" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{needle_color}" stroke-width="5" stroke-linecap="round"/>'
        '<circle cx="130" cy="140" r="8" fill="' + needle_color + '"/>'
        f'<text x="130" y="162" fill="#e7edf1" font-size="13" font-weight="700" text-anchor="middle">'
        f'RISK LEVEL: <tspan fill="{needle_color}">{risk_level.upper()}</tspan></text>'
        '</svg>'
    )


# ============================================================
# HEADER
# ============================================================

render("""
<div class="logo-title">🛡️ SafeRoad AI</div>
<div class="subtitle">CNN-Based Pothole Detection System</div>
""")

left_column, right_column = st.columns([1.4, 1], gap="large")

# ------------------------------------------------------------
# LEFT COLUMN — IMAGE ANALYSIS
# ------------------------------------------------------------

with left_column:

    render('<div class="section-title">Image Analysis</div>')

    with st.container(key="upload_card"):
        render('<div class="card-title">Upload Road Image</div>')
        uploaded_file = st.file_uploader(
            "Upload Road Image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

    if uploaded_file is not None:

        original_image = Image.open(uploaded_file).convert("RGB")

        with st.container(key="image_card"):
            st.image(original_image, use_container_width=True)
            render('<div class="image-caption">CURRENT IMAGE VIEW</div>')

        # Only re-run inference when a new file is uploaded
        file_identity = (uploaded_file.name, uploaded_file.size)
        if st.session_state.get("last_file_identity") != file_identity:
            label, confidence, severity, risk, recommendation = run_inference(original_image)
            st.session_state["last_file_identity"] = file_identity
            st.session_state["label"] = label
            st.session_state["confidence"] = confidence
            st.session_state["severity"] = severity
            st.session_state["risk"] = risk
            st.session_state["recommendation"] = recommendation
            st.session_state["analyzed_on"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ------------------------------------------------------------
# RIGHT COLUMN — RESULTS
# ------------------------------------------------------------

with right_column:

    render('<div class="section-title">Analysis Results &amp; Risk Assessment</div>')

    if uploaded_file is not None:

        label = st.session_state["label"]
        confidence = st.session_state["confidence"]
        severity = st.session_state["severity"]
        risk = st.session_state["risk"]
        recommendation = st.session_state["recommendation"]
        analyzed_on = st.session_state["analyzed_on"]
        is_normal = label == "Normal"

        # ---------------- DETECTION RESULT ----------------
        with st.container(key="detect_card"):

            status_pill = (
                '<span class="status-pill-ok">STATUS: OK</span>' if is_normal
                else '<span class="status-pill-alert">STATUS: ALERT</span>'
            )
            render(f"""
                <div class="card-header-row">
                    <div class="card-title">Detection Result</div>
                    {status_pill}
                </div>
                <div class="card-title">AI Pothole Detection</div>
            """)

            condition_col, confidence_col = st.columns(2)

            with condition_col:
                if is_normal:
                    render("""
                        <div class="mini-label">Road Condition</div>
                        <div class="condition-row">
                            <div class="condition-icon-ok">✓</div>
                            <div class="condition-label-ok">NORMAL</div>
                        </div>
                    """)
                else:
                    render("""
                        <div class="mini-label">Road Condition</div>
                        <div class="condition-row">
                            <div class="condition-icon-alert">⚠</div>
                            <div class="condition-label-alert">POTHOLE</div>
                        </div>
                    """)

            with confidence_col:
                degrees = confidence * 3.6
                render(f"""
                    <div class="mini-label" style="text-align:center;">Confidence Level</div>
                    <div class="confidence-container">
                        <div class="confidence-circle" style="--percentage:{degrees}deg;">
                            <div class="confidence-text">{confidence:.2f}%</div>
                        </div>
                    </div>
                """)

        # ---------------- ROAD RISK ANALYSIS ----------------
        with st.container(key="risk_card"):
            render("""
                <div class="card-title">Road Risk Analysis</div>
                <div class="section-divider"></div>
                <div class="card-title">Detailed Risk Assessment</div>
            """)

            render(risk_gauge_svg(risk))

            render(f"""
                <div class="info-row"><div class="info-icon">✓</div><div>Road Condition: <b>{label}</b></div></div>
                <div class="info-row"><div class="info-icon">⚙</div><div>Visual Severity: <b>{severity}</b></div></div>
                <div class="info-row"><div class="info-icon">⚠</div><div>Risk Level: <b>{risk}</b></div></div>
                <div class="info-row"><div class="info-icon">◉</div><div>Detection Confidence: <b>{confidence:.2f}%</b></div></div>
            """)

        # ---------------- RECOMMENDATION ----------------
        render(f"""
            <div class="recommendation-wrap">
                <div class="recommendation-header">ⓘ &nbsp; Recommendation</div>
                <div class="recommendation-body">
                    {recommendation}
                    <div class="recommendation-timestamp">Analyzed on: {analyzed_on}</div>
                </div>
            </div>
        """)

    else:
        render("""
            <div style="border-radius:14px; text-align:center; padding:50px 20px; background:rgba(28,40,49,0.92); border:1px solid #52616c;">
                <div style="font-size:45px;">🛣️</div>
                <div style="font-size:18px; font-weight:600; margin-top:15px;">Waiting for Road Image</div>
                <div style="color:#9baab4; font-size:14px; margin-top:8px;">Upload an image to start AI analysis.</div>
            </div>
        """)

render("""
<div class="footer">SafeRoad AI &nbsp;•&nbsp; MobileNetV2 CNN &nbsp;•&nbsp; 224 × 224 Image Analysis</div>
""")