import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from nps_analyzer import NPSAnalyzer
from data_generator import generate_nps_data

st.set_page_config(page_title="NPS Intelligence Dashboard", page_icon="💬", layout="wide")

st.title("💬 NPS Intelligence Dashboard")
st.markdown("**AI-Powered Customer Loyalty Analysis** — Beyond the score: themes, churn risk, and PM action plans.")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configuration")
n_clusters = st.sidebar.slider("NLP theme clusters per segment", 2, 6, 3)
n_responses = st.sidebar.slider("Synthetic responses to generate", 100, 500, 250, step=50)
show_trend = st.sidebar.checkbox("Show NPS trend over time", value=True)

# Load data
nps_df = generate_nps_data(n=n_responses)
analyzer = NPSAnalyzer(n_clusters=n_clusters)

# Section 1: NPS Score Overview
st.header("📊 NPS Score Overview")

promoters = len(nps_df[nps_df["score"] >= 9])
passives = len(nps_df[(nps_df["score"] >= 7) & (nps_df["score"] < 9)])
detractors = len(nps_df[nps_df["score"] < 7])
total = len(nps_df)
nps_score = round((promoters - detractors) / total * 100)

col1, col2, col3, col4 = st.columns(4)
col1.metric("NPS Score", nps_score, delta="Industry median: ~30")
col2.metric("Promoters (9-10)", f"{promoters} ({promoters/total*100:.0f}%)", delta=None)
col3.metric("Passives (7-8)", f"{passives} ({passives/total*100:.0f}%)", delta=None)
col4.metric("Detractors (0-6)", f"{detractors} ({detractors/total*100:.0f}%)", delta=None)

# NPS gauge
fig_gauge = go.Figure(go.Indicator(
      mode="gauge+number+delta",
      value=nps_score,
      domain={"x": [0, 1], "y": [0, 1]},
      title={"text": "NPS Score"},
      delta={"reference": 30, "relative": False},
      gauge={
                "axis": {"range": [-100, 100]},
                "bar": {"color": "steelblue"},
                "steps": [
                              {"range": [-100, 0], "color": "#ffcccc"},
                              {"range": [0, 30], "color": "#fff3cd"},
                              {"range": [30, 70], "color": "#d4edda"},
                              {"range": [70, 100], "color": "#c3e6cb"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 30}
      }
))
fig_gauge.update_layout(height=300)

col_gauge, col_dist = st.columns(2)
with col_gauge:
      st.plotly_chart(fig_gauge, use_container_width=True)
  with col_dist:
        dist_data = pd.DataFrame({"Segment": ["Detractors", "Passives", "Promoters"],
                                                                 "Count": [detractors, passives, promoters],
                                                                 "Color": ["#dc3545", "#ffc107", "#28a745"]})
        fig_dist = px.bar(dist_data, x="Segment", y="Count", color="Segment",
                          color_discrete_map={"Detractors": "#dc3545", "Passives": "#ffc107", "Promoters": "#28a745"},
                          title="Response Distribution")
        st.plotly_chart(fig_dist, use_container_width=True)

# Section 2: Trend
if show_trend:
      st.markdown("---")
      st.header("📈 NPS Trend")
      trend_df = nps_df.groupby("date").apply(
          lambda g: (len(g[g["score"] >= 9]) - len(g[g["score"] < 7])) / len(g) * 100
      ).reset_index()
      trend_df.columns = ["date", "nps"]
      trend_df["rolling_nps"] = trend_df["nps"].rolling(7, min_periods=1).mean()
      fig_trend = go.Figure()
      fig_trend.add_scatter(x=trend_df["date"], y=trend_df["nps"], name="Daily NPS", opacity=0.4, mode="lines")
      fig_trend.add_scatter(x=trend_df["date"], y=trend_df["rolling_nps"], name="7-day Rolling Avg",
                            line=dict(color="steelblue", width=2))
      fig_trend.add_hline(y=30, line_dash="dash", line_color="gray", annotation_text="Industry Median (30)")
      fig_trend.update_layout(title="NPS Over Time", yaxis_title="NPS Score", height=300)
      st.plotly_chart(fig_trend, use_container_width=True)

# Section 3: Verbatim Theme Analysis
st.markdown("---")
st.header("🧠 Verbatim Theme Analysis (NLP)")

tab_det, tab_pass, tab_pro = st.tabs(["🔴 Detractors", "🟡 Passives", "🟢 Promoters"])

for tab, segment in [(tab_det, "detractor"), (tab_pass, "passive"), (tab_pro, "promoter")]:
      with tab:
                seg_df = nps_df[nps_df["segment"] == segment]
                if len(seg_df) < 5:
                              st.info("Not enough responses for this segment.")
                              continue

                themes = analyzer.extract_themes(seg_df["verbatim"].tolist())
                st.write(f"**{len(seg_df)} responses analyzed | {len(themes)} themes detected**")

          for theme in themes:
                        sentiment_icon = "😡" if theme["avg_sentiment"] < -0.3 else "😐" if theme["avg_sentiment"] < 0.3 else "😊"
                        with st.expander(f"{sentiment_icon} **{theme['label']}** — {theme['pct']:.0f}% of segment | Sentiment: {theme['avg_sentiment']:.2f}"):
                                          st.markdown(f"**Key quote:** *\"{theme['key_quote']}\"*")
                                          st.markdown(f"**Top words:** {', '.join(theme['top_words'])}")
                                          if segment == "detractor":
                                                                st.warning(f"**PM Action:** This theme affects {theme['pct']:.0f}% of detractors. Address to convert detractors to passives.")
elif segment == "passive":
                    st.info(f"**PM Action:** Resolve this barrier to convert passives to promoters.")
else:
                    st.success(f"**PM Action:** Amplify this strength in marketing and product narrative.")

# Section 4: Churn Risk for Passives
st.markdown("---")
st.header("🔮 Passive Churn Risk Prediction")
passives_df = nps_df[nps_df["segment"] == "passive"].copy()

if len(passives_df) > 5:
      churn_risk = analyzer.predict_passive_churn_risk(passives_df)
      passives_df["churn_risk"] = churn_risk

    high_risk = passives_df[passives_df["churn_risk"] > 0.6]
    upgrade_potential = passives_df[passives_df["churn_risk"] < 0.35]

    c1, c2 = st.columns(2)
    c1.metric("🚨 High Churn Risk Passives", len(high_risk),
                            delta=f"{len(high_risk)/len(passives_df)*100:.0f}% of passives")
    c2.metric("📈 Upgrade Potential Passives", len(upgrade_potential),
                            delta=f"{len(upgrade_potential)/len(passives_df)*100:.0f}% of passives")

    fig_risk = px.histogram(passives_df, x="churn_risk", nbins=20,
                                                        title="Churn Risk Distribution for Passives",
                                                        labels={"churn_risk": "Churn Risk Score (0=low, 1=high)"},
                                                        color_discrete_sequence=["#ffc107"])
    fig_risk.add_vline(x=0.6, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
    st.plotly_chart(fig_risk, use_container_width=True)

st.caption("NPS Intelligence Dashboard | [GitHub](https://github.com/Poojaahegde/nps-intelligence-dashboard)")
