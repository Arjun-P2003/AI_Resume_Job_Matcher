
# AI-Powered Resume & Job Matcher

An intelligent resume analysis application built using Python and Streamlit. It helps job seekers evaluate their resumes against job descriptions, identify skill gaps, check ATS compatibility, and discover suitable career opportunities.

## Features

- **Resume Upload:** Upload resumes in PDF format.
- **Skill Extraction:** Automatically extract technical skills from resumes and job descriptions.
- **Resume Matching:** Calculate similarity between a resume and a job description using TF-IDF and Cosine Similarity.
- **Skill Gap Analysis:** Identify matched, missing, and additional skills.
- **ATS Compatibility Checker:** Evaluate resumes for ATS-related improvements.
- **Resume Quality Analysis:** Check resume quality and provide suggestions.
- **Bullet Point Enhancer:** Improve resume bullet points using action verbs and writing suggestions.
- **Job Role Recommendations:** Recommend suitable job roles based on extracted skills.
- **Learning Roadmap:** Suggest learning resources and practical projects for missing skills.
- **Visual Dashboard:** Display resume analysis results using interactive charts.
- **PDF Report:** Generate downloadable resume analysis reports.
- **Analysis History:** Store and view previous analyses using SQLite.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend / UI | Streamlit |
| Data Visualization | Plotly |
| Machine Learning | Scikit-learn |
| Text Processing | TF-IDF, Cosine Similarity, Regular Expressions |
| PDF Processing | PyMuPDF |
| PDF Report Generation | ReportLab |
| Database | SQLite |

## Project Structure

```text
AI_Resume_Job_Matcher/
│
├── database/
│   └── database.py
│
├── modules/
│   ├── ats_checker.py
│   ├── bullet_enhancer.py
│   ├── chart_test.py
│   ├── dashboard.py
│   ├── improvement_suggestions.py
│   ├── job_role_recommender.py
│   ├── pdf_reader.py
│   ├── pdf_report.py
│   ├── resume_analyzer.py
│   ├── resume_quality.py
│   ├── skill_extractor.py
│   └── style.py
│
├── app.py
├── chart_test.py
├── dashboard_test.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Arjun-P2003/AI_Resume_Job_Matcher.git
```

### 2. Navigate to the project folder

```bash
cd AI_Resume_Job_Matcher
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Machine Learning Approach

The application uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert resume and job description text into numerical representations.

Cosine Similarity is then used to measure how closely the resume matches the job description.

Skill extraction and comparison help identify relevant skills, missing skills, and additional skills.

## Database

SQLite is used to store resume analysis history, including:

- Resume filename
- Job description
- Similarity score
- Skill match percentage
- Matched skills
- Missing skills
- Analysis date

## Future Enhancements

- Integration with external job portals.
- Advanced semantic matching using transformer models.
- AI-powered resume content generation.
- Support for additional resume formats.
- Personalized career and course recommendations.

## Author

**Arjun P**

AI & Machine Learning Student  
Acharya Institute of Technology

## GitHub Repository

[AI-Powered Resume & Job Matcher](https://github.com/Arjun-P2003/AI_Resume_Job_Matcher)
