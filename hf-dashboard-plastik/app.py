import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="3P",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# COLORS
# =========================
CREAM = "#F5EEDF"
BLACK = "#111111"
TEXT = "#171717"
MUTED = "#6B6258"
PINK = "#F4A7C8"
YELLOW = "#F6D85B"
GREEN = "#A7B86D"
BLUE = "#A9C3E8"
PURPLE = "#C8A2D8"
CARD = "#FFF8EA"
BORDER = "#2B2B2B"

# =========================
# INTERNAL PAGE NAVIGATION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

page = st.session_state.page

# =========================
# CSS
# =========================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didact+Gothic&family=Montserrat:wght@400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        background: {CREAM};
        color: {TEXT};
        font-family: 'Didact Gothic', sans-serif;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        padding-top: 1.4rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1420px;
    }}

    [data-testid="stSidebar"] {{
        background: {BLACK};
        border-right: 2px solid {BORDER};
    }}

    [data-testid="stSidebar"] * {{
        color: #F8F5EC;
    }}

    .sidebar-brand {{
        margin-top: 34px;
        margin-bottom: 34px;
    }}

    .brand-name {{
        font-family: 'Montserrat', sans-serif;
        font-size: 27px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #F8F5EC;
    }}

    .brand-subtitle {{
        font-family: 'Didact Gothic', sans-serif;
        font-size: 11px;
        font-weight: 400;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(248,245,236,0.58);
        margin-top: 8px;
    }}

    .side-group {{
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(248,245,236,0.45);
        margin-top: 24px;
        margin-bottom: 10px;
    }}

    .side-info-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        color: rgba(248,245,236,0.48);
        margin-top: 26px;
        margin-bottom: 10px;
    }}

    .side-info-box {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 14px;
        font-family: 'Didact Gothic', sans-serif;
        font-size: 14px;
        line-height: 1.7;
        color: rgba(248,245,236,0.72);
    }}

    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        background: transparent;
        border: none;
        border-radius: 14px;
        padding: 13px 16px;
        text-align: left;
        justify-content: flex-start;
        color: rgba(248,245,236,0.82);
        font-family: 'Didact Gothic', sans-serif;
        font-size: 16px;
        font-weight: 400;
    }}

    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(255,255,255,0.10);
        color: #FFFFFF;
        border: none;
    }}

    [data-testid="stSidebar"] .stButton > button:focus {{
        box-shadow: none;
        border: none;
    }}

    [data-testid="stSidebar"] .stButton > button:active {{
        background: rgba(255,255,255,0.13);
        color: #FFFFFF;
        border: none;
    }}

    .top-outline {{
        width: 100%;
        height: 58px;
        border: 3px solid {BORDER};
        border-radius: 999px;
        margin-bottom: 24px;
    }}

    .hero-date {{
        display: inline-flex;
        background: {PINK};
        border-radius: 999px;
        padding: 8px 17px;
        font-family: 'Didact Gothic', sans-serif;
        font-size: 13px;
        font-weight: 400;
        margin-bottom: 18px;
        color: {TEXT};
    }}

    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 48px;
        line-height: 1.08;
        letter-spacing: -0.8px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 18px;
    }}

    .hero-subtitle {{
    font-family: 'Didact Gothic', sans-serif;
    color: {MUTED};
    font-size: 16px;
    line-height: 1.72;
    max-width: 880px;
    text-align: justify;
    text-justify: inter-word;
}}

    .calendar-card {{
        background: {CARD};
        border-radius: 28px;
        padding: 26px;
        border: 1.5px solid rgba(0,0,0,0.08);
        min-height: 330px;
    }}

    .calendar-month {{
        display: inline-block;
        background: {PINK};
        padding: 10px 22px;
        border-radius: 999px;
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 20px;
    }}

    .calendar-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 8px;
        margin-bottom: 22px;
        font-size: 12px;
        text-align: center;
    }}

    .calendar-day-name {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        color: {MUTED};
        font-size: 11px;
    }}

    .calendar-day {{
        padding: 8px 0;
        border-radius: 999px;
        color: {TEXT};
        font-family: 'Didact Gothic', sans-serif;
        font-weight: 400;
    }}

    .calendar-active {{
        background: {PINK};
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
    }}

    .calendar-summary {{
        border-top: 1px solid rgba(0,0,0,0.08);
        padding-top: 14px;
    }}

    .summary-item {{
        display: flex;
        justify-content: space-between;
        gap: 18px;
        padding: 9px 0;
        font-size: 13px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }}

    .summary-label {{
        color: {MUTED};
        font-family: 'Didact Gothic', sans-serif;
        font-weight: 400;
    }}

    .summary-value {{
        color: {TEXT};
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        text-align: right;
    }}

    .section-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 30px;
        font-weight: 700;
        letter-spacing: -0.4px;
        margin-top: 30px;
        margin-bottom: 4px;
        color: {TEXT};
    }}

    .section-subtitle {{
        font-family: 'Didact Gothic', sans-serif;
        color: {MUTED};
        font-size: 15px;
        margin-bottom: 18px;
    }}

    .metric-card {{
        border-radius: 24px;
        padding: 26px;
        min-height: 166px;
        border: 1.5px solid rgba(0,0,0,0.07);
        position: relative;
        overflow: hidden;
        margin-bottom: 16px;
    }}

    .metric-card:after {{
        content: "";
        width: 120px;
        height: 120px;
        position: absolute;
        bottom: -35px;
        right: -35px;
        background: rgba(0,0,0,0.06);
        border-radius: 999px;
    }}

    .yellow {{ background: {YELLOW}; }}
    .pink {{ background: {PINK}; }}
    .blue {{ background: {BLUE}; }}
    .green {{ background: {GREEN}; }}
    .purple {{ background: {PURPLE}; }}

    .metric-label {{
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: rgba(0,0,0,0.62);
        margin-bottom: 14px;
    }}

    .metric-value {{
        font-family: 'Montserrat', sans-serif;
        font-size: 38px;
        font-weight: 700;
        letter-spacing: -0.4px;
        color: {TEXT};
        line-height: 1.08;
    }}

    .metric-note {{
        font-family: 'Didact Gothic', sans-serif;
        font-size: 14px;
        color: rgba(0,0,0,0.56);
        margin-top: 10px;
    }}

    .metric-badge {{
        display: inline-block;
        margin-top: 12px;
        border-radius: 999px;
        padding: 5px 12px;
        background: rgba(0,0,0,0.10);
        font-family: 'Didact Gothic', sans-serif;
        font-size: 12px;
        font-weight: 400;
    }}

    .chart-title-pill {{
        display: inline-block;
        background: #FFF8EA;
        border: 1.5px solid rgba(0,0,0,0.08);
        border-radius: 999px;
        padding: 10px 22px;
        margin: 22px 0 10px 0;
        font-family: 'Montserrat', sans-serif;
        font-size: 15px;
        font-weight: 600;
        color: #171717;
    }}

    div[data-testid="stTabs"] button {{
        color: #171717 !important;
        font-family: 'Didact Gothic', sans-serif !important;
        font-weight: 400 !important;
        font-size: 16px !important;
    }}

    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: #111111 !important;
        border-bottom-color: #111111 !important;
        font-weight: 600 !important;
    }}

    [data-testid="stDataFrame"] {{
        background-color: #111111 !important;
        border-radius: 18px;
        overflow: hidden;
        border: 1.5px solid #111111;
    }}

    .insight-box {{
        background: {BLACK};
        color: #F8F5EC;
        border-radius: 26px;
        padding: 28px 32px;
        margin-top: 22px;
        margin-bottom: 20px;
    }}

    .insight-box h3 {{
        font-family: 'Montserrat', sans-serif;
        color: {YELLOW};
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .insight-box p {{
        font-family: 'Didact Gothic', sans-serif;
        color: rgba(248,245,236,0.82);
        line-height: 1.75;
        font-size: 15px;
        font-weight: 400;
    }}

    .insight-tag {{
        display: inline-block;
        background: rgba(255,255,255,0.10);
        padding: 6px 13px;
        border-radius: 999px;
        font-family: 'Didact Gothic', sans-serif;
        font-size: 12px;
        font-weight: 400;
        margin-right: 6px;
        margin-top: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("plastic_prices.csv")
    pred = pd.read_csv("plastic_price_predictions.csv")

    df["date"] = pd.to_datetime(df["date"])
    pred["prediction_date"] = pd.to_datetime(pred["prediction_date"])

    df = df.sort_values("date")
    pred = pred.sort_values("prediction_date")

    return df, pred


df, pred = load_data()

# =========================
# SIDEBAR NAVIGATION
# =========================
def nav_button(label, target):
    if st.button(label, use_container_width=True, key=f"nav_{target}"):
        st.session_state.page = target
        st.rerun()


with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="brand-name">3<span style="color:{YELLOW};">P</span></div>
            <div class="brand-subtitle">Predict Plastic Price</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-group">General</div>', unsafe_allow_html=True)

    nav_button("▦  Dashboard", "dashboard")
    nav_button("📈  Market Trends", "trends")
    nav_button("🔗  Correlation", "correlation")
    nav_button("🔮  Forecast", "forecast")

    st.markdown('<div class="side-group">Tools</div>', unsafe_allow_html=True)

    nav_button("🗄️  Data Source", "source")

    st.markdown(
        """
        <div class="side-info-title">Plastic Types</div>
        <div class="side-info-box">
            Jenis plastik yang masuk dalam analisis ini:<br>
            <b>HDPE</b>, <b>LDPE</b>, <b>PP</b>, <b>PET</b>, dan <b>PVC</b>.<br><br>
            Data utama dashboard direpresentasikan sebagai indeks/harga plastik gabungan.
        </div>

        <div class="side-info-title">Pipeline</div>
        <div class="side-info-box">
            🟢 Airflow Pipeline<br>
            🟢 PostgreSQL<br>
            🟡 Streamlit Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# DATA PREP
# =========================
filtered_df = df.copy()

latest = filtered_df.iloc[-1]
latest_date = latest["date"].strftime("%d %B %Y")

data_min = df["date"].min()
data_max = df["date"].max()

corr_oil = filtered_df[["plastic_price", "oil_price"]].corr().iloc[0, 1]
corr_usd = filtered_df[["plastic_price", "usd_idr"]].corr().iloc[0, 1]
corr_oil = 0 if pd.isna(corr_oil) else float(corr_oil)
corr_usd = 0 if pd.isna(corr_usd) else float(corr_usd)

pred_start = float(pred["predicted_price"].iloc[0])
pred_end = float(pred["predicted_price"].iloc[-1])
pred_change_pct = ((pred_end - pred_start) / pred_start * 100) if pred_start else 0

trend_direction = (
    "meningkat 📈"
    if pred_end > pred_start
    else "menurun 📉"
    if pred_end < pred_start
    else "stabil ➡️"
)

corr_oil_strength = (
    "Sangat kuat"
    if abs(corr_oil) > 0.8
    else "Kuat"
    if abs(corr_oil) > 0.6
    else "Moderat"
    if abs(corr_oil) > 0.4
    else "Lemah"
)

corr_usd_strength = (
    "Sangat kuat"
    if abs(corr_usd) > 0.8
    else "Kuat"
    if abs(corr_usd) > 0.6
    else "Moderat"
    if abs(corr_usd) > 0.4
    else "Lemah"
)

# =========================
# HELPERS
# =========================
plastic_start = float(filtered_df["plastic_price"].iloc[0])
plastic_end = float(filtered_df["plastic_price"].iloc[-1])
plastic_change = plastic_end - plastic_start
plastic_change_pct = (plastic_change / plastic_start * 100) if plastic_start else 0

oil_start = float(filtered_df["oil_price"].iloc[0])
oil_end = float(filtered_df["oil_price"].iloc[-1])
oil_change = oil_end - oil_start
oil_change_pct = (oil_change / oil_start * 100) if oil_start else 0

usd_start = float(filtered_df["usd_idr"].iloc[0])
usd_end = float(filtered_df["usd_idr"].iloc[-1])
usd_change = usd_end - usd_start
usd_change_pct = (usd_change / usd_start * 100) if usd_start else 0

plastic_trend_text = (
    "meningkat" if plastic_change > 0
    else "menurun" if plastic_change < 0
    else "stabil"
)

oil_trend_text = (
    "meningkat" if oil_change > 0
    else "menurun" if oil_change < 0
    else "stabil"
)

usd_trend_text = (
    "menguat terhadap rupiah" if usd_change > 0
    else "melemah terhadap rupiah" if usd_change < 0
    else "stabil"
)

dominant_external_factor = (
    "harga minyak"
    if abs(corr_oil) >= abs(corr_usd)
    else "nilai tukar USD/IDR"
)

def metric_card(label, value, note, badge, color_class):
    st.markdown(
        f"""
        <div class="metric-card {color_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
            <div class="metric-badge">{badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def line_chart(data, x, y, title, color, height=340):
    fig = px.line(data, x=x, y=y, markers=True, title=title)
    fig.update_traces(
        line=dict(color=color, width=2.8),
        marker=dict(size=6, color=color, line=dict(color="white", width=1)),
    )
    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT, family="Didact Gothic"),
        title=dict(font=dict(size=16, family="Montserrat", color=TEXT), x=0.01),
        xaxis=dict(title="", gridcolor="rgba(0,0,0,0.06)"),
        yaxis=dict(title="", gridcolor="rgba(0,0,0,0.06)"),
        margin=dict(l=15, r=15, t=55, b=15),
        height=height,
        hovermode="x unified",
    )
    return fig


def scatter_chart(data, x, y, title, color):
    fig = px.scatter(data, x=x, y=y, trendline="ols", title=title)
    fig.update_traces(
        marker=dict(size=7, color=color, opacity=0.78, line=dict(color="white", width=0.8))
    )
    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT, family="Didact Gothic"),
        title=dict(font=dict(size=16, family="Montserrat", color=TEXT), x=0.01),
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        margin=dict(l=15, r=15, t=55, b=15),
        height=350,
    )
    return fig


def chart_card(title, fig, key=None):
    st.markdown(
        f'<div class="chart-title-pill">{title}</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, use_container_width=True, key=key)


def dark_table_style(styler):
    return styler.set_table_styles(
        [
            {
                "selector": "thead th",
                "props": [
                    ("background-color", "#111111"),
                    ("color", "#F8F5EC"),
                    ("font-weight", "700"),
                    ("border-color", "#2B2B2B"),
                    ("font-family", "Montserrat"),
                ],
            },
            {
                "selector": "tbody td",
                "props": [
                    ("background-color", "#111111"),
                    ("color", "#F8F5EC"),
                    ("border-color", "#2B2B2B"),
                    ("font-family", "Didact Gothic"),
                    ("font-weight", "400"),
                ],
            },
            {
                "selector": "tbody tr:nth-child(even) td",
                "props": [
                    ("background-color", "#1A1A1A"),
                    ("color", "#F8F5EC"),
                ],
            },
        ]
    )


def calendar_panel():
    latest_day = int(latest["date"].day)

    days = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
    day_numbers = list(range(1, 29))

    html = f"""
    <div class="calendar-card">
        <div class="calendar-month">{latest["date"].strftime("%B %Y")}</div>
        <div class="calendar-grid">
    """

    for d in days:
        html += f'<div class="calendar-day-name">{d}</div>'

    for d in day_numbers:
        active = "calendar-active" if d == latest_day else ""
        html += f'<div class="calendar-day {active}">{d}</div>'

    html += f"""
        </div>
        <div class="calendar-summary">
            <div class="summary-item">
                <span class="summary-label">Data range</span>
                <span class="summary-value">{data_min.strftime("%d %b %Y")} → {data_max.strftime("%d %b %Y")}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Forecast</span>
                <span class="summary-value">30 days ahead</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Last updated</span>
                <span class="summary-value">{latest_date}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Records</span>
                <span class="summary-value">{len(filtered_df):,} rows</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# =========================
# DASHBOARD HEADER
# =========================
if page == "dashboard":
    st.markdown('<div class="top-outline"></div>', unsafe_allow_html=True)

    hleft, hright = st.columns([2.2, 1.0], gap="large")

    with hleft:
        st.markdown(
            f"""
            <div class="hero-date">📅 {latest_date}</div>
            <div class="hero-title">Welcome!<br>Plastic Market Analyst 👋</div>
            <div class="hero-subtitle">
                Dashboard ini dirancang untuk memantau dinamika harga plastik, khususnya polyethylene, dengan mengintegrasikan berbagai faktor global yang memengaruhinya, seperti harga minyak mentah dan nilai tukar USD/IDR. Karena plastik merupakan produk turunan minyak bumi, perubahan harga minyak dapat berdampak langsung terhadap biaya produksi dan pergerakan harga plastik di pasar.
                Melalui sistem Big Data Pipeline end-to-end, data dari berbagai sumber dikumpulkan, diproses, dan dimuat secara otomatis melalui tahapan ETL. Dashboard ini tidak hanya menampilkan tren historis harga plastik, harga minyak, dan nilai tukar, tetapi juga menyajikan analisis korelasi antarvariabel serta prediksi harga plastik untuk 30 hari ke depan menggunakan model machine learning.
                Dengan adanya dashboard ini, pengguna dapat memperoleh insight yang lebih terintegrasi, informatif, dan berbasis data dalam memahami perubahan harga plastik serta faktor-faktor yang memengaruhinya.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hright:
        calendar_panel()

# =========================
# KEY INDICATORS
# =========================
if page == "dashboard":
    st.markdown('<div class="section-title">Key indicators</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "🧴 Plastic price",
            f"{latest['plastic_price']:,.2f}",
            "IDR/kg · latest observed value",
            "Historical data",
            "yellow",
        )

    with c2:
        metric_card(
            "🛢️ Oil price",
            f"{latest['oil_price']:,.2f}",
            "USD/barrel · supporting variable",
            "Commodity",
            "pink",
        )

    with c3:
        metric_card(
            "💱 USD/IDR rate",
            f"{latest['usd_idr']:,.0f}",
            "Exchange rate · macro indicator",
            "FX",
            "blue",
        )

    c4, c5 = st.columns(2)

    with c4:
        metric_card(
            "🔗 Oil ↔ Plastic correlation",
            f"{corr_oil:.3f} {'↗' if corr_oil >= 0 else '↘'}",
            "Pearson correlation coefficient",
            corr_oil_strength,
            "green",
        )

    with c5:
        metric_card(
            "🔮 30-day forecast",
            f"{pred_end:,.2f}",
            f"{'+' if pred_change_pct >= 0 else ''}{pred_change_pct:.2f}% vs first forecast day",
            "Predicted price",
            "purple",
        )

# =========================
# MARKET TRENDS
# =========================
if page in ["dashboard", "trends"]:
    st.markdown('<div class="section-title">Market trends</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Historical price movements across key variables.</div>',
        unsafe_allow_html=True,
    )

    chart_card(
        "Tren Harga Plastik",
        line_chart(filtered_df, "date", "plastic_price", "Plastic Price (IDR/kg)", PURPLE, 360),
        key="chart_plastic_price",
    )

    

    left, right = st.columns(2)

    with left:
        chart_card(
            "Tren Harga Minyak",
            line_chart(filtered_df, "date", "oil_price", "Oil Price (USD/bbl)", PINK, 320),
            key="chart_oil_price",
        )

    with right:
        chart_card(
            "Tren Nilai Tukar USD/IDR",
            line_chart(filtered_df, "date", "usd_idr", "USD/IDR Exchange Rate", BLUE, 320),
            key="chart_usd_idr",
        )

    if "plastic_ma_3" in filtered_df.columns:
        fig_ma = go.Figure()

        fig_ma.add_trace(
            go.Scatter(
                x=filtered_df["date"],
                y=filtered_df["plastic_price"],
                name="Actual",
                line=dict(color=PURPLE, width=2.4),
            )
        )

        fig_ma.add_trace(
            go.Scatter(
                x=filtered_df["date"],
                y=filtered_df["plastic_ma_3"],
                name="MA(3)",
                line=dict(color=YELLOW, width=2.8, dash="dot"),
            )
        )

        fig_ma.update_layout(
            title=dict(text="Plastic Price vs Moving Average", font=dict(size=16, family="Montserrat", color=TEXT), x=0.01),
            paper_bgcolor=CARD,
            plot_bgcolor=CARD,
            font=dict(color=TEXT, family="Didact Gothic"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
            margin=dict(l=15, r=15, t=55, b=15),
            height=320,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
        )

        chart_card(
            "Harga Plastik vs Moving Average",
            fig_ma,
            key="chart_moving_average",
        )

         # =========================
    # MARKET TRENDS INSIGHT SUMMARY
    # =========================
    st.markdown(
        f"""
        <div class="insight-box">
            <h3>📈 Market Trends Insight Summary</h3>
            <p>
                Berdasarkan data historis, harga plastik menunjukkan tren
                <b>{plastic_trend_text}</b> dari <b>{plastic_start:,.2f}</b>
                menjadi <b>{plastic_end:,.2f}</b>, atau berubah sebesar
                <b>{'+' if plastic_change_pct >= 0 else ''}{plastic_change_pct:.2f}%</b>
                selama periode pengamatan.
            </p>
            <p>
                Pada periode yang sama, harga minyak tercatat
                <b>{oil_trend_text}</b> sebesar
                <b>{'+' if oil_change_pct >= 0 else ''}{oil_change_pct:.2f}%</b>,
                sedangkan nilai tukar USD/IDR cenderung <b>{usd_trend_text}</b>
                dengan perubahan sebesar
                <b>{'+' if usd_change_pct >= 0 else ''}{usd_change_pct:.2f}%</b>.
            </p>
            <p>
                Pergerakan ini menunjukkan bahwa dinamika harga plastik tidak berdiri sendiri,
                tetapi bergerak bersama faktor eksternal seperti harga minyak mentah dan kurs
                USD/IDR. Lonjakan atau pelemahan pada variabel pendukung dapat menjadi sinyal
                awal perubahan harga plastik pada periode berikutnya.
            </p>
            <span class="insight-tag">🧴 Plastic: {'+' if plastic_change_pct >= 0 else ''}{plastic_change_pct:.2f}%</span>
            <span class="insight-tag">🛢️ Oil: {'+' if oil_change_pct >= 0 else ''}{oil_change_pct:.2f}%</span>
            <span class="insight-tag">💱 USD/IDR: {'+' if usd_change_pct >= 0 else ''}{usd_change_pct:.2f}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# CORRELATION
# =========================
if page in ["dashboard", "correlation"]:
    st.markdown('<div class="section-title">Relationship analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Analisis hubungan harga minyak, kurs USD/IDR, dan harga plastik.</div>',
        unsafe_allow_html=True,
    )

    r1, r2 = st.columns(2)

    with r1:
        chart_card(
            "Dampak Harga Minyak terhadap Harga Plastik",
            scatter_chart(filtered_df, "oil_price", "plastic_price", "Oil Price Impact on Plastic", PINK),
            key="chart_scatter_oil",
        )

    with r2:
        chart_card(
            "Dampak USD/IDR terhadap Harga Plastik",
            scatter_chart(filtered_df, "usd_idr", "plastic_price", "USD/IDR Impact on Plastic", BLUE),
            key="chart_scatter_usd",
        )

    corr_matrix = filtered_df[["plastic_price", "oil_price", "usd_idr"]].corr()

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=["Plastic", "Oil", "USD/IDR"],
            y=["Plastic", "Oil", "USD/IDR"],
            colorscale=[[0, BLUE], [0.5, CARD], [1, PINK]],
            text=corr_matrix.round(3).values,
            texttemplate="%{text}",
            zmin=-1,
            zmax=1,
            showscale=True,
        )
    )

    fig_heat.update_layout(
        title=dict(text="Correlation Matrix", font=dict(size=16, family="Montserrat", color=TEXT), x=0.01),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT, family="Didact Gothic"),
        margin=dict(l=15, r=15, t=55, b=15),
        height=310,
    )

    chart_card(
        "Matriks Korelasi",
        fig_heat,
        key="chart_correlation_matrix",
    )

        # =========================
    # CORRELATION INSIGHT SUMMARY
    # =========================
    oil_corr_direction = "positif" if corr_oil >= 0 else "negatif"
    usd_corr_direction = "positif" if corr_usd >= 0 else "negatif"

    oil_corr_meaning = (
        "kenaikan harga minyak cenderung diikuti oleh kenaikan harga plastik"
        if corr_oil > 0
        else "kenaikan harga minyak cenderung tidak selalu diikuti oleh kenaikan harga plastik"
    )

    usd_corr_meaning = (
        "kenaikan USD/IDR cenderung berkaitan dengan kenaikan harga plastik"
        if corr_usd > 0
        else "kenaikan USD/IDR cenderung tidak selalu berkaitan dengan kenaikan harga plastik"
    )

    st.markdown(
        f"""
        <div class="insight-box">
            <h3>🔗 Correlation Insight Summary</h3>
            <p>
                Hasil analisis korelasi menunjukkan bahwa hubungan antara harga minyak
                dan harga plastik bernilai <b>{corr_oil:.3f}</b>, yang termasuk kategori
                <b>{corr_oil_strength.lower()}</b> dan bersifat <b>{oil_corr_direction}</b>.
                Artinya, {oil_corr_meaning}.
            </p>
            <p>
                Sementara itu, korelasi antara nilai tukar USD/IDR dan harga plastik bernilai
                <b>{corr_usd:.3f}</b>, yang termasuk kategori
                <b>{corr_usd_strength.lower()}</b> dan bersifat <b>{usd_corr_direction}</b>.
                Artinya, {usd_corr_meaning}.
            </p>
            <p>
                Berdasarkan perbandingan nilai korelasi, faktor yang paling dominan dalam
                menjelaskan pergerakan harga plastik pada dataset ini adalah
                <b>{dominant_external_factor}</b>. Hal ini memperkuat asumsi bahwa harga plastik,
                sebagai produk turunan minyak bumi, sangat dipengaruhi oleh dinamika komoditas
                energi global dan faktor makroekonomi.
            </p>
            <span class="insight-tag">🛢️ Oil corr: {corr_oil:.3f}</span>
            <span class="insight-tag">💱 FX corr: {corr_usd:.3f}</span>
            <span class="insight-tag">Dominant factor: {dominant_external_factor}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# FORECAST
# =========================
if page in ["dashboard", "forecast"]:
    st.markdown('<div class="section-title">Forecast & movement summary</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Komposisi pergerakan harga dan prediksi 30 hari ke depan.</div>',
        unsafe_allow_html=True,
    )

    pcol, fcol = st.columns([0.9, 1.6])

    with pcol:
        if "plastic_lag_1" in filtered_df.columns:
            move_df = filtered_df.dropna(subset=["plastic_price", "plastic_lag_1"]).copy()

            move_df["movement"] = move_df.apply(
                lambda r: "Naik"
                if r["plastic_price"] - r["plastic_lag_1"] > 0
                else "Turun"
                if r["plastic_price"] - r["plastic_lag_1"] < 0
                else "Stabil",
                axis=1,
            )

            counts = move_df["movement"].value_counts().reset_index()
            counts.columns = ["movement", "count"]

            fig_pie = px.pie(
                counts,
                names="movement",
                values="count",
                title="Price Movement Composition",
                hole=0.5,
                color="movement",
                color_discrete_map={"Naik": GREEN, "Turun": PINK, "Stabil": BLUE},
            )

            fig_pie.update_layout(
                paper_bgcolor=CARD,
                plot_bgcolor=CARD,
                font=dict(color=TEXT, family="Didact Gothic"),
                title=dict(font=dict(size=16, family="Montserrat", color=TEXT), x=0.01),
                margin=dict(l=15, r=15, t=55, b=15),
                height=390,
            )

            chart_card(
                "Komposisi Pergerakan Harga Plastik",
                fig_pie,
                key="chart_movement_composition",
            )

    with fcol:
        tail_df = filtered_df.tail(30)

        fig_pred = go.Figure()

        fig_pred.add_trace(
            go.Scatter(
                x=tail_df["date"],
                y=tail_df["plastic_price"],
                name="Historical",
                line=dict(color=MUTED, width=2, dash="dot"),
            )
        )

        fig_pred.add_trace(
            go.Scatter(
                x=pred["prediction_date"],
                y=pred["predicted_price"],
                name="Forecast",
                line=dict(color=PURPLE, width=3),
                marker=dict(size=6, color=PURPLE, line=dict(color="white", width=1.2)),
                fill="tozeroy",
                fillcolor="rgba(200,162,216,0.14)",
            )
        )

        fig_pred.update_layout(
            title=dict(text="30-Day Plastic Price Forecast", font=dict(size=16, family="Montserrat", color=TEXT), x=0.01),
            paper_bgcolor=CARD,
            plot_bgcolor=CARD,
            font=dict(color=TEXT, family="Didact Gothic"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
            margin=dict(l=15, r=15, t=55, b=15),
            height=390,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
        )

        chart_card(
            "Prediksi Harga Plastik 30 Hari",
            fig_pred,
            key="chart_forecast_30_days",
        )

            # =========================
    # FORECAST INSIGHT SUMMARY
    # =========================
    movement_summary = "belum tersedia"

    if "plastic_lag_1" in filtered_df.columns:
        naik_pct = 0
        turun_pct = 0
        stabil_pct = 0

        if not counts.empty:
            total_count = counts["count"].sum()

            naik_val = counts.loc[counts["movement"] == "Naik", "count"].sum()
            turun_val = counts.loc[counts["movement"] == "Turun", "count"].sum()
            stabil_val = counts.loc[counts["movement"] == "Stabil", "count"].sum()

            naik_pct = (naik_val / total_count) * 100 if total_count else 0
            turun_pct = (turun_val / total_count) * 100 if total_count else 0
            stabil_pct = (stabil_val / total_count) * 100 if total_count else 0

            dominant_move = counts.sort_values("count", ascending=False).iloc[0]["movement"]

            movement_summary = (
                f"Pergerakan historis harga plastik didominasi oleh kategori "
                f"<b>{dominant_move}</b>, dengan komposisi naik sebesar "
                f"<b>{naik_pct:.1f}%</b>, turun sebesar <b>{turun_pct:.1f}%</b>, "
                f"dan stabil sebesar <b>{stabil_pct:.1f}%</b>."
            )

    forecast_direction_text = (
        "mengalami kenaikan" if pred_end > pred_start
        else "mengalami penurunan" if pred_end < pred_start
        else "cenderung stabil"
    )

    st.markdown(
        f"""
        <div class="insight-box">
            <h3>🔮 Forecast Insight Summary</h3>
            <p>
                {movement_summary}
            </p>
            <p>
                Berdasarkan hasil prediksi model, harga plastik diproyeksikan
                <b>{forecast_direction_text}</b> dalam 30 hari ke depan.
                Nilai prediksi bergerak dari sekitar <b>{pred_start:,.2f}</b>
                menjadi <b>{pred_end:,.2f}</b>, atau berubah sebesar
                <b>{'+' if pred_change_pct >= 0 else ''}{pred_change_pct:.2f}%</b>.
            </p>
            <p>
                Tren prediksi ini menunjukkan bahwa pergerakan harga plastik masih perlu
                dipantau bersama faktor pendukung seperti harga minyak dan nilai tukar USD/IDR,
                karena kedua variabel tersebut memiliki hubungan terhadap dinamika harga plastik.
            </p>
            <p style="font-size:12px;color:rgba(248,245,236,0.45);">
                ⚠️ Insight ini bersifat estimatif dan digunakan sebagai alat bantu analisis,
                bukan sebagai nilai pasti harga pasar.
            </p>
            <span class="insight-tag">📊 Movement: {movement_summary.replace('<b>', '').replace('</b>', '')[:40]}...</span>
            <span class="insight-tag">🔮 Forecast: {forecast_direction_text}</span>
            <span class="insight-tag">📅 Horizon: 30 days</span>
            <span class="insight-tag">📈 Change: {'+' if pred_change_pct >= 0 else ''}{pred_change_pct:.2f}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# DATA SOURCE
# =========================
if page == "source":
    st.markdown('<div class="section-title">Data Source</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Informasi dataset, jenis plastik, dan pipeline yang digunakan.</div>',
        unsafe_allow_html=True,
    )

    st.info(
        """
        **Jenis plastik dalam ruang lingkup analisis:** HDPE, LDPE, PP, PET, dan PVC.

        **Dataset yang digunakan:**
        - `plastic_prices.csv`
        - `plastic_price_predictions.csv`

        **Pipeline:** Airflow → Processing → PostgreSQL → Streamlit Dashboard → Hugging Face Spaces
        """
    )

# =========================
# INSIGHT
# =========================
if page == "dashboard":
    insight_html = "".join([
        '<div class="insight-box">',
        '<h3>💡 Insight Summary</h3>',

        '<p>',
        f'Korelasi harga minyak terhadap harga plastik tercatat <b>{corr_oil:.3f}</b> ',
        f'({corr_oil_strength.lower()}, {"positif" if corr_oil >= 0 else "negatif"}), sedangkan ',
        f'korelasi USD/IDR terhadap harga plastik tercatat <b>{corr_usd:.3f}</b> ',
        f'({corr_usd_strength.lower()}, {"positif" if corr_usd >= 0 else "negatif"}).',
        '</p>',

        '<p>',
        f'Model prediksi memproyeksikan harga plastik <b>{trend_direction}</b> dalam 30 hari ',
        f'ke depan, dari <b>{pred_start:,.2f}</b> menjadi <b>{pred_end:,.2f}</b> ',
        f'({"+" if pred_change_pct >= 0 else ""}{pred_change_pct:.2f}%).',
        '</p>',

        '<p style="font-size:12px;color:rgba(248,245,236,0.45);">',
        '⚠️ Hasil prediksi bersifat estimatif berdasarkan model machine learning dan digunakan ',
        'sebagai alat bantu analisis, bukan sebagai nilai pasti harga pasar.',
        '</p>',

        f'<span class="insight-tag">🛢️ Oil corr: {corr_oil:.3f}</span>',
        f'<span class="insight-tag">💱 FX corr: {corr_usd:.3f}</span>',
        '<span class="insight-tag">📅 Horizon: 30 days</span>',
        f'<span class="insight-tag">📈 Trend: {trend_direction}</span>',

        '</div>',
    ])

    st.markdown(insight_html, unsafe_allow_html=True)

# =========================
# TABLES
# =========================
if page in ["dashboard", "source"]:
    st.markdown('<div class="section-title">Detailed data</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📄 Historical dataset", "🔮 Forecast dataset"])

    with tab1:
        st.dataframe(
            dark_table_style(
                filtered_df.style.format(
                    {
                        "plastic_price": "{:,.2f}",
                        "oil_price": "{:,.2f}",
                        "usd_idr": "{:,.0f}",
                    }
                )
            ),
            use_container_width=True,
            height=320,
        )

    with tab2:
        st.dataframe(
            dark_table_style(
                pred.style.format({"predicted_price": "{:,.2f}"})
            ),
            use_container_width=True,
            height=320,
        )