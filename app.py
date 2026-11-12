
import streamlit as st
import json

from modules.style import apply_custom_style

from modules.pdf_reader import extract_resume_text
from modules.skill_extractor import (
    extract_skills,
    extract_job_skills,
    compare_skills
)
from modules.resume_analyzer import calculate_similarity
from modules.dashboard import show_dashboard
from modules.pdf_report import generate_pdf_report
from modules.improvement_suggestions import generate_suggestions
from modules.resume_quality import check_resume_quality
from modules.ats_checker import check_ats_compatibility
from modules.bullet_enhancer import enhance_bullet_point
from modules.job_role_recommender import recommend_job_roles

from database.database import (
    create_table,
    save_analysis,
    get_analysis_history
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Resume AI | Career Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()
apply_custom_style()


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "resume_text": "",
    "resume_skills": [],
    "resume_filename": "",
    "analysis_results": None,
    "similarity_score": None,
    "analyzed_job_description": "",
    "ats_results": None,
    "bullet_enhancement_result": None,
    "selected_page": "Resume Analyzer"
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# REUSABLE FUNCTIONS
# =========================================================

def section_title(number, title, description=""):

    st.markdown(f"### {number}  {title}")

    if description:
        st.caption(description)


def display_skill_list(skills, success=True):

    if not skills:
        st.info("No skills detected.")
        return

    skill_text = ", ".join(skills)

    if success:
        st.success(skill_text)
    else:
        st.warning(skill_text)


def get_requirement_counts(ats, category):

    if category == "required":

        matched_list = ats.get("matched_required_skills", [])
        missing_list = ats.get("missing_required_skills", [])

        matched_count = ats.get("matched_required_count")
        total_count = ats.get("required_skill_count")

    else:

        matched_list = ats.get("matched_preferred_skills", [])
        missing_list = ats.get("missing_preferred_skills", [])

        matched_count = ats.get("matched_preferred_count")
        total_count = ats.get("preferred_skill_count")

    if matched_count is not None and total_count is not None:
        return int(matched_count), int(total_count)

    matched_count = len(matched_list)
    total_count = matched_count + len(missing_list)

    return matched_count, total_count


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # Custom Resume AI brand heading
    st.markdown(
        """
        <div class="resume-ai-brand">
            <span class="brand-star">✦</span>
            <span>Resume AI</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("SMART CAREER ASSISTANT")
    st.divider()
    st.caption("WORKSPACE")

    if st.button(
        "Resume Analyzer",
        icon=":material/space_dashboard:",
        key="nav_resume",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page == "Resume Analyzer"
            else "secondary"
        )
    ):

        st.session_state.selected_page = "Resume Analyzer"
        st.rerun()

    if st.button(
        "Analysis History",
        icon=":material/history:",
        key="nav_history",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page == "Analysis History"
            else "secondary"
        )
    ):

        st.session_state.selected_page = "Analysis History"
        st.rerun()

    st.divider()
    st.caption("Powered by Python & Machine Learning")
    st.caption("Version 5.0 · Resume AI")


# =========================================================
# MAIN HEADER AND PROFESSIONAL FEATURE CARDS
# =========================================================

def show_hero():

    st.markdown(
        '<div class="hero-label">✦ SMART CAREER ASSISTANT</div>',
        unsafe_allow_html=True
    )

    st.markdown("# AI-Powered Resume")

    st.markdown(
        """
        <h1 style="
            color: #3268D6;
            font-size: 42px;
            font-weight: 800;
            margin-top: -20px;
        ">
            &amp; Job Matcher
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
            Turn your resume into a career advantage.
            Discover your technical strengths, identify missing skills,
            explore suitable job roles, and measure your compatibility
            with job requirements.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.divider()

    feature_cards_html = """
    <style>

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 20px;
        width: 100%;
        margin: 10px 0 20px 0;
    }

    .feature-card {
        min-height: 215px;
        padding: 25px 22px;
        border-radius: 17px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
        transition: all 0.25s ease;
        box-sizing: border-box;
        font-family: Arial, sans-serif;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(15, 23, 42, 0.11);
    }

    .feature-blue {
        background: linear-gradient(145deg, #EAF1FF, #FFFFFF);
        border-top: 4px solid #3268D6;
    }

    .feature-green {
        background: linear-gradient(145deg, #E8FAF2, #FFFFFF);
        border-top: 4px solid #10B981;
    }

    .feature-purple {
        background: linear-gradient(145deg, #F2ECFF, #FFFFFF);
        border-top: 4px solid #8B5CF6;
    }

    .feature-icon {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        font-size: 27px;
        line-height: 1;
    }

    .feature-blue .feature-icon {
        background: #DCE8FF;
    }

    .feature-green .feature-icon {
        background: #D1FAE5;
    }

    .feature-purple .feature-icon {
        background: #EDE9FE;
    }

    .feature-title {
        color: #172554;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 10px;
        letter-spacing: -0.3px;
    }

    .feature-description {
        color: #64748B;
        font-size: 13px;
        line-height: 1.75;
        margin: 0;
    }

    @media (max-width: 768px) {

        .feature-grid {
            grid-template-columns: 1fr;
        }

        .feature-card {
            min-height: 180px;
            padding: 20px;
        }

        .feature-title {
            font-size: 16px;
        }
    }

    </style>

    <div class="feature-grid">

        <div class="feature-card feature-blue">

            <div class="feature-icon">📄</div>

            <div class="feature-title">
                Resume Intelligence
            </div>

            <p class="feature-description">
                Extract technical skills, evaluate resume quality,
                and understand your professional profile.
            </p>

        </div>

        <div class="feature-card feature-green">

            <div class="feature-icon">🎯</div>

            <div class="feature-title">
                Smart Job Matching
            </div>

            <p class="feature-description">
                Compare your skills with job requirements,
                identify skill gaps, and improve compatibility.
            </p>

        </div>

        <div class="feature-card feature-purple">

            <div class="feature-icon">📊</div>

            <div class="feature-title">
                Career Insights
            </div>

            <p class="feature-description">
                Explore career recommendations, ATS compatibility,
                and interactive analysis reports.
            </p>

        </div>

    </div>
    """

    st.html(feature_cards_html)

    st.divider()


# =========================================================
# RESUME QUALITY CHECKER
# =========================================================

def show_resume_quality():

    section_title(
        "02",
        "Resume Quality Assessment",
        "Review the important sections of your resume."
    )

    quality = check_resume_quality(
        st.session_state.resume_text
    )

    score = quality["quality_score"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resume Quality Score", f"{score}%")

    with col2:
        st.metric(
            "Completed Sections",
            f"{quality['completed_sections']}/"
            f"{quality['total_sections']}"
        )

    st.progress(min(max(score, 0), 100) / 100)

    if score >= 80:
        st.success("Your resume contains most important sections.")
    elif score >= 50:
        st.warning("Some important sections need improvement.")
    else:
        st.error("Your resume needs improvement.")

    with st.expander("View Section Analysis", expanded=True):

        for name, details in quality["checks"].items():

            if details["found"]:
                st.success(f"{name} — Found")
            else:
                st.warning(f"{name} — Not detected")

    st.caption(
        "This checker uses keyword-based detection. "
        "Different section headings may affect detection."
    )


# =========================================================
# CAREER ROLE RECOMMENDATIONS
# =========================================================

def show_job_recommendations():

    section_title(
        "03",
        "Career Role Recommendations",
        "Discover suitable roles based on your detected technical skills."
    )

    if not st.session_state.resume_skills:
        st.warning("No recognized technical skills found.")
        return

    recommendations = recommend_job_roles(
        st.session_state.resume_skills
    )

    if not recommendations:
        st.info("No recommendations available.")
        return

    st.markdown("#### Your Top Career Matches")

    st.caption(
        "Explore your skill compatibility with different job roles. "
        "Expand a role to view its personalized learning roadmap."
    )

    for index, item in enumerate(recommendations, start=1):

        role = item["job_role"]
        score = item["match_percentage"]
        matched = item["matched_skills"]
        missing = item["missing_skills"]
        roadmap = item["learning_roadmap"]

        with st.container(border=True):

            st.markdown(f"#### {index}. {role}")

            col1, col2 = st.columns([1, 3])

            with col1:
                st.metric("Skill Match", f"{score}%")

            with col2:
                st.markdown("**Match Progress**")
                st.progress(min(max(score, 0), 100) / 100)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Matching Skills**")

                if matched:
                    st.success(", ".join(matched))
                else:
                    st.info("No matching skills detected.")

            with col2:
                st.markdown("**Skills to Improve**")

                if missing:
                    st.warning(", ".join(missing))
                else:
                    st.success("No missing skills identified.")

            with st.expander(
                f"View Learning Roadmap and Project Ideas — {role}",
                expanded=(index == 1)
            ):

                st.markdown("### Personalized Learning Roadmap")

                if roadmap:

                    for step_number, skill_data in enumerate(
                        roadmap,
                        start=1
                    ):

                        skill_name = skill_data.get(
                            "skill",
                            "Recommended Skill"
                        )

                        learning_description = skill_data.get(
                            "learn",
                            "Develop practical knowledge of this skill."
                        )

                        project_idea = skill_data.get(
                            "project",
                            "Build a small practical project using this skill."
                        )

                        st.markdown(
                            f"**Step {step_number}: Learn {skill_name}**"
                        )

                        st.write(learning_description)

                        st.info(f"Practice Project: {project_idea}")

                        if step_number < len(roadmap):
                            st.divider()

                else:
                    st.success(
                        "Your detected skills already cover the "
                        "recommended skills for this role."
                    )

    st.caption(
        "Match percentages represent skill overlap, not hiring probability. "
        "Recommendations use predefined skill lists. "
        "Learning roadmaps are suggestions based on missing skills."
    )


# =========================================================
# ATS CHECKER
# =========================================================

def show_ats_results():

    ats = st.session_state.ats_results

    if ats is None:
        return

    section_title(
        "06",
        "ATS Compatibility Analysis",
        "Understand how your resume aligns with the target job."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", f"{ats['ats_score']}%")

    with col2:
        st.metric("Keyword Match", f"{ats['keyword_score']}%")

    with col3:
        st.metric("Action Verb Score", f"{ats['action_verb_score']}%")

    st.progress(min(max(ats["ats_score"], 0), 100) / 100)

    if ats["ats_score"] >= 80:
        st.success("Your resume shows a strong compatibility score.")
    elif ats["ats_score"] >= 50:
        st.warning("Your resume has moderate ATS compatibility.")
    else:
        st.error("Your resume needs improvement.")

    st.divider()
    st.markdown("**Required Skills Analysis**")

    required_score = ats.get("required_skill_score", 0)

    required_matched_count, required_total_count = (
        get_requirement_counts(ats, "required")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Required Skill Match", f"{required_score}%")
        st.progress(min(max(required_score, 0), 100) / 100)

    with col2:
        st.metric(
            "Required Skills Found",
            f"{required_matched_count}/{required_total_count}"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Matched Required Skills**")
        display_skill_list(
            ats.get("matched_required_skills", []),
            success=True
        )

    with col2:
        st.markdown("**Missing Required Skills**")
        display_skill_list(
            ats.get("missing_required_skills", []),
            success=False
        )

    st.divider()
    st.markdown("**Preferred Skills Analysis**")

    preferred_score = ats.get("preferred_skill_score", 0)

    preferred_matched_count, preferred_total_count = (
        get_requirement_counts(ats, "preferred")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Preferred Skill Match", f"{preferred_score}%")
        st.progress(min(max(preferred_score, 0), 100) / 100)

    with col2:
        st.metric(
            "Preferred Skills Found",
            f"{preferred_matched_count}/{preferred_total_count}"
        )

    with st.expander("View Preferred Skills Details"):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Matched Preferred Skills**")
            display_skill_list(
                ats.get("matched_preferred_skills", []),
                success=True
            )

        with col2:
            st.markdown("**Missing Preferred Skills**")
            display_skill_list(
                ats.get("missing_preferred_skills", []),
                success=False
            )

    st.divider()
    st.markdown("**Overall Keyword Analysis**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Matched Keywords**")
        display_skill_list(
            ats.get("matched_keywords", []),
            success=True
        )

    with col2:
        st.markdown("**Missing Keywords**")
        display_skill_list(
            ats.get("missing_keywords", []),
            success=False
        )

    st.divider()
    st.markdown("**Action Verb Analysis**")

    if ats["found_action_verbs"]:
        st.success(", ".join(ats["found_action_verbs"]))
    else:
        st.warning(
            "Try strong action verbs such as Developed, Created, "
            "Implemented, Designed, and Improved."
        )

    st.markdown("**Achievement Analysis**")

    if ats["has_quantified_achievements"]:
        st.success(
            "Measurable numbers or percentages were detected."
        )
    else:
        st.warning(
            "Add measurable achievements where accurate. "
            "For example, mention improvements in accuracy, "
            "processing time, or project performance."
        )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resume Word Count", ats["word_count"])

    with col2:
        st.metric("Length Status", ats["length_status"])

    st.caption(
        "This is a keyword-based ATS estimate, not a real ATS system "
        "or a guarantee of selection. Required and preferred skill "
        "classification depends on job description section headings."
    )


# =========================================================
# IMPROVEMENT SUGGESTIONS
# =========================================================

def show_improvement_suggestions(results):

    section_title(
        "07",
        "Resume Improvement Recommendations",
        "Practical suggestions based on your job match."
    )

    suggestions = generate_suggestions(results)

    for index, item in enumerate(suggestions, start=1):

        with st.expander(
            f"{index}. {item['title']}",
            expanded=(index == 1)
        ):

            st.write(item["description"])
            st.markdown("**Recommended Actions**")

            for action in item["actions"]:
                st.markdown(f"- {action}")


# =========================================================
# BULLET POINT ENHANCER
# =========================================================

def show_bullet_enhancer():

    section_title(
        "08",
        "Resume Bullet Point Enhancer",
        "Improve your project and work experience descriptions."
    )

    st.info(
        "Enter an existing resume bullet point to get a "
        "professional rewrite and improvement tips."
    )

    original = st.text_area(
        "Your Existing Bullet Point",
        placeholder=(
            "Example: Worked on a project using Python "
            "and machine learning."
        ),
        height=120,
        key="bullet_input"
    )

    if st.button(
        "Enhance Bullet Point",
        type="primary",
        use_container_width=True,
        key="enhance_bullet_button"
    ):

        if not original.strip():
            st.warning("Please enter a bullet point first.")

        else:
            st.session_state.bullet_enhancement_result = (
                enhance_bullet_point(original)
            )

    result = st.session_state.bullet_enhancement_result

    if result is not None:

        if result["enhanced"]:

            st.markdown("**Enhanced Resume Bullet Point**")
            st.success(result["enhanced"])
            st.code(result["enhanced"], language="text")

            st.caption(
                "Verify the statement before adding it to your resume."
            )

        st.markdown("**Improvement Tips**")

        for tip in result["tips"]:
            st.markdown(f"- {tip}")


# =========================================================
# RESUME ANALYZER PAGE
# =========================================================

def show_resume_analyzer():

    show_hero()

    section_title(
        "01",
        "Upload Your Resume",
        "Upload your PDF resume to begin the analysis."
    )

    with st.container(border=True):

        resume = st.file_uploader(
            "Choose your resume",
            type=["pdf"],
            help="Only PDF files are supported."
        )

        if st.button(
            "Extract Resume Information",
            type="primary",
            use_container_width=True,
            key="extract_resume_button"
        ):

            if resume is None:
                st.warning("Please select a PDF resume first.")

            else:

                with st.spinner("Extracting resume information..."):

                    extracted_text = extract_resume_text(resume)

                if extracted_text.startswith("Error reading PDF:"):
                    st.error(extracted_text)

                elif not extracted_text.strip():
                    st.warning(
                        "No text found. The PDF may be scanned "
                        "or image-based."
                    )

                else:

                    st.session_state.resume_text = extracted_text
                    st.session_state.resume_filename = resume.name

                    st.session_state.resume_skills = extract_skills(
                        extracted_text
                    )

                    st.session_state.analysis_results = None
                    st.session_state.similarity_score = None
                    st.session_state.analyzed_job_description = ""
                    st.session_state.ats_results = None
                    st.session_state.bullet_enhancement_result = None

                    st.success("Resume extracted successfully!")

    if st.session_state.resume_text:

        st.divider()
        st.markdown("### Current Resume")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.info(
                f"Uploaded File: {st.session_state.resume_filename}"
            )

        with col2:
            st.metric(
                "Detected Skills",
                len(st.session_state.resume_skills)
            )

        with st.expander("View Extracted Resume Text"):

            st.text_area(
                "Resume Content",
                value=st.session_state.resume_text,
                height=280,
                disabled=True
            )

        st.markdown("**Technical Skills Detected**")

        display_skill_list(
            st.session_state.resume_skills,
            success=True
        )

        st.divider()
        show_resume_quality()

        st.divider()
        show_job_recommendations()

    else:

        st.info(
            "Your analysis workspace is ready. Upload your resume "
            "to unlock skill extraction, quality assessment, "
            "career recommendations, and job matching."
        )

    st.divider()

    section_title(
        "04",
        "Target Job Description",
        "Paste the job description you want to compare with your resume."
    )

    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the complete job description here...",
        key="job_description_input"
    )

    if st.button(
        "Run Complete Resume Analysis",
        type="primary",
        use_container_width=True,
        key="run_complete_analysis_button"
    ):

        if not st.session_state.resume_text:

            st.warning(
                "Please upload and extract your resume first."
            )

        elif not job_description.strip():

            st.warning("Please enter a job description.")

        else:

            with st.spinner("Analyzing your resume..."):

                job_skill_data = extract_job_skills(
                    job_description
                )

                job_skills = job_skill_data["all_skills"]

                results = compare_skills(
                    st.session_state.resume_skills,
                    job_skills
                )

                similarity_score = calculate_similarity(
                    st.session_state.resume_text,
                    job_description
                )

                ats_results = check_ats_compatibility(
                    st.session_state.resume_text,
                    job_description
                )

                st.session_state.analysis_results = results
                st.session_state.similarity_score = similarity_score

                st.session_state.analyzed_job_description = (
                    job_description
                )

                st.session_state.ats_results = ats_results

                save_analysis(
                    st.session_state.resume_filename,
                    job_description,
                    similarity_score,
                    results["match_percentage"],
                    results["matched_skills"],
                    results["missing_skills"]
                )

                st.success(
                    "Analysis completed and saved successfully!"
                )

                if not job_skills:

                    st.warning(
                        "No technical skills from the current skill "
                        "database were detected in the job description. "
                        "The skill match may therefore be 0%. "
                        "Text similarity and other ATS checks are still available."
                    )

    if st.session_state.analysis_results is not None:

        results = st.session_state.analysis_results
        similarity_score = st.session_state.similarity_score

        st.divider()

        section_title(
            "05",
            "Resume Match Results",
            "Review your resume's alignment with the selected job."
        )

        show_dashboard(results, similarity_score)

        st.divider()
        show_ats_results()

        st.divider()
        show_improvement_suggestions(results)

        st.divider()
        show_bullet_enhancer()

        st.divider()
        st.markdown("### Download Analysis Report")

        st.caption(
            "Generate a PDF summary of your resume "
            "and job matching results."
        )

        pdf_file = generate_pdf_report(
            st.session_state.resume_filename,
            st.session_state.analyzed_job_description,
            similarity_score,
            results
        )

        st.download_button(
            label="Download PDF Analysis Report",
            data=pdf_file,
            file_name="Resume_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.divider()
        st.markdown("### Detailed Skill Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Matched Skills**")
            display_skill_list(
                results["matched_skills"],
                success=True
            )

        with col2:
            st.markdown("**Missing Skills**")
            display_skill_list(
                results["missing_skills"],
                success=False
            )

        with col3:
            st.markdown("**Additional Skills**")

            if results["extra_skills"]:
                st.info(", ".join(results["extra_skills"]))
            else:
                st.write("No additional skills detected.")

        st.caption(
            "Text Similarity measures document similarity. "
            "Skill Match measures recognized job skill coverage. "
            "ATS Compatibility is a basic heuristic estimate. "
            "Job recommendations use skill overlap. "
            "None of these scores represents hiring probability."
        )


# =========================================================
# ANALYSIS HISTORY PAGE
# =========================================================

def show_analysis_history():

    st.title("Analysis History")

    st.caption(
        "Review your previous resume evaluations "
        "and job matching results."
    )

    st.divider()

    history = get_analysis_history()

    if not history:

        st.info(
            "No analysis history available yet. "
            "Complete your first resume analysis to see it here."
        )

        return

    st.metric("Total Analyses Completed", len(history))
    st.divider()

    for record in history:

        with st.expander(
            f"Analysis #{record[0]} | {record[1]} | {record[7]}"
        ):

            st.markdown("**Target Job Description**")
            st.write(record[2])

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "AI Text Similarity",
                    f"{record[3]}%"
                )

            with col2:
                st.metric(
                    "Skill Match",
                    f"{record[4]}%"
                )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Matched Skills**")
                matched = json.loads(record[5])
                display_skill_list(matched, success=True)

            with col2:
                st.markdown("**Missing Skills**")
                missing = json.loads(record[6])
                display_skill_list(missing, success=False)


# =========================================================
# PAGE ROUTING
# =========================================================

if st.session_state.selected_page == "Resume Analyzer":
    show_resume_analyzer()
else:
    show_analysis_history()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="app-footer">
        RESUME AI | AI-POWERED CAREER INTELLIGENCE
        <br>
        Built with Python, Streamlit & Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
