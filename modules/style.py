
import streamlit as st


def apply_custom_style():

    st.markdown(
        """
        <style>

        /* =========================================
           1. GLOBAL APPLICATION
        ========================================= */

        .stApp {
            background: #F5F7FC;
            color: #1E293B;
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        .main .block-container {
            max-width: 1380px;
            padding-top: 2rem;
            padding-bottom: 3rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }


        /* =========================================
           2. TYPOGRAPHY
        ========================================= */

        h1, h2, h3, h4, h5, h6 {
            color: #14213D !important;
            font-weight: 750 !important;
            letter-spacing: -0.5px;
        }

        h1 {
            font-size: 2.25rem !important;
            line-height: 1.25 !important;
        }

        h2 {
            font-size: 1.65rem !important;
        }

        h3 {
            font-size: 1.2rem !important;
        }

        .stMarkdown p,
        .stMarkdown li {
            color: #526078;
            line-height: 1.7;
        }

        label,
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] p {
            color: #27364F !important;
            font-weight: 600 !important;
        }


        /* =========================================
           3. PROFESSIONAL SIDEBAR
        ========================================= */

        [data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #101B33 0%,
                #142440 55%,
                #101B33 100%
            ) !important;

            border-right: 1px solid #263958;
        }

        [data-testid="stSidebar"] > div {
            background: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding: 1.5rem 1rem 1rem 1rem;
        }

        /* General sidebar text */

        [data-testid="stSidebar"],
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] li {
            color: #F1F5FF !important;
        }

        /* Resume AI brand heading */

        [data-testid="stSidebar"] .resume-ai-brand,
        [data-testid="stSidebar"] .resume-ai-brand h2,
        [data-testid="stSidebar"] h2.resume-ai-brand {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            opacity: 1 !important;
            visibility: visible !important;
            font-size: 27px !important;
            font-weight: 800 !important;
            letter-spacing: -0.8px !important;
            line-height: 1.3 !important;
            margin: 0 0 5px 0 !important;
            padding: 0 !important;
            text-shadow: none !important;
        }

        [data-testid="stSidebar"] .resume-ai-brand span {
            color: #60A5FA !important;
            -webkit-text-fill-color: #60A5FA !important;
        }

        /* Fallback for any sidebar h2 */

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* Brand subtitle */

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: #C5D5F0 !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase;
        }

        /* Workspace label */

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            margin-bottom: 10px;
        }

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: #D5E2F7 !important;
            font-weight: 650 !important;
        }

        /* Dividers */

        [data-testid="stSidebar"] hr {
            border: none !important;
            border-top: 1px solid #405372 !important;
            margin-top: 20px !important;
            margin-bottom: 20px !important;
        }

        /* Navigation button spacing */

        [data-testid="stSidebar"] .stButton {
            margin-top: 5px;
            margin-bottom: 9px;
        }

        /* Navigation buttons */

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 49px;

            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 13px;

            padding: 11px 15px !important;

            border-radius: 11px !important;
            background: transparent !important;

            color: #F1F5FF !important;
            -webkit-text-fill-color: #F1F5FF !important;

            border: 1px solid transparent !important;
            box-shadow: none !important;

            font-size: 14px !important;
            font-weight: 700 !important;

            transition: all 0.2s ease;
        }

        /* Navigation button text */

        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span,
        [data-testid="stSidebar"] .stButton > button div {
            color: #F1F5FF !important;
            -webkit-text-fill-color: #F1F5FF !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }

        /* Navigation icons */

        [data-testid="stSidebar"] .stButton > button svg {
            color: #D5E2F7 !important;
            fill: none !important;
            width: 19px !important;
            height: 19px !important;
        }

        /* Hover effect */

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #203D65 !important;
            color: #FFFFFF !important;
            border: 1px solid #5276A8 !important;
            transform: translateX(2px);
        }

        [data-testid="stSidebar"] .stButton > button:hover p,
        [data-testid="stSidebar"] .stButton > button:hover span {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover svg {
            color: #FFFFFF !important;
        }

        /* Active navigation item */

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: linear-gradient(
                100deg,
                #2859B8,
                #326BD5
            ) !important;

            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;

            border: 1px solid #6A96F0 !important;
            box-shadow: 0 4px 12px rgba(30, 91, 195, 0.25) !important;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] p,
        [data-testid="stSidebar"] .stButton > button[kind="primary"] span,
        [data-testid="stSidebar"] .stButton > button[kind="primary"] div {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] svg {
            color: #FFFFFF !important;
        }

        /* Sidebar markdown and bottom text */

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #E2EAF8 !important;
        }


        /* =========================================
           4. TEXT INPUTS
        ========================================= */

        .stTextInput input,
        .stTextArea textarea {
            background: #FFFFFF !important;
            color: #172554 !important;
            border: 1px solid #D9E1EF !important;
            border-radius: 10px !important;
            min-height: 43px;
            opacity: 1 !important;
            -webkit-text-fill-color: #172554 !important;
            transition: border 0.2s ease, box-shadow 0.2s ease;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: #315EDE !important;
            box-shadow: 0 0 0 3px rgba(49, 94, 222, 0.12) !important;
        }

        .stTextArea textarea {
            font-size: 14px !important;
            line-height: 1.7 !important;
            caret-color: #315EDE !important;
        }

        .stTextArea textarea:disabled {
            background: #F8FAFC !important;
            color: #334155 !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #334155 !important;
        }

        .stTextArea textarea::placeholder,
        .stTextInput input::placeholder {
            color: #94A3B8 !important;
            opacity: 1 !important;
        }


        /* =========================================
           5. PRIMARY BUTTONS
        ========================================= */

        .main [data-testid="stBaseButton-primary"] {
            background-color: #1746B8 !important;
            background-image: none !important;
            border: 2px solid #1746B8 !important;
            border-radius: 10px !important;
            min-height: 48px !important;
            padding: 10px 20px !important;
            box-shadow: 0 3px 8px rgba(23, 70, 184, 0.16) !important;
            opacity: 1 !important;
            transition: all 0.2s ease;
        }

        .main [data-testid="stBaseButton-primary"] p,
        .main [data-testid="stBaseButton-primary"] span,
        .main [data-testid="stBaseButton-primary"] div,
        .main [data-testid="stBaseButton-primary"] label {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-size: 14px !important;
            font-weight: 750 !important;
            opacity: 1 !important;
            text-shadow: none !important;
        }

        .main [data-testid="stBaseButton-primary"] svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        .main [data-testid="stBaseButton-primary"]:hover {
            background-color: #10378F !important;
            border-color: #10378F !important;
            box-shadow: 0 5px 12px rgba(23, 70, 184, 0.22) !important;
        }

        .main [data-testid="stBaseButton-primary"]:active {
            background-color: #0D2D78 !important;
            border-color: #0D2D78 !important;
        }

        .main [data-testid="stBaseButton-secondary"],
        .main .stDownloadButton button {
            background: #FFFFFF !important;
            color: #244BB8 !important;
            border: 1px solid #D6E0F0 !important;
            border-radius: 9px !important;
            min-height: 42px !important;
            font-weight: 650 !important;
            transition: all 0.2s ease;
        }

        .main [data-testid="stBaseButton-secondary"]:hover,
        .main .stDownloadButton button:hover {
            background: #EFF4FF !important;
            border-color: #A8BDEB !important;
        }


        /* =========================================
           6. FILE UPLOADER
        ========================================= */

        [data-testid="stFileUploader"] {
            background: #FFFFFF !important;
            border: 1.5px dashed #9DB5E8 !important;
            border-radius: 14px !important;
            padding: 18px !important;
            transition: border 0.2s ease, background 0.2s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #315EDE !important;
            background: #F9FBFF !important;
        }

        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] p,
        [data-testid="stFileUploader"] span {
            color: #334155 !important;
        }

        [data-testid="stFileUploader"] button {
            border-radius: 8px !important;
        }


        /* =========================================
           7. METRIC CARDS
        ========================================= */

        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 13px !important;
            padding: 19px !important;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.035);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.07);
        }

        [data-testid="stMetricLabel"] {
            color: #64748B !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricValue"] {
            color: #244BB8 !important;
            font-size: 1.8rem !important;
            font-weight: 750 !important;
        }


        /* =========================================
           8. FEATURE CARDS
        ========================================= */

        .dashboard-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            padding: 23px !important;
            margin-bottom: 15px !important;
            box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .dashboard-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.07);
        }

        .dashboard-card h3 {
            color: #172554 !important;
        }

        .dashboard-card p {
            color: #64748B !important;
        }


        /* =========================================
           9. EXPANDERS
        ========================================= */

        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E0E7F0 !important;
            border-radius: 12px !important;
            margin-bottom: 10px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.025);
        }

        [data-testid="stExpander"] summary {
            color: #172554 !important;
            font-weight: 650 !important;
        }

        [data-testid="stExpander"] summary:hover {
            color: #315EDE !important;
        }


        /* =========================================
           10. ALERTS
        ========================================= */

        [data-testid="stAlert"] {
            border-radius: 11px !important;
            border: 1px solid #E2E8F0 !important;
        }


        /* =========================================
           11. TABLES
        ========================================= */

        [data-testid="stDataFrame"] {
            background: #FFFFFF !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            overflow: hidden;
        }


        /* =========================================
           12. PROGRESS BARS
        ========================================= */

        [data-testid="stProgressBar"] > div > div {
            background: #315EDE !important;
            border-radius: 20px !important;
        }


        /* =========================================
           13. SELECT BOXES
        ========================================= */

        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: #FFFFFF !important;
            border-color: #D9E1EF !important;
            border-radius: 9px !important;
        }


        /* =========================================
           14. DIVIDERS
        ========================================= */

        hr {
            border-color: #E2E8F0 !important;
        }


        /* =========================================
           15. RESPONSIVE DESIGN
        ========================================= */

        @media (max-width: 768px) {

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.3rem;
            }

            h1 {
                font-size: 1.7rem !important;
            }

            h2 {
                font-size: 1.4rem !important;
            }

            .dashboard-card {
                padding: 16px !important;
            }

            [data-testid="stMetric"] {
                padding: 14px !important;
            }

            [data-testid="stSidebar"] .stButton > button {
                min-height: 46px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )
