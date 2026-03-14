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

# ── Inline Data (no CSV file needed) ──────────────────────────────
@st.cache_data
def load_data():
    import io
    raw = """player,squad,nation,save_pct,clean_sheet_pct,psxg_diff,pass_completion_pct,ucl_save_pct,penalty_save_pct,goals_per_game,matches_played,seasons_played,ucl_matches,composite_score,rank,prog_passes_p90,sweeping_opa_p90,sca_p90,launch_pct,attacking_insight,norm_prog_passes_p90,norm_sweeping_opa_p90,norm_sca_p90,norm_launch_pct,attacking_score
Ederson,Manchester City,BRA,66.7,55.8,1.9,89.5,70.4,37.5,0.88,156,5,58,66.5,9,5.8,1.6,0.18,22.0,The Playmaker. His passing is a primary attacking weapon for Man City.,100.0,70.6,100.0,100.0,90
Manuel Neuer,Bayern Munich,GER,70.6,42.9,1.1,83.5,76.1,28.6,1.03,133,5,38,56.9,10,5.5,2.1,0.14,27.0,The Blueprint. Defined the modern Sweeper-Keeper role.,90.9,100.0,71.4,88.4,91
Alisson Becker,Liverpool,BRA,69.5,42.6,-1.0,84.6,71.2,36.4,1.06,155,5,32,43.8,13,4.9,1.8,0.15,24.0,The Complete Keeper. Balanced excellence in distribution and sweeping.,72.7,82.4,78.6,95.3,80
André Onana,Manchester United,CMR,70.6,33.8,1.4,81.5,73.4,40.0,1.12,154,5,22,52.5,11,4.8,1.1,0.11,30.0,"Line-breaker. High-risk, high-reward distribution that creates overloads.",69.7,41.2,50.0,81.4,59
Marc-André ter Stegen,Barcelona,GER,73.9,49.5,2.8,85.8,70.2,16.7,1.05,111,5,24,73.5,5,4.7,1.4,0.13,25.0,The 11th outfielder. Elite passing range and high-line sweeping.,66.7,58.8,64.3,93.0,68
Mike Maignan,AC Milan,FRA,77.9,48.4,3.5,79.0,75.0,30.0,0.84,159,5,22,88.0,1,4.3,1.3,0.12,31.0,Direct and clinical. Rapid distribution bypasses defensive blocks.,54.5,52.9,57.1,79.1,58
Unai Simón,Athletic Club,ESP,70.9,29.3,3.1,73.8,0.0,58.3,1.18,174,5,0,48.5,12,3.9,1.2,0.08,46.0,Proactive. High sweeping volume and reliable short-to-medium passing.,42.4,47.1,28.6,44.2,42
Yann Sommer,Inter Milan,SUI,72.9,39.8,2.7,79.6,71.6,57.1,1.11,123,4,26,67.8,8,3.8,0.8,0.09,33.0,"Technical. Small but agile, excels in short-passing under pressure.",39.4,23.5,35.7,74.4,39
Gregor Kobel,Borussia Dortmund,SUI,72.6,43.4,2.4,77.5,76.6,28.6,0.91,136,5,29,68.2,7,3.3,1.0,0.07,35.0,Modern & Bold. High involvement in Dortmund's initial build-up phase.,24.2,35.3,21.4,69.8,35
Thibaut Courtois,Real Madrid,BEL,75.0,53.8,2.1,79.5,77.6,40.0,0.82,143,5,41,80.5,3,3.5,0.9,0.08,45.0,Calculated. Uses his height to dominate crosses and starts safe build-ups.,30.3,29.4,28.6,46.5,32
Kevin Trapp,Eintracht Frankfurt,GER,66.4,30.4,2.5,75.1,0.0,50.0,1.27,148,5,0,36.1,14,3.2,1.1,0.07,55.0,Strategic. Reliable distributor who organizes the defense well.,21.2,41.2,21.4,23.3,29
Gianluigi Donnarumma,PSG,ITA,73.5,49.7,3.7,71.1,72.5,37.5,0.99,169,5,34,77.5,4,3.1,0.8,0.06,38.0,Strong presence. Improving in distribution but excels in space coverage.,18.2,23.5,14.3,62.8,26
Wojciech Szczęsny,Juventus,POL,73.3,41.4,2.7,72.7,70.1,40.0,0.93,157,5,14,68.7,6,3.1,0.7,0.05,40.0,Pragmatic. Focused on quick recycling to midfielders.,18.2,17.6,7.1,58.1,22
Hugo Lloris,Tottenham,FRA,63.2,30.7,2.4,75.8,0.0,45.5,1.60,127,4,0,23.5,16,2.7,0.6,0.06,58.0,"Agile. Great shot-stopper with a focus on quick, safe distribution.",6.1,11.8,14.3,16.3,11
Jan Oblak,Atletico Madrid,SVN,77.3,45.6,3.6,74.1,74.0,25.0,0.87,169,5,38,83.4,2,2.8,0.4,0.05,65.0,Traditionalist. Focused on safe retention and pure shot-stopping.,9.1,0.0,7.1,0.0,4
David de Gea,Manchester United,ESP,68.5,33.3,0.9,73.4,0.0,43.8,1.28,150,4,0,31.2,15,2.5,0.5,0.04,60.0,"Traditional. World-class reflexes but prefers safe, long launches.",0.0,5.9,0.0,11.6,4"""
    return pd.read_csv(io.StringIO(raw))

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

