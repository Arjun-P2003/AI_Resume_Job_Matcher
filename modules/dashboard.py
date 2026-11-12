
import streamlit as st
import plotly.express as px
import html


def show_dashboard(results, similarity_score):

    # --------------------------------------------------
    # 1. GET SKILL DATA
    # --------------------------------------------------
    matched_skills = results.get("matched_skills", []) or []
    missing_skills = results.get("missing_skills", []) or []
    extra_skills = results.get("extra_skills", []) or []

    matched = len(matched_skills)
    missing = len(missing_skills)
    extra = len(extra_skills)

    total_job_skills = matched + missing
    skill_match = results.get("match_percentage", 0)

    # --------------------------------------------------
    # 2. DASHBOARD HEADER
    # --------------------------------------------------
    st.markdown(
        """
        <div style="margin-bottom: 22px;">
            <div style="
                color: #1746B8;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 1.5px;
                margin-bottom: 7px;
            ">
                CAREER INTELLIGENCE
            </div>
            <h2 style="
                color: #111C35;
                font-size: 29px;
                font-weight: 800;
                margin: 0;
            ">
                Resume Analysis Dashboard
            </h2>
            <p style="
                color: #64748b;
                font-size: 14px;
                margin-top: 7px;
            ">
                Understand your resume performance and identify
                opportunities to improve your job compatibility.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # 3. KEY METRIC CARDS
    # --------------------------------------------------
    st.markdown(
        """
        <p style="
            color: #334155;
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 10px;
        ">
            Key Performance Indicators
        </p>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="AI Text Similarity",
            value=f"{similarity_score}%"
        )

    with col2:
        st.metric(
            label="Skill Match",
            value=f"{skill_match}%"
        )

    with col3:
        st.metric(
            label="Matched Skills",
            value=matched,
            delta="Found in resume",
            delta_color="normal"
        )

    with col4:
        st.metric(
            label="Missing Skills",
            value=missing,
            delta="Needs improvement" if missing else "All covered",
            delta_color="inverse" if missing else "normal"
        )

    st.divider()

    # --------------------------------------------------
    # 4. SKILL MATCH DISTRIBUTION
    # --------------------------------------------------
    st.subheader("Skill Match Distribution")

    st.caption(
        "A visual breakdown of the skills required by the job "
        "and the skills identified in your resume."
    )

    chart_col1, chart_col2 = st.columns([1.3, 1])

    with chart_col1:

        if total_job_skills > 0:

            pie_data = {
                "Category": [
                    "Matched Skills",
                    "Missing Skills"
                ],
                "Count": [
                    matched,
                    missing
                ]
            }

            pie_chart = px.pie(
                pie_data,
                names="Category",
                values="Count",
                hole=0.65,
                title="Job Skills Overview",
                color="Category",
                color_discrete_map={
                    "Matched Skills": "#2563EB",
                    "Missing Skills": "#F59E0B"
                }
            )

            pie_chart.update_traces(
                textposition="inside",
                textinfo="percent",
                textfont=dict(
                    size=13,
                    color="white"
                ),
                marker=dict(
                    line=dict(
                        color="white",
                        width=3
                    )
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Skills: %{value}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                )
            )

            pie_chart.update_layout(
                annotations=[
                    dict(
                        text=f"<b>{total_job_skills}</b><br><sup>Total Skills</sup>",
                        x=0.5,
                        y=0.5,
                        font=dict(
                            size=17,
                            color="#111C35"
                        ),
                        showarrow=False
                    )
                ],
                template="plotly_white",
                title_font=dict(
                    size=17,
                    color="#111C35"
                ),
                font=dict(
                    family="Arial",
                    color="#334155"
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(
                    l=10,
                    r=10,
                    t=55,
                    b=45
                ),
                height=350
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        else:
            st.info(
                "No job skills were detected. Add a job description "
                "to view the skill distribution."
            )

    with chart_col2:

        st.markdown("#### Skill Analysis Summary")
        st.caption("Your resume's skill coverage at a glance.")

        st.metric(
            "Total Job Skills",
            total_job_skills
        )

        st.metric(
            "Matched Skills",
            matched
        )

        st.metric(
            "Missing Skills",
            missing
        )

        st.metric(
            "Additional Resume Skills",
            extra
        )

        if total_job_skills > 0:
            coverage = (matched / total_job_skills) * 100
            st.progress(
                min(max(coverage / 100, 0.0), 1.0),
                text=f"Skill coverage: {coverage:.1f}%"
            )

    st.divider()

    # --------------------------------------------------
    # 5. SKILLS COMPARISON CHART
    # --------------------------------------------------
    st.subheader("Skills Comparison")

    st.caption(
        "Compare matched, missing, and additional skills "
        "to understand your overall skill profile."
    )

    bar_data = {
        "Skill": [
            "Matched Skills",
            "Missing Skills",
            "Additional Skills"
        ],
        "Count": [
            matched,
            missing,
            extra
        ]
    }

    bar_chart = px.bar(
        bar_data,
        x="Skill",
        y="Count",
        color="Skill",
        text="Count",
        color_discrete_map={
            "Matched Skills": "#2563EB",
            "Missing Skills": "#F59E0B",
            "Additional Skills": "#64748B"
        },
        category_orders={
            "Skill": [
                "Matched Skills",
                "Missing Skills",
                "Additional Skills"
            ]
        }
    )

    bar_chart.update_traces(
        textposition="outside",
        textfont=dict(
            size=13,
            color="#334155"
        ),
        marker_line_width=0,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Number of skills: %{y}"
            "<extra></extra>"
        )
    )

    bar_chart.update_layout(
        template="plotly_white",
        showlegend=False,
        height=350,
        xaxis_title="Skill Category",
        yaxis_title="Number of Skills",
        title=dict(
            text="Resume Skills Analysis",
            font=dict(
                size=17,
                color="#111C35"
            )
        ),
        font=dict(
            family="Arial",
            color="#334155"
        ),
        margin=dict(
            l=25,
            r=25,
            t=65,
            b=50
        ),
        yaxis=dict(
            rangemode="tozero",
            gridcolor="#E9EEF5",
            zeroline=False
        ),
        xaxis=dict(
            showgrid=False
        )
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.divider()

    # --------------------------------------------------
    # 6. SKILL BADGE FUNCTION
    # --------------------------------------------------
    def display_skill_badges(
        skills,
        background,
        text_color,
        border_color
    ):

        if not skills:
            st.info("No skills found in this category.")
            return

        badges = ""

        for skill in skills:

            safe_skill = html.escape(str(skill))

            badges += f"""
                <span style="
                    display: inline-block;
                    background-color: {background};
                    color: {text_color};
                    padding: 8px 13px;
                    margin: 4px;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: 650;
                    border: 1px solid {border_color};
                ">{safe_skill}</span>
            """

        st.markdown(
            f"""
            <div style="
                display: flex;
                flex-wrap: wrap;
                gap: 3px;
                padding: 8px 0 14px 0;
            ">
                {badges}
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # 7. DETAILED SKILL ANALYSIS
    # --------------------------------------------------
    st.subheader("Detailed Skill Analysis")

    st.caption(
        "Review the individual skills identified during resume analysis."
    )

    skill_col1, skill_col2, skill_col3 = st.columns(3)

    with skill_col1:

        st.markdown(
            """
            <div style="
                color: #166534;
                font-size: 14px;
                font-weight: 750;
                margin-bottom: 8px;
            ">
                ✓ Matched Skills
            </div>
            """,
            unsafe_allow_html=True
        )

        display_skill_badges(
            matched_skills,
            "#DCFCE7",
            "#166534",
            "#BBF7D0"
        )

    with skill_col2:

        st.markdown(
            """
            <div style="
                color: #92400E;
                font-size: 14px;
                font-weight: 750;
                margin-bottom: 8px;
            ">
                ! Missing Skills
            </div>
            """,
            unsafe_allow_html=True
        )

        display_skill_badges(
            missing_skills,
            "#FEF3C7",
            "#92400E",
            "#FDE68A"
        )

    with skill_col3:

        st.markdown(
            """
            <div style="
                color: #1E40AF;
                font-size: 14px;
                font-weight: 750;
                margin-bottom: 8px;
            ">
                + Additional Skills
            </div>
            """,
            unsafe_allow_html=True
        )

        display_skill_badges(
            extra_skills,
            "#DBEAFE",
            "#1E40AF",
            "#BFDBFE"
        )

    st.divider()

    # --------------------------------------------------
    # 8. INFORMATION NOTE
    # --------------------------------------------------
    st.info(
        "**Understanding your scores:** AI Text Similarity measures "
        "textual similarity between your resume and the job description. "
        "It does not represent the probability of getting hired. "
        "Skill Match measures how many detected job skills are also "
        "present in your resume."
    )
