
# ==================================================
# JOB ROLE SKILL DATABASE
# ==================================================

JOB_ROLES = {

    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI",
        "Tableau", "Pandas", "NumPy", "Data Analysis"
    ],

    "Python Developer": [
        "Python", "FastAPI", "Flask", "Django",
        "SQL", "Git", "REST API"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "Scikit-learn", "TensorFlow", "PyTorch",
        "Pandas", "NumPy"
    ],

    "Data Scientist": [
        "Python", "SQL", "Machine Learning",
        "Deep Learning", "Pandas", "NumPy",
        "Scikit-learn", "Data Analysis"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Python", "Git"
    ],

    "Backend Developer": [
        "Python", "Java", "FastAPI", "Flask",
        "Django", "SQL", "MySQL", "REST API"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React"
    ],

    "Database Developer": [
        "SQL", "MySQL", "PostgreSQL",
        "MongoDB", "SQLite", "Python"
    ],

    "AI/ML Intern": [
        "Python", "Machine Learning", "Deep Learning",
        "NLP", "TensorFlow", "PyTorch",
        "Scikit-learn", "NumPy"
    ],

    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Python", "FastAPI", "Flask", "SQL",
        "MongoDB", "REST API"
    ]
}


# ==================================================
# SKILL LEARNING ROADMAP
# ==================================================

SKILL_LEARNING = {

    "Python": {
        "learn": "Python fundamentals, functions, OOP and file handling.",
        "project": "Build a Python-based expense tracker."
    },

    "SQL": {
        "learn": "SQL queries, joins, grouping and subqueries.",
        "project": "Build a student database and practise SQL queries."
    },

    "Excel": {
        "learn": "Excel formulas, sorting, filtering and pivot tables.",
        "project": "Create an Excel sales analysis dashboard."
    },

    "Power BI": {
        "learn": "Power BI, data cleaning, DAX and interactive dashboards.",
        "project": "Create an interactive business sales dashboard."
    },

    "Tableau": {
        "learn": "Tableau charts, filters and interactive visualizations.",
        "project": "Build a Tableau data visualization dashboard."
    },

    "Pandas": {
        "learn": "DataFrames, data cleaning, filtering and grouping.",
        "project": "Analyse a real-world CSV dataset using Pandas."
    },

    "NumPy": {
        "learn": "Arrays, indexing, mathematical operations and statistics.",
        "project": "Create a numerical data analysis program."
    },

    "Data Analysis": {
        "learn": "Data cleaning, exploratory analysis and data interpretation.",
        "project": "Create a student performance analysis dashboard using Python and Pandas."
    },

    "Machine Learning": {
        "learn": "Supervised learning, unsupervised learning and model evaluation.",
        "project": "Build a student performance prediction model."
    },

    "Deep Learning": {
        "learn": "Neural networks, CNNs, training and model evaluation.",
        "project": "Build an image classification application."
    },

    "Scikit-learn": {
        "learn": "Preprocessing, model training and evaluation using Scikit-learn.",
        "project": "Build a machine learning classification model."
    },

    "TensorFlow": {
        "learn": "TensorFlow fundamentals, neural networks and model training.",
        "project": "Build a simple image recognition model."
    },

    "PyTorch": {
        "learn": "Tensors, neural networks, loss functions and training loops.",
        "project": "Build a basic neural network classifier."
    },

    "NLP": {
        "learn": "Text preprocessing, tokenization and text classification.",
        "project": "Build a sentiment analysis application."
    },

    "FastAPI": {
        "learn": "API routes, request handling and data validation.",
        "project": "Create a REST API for a machine learning model."
    },

    "Flask": {
        "learn": "Flask routes, templates and backend development.",
        "project": "Build a simple web application using Flask."
    },

    "Django": {
        "learn": "Django models, views, templates and authentication.",
        "project": "Build a student management web application."
    },

    "Java": {
        "learn": "Java fundamentals, OOP, collections and exception handling.",
        "project": "Build a library management application."
    },

    "JavaScript": {
        "learn": "JavaScript fundamentals, DOM manipulation and events.",
        "project": "Build an interactive task management application."
    },

    "HTML": {
        "learn": "HTML elements, forms and semantic page structure.",
        "project": "Create a personal portfolio website."
    },

    "CSS": {
        "learn": "CSS layouts, Flexbox, Grid and responsive design.",
        "project": "Design a responsive portfolio website."
    },

    "React": {
        "learn": "React components, props, state and hooks.",
        "project": "Build a React-based job search dashboard."
    },

    "Git": {
        "learn": "Git commands, commits, branches and GitHub workflows.",
        "project": "Upload and maintain a project on GitHub."
    },

    "MySQL": {
        "learn": "Database design, SQL queries and relationships.",
        "project": "Build a student information management database."
    },

    "PostgreSQL": {
        "learn": "PostgreSQL queries, relationships and database management.",
        "project": "Build a database-backed application."
    },

    "MongoDB": {
        "learn": "NoSQL concepts, collections and document operations.",
        "project": "Build a simple inventory management application."
    },

    "SQLite": {
        "learn": "SQLite tables, queries and database operations.",
        "project": "Build a local task management application."
    },

    "REST API": {
        "learn": "HTTP methods, API endpoints and JSON responses.",
        "project": "Create a REST API for a student management system."
    }
}


# ==================================================
# SKILL NORMALIZATION
# ==================================================

def normalize_skill(skill):
    """
    Normalize skill names to avoid matching problems
    caused by uppercase/lowercase differences.
    """

    return str(skill).strip().lower()


# ==================================================
# FALLBACK ROADMAP
# ==================================================

def get_skill_roadmap(skill):
    """
    Return a predefined roadmap when available.
    Otherwise, generate a simple fallback roadmap.
    """

    details = SKILL_LEARNING.get(skill)

    if details:
        return {
            "skill": skill,
            "learn": details["learn"],
            "project": details["project"]
        }

    return {
        "skill": skill,
        "learn": (
            f"Understand the fundamentals of {skill}, "
            "learn its important concepts and practise its applications."
        ),
        "project": (
            f"Build a small practical project using {skill} "
            "to demonstrate your knowledge."
        )
    }


# ==================================================
# JOB ROLE RECOMMENDATION FUNCTION
# ==================================================

def recommend_job_roles(resume_skills):
    """
    Recommend suitable job roles based on resume skills.

    Returns the top 5 roles with:
    - Match percentage
    - Matched skills
    - Missing skills
    - Personalized learning roadmap
    """

    if not resume_skills:
        return []

    # Normalize resume skills
    resume_skill_map = {}

    for skill in resume_skills:
        normalized = normalize_skill(skill)

        if normalized:
            resume_skill_map[normalized] = str(skill).strip()

    recommendations = []

    # Compare resume skills with every job role
    for role, required_skills in JOB_ROLES.items():

        required_map = {
            normalize_skill(skill): skill
            for skill in required_skills
        }

        required_set = set(required_map.keys())
        resume_set = set(resume_skill_map.keys())

        # Find matching and missing skills
        matched_keys = resume_set.intersection(required_set)
        missing_keys = required_set - resume_set

        # Calculate match percentage
        if not required_set:
            percentage = 0
        else:
            percentage = (
                len(matched_keys) / len(required_set)
            ) * 100

        matched = sorted(
            required_map[key]
            for key in matched_keys
        )

        missing = sorted(
            required_map[key]
            for key in missing_keys
        )

        # Generate learning roadmap
        roadmap = []

        for skill in missing:
            roadmap.append(get_skill_roadmap(skill))

        recommendations.append({

            "job_role": role,

            "match_percentage": round(percentage, 2),

            "matched_skills": matched,

            "missing_skills": missing,

            "learning_roadmap": roadmap[:4]

        })

    # Sort by highest skill match
    recommendations.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    # Return top 5 recommendations
    return recommendations[:5]
