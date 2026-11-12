
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Dashboard Chart Layout Test")

chart_col1, chart_col2 = st.columns([1.2, 1])

with chart_col1:
    st.subheader("Skill Match Distribution")

    pie_data = {
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [12, 3]
    }

    fig1 = px.pie(
        pie_data,
        names="Category",
        values="Count",
        hole=0.60,
        title="Required Skills Overview"
    )

    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.subheader("Skill Analysis Summary")
    st.write("Total Required Skills: 15")
    st.write("Matched Skills: 12")
    st.write("Missing Skills: 3")
    st.write("Additional Resume Skills: 8")

st.divider()

st.subheader("Skills Comparison")

bar_data = {
    "Skill": ["Matched", "Missing", "Additional"],
    "Count": [12, 3, 8]
}

fig2 = px.bar(
    bar_data,
    x="Skill",
    y="Count",
    text="Count",
    title="Resume Skills Analysis"
)

st.plotly_chart(fig2, use_container_width=True)
