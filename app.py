import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="The First Attacker | Tactical GK Analysis",
    page_icon="🎯",
    layout="wide",
)

# ── Themes & Styles ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
.stApp { background: linear-gradient(135deg, #09090b 0%, #18181b 100%); }
h1, h2, h3 { color: #f4f4f5 !important; }
.gk-card {
    background: linear-gradient(135deg, #18181b 0%, #27272a 100%);
    border: 1px solid #3f3f46;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 8px 32px rgba(239, 68, 68, 0.1);
}
.insight-box {
    background: rgba(239, 68, 68, 0.1);
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 16px;
    color: #fca5a5;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = Path(__file__).parent
    csv_path = base_dir / "data" / "first_attacker_stats.csv"
    return pd.read_csv(csv_path)

df = load_data()
df = df.sort_values("attacking_score", ascending=False).reset_index(drop=True)

# ── Sidebar ──────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center; padding: 20px 0 10px;">
    <div style="font-size: 3rem;">🎯</div>
    <div style="font-size: 1.4rem; font-weight: 800; color: #ef4444;">THE FIRST ATTACKER</div>
</div>
<hr style="border-color:#3f3f46; margin:0 0 12px;">
""", unsafe_allow_html=True)

nav = st.sidebar.radio("Navigation", ["🏠 Home", "🔥 Rankings", "🧠 Profiles", "🔭 Tactical Matrix", "📖 Fan Guide"])

# ── Analyst Profile ───────────────────────────────────────────────
st.sidebar.markdown("""
<hr style="border-color:#3f3f46; margin:12px 0;">
<div style="text-align:center; padding-bottom:16px;">
    <div style="font-size:3rem; margin-bottom:6px;">⚽</div>
    <div style="font-size:1.2rem; font-weight:800; color:#f4f4f5;">Kareem Elshafey</div>
    <div style="font-size:0.9rem; color:#ef4444; font-weight:600;">Football Analyst</div>
    <div style="font-size:0.8rem; color:#71717a; margin-top:4px;">📱 +20 112 797 3132</div>
</div>
""", unsafe_allow_html=True)

# ── Home Page (Why this matters?) ──────────────────────────────────
if nav == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>🎯 The First Attacker Project</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("""
        <div class="gk-card">
            <h3>❓ Why does this data matter?</h3>
            <p style="color:#a1a1aa; font-size:1.1rem;">
                In modern football, a goalkeeper isn't just a "shot-stopper"—they are the <b>first attacker</b>. 
                This dashboard answers one crucial question for coaches & fans:
            </p>
            <div style="background:rgba(239, 68, 68, 0.1); border-radius:8px; padding:20px; border:1px solid #ef4444; margin:15px 0;">
                <h2 style="color:#ef4444; margin-bottom:10px;">The Core Question:</h2>
                <i style="font-size:1.3rem; color:#f4f4f5;">"Which goalkeeper helps my team build an attack and score goals the fastest?"</i>
            </div>
            <p style="color:#d4d4d8;">
                By looking at data beyond just saves, we identify the playmakers who break lines and create scoring chances from their own box.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="gk-card">
            <h3>💡 For the Coach</h3>
            <p style="color:#a1a1aa;">Inspire your team by picking keepers who:</p>
            <ul style="color:#d4d4d8;">
                <li>Cover the space behind your high line.</li>
                <li>Turn defense into attack in 2 seconds.</li>
                <li>Act as an extra midfielder in possession.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ── Rankings Page ─────────────────────────────────────────────────
elif nav == "🔥 Rankings":
    st.markdown("<h1 style='text-align:center;'>🔥 Tactical Playmakers Rankings</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:rgba(24, 24, 27, 0.6); padding:15px; border-radius:10px; border:1px solid #3f3f46; margin-bottom:25px; text-align:center;">
        <b style="color:#ef4444;">Simple Tip:</b> The <b>Tactical Score</b> tells you how much a keeper helps his team <i>start attacks</i>. High score = High impact.
    </div>
    """, unsafe_allow_html=True)

    top3 = df.head(3)
    cols = st.columns(3)
    for i, row in top3.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div class="gk-card" style="text-align:center;">
                <div style="font-size:1.2rem; color:#ef4444; font-weight:800;">#{i+1}</div>
                <div style="font-size:1.8rem; font-weight:800; color:#f4f4f5;">{row['player']}</div>
                <div style="font-size:1.1rem; color:#a1a1aa; margin-bottom:16px;">{row['squad']}</div>
                <div style="font-size:3.5rem; font-weight:900; color:#ef4444; line-height:1;">{int(row['attacking_score'])}</div>
                <div style="font-size:0.8rem; color:#71717a; text-transform:uppercase;">Tactical Score</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("### Full Comparison Table")
    # Formatting for display
    display_df = df[["player", "squad", "attacking_score", "prog_passes_p90", "sweeping_opa_p90", "launch_pct"]].copy()
    display_df["attacking_score"] = display_df["attacking_score"].astype(int)
    st.dataframe(display_df.style.background_gradient(cmap="Reds"), use_container_width=True)

# ── Profiles Page ─────────────────────────────────────────────────
elif nav == "🧠 Profiles":
    st.markdown("<h1>🧠 Tactical Scouting Reports</h1>", unsafe_allow_html=True)
    selected = st.selectbox("Select Player", df["player"].tolist())
    row = df[df["player"] == selected].iloc[0]
    
    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        st.markdown(f"""
        <div class="gk-card">
            <h2 style="margin-bottom:0;">{row['player']}</h2>
            <div style="color:#ef4444; font-weight:700;">{row['squad']}</div>
            <div class="insight-box" style="margin:20px 0;">
                <b style="color:#fff;">Coach's View:</b><br>{row['attacking_insight']}
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:8px;">
                <b style="color:#60a5fa;">🙋 Fan Explanation:</b><br>
                <span style="font-size:0.9rem; color:#d1d5db;">
                    Imagine watching <b>{row['player']}</b> play — every 90 minutes, he makes <b>{row['prog_passes_p90']}</b> passes that pierce the opponent's defense and start attacks. 
                    He also rushes out of his goal <b>{row['sweeping_opa_p90']}</b> times per game to stop danger before it even reaches the box!
                    His style? {'Short, sharp passes — like a midfielder in gloves 🧤' if row['launch_pct'] < 35 else 'A mix of smart short builds and well-timed long balls ⚡' if row['launch_pct'] < 50 else 'Direct and fast — clear the danger and restart quickly 🚀'}
                </span>
            </div>
            <div style="margin-top:16px; display:flex; gap:10px; flex-wrap:wrap;">
                <div style="background:rgba(239,68,68,0.1); border:1px solid #ef4444; border-radius:8px; padding:10px 14px; flex:1;">
                    <div style="font-size:1.6rem; font-weight:900; color:#ef4444;">{int(row['attacking_score'])}</div>
                    <div style="font-size:0.7rem; color:#a1a1aa; text-transform:uppercase;">Tactical Score</div>
                </div>
                <div style="background:rgba(96,165,250,0.1); border:1px solid #3b82f6; border-radius:8px; padding:10px 14px; flex:1;">
                    <div style="font-size:1.6rem; font-weight:900; color:#60a5fa;">{int(row['launch_pct'])}%</div>
                    <div style="font-size:0.7rem; color:#a1a1aa; text-transform:uppercase;">Launch Rate</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_r:
        # Mini Radar
        metrics = ["norm_prog_passes_p90", "norm_sca_p90", "norm_sweeping_opa_p90", "norm_launch_pct", "pass_completion_pct"]
        labels = ["Prog Passing", "Shot Creation", "Sweeping", "Short Build-up", "Accuracy %"]
        vals = [row[m] for m in metrics]
        vals.append(vals[0])
        
        fig = go.Figure(go.Scatterpolar(r=vals, theta=labels + [labels[0]], fill="toself", line=dict(color="#ef4444", width=3), fillcolor="rgba(239, 68, 68, 0.2)"))
        fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0,100], gridcolor="#3f3f46")), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#d4d4d8"), margin=dict(t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)

# ── Matrix Page (Optimized for Fans) ─────────────────────────────
elif nav == "🔭 Tactical Matrix":
    st.markdown("<h1>🔭 The Tactical Playmaker Matrix</h1>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background:rgba(239, 68, 68, 0.05); padding:15px; border-radius:10px; border:1px solid #ef4444; margin-bottom:20px;">
            <h4 style="color:#fca5a5; margin:0;">How to use this chart?</h4>
            <p style="color:#d1d5db; margin:5px 0 0 0;">
                Look at the <b>Top-Right</b> corner. These are the "Monsters" of modern football. They pass forward perfectly AND they sweep the floor outside their box!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    fig = px.scatter(df, x="prog_passes_p90", y="sweeping_opa_p90", color="attacking_score", size="pass_completion_pct", text="player", color_continuous_scale="Reds", labels={"prog_passes_p90": "Forward Passing Impact ➡️", "sweeping_opa_p90": "Space Coverage (Sweeping) ⬆️"})
    fig.update_traces(textposition="top center")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(24, 24, 27, 0.5)", font=dict(color="#a1a1aa"))
    st.plotly_chart(fig, use_container_width=True)

# ── Fan Guide (The Dictionary) ────────────────────────────────────
elif nav == "📖 Fan Guide":
    st.markdown("<h1>📖 Tactical Guide for Fans</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#a1a1aa;'>We translated the complicated data into easy football language!</p>", unsafe_allow_html=True)
    
    guides = [
        ("➡️ Progressive Passes", "Instead of passing sideways, these are passes that break the opponent's lines and move your team into a scoring position."),
        ("⬆️ Sweeping Actions", "Think of Manuel Neuer! This is when the keeper leaves his goal line to clear the ball or tackle an attacker far away from the net."),
        ("🎯 Shot-Creating Actions (SCA)", "When the goalkeeper's pass or action leads directly to a teammate taking a shot on goal."),
        ("📉 Launch %", "How often the keeper just kicks it long. A <b>lower</b> percentage means they are brave and prefer building slowly with clever short passes."),
        ("🌟 Tactical Score", "A balanced grade (0-100) that shows how much the keeper helps the team attack and stay dominant.")
    ]
    
    for title, desc in guides:
        st.markdown(f"""
        <div class="gk-card" style="padding:15px; border-left: 4px solid #ef4444; text-align:left;">
            <h4 style="color:#ef4444; margin-bottom:5px;">{title}</h4>
            <p style="color:#d4d4d8; margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

