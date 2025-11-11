import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------

st.set_page_config(page_title="COVID-19 Dashboard", page_icon="🦠", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}  /* hides the three-dot menu */
        footer {visibility: hidden;}     /* hides default footer */
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="COVID-19 Global Analytics Dashboard",
    page_icon="🦠",
    layout="wide",
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("covid_19_clean_complete.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

data = load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("🌍 Navigation Panel")
menu = st.sidebar.radio(
    "Go to Section:",
    ["Home", "Top 10 Affected Countries", "Country Insights", "About"],
)

# --- Sidebar Footer Section with Separators ---

st.sidebar.markdown("""
<style>
.footer-item {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}
.footer-text {
    line-height: 1.2;
    font-weight: bold;
}
.separator {
    border: 0;
    border-top: 1px solid #555;  /* gray separator line */
    margin: 8px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Line separator before footer info ---
st.sidebar.markdown('<hr class="separator">', unsafe_allow_html=True)

# --- Footer items (aligned and neat) ---
st.sidebar.markdown(
    '<div class="footer-item">👨‍💻 <span class="footer-text">Created by [Mohd Soban]</span></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="footer-item">🎓 <span class="footer-text">B.Tech CSE | 2nd Year | 2025</span></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="footer-item">🏫 <span class="footer-text">Kamla Nehru Institute of Technology, Sultanpur</span></div>',
    unsafe_allow_html=True
)

# --- Line separator after footer info (optional) ---
st.sidebar.markdown('<hr class="separator">', unsafe_allow_html=True)

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
if menu == "Home":
    st.markdown("# 🧭 COVID-19 Global Dashboard")
    st.markdown("Gain insights into the worldwide spread of COVID-19 using real-time data visualization and analytics.")

    # Latest stats
    latest_date = data["Date"].max()
    latest_data = data[data["Date"] == latest_date]

    total_confirmed = int(latest_data["Confirmed"].sum())
    total_deaths = int(latest_data["Deaths"].sum())
    total_recovered = int(latest_data["Recovered"].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("🌐 Total Confirmed", f"{total_confirmed:,}")
    col2.metric("💀 Total Deaths", f"{total_deaths:,}")
    col3.metric("💚 Total Recovered", f"{total_recovered:,}")

    st.markdown("### 🌎 Global Spread Map")
    fig_map = px.choropleth(
        latest_data,
        locations="Country/Region",
        locationmode="country names",
        color="Confirmed",
        hover_name="Country/Region",
        color_continuous_scale="Reds",
        title=f"Worldwide COVID-19 Cases (as of {latest_date.date()})",
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # -------------------------------------------------
    # ARTICLE-STYLE INFO CARDS SECTION
    # -------------------------------------------------
    st.markdown("## 📰 COVID-19 Articles & Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background-color:#1E1E1E; padding:20px; border-radius:12px; box-shadow:0 0 10px #00000040;'>
            <img src='https://cdn-icons-png.flaticon.com/512/2785/2785819.png' width='60'>
            <h4>📖 What is COVID-19?</h4>
            <p>COVID-19 (Coronavirus Disease 2019) is an infectious disease caused by SARS-CoV-2, first identified in Wuhan, China in 2019. It primarily affects the respiratory system and spread globally, leading to a worldwide pandemic.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color:#1E1E1E; padding:20px; border-radius:12px; box-shadow:0 0 10px #00000040;'>
            <img src='https://cdn-icons-png.flaticon.com/512/2785/2785816.png' width='60'>
            <h4>🧬 Origin & First Case</h4>
            <p>The first known case of COVID-19 was reported in Wuhan, China, in December 2019. It was linked to a seafood market selling live wild animals. WHO declared it a pandemic on March 11, 2020.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color:#1E1E1E; padding:20px; border-radius:12px; box-shadow:0 0 10px #00000040;'>
            <img src='https://cdn-icons-png.flaticon.com/512/2927/2927347.png' width='60'>
            <h4>😷 Symptoms & Precautions</h4>
            <p>Common symptoms include fever, cough, fatigue, and loss of smell. Preventive measures include mask-wearing, hand hygiene, and vaccination to reduce transmission risks.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color:#1E1E1E; padding:20px; border-radius:12px; box-shadow:0 0 10px #00000040;'>
            <img src='https://cdn-icons-png.flaticon.com/512/2966/2966327.png' width='60'>
            <h4>💉 Vaccination & Recovery</h4>
            <p>Global vaccination efforts began in late 2020. Major vaccines include Pfizer, Moderna, Covaxin, and AstraZeneca. Vaccination campaigns drastically reduced hospitalization and death rates.</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------
# TOP 10 AFFECTED COUNTRIES
# -------------------------------------------------
elif menu == "Top 10 Affected Countries":
    st.markdown("# 🔝 Top 10 Most Affected Countries")

    latest_date = data["Date"].max()
    latest_data = data[data["Date"] == latest_date]

    top_countries = (
        latest_data.groupby("Country/Region")["Confirmed"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_top = px.bar(
        top_countries,
        x="Country/Region",
        y="Confirmed",
        color="Country/Region",
        title="Top 10 Countries by Confirmed Cases",
        text_auto=True,
    )
    st.plotly_chart(fig_top, use_container_width=True)

# -------------------------------------------------
# COUNTRY INSIGHTS
# -------------------------------------------------
elif menu == "Country Insights":
    st.markdown("# 📊 Country-wise Insights")
    st.markdown("Use the search bar below to explore COVID-19 trends for any country.")

    all_countries = sorted(data["Country/Region"].unique())
    search_input = st.text_input("🔍 Search Country").strip().title()

    if search_input in all_countries:
        selected_country = search_input
    else:
        selected_country = st.selectbox("Select Country", all_countries)

    country_data = data[data["Country/Region"] == selected_country]
    latest_date = country_data["Date"].max()
    latest_record = country_data[country_data["Date"] == latest_date].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Confirmed", f"{latest_record['Confirmed']:,}")
    col2.metric("Deaths", f"{latest_record['Deaths']:,}")
    col3.metric("Recovered", f"{latest_record['Recovered']:,}")

    with st.expander("📈 Show Trend Graphs"):
        fig1 = px.line(country_data, x="Date", y="Confirmed", title=f"{selected_country}: Confirmed Cases Over Time", markers=True)
        fig2 = px.line(country_data, x="Date", y="Deaths", title=f"{selected_country}: Deaths Over Time", markers=True)
        fig3 = px.line(country_data, x="Date", y="Recovered", title=f"{selected_country}: Recoveries Over Time", markers=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# ABOUT
# -------------------------------------------------
elif menu == "About":
    st.markdown("# 🧾 About This Project")
    st.write("""
    This interactive dashboard visualizes the spread and analysis of COVID-19 globally.
    It combines data science with real-world health information.

    **Technologies Used:**
    - 🐍 Python  
    - 📊 Pandas & Plotly  
    - 🌐 Streamlit  

    **Developer Info:**
    - 👨‍💻 [Mohd Soban]  
    - 🎓 B.Tech (CSE) | 2nd Year | 2025  
    - 🏫 [Kamla Nehru Institute of Technology, Sultanpur]
    """)
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:gray;'>© 2025 | COVID-19 Analytics & Info Dashboard</p>", unsafe_allow_html=True)

#    ------------------------------------------------------------------------------------------------------------------

import streamlit as st

footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 -1px 5px rgba(0,0,0,0.2);
        z-index: 100;
    }
    .college {
        font-size: 14px;
        color: #ddd;
    }
    </style>

    <div class="footer">
        © 2025 | Created by 👨‍🎓 <b>Mohd Soban</b> | B.Tech CSE (2nd Year)
        <div class="college">🎓<b> Kamla Nehru Institute of Technology, Sultanpur </b></div>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)

