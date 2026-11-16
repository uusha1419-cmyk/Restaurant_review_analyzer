import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Restaurant Review Analyzer", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 1300px; }

.stApp {
    background-image: url('https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1920&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.88);
    z-index: 0;
}

.hero-wrap {
    position: relative;
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    border-bottom: 2px solid rgba(232,160,48,0.5);
    margin-bottom: 2rem;
}
.hero-wrap::after {
    content: "🍕  🍜  🍣  🥗  🍔  🍷  🥘  🍰";
    position: absolute;
    bottom: 6px; left: 50%;
    transform: translateX(-50%);
    font-size: 1.4rem;
    letter-spacing: 16px;
    opacity: 0.5;
    white-space: nowrap;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.8rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -2px;
    line-height: 1;
    margin: 0 0 0.6rem 0;
    text-shadow: 0 2px 20px rgba(0,0,0,0.8);
}
.hero-title .accent { color: #e8a030; }
.hero-sub {
    color: #ffcc80;
    font-size: 0.95rem;
    font-weight: 400;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.6);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(232,160,48,0.4);
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #ffffff;
    border-radius: 9px;
    font-family: 'Outfit', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 0.55rem 1.5rem;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #e8a030, #c97020) !important;
    color: #000000 !important;
    font-weight: 700 !important;
}

textarea, .stTextArea textarea {
    background: rgba(0,0,0,0.7) !important;
    border: 2px solid rgba(232,160,48,0.6) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    padding: 1rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #e8a030 0%, #c97020 100%);
    color: #000000;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 2rem;
    font-size: 0.95rem;
    box-shadow: 0 4px 20px rgba(232,160,48,0.4);
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(232,160,48,0.6);
}

.card {
    background: rgba(0,0,0,0.7);
    border: 1px solid rgba(232,160,48,0.4);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: all 0.2s;
}
.card:hover { border-color: #e8a030; transform: translateY(-2px); }
.card-label {
    font-size: 0.75rem;
    color: #ffcc80;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.5rem;
    font-weight: 600;
}
.card-value { font-size: 1.05rem; color: #ffffff; font-weight: 500; line-height: 1.5; }

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0.4rem 1.1rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-positive { background: rgba(76,175,80,0.3); color: #00ff00; border: 2px solid #4caf50; }
.badge-negative { background: rgba(239,83,80,0.3); color: #ff6b6b; border: 2px solid #ef5350; }
.badge-neutral  { background: rgba(232,160,48,0.3); color: #ffcc00; border: 2px solid #e8a030; }

.conf-wrap { margin-top: 0.6rem; }
.conf-track { background: rgba(255,255,255,0.2); border-radius: 999px; height: 10px; overflow: hidden; }
.conf-fill  { height: 100%; border-radius: 999px; }
.conf-label { font-size: 0.8rem; color: #ffcc80; font-weight: 600; }

.cat-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 0.8rem; margin-top: 1rem; }
.cat-card {
    background: rgba(0,0,0,0.7);
    border: 1px solid rgba(232,160,48,0.4);
    border-radius: 14px;
    padding: 1.2rem 0.9rem;
    text-align: center;
    transition: all 0.25s;
}
.cat-card:hover { transform: translateY(-4px); background: rgba(0,0,0,0.85); border-color: #e8a030; }
.cat-icon  { font-size: 2rem; margin-bottom: 0.4rem; display: block; }
.cat-name  { font-size: 0.8rem; color: #ffcc80; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; font-weight: 600; }
.cat-positive { border-top: 3px solid #4caf50; }
.cat-negative { border-top: 3px solid #ef5350; }
.cat-neutral  { border-top: 3px solid #e8a030; }

.sec-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e8a030;
    margin: 1.5rem 0 1rem;
    padding-left: 0.8rem;
    border-left: 4px solid #e8a030;
    text-shadow: 0 0 20px rgba(232,160,48,0.4);
}

.metric-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 0.75rem; margin-bottom: 1.5rem; }
.metric-card {
    background: rgba(0,0,0,0.7);
    border: 1px solid rgba(232,160,48,0.4);
    border-radius: 14px;
    padding: 1.3rem;
    text-align: center;
    transition: all 0.2s;
}
.metric-card:hover { border-color: #e8a030; transform: translateY(-2px); }
.m-val   { font-family: 'Cormorant Garamond', serif; font-size: 2.6rem; font-weight: 700; line-height: 1; }
.m-label { font-size: 0.8rem; color: #ffcc80; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.4rem; font-weight: 600; }

.rev-row {
    background: rgba(0,0,0,0.7);
    border: 1px solid rgba(232,160,48,0.3);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    transition: all 0.2s;
}
.rev-row:hover { background: rgba(0,0,0,0.85); border-color: #e8a030; }
.rev-text { flex: 1; font-size: 0.95rem; color: #ffffff; line-height: 1.6; font-weight: 400; }
.rev-cats { margin-top: 0.4rem; font-size: 0.8rem; color: #ffcc80; }
.rev-meta { min-width: 110px; text-align: right; }

.score-emoji { font-size: 3rem; text-align: center; padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)

BACKEND    = "http://127.0.0.1:8000"
CAT_ICONS  = {"food":"🍽️","service":"👨‍🍳","cleanliness":"✨","waiting_time":"⏱️"}
CAT_LABELS = {"food":"Food","service":"Service","cleanliness":"Cleanliness","waiting_time":"Wait Time"}
SAMPLES    = [
    "The pasta was amazing! Sauce was rich and perfectly cooked. But our waiter was rude and we waited 40 minutes.",
    "Absolutely loved everything. Staff were friendly, food came fast, and the dessert was heavenly!",
    "Disappointing visit. Tables were dirty, food was cold, and staff completely ignored us.",
    "Decent food but nothing special. Service was average, place was clean. Would not rush back.",
]
SENT_EMOJI = {"POSITIVE":"😄","NEGATIVE":"😞","NEUTRAL":"😐"}

def badge(label):
    return f'<span class="badge badge-{label.lower()}">● {label}</span>'

def conf_bar(score):
    c = "#00ff00" if score>=70 else "#ffcc00" if score>=50 else "#ff6b6b"
    return (f'<div class="conf-wrap">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
            f'<span class="conf-label">Confidence</span>'
            f'<span class="conf-label" style="color:{c};">{score}%</span></div>'
            f'<div class="conf-track"><div class="conf-fill" style="width:{score}%;background:{c};"></div></div></div>')

def cat_html(cats):
    cards = ""
    for k,s in cats.items():
        cards += (f'<div class="cat-card cat-{s}">'
                  f'<span class="cat-icon">{CAT_ICONS.get(k,"📌")}</span>'
                  f'<div class="cat-name">{CAT_LABELS.get(k,k)}</div>'
                  f'{badge(s)}</div>')
    return f'<div class="cat-row">{cards}</div>'

def dlayout(**kw):
    d = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             font=dict(color="#ffffff", family="Outfit"),
             legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#ffffff")),
             margin=dict(t=15,b=15,l=10,r=10), height=300)
    d.update(kw)
    return d

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">Restaurant <span class="accent">Review</span> Analyzer</div>
  <div class="hero-sub">Sentiment · Category Intelligence · Insights</div>
</div>""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["  🔍  Analyze a Review  ", "  📊  Dataset Dashboard  "])

# ── TAB 1 ────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="sec-title">Paste or type a customer review</div>', unsafe_allow_html=True)

    if "prefill" not in st.session_state:
        st.session_state["prefill"] = ""

    col_in, col_side = st.columns([3, 1])
    with col_in:
        review_text = st.text_area("", value=st.session_state["prefill"],
            placeholder="e.g. The pizza was incredible but I waited an hour and the tables were filthy...",
            height=145, label_visibility="collapsed", key="rbox")
    
        
    b1, b2, _ = st.columns([1.3, 0.8, 3])
    with b1:
        go_btn = st.button("🔍  Analyze Review", use_container_width=True)
    with b2:
        if st.button("Clear", use_container_width=True):
            st.session_state["prefill"] = ""
            st.rerun()

    if go_btn:
        text = review_text.strip()
        if not text:
            st.warning("Please enter a review or pick a sample.")
        else:
            with st.spinner("Running AI analysis..."):
                try:
                    res = requests.post(f"{BACKEND}/analyze_review", json={"review": text}, timeout=60)
                    d   = res.json()
                    sent, conf, summ, cats = d["sentiment"], d["confidence"], d["summary"], d["categories"]

                    st.markdown("---")
                    st.markdown('<div class="sec-title">Results</div>', unsafe_allow_html=True)

                    c0, c1, c2, c3 = st.columns([0.6, 1.5, 1.5, 1.5])
                    with c0:
                        st.markdown(f'<div class="score-emoji">{SENT_EMOJI.get(sent,"🤔")}</div>', unsafe_allow_html=True)
                    with c1:
                        st.markdown(f'<div class="card"><div class="card-label">Overall Sentiment</div><div style="margin-top:0.5rem">{badge(sent)}</div></div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="card"><div class="card-label">Model Confidence</div>{conf_bar(conf)}</div>', unsafe_allow_html=True)
                    with c3:
                        wc = len(text.split())
                        st.markdown(f'<div class="card"><div class="card-label">Review Length</div><div class="card-value">{wc} words</div></div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="card" style="border-left:4px solid #e8a030;"><div class="card-label">📝 Summary</div><div class="card-value" style="font-style:italic;color:#ffcc80;">"{summ}"</div></div>', unsafe_allow_html=True)

                    st.markdown('<div class="sec-title">Category Breakdown</div>', unsafe_allow_html=True)
                    st.markdown(cat_html(cats), unsafe_allow_html=True)

                    sm   = {"positive": 90, "neutral": 50, "negative": 15}
                    keys = list(CAT_LABELS.values())
                    vals = [sm.get(cats.get(k, "neutral"), 50) for k in cats]
                    fig  = go.Figure(go.Scatterpolar(
                        r=vals+[vals[0]], theta=keys+[keys[0]],
                        fill="toself", fillcolor="rgba(232,160,48,0.15)",
                        line=dict(color="#e8a030", width=2),
                        marker=dict(color="#e8a030", size=8)
                    ))
                    fig.update_layout(
                        polar=dict(bgcolor="rgba(0,0,0,0)",
                            radialaxis=dict(visible=False, range=[0,100]),
                            angularaxis=dict(
                                tickcolor="#ffffff",
                                linecolor="rgba(255,255,255,0.2)",
                                tickfont=dict(color="#ffffff", size=12))),
                        **dlayout(height=320, margin=dict(t=45, b=45, l=45, r=45)))
                    st.plotly_chart(fig, use_container_width=True)

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to backend. Run: uvicorn main:app --reload")

# ── TAB 2 ────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-title">Batch Analysis Dashboard</div>', unsafe_allow_html=True)
    cb, _ = st.columns([1.5, 4])
    with cb:
        load_btn = st.button("📊  Load & Analyze Dataset", use_container_width=True)

    if load_btn:
        with st.spinner("Analyzing all reviews..."):
            try:
                res   = requests.get(f"{BACKEND}/batch_analysis", timeout=120)
                data  = res.json()
                stats = data["summary_stats"]
                revs  = data["reviews"]

                st.markdown("---")
                st.markdown(f"""
                <div class="metric-grid">
                  <div class="metric-card"><div class="m-val" style="color:#e8a030">{data['total_reviews']}</div><div class="m-label">Total Reviews</div></div>
                  <div class="metric-card"><div class="m-val" style="color:#00ff00">{stats['positive_pct']}%</div><div class="m-label">Positive</div></div>
                  <div class="metric-card"><div class="m-val" style="color:#ff6b6b">{stats['negative_pct']}%</div><div class="m-label">Negative</div></div>
                  <div class="metric-card"><div class="m-val" style="color:#ffcc00">{stats['neutral_pct']}%</div><div class="m-label">Neutral</div></div>
                </div>""", unsafe_allow_html=True)

                ch1, ch2 = st.columns(2)
                with ch1:
                    st.markdown('<div class="sec-title">Sentiment Split</div>', unsafe_allow_html=True)
                    fig_pie = go.Figure(go.Pie(
                        labels=["Positive","Negative","Neutral"],
                        values=[stats["positive"],stats["negative"],stats["neutral"]],
                        hole=0.6,
                        marker=dict(colors=["#4caf50","#ef5350","#e8a030"],
                                    line=dict(color="rgba(0,0,0,0)",width=0)),
                        textfont=dict(family="Outfit", color="#ffffff", size=13),
                        hovertemplate="<b>%{label}</b><br>%{value} reviews (%{percent})<extra></extra>"
                    ))
                    fig_pie.update_layout(**dlayout())
                    st.plotly_chart(fig_pie, use_container_width=True)

                with ch2:
                    st.markdown('<div class="sec-title">Category Breakdown</div>', unsafe_allow_html=True)
                    cc = {c: {"positive":0,"negative":0,"neutral":0} for c in CAT_LABELS}
                    for r in revs:
                        for cat, s in r["categories"].items():
                            if cat in cc: cc[cat][s] += 1
                    cdf = pd.DataFrame(cc).T
                    cdf.index = list(CAT_LABELS.values())
                    fig_bar = go.Figure()
                    for s, col in [("positive","#4caf50"),("negative","#ef5350"),("neutral","#e8a030")]:
                        fig_bar.add_trace(go.Bar(name=s.capitalize(), x=cdf.index, y=cdf[s],
                            marker_color=col, marker_line_width=0))
                    fig_bar.update_layout(barmode="group",
                        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#ffffff")),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#ffffff")),
                        **dlayout())
                    st.plotly_chart(fig_bar, use_container_width=True)

                avg_conf = round(sum(r["confidence"] for r in revs)/len(revs), 1) if revs else 0
                st.markdown(
                    f'<div class="card" style="text-align:center">'
                    f'<div class="card-label">Average Confidence Across All Reviews</div>'
                    f'<div style="font-family:serif;font-size:3rem;font-weight:700;color:#e8a030">{avg_conf}%</div>'
                    f'{conf_bar(avg_conf)}</div>', unsafe_allow_html=True)

                st.markdown('<div class="sec-title">All Reviews</div>', unsafe_allow_html=True)

                if "filt" not in st.session_state:
                    st.session_state["filt"] = "ALL"

                fa, fb, fc, fd, _ = st.columns([0.6,1,1,1,3])
                with fa:
                    if st.button("All", use_container_width=True): st.session_state["filt"] = "ALL"
                with fb:
                    if st.button("✅ Positive", use_container_width=True): st.session_state["filt"] = "POSITIVE"
                with fc:
                    if st.button("❌ Negative", use_container_width=True): st.session_state["filt"] = "NEGATIVE"
                with fd:
                    if st.button("➖ Neutral",  use_container_width=True): st.session_state["filt"] = "NEUTRAL"

                filtered = [r for r in revs if st.session_state["filt"]=="ALL" or r["sentiment"]==st.session_state["filt"]]

                for r in filtered:
                    dot = "🟢" if r["sentiment"]=="POSITIVE" else "🔴" if r["sentiment"]=="NEGATIVE" else "🟡"
                    cats_mini = " · ".join([f"{CAT_ICONS[k]} {v}" for k,v in r["categories"].items()])
                    st.markdown(
                        f'<div class="rev-row">'
                        f'<div class="rev-text">{r["review"]}'
                        f'<div class="rev-cats">{cats_mini}</div></div>'
                        f'<div class="rev-meta">'
                        f'<div style="font-size:1.4rem">{dot}</div>'
                        f'<div style="font-size:0.8rem;color:#ffffff;font-weight:600">{r["sentiment"]}</div>'
                        f'<div style="font-size:0.8rem;color:#e8a030;font-weight:600">{r["confidence"]}%</div>'
                        f'</div></div>', unsafe_allow_html=True)

                if not filtered:
                    st.info(f"No {st.session_state['filt'].lower()} reviews found.")

            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot connect to backend. Run: uvicorn main:app --reload")