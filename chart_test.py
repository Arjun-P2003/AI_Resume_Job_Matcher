import streamlit as st
import plotly.express as px

st.title("Chart Display Test")

pie_data = {
    "Category": ["Matched Skills", "Missing Skills"],
    "Count": [12, 3]
}

fig1 = px.pie(
    pie_data,
    names="Category",
    values="Count",
    title="Skill Match Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

bar_data = {
    "Skill": ["Matched", "Missing", "Additional"],
    "Count": [12, 3, 8]
}

fig2 = px.bar(
    bar_data,
    x="Skill",
    y="Count",
    title="Skills Comparison"
)

st.plotly_chart(fig2, use_container_width=True)
