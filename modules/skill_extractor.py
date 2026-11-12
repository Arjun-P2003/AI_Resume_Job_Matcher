
import re


SKILL_DATABASE = {
    # Programming Languages
    "Python": ["python", "python programming"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "C": ["programming language c"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"],

    # Web Development
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],

    # Databases
    "SQL": ["sql", "structured query language"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb"],
    "SQLite": ["sqlite"],
    "Database Management": ["database management", "dbms"],

    # Data Science
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch", "torch"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],

    # AI and Machine Learning
    "Artificial Intelligence": ["artificial intelligence"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "NLP": ["natural language processing", "nlp"],
    "Computer Vision": ["computer vision"],
    "Neural Networks": ["neural networks", "neural network"],

    # Data Analysis
    "Data Analysis": [
        "data analysis", "data analytics",
        "analyze data", "analysing data",
        "analyzing data", "analyzed data",
        "analyse data", "analysed data"
    ],
    "Data Cleaning": [
        "data cleaning", "cleaning data",
        "cleaned data", "clean data", "data cleansing"
    ],
    "Data Preprocessing": [
        "data preprocessing", "data pre-processing",
        "preprocessing data", "pre-process data",
        "preprocess data", "preprocessed data",
        "pre-processing"
    ],
    "Data Collection": [
        "data collection", "collecting data",
        "collect data", "collected data"
    ],
    "Data Visualization": [
        "data visualization", "data visualisation",
        "visualizing data", "visualising data"
    ],
    "Statistics": ["statistics", "statistical analysis"],
    "Probability": ["probability", "probability theory"],
    "Exploratory Data Analysis": [
        "exploratory data analysis", "exploratory analysis", "eda"
    ],

    # Business Intelligence
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],

    # Tools and Platforms
    "Jupyter Notebook": ["jupyter notebook", "jupyter"],
    "Git": ["git", "git version control"],
    "GitHub": ["github"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["microsoft azure", "azure"],
    "Google Cloud": ["google cloud", "gcp"],
    "Streamlit": ["streamlit"],

    # APIs and Backend
    "REST API": ["rest api", "restful api", "rest apis"],
    "API Development": ["api development", "developing apis"],
    "Model Deployment": [
        "model deployment", "deploying models",
        "deploy machine learning models",
        "deployment of models"
    ],

    # Other Technical Skills
    "Data Structures": ["data structures"],
    "Algorithms": ["algorithms", "algorithm design"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Version Control": ["version control"],
    "Cloud Computing": ["cloud computing"],
}


def normalize_text(text):
    """Normalize text for consistent skill matching."""

    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_phrase(text, phrase):
    """Check for a complete word or phrase."""

    text = normalize_text(text)
    phrase = normalize_text(phrase)

    if not text or not phrase:
        return False

    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(phrase)
        + r"(?![a-zA-Z0-9])"
    )

    return bool(re.search(pattern, text))


def extract_skills(text, infer_related=True):
    """
    Extract recognized technical skills from text.

    infer_related=True:
        Also detects related skills such as SQL from MySQL.

    infer_related=False:
        Detects only explicitly mentioned skills.
        This is used when identifying alternative skill groups.
    """

    text = normalize_text(text)

    if not text:
        return []

    found_skills = set()

    for skill, keywords in SKILL_DATABASE.items():

        for keyword in keywords:

            if contains_phrase(text, keyword):
                found_skills.add(skill)
                break

    if infer_related:

        # Relational databases also indicate SQL knowledge.
        relational_databases = {
            "MySQL",
            "PostgreSQL",
            "SQLite"
        }

        if found_skills.intersection(relational_databases):
            found_skills.add("SQL")

        # REST API indicates API development knowledge.
        # Flask and FastAPI alone are not used for this inference.
        if "REST API" in found_skills:
            found_skills.add("API Development")

    return sorted(found_skills)


def canonicalize_skills(skills):
    """Convert skill names into official display names."""

    canonical_map = {
        skill.lower(): skill
        for skill in SKILL_DATABASE
    }

    result = set()

    if not skills:
        return result

    for skill in skills:

        if not skill:
            continue

        cleaned = str(skill).strip()

        canonical = canonical_map.get(
            cleaned.lower(),
            cleaned
        )

        result.add(canonical)

    return result


def compare_skills(resume_skills, job_skills):
    """Compare resume skills with job description skills."""

    resume_set = canonicalize_skills(resume_skills)
    job_set = canonicalize_skills(job_skills)

    matched = sorted(
        resume_set.intersection(job_set)
    )

    missing = sorted(
        job_set - resume_set
    )

    extra = sorted(
        resume_set - job_set
    )

    percentage = (
        len(matched) / len(job_set) * 100
        if job_set else 0
    )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "match_percentage": round(percentage, 2)
    }


def extract_alternative_groups(lines):
    """
    Detect alternative skills mentioned using 'or'.

    Examples:
        TensorFlow or PyTorch
        Flask or FastAPI
        Power BI or Tableau
        AWS or Azure

    Each group represents one requirement.

    Important:
        Related skills are not automatically inferred here.
        Only explicitly mentioned alternatives are included.
    """

    alternative_groups = []
    seen_groups = set()

    for line in lines:

        if not re.search(r"\bor\b", line, re.IGNORECASE):
            continue

        alternatives = re.split(
            r"\bor\b",
            line,
            flags=re.IGNORECASE
        )

        group = set()

        for alternative in alternatives:

            # Disable related-skill inference so that
            # Flask or FastAPI does not become
            # API Development or Flask or FastAPI.
            detected = set(
                extract_skills(
                    alternative,
                    infer_related=False
                )
            )

            group.update(detected)

        if len(group) >= 2:

            canonical_group = sorted(
                canonicalize_skills(group)
            )

            group_key = frozenset(canonical_group)

            if group_key not in seen_groups:

                alternative_groups.append(canonical_group)
                seen_groups.add(group_key)

    return alternative_groups


def extract_job_skills(job_description):
    """
    Extract all job skills and classify them into
    required and preferred categories.

    Also identifies alternative skill groups.
    """

    if not isinstance(job_description, str):
        job_description = ""

    all_skills = set(
        extract_skills(job_description)
    )

    preferred_headings = {
        "preferred skills",
        "preferred qualifications",
        "good to have",
        "nice to have",
        "bonus skills",
        "additional skills",
        "optional skills"
    }

    required_headings = {
        "required skills",
        "required qualifications",
        "must have skills",
        "must-have skills",
        "essential skills"
    }

    other_headings = {
        "responsibilities",
        "job responsibilities",
        "job overview",
        "overview",
        "requirements",
        "qualifications",
        "educational qualification",
        "education",
        "what we offer",
        "ideal candidate",
        "about the role",
        "about the job"
    }

    required_lines = []
    preferred_lines = []

    current_section = None
    has_required_section = False

    for line in job_description.splitlines():

        cleaned_line = line.strip().lower()

        # Remove Markdown heading and bullet characters.
        cleaned_line = re.sub(
            r"^[\s#>*\-]+",
            "",
            cleaned_line
        )

        cleaned_line = cleaned_line.strip("* ").strip()
        cleaned_line = cleaned_line.rstrip(":").strip()

        if cleaned_line in preferred_headings:

            current_section = "preferred"
            continue

        if cleaned_line in required_headings:

            current_section = "required"
            has_required_section = True
            continue

        if cleaned_line in other_headings:

            current_section = None
            continue

        if current_section == "required":
            required_lines.append(line)

        elif current_section == "preferred":
            preferred_lines.append(line)

    # Extract skills from individual sections.
    preferred_skills = set(
        extract_skills(
            "\n".join(preferred_lines)
        )
    )

    if has_required_section:

        required_skills = set(
            extract_skills(
                "\n".join(required_lines)
            )
        )

    else:

        # Fallback when no explicit Required Skills section exists.
        required_skills = (
            all_skills - preferred_skills
        )

    # A skill should not belong to both categories.
    required_skills.difference_update(
        preferred_skills
    )

    # Detect alternatives separately for ATS analysis.
    required_alternative_groups = (
        extract_alternative_groups(required_lines)
    )

    preferred_alternative_groups = (
        extract_alternative_groups(preferred_lines)
    )

    return {
        "all_skills": sorted(all_skills),

        "required_skills": sorted(required_skills),

        "preferred_skills": sorted(preferred_skills),

        "required_alternative_groups": (
            required_alternative_groups
        ),

        "preferred_alternative_groups": (
            preferred_alternative_groups
        )
    }
