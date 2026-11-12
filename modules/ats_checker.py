
import re

from modules.skill_extractor import (
    extract_skills,
    extract_job_skills,
    canonicalize_skills
)


# =========================================================
# ACTION VERB DICTIONARY
# =========================================================

ACTION_VERB_FORMS = {
    "develop": ["develop", "developed", "developing", "develops"],
    "create": ["create", "created", "creating", "creates"],
    "design": ["design", "designed", "designing", "designs"],
    "build": ["build", "built", "building", "builds"],
    "implement": ["implement", "implemented", "implementing", "implements"],
    "manage": ["manage", "managed", "managing", "manages"],
    "improve": ["improve", "improved", "improving", "improves"],
    "analyze": ["analyze", "analyzed", "analyzing", "analyses", "analysed"],
    "automate": ["automate", "automated", "automating", "automates"],
    "optimize": ["optimize", "optimized", "optimizing", "optimises", "optimised"],
    "program": ["program", "programmed", "programming", "programs"],
    "deploy": ["deploy", "deployed", "deploying", "deploys"],
    "integrate": ["integrate", "integrated", "integrating", "integrates"],
    "test": ["test", "tested", "testing", "tests"],
    "lead": ["lead", "led", "leading", "leads"],
    "achieve": ["achieve", "achieved", "achieving", "achieves"],
    "increase": ["increase", "increased", "increasing", "increases"],
    "reduce": ["reduce", "reduced", "reducing", "reduces"],
    "organize": ["organize", "organized", "organizing", "organises", "organised"],
    "conduct": ["conduct", "conducted", "conducting", "conducts"],
    "engineer": ["engineer", "engineered", "engineering", "engineers"],
    "deliver": ["deliver", "delivered", "delivering", "delivers"],
    "generate": ["generate", "generated", "generating", "generates"],
    "maintain": ["maintain", "maintained", "maintaining", "maintains"],
    "streamline": ["streamline", "streamlined", "streamlining"],
    "evaluate": ["evaluate", "evaluated", "evaluating", "evaluates"],
    "configure": ["configure", "configured", "configuring", "configures"],
    "train": ["train", "trained", "training", "trains"],
    "execute": ["execute", "executed", "executing", "executes"],
    "research": ["research", "researched", "researching"],
    "solve": ["solve", "solved", "solving", "solves"],
    "process": ["process", "processed", "processing", "processes"],
    "support": ["support", "supported", "supporting", "supports"],
    "collaborate": ["collaborate", "collaborated", "collaborating"],
    "contribute": ["contribute", "contributed", "contributing"],
    "monitor": ["monitor", "monitored", "monitoring"],
    "secure": ["secure", "secured", "securing"]
}


# =========================================================
# ADDITIONAL JOB KEYWORDS
# =========================================================

EXTRA_KEYWORDS = [
    "data collection",
    "business analysis",
    "dashboard",
    "reporting",
    "pivot tables",
    "model evaluation",
    "model training",
    "predictive modeling",
    "predictive modelling",
    "version control",
    "cloud computing"
]


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    """Normalize text for consistent keyword matching."""

    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_phrase(text, phrase):
    """Check whether a complete word or phrase exists."""

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


def keyword_key(keyword):
    """Normalize a keyword for duplicate detection."""

    return re.sub(
        r"[^a-z0-9]+",
        " ",
        normalize_text(keyword)
    ).strip()


# =========================================================
# EXTRA KEYWORD EXTRACTION
# =========================================================

def extract_extra_keywords(job_description):
    """Find additional job-related keywords."""

    found = set()

    for phrase in EXTRA_KEYWORDS:

        if contains_phrase(job_description, phrase):
            found.add(phrase)

    return found


# =========================================================
# QUANTIFIED ACHIEVEMENT CHECKER
# =========================================================

def check_quantified_achievements(resume_text):
    """
    Detect measurable achievements such as percentages,
    quantities and numerical improvements.
    """

    patterns = [
        r"\b\d+(?:\.\d+)?\s*%",
        (
            r"\b\d+(?:\.\d+)?\s*"
            r"(?:users|customers|records|datasets|projects|"
            r"employees|clients|seconds|minutes|hours|days|"
            r"months|years)\b"
        ),
        (
            r"\b(?:increased|improved|reduced|decreased|"
            r"achieved|saved|generated|processed|managed|"
            r"handled|boosted)\b.{0,60}\b\d+(?:\.\d+)?\b"
        )
    ]

    text = normalize_text(resume_text)

    return any(
        re.search(pattern, text)
        for pattern in patterns
    )


# =========================================================
# ACTION VERB ANALYSIS
# =========================================================

def find_action_verbs(resume_text):
    """Find unique base action verbs in the resume."""

    text = normalize_text(resume_text)

    found = []

    for base_verb, forms in ACTION_VERB_FORMS.items():

        if any(
            contains_phrase(text, form)
            for form in forms
        ):
            found.append(base_verb)

    return sorted(found)


# =========================================================
# SKILL REQUIREMENT EVALUATION
# =========================================================

def evaluate_skill_category(
    resume_skills,
    category_skills,
    alternative_groups
):
    """
    Calculate skill coverage while treating alternative
    skills as one requirement.

    Example:
        TensorFlow OR PyTorch = one requirement.

    Having either one satisfies that requirement.
    """

    resume_skills = set(
        canonicalize_skills(resume_skills)
    )

    category_skills = set(
        canonicalize_skills(category_skills)
    )

    valid_groups = []

    for group in alternative_groups:

        group = set(
            canonicalize_skills(group)
        )

        group = group.intersection(category_skills)

        if len(group) >= 2:
            valid_groups.append(group)

    # Collect all skills belonging to alternative groups.
    grouped_skills = set()

    for group in valid_groups:
        grouped_skills.update(group)

    # Remaining skills are individual requirements.
    individual_skills = (
        category_skills - grouped_skills
    )

    matched_individual = (
        individual_skills.intersection(resume_skills)
    )

    missing_individual = (
        individual_skills - resume_skills
    )

    matched_groups = []
    missing_groups = []

    matched_group_count = 0

    for group in valid_groups:

        matched_alternatives = group.intersection(
            resume_skills
        )

        if matched_alternatives:

            matched_groups.extend(
                matched_alternatives
            )

            # An alternative group counts as one requirement.
            matched_group_count += 1

        else:

            missing_groups.append(
                " or ".join(sorted(group))
            )

    # Effective requirement counts.
    total_requirements = (
        len(individual_skills) + len(valid_groups)
    )

    matched_requirements = (
        len(matched_individual) + matched_group_count
    )

    missing_requirements = (
        total_requirements - matched_requirements
    )

    score = (
        matched_requirements / total_requirements * 100
        if total_requirements else 0
    )

    matched_skills = sorted(
        matched_individual.union(matched_groups)
    )

    missing_skills = (
        sorted(missing_individual) + sorted(missing_groups)
    )

    return {
        "score": round(score, 2),
        "matched": matched_skills,
        "missing": missing_skills,
        "total": total_requirements,
        "matched_count": matched_requirements,
        "missing_count": missing_requirements
    }


# =========================================================
# MAIN ATS COMPATIBILITY FUNCTION
# =========================================================

def check_ats_compatibility(resume_text, job_description):
    """
    Estimate ATS compatibility using:

    - Required technical skills
    - Preferred technical skills
    - Alternative skill requirements
    - Additional job keywords
    - Unique action verbs
    - Measurable achievements
    - Resume length
    """

    if not isinstance(resume_text, str):
        resume_text = ""

    if not isinstance(job_description, str):
        job_description = ""

    resume_lower = normalize_text(resume_text)

    resume_skills = set(
        canonicalize_skills(
            extract_skills(resume_text)
        )
    )

    job_skill_data = extract_job_skills(
        job_description
    )

    all_job_skills = set(
        job_skill_data["all_skills"]
    )

    required_skills = set(
        job_skill_data["required_skills"]
    )

    preferred_skills = set(
        job_skill_data["preferred_skills"]
    )

    required_groups = job_skill_data.get(
        "required_alternative_groups", []
    )

    preferred_groups = job_skill_data.get(
        "preferred_alternative_groups", []
    )

    # -----------------------------------------------------
    # OVERALL SKILL MATCHING
    # -----------------------------------------------------

    matched_skills = resume_skills.intersection(
        all_job_skills
    )

    missing_skills = (
        all_job_skills - resume_skills
    )

    # -----------------------------------------------------
    # REQUIRED SKILL ANALYSIS
    # -----------------------------------------------------

    required_result = evaluate_skill_category(
        resume_skills,
        required_skills,
        required_groups
    )

    matched_required = set(
        required_result["matched"]
    )

    missing_required = set(
        required_result["missing"]
    )

    required_skill_score = required_result["score"]

    # -----------------------------------------------------
    # PREFERRED SKILL ANALYSIS
    # -----------------------------------------------------

    preferred_result = evaluate_skill_category(
        resume_skills,
        preferred_skills,
        preferred_groups
    )

    matched_preferred = set(
        preferred_result["matched"]
    )

    missing_preferred = set(
        preferred_result["missing"]
    )

    preferred_skill_score = preferred_result["score"]

    # -----------------------------------------------------
    # ADDITIONAL KEYWORD MATCHING
    # -----------------------------------------------------

    required_phrases = extract_extra_keywords(
        job_description
    )

    matched_phrases = {
        phrase
        for phrase in required_phrases
        if contains_phrase(resume_lower, phrase)
    }

    # -----------------------------------------------------
    # OVERALL KEYWORD ANALYSIS
    # -----------------------------------------------------

    all_groups = (
        required_groups + preferred_groups
    )

    grouped_skills = set()
    valid_all_groups = []

    for group in all_groups:

        group = set(
            canonicalize_skills(group)
        )

        group = group.intersection(all_job_skills)

        if len(group) >= 2:

            valid_all_groups.append(group)
            grouped_skills.update(group)

    keyword_entries = {}

    individual_job_skills = (
        all_job_skills - grouped_skills
    )

    # Add individual skills.
    for skill in individual_job_skills:

        keyword_entries[keyword_key(skill)] = {
            "label": skill,
            "matched": skill in resume_skills
        }

    # Add alternative groups as single keyword entries.
    for group in valid_all_groups:

        group_label = " or ".join(sorted(group))

        group_matched = bool(
            group.intersection(resume_skills)
        )

        keyword_entries[keyword_key(group_label)] = {
            "label": group_label,
            "matched": group_matched
        }

    # Add extra keywords without duplicates.
    for phrase in required_phrases:

        key = keyword_key(phrase)

        if key not in keyword_entries:

            keyword_entries[key] = {
                "label": phrase,
                "matched": phrase in matched_phrases
            }

    matched_keywords = sorted(
        entry["label"]
        for entry in keyword_entries.values()
        if entry["matched"]
    )

    missing_keywords = sorted(
        entry["label"]
        for entry in keyword_entries.values()
        if not entry["matched"]
    )

    total_keywords = len(keyword_entries)

    keyword_score = (
        len(matched_keywords) / total_keywords * 100
        if total_keywords else 0
    )

    # -----------------------------------------------------
    # ACTION VERB ANALYSIS
    # -----------------------------------------------------

    found_action_verbs = find_action_verbs(
        resume_text
    )

    action_verb_score = min(
        len(found_action_verbs) / 5 * 100,
        100
    )

    # -----------------------------------------------------
    # ACHIEVEMENT ANALYSIS
    # -----------------------------------------------------

    has_quantified_achievements = (
        check_quantified_achievements(resume_text)
    )

    achievement_score = (
        100 if has_quantified_achievements else 0
    )

    # -----------------------------------------------------
    # RESUME LENGTH ANALYSIS
    # -----------------------------------------------------

    word_count = len(resume_text.split())

    if 200 <= word_count <= 1000:
        length_status = "Good"

    elif word_count < 200:
        length_status = "Too Short"

    else:
        length_status = "Too Long"

    # -----------------------------------------------------
    # WEIGHTED ATS SCORE
    # -----------------------------------------------------

    # Required skills: 70%
    # Preferred skills: 15%
    # Action verbs: 10%
    # Achievements: 5%

    score_components = []

    if required_result["total"] > 0:

        score_components.append(
            (required_skill_score, 70)
        )

    if preferred_result["total"] > 0:

        score_components.append(
            (preferred_skill_score, 15)
        )

    score_components.append(
        (action_verb_score, 10)
    )

    score_components.append(
        (achievement_score, 5)
    )

    total_weight = sum(
        weight
        for score, weight in score_components
    )

    overall_score = (
        sum(
            score * weight
            for score, weight in score_components
        ) / total_weight
        if total_weight else 0
    )

    if length_status in ("Too Short", "Too Long"):
        overall_score -= 5

    overall_score = round(
        max(0, min(overall_score, 100)),
        2
    )

    # -----------------------------------------------------
    # RETURN RESULTS
    # -----------------------------------------------------

    return {
        "ats_score": overall_score,

        "keyword_score": round(
            keyword_score, 2
        ),

        "action_verb_score": round(
            action_verb_score, 2
        ),

        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,

        "found_action_verbs": found_action_verbs,

        "has_quantified_achievements": (
            has_quantified_achievements
        ),

        "word_count": word_count,
        "length_status": length_status,

        "required_skills": sorted(required_skills),
        "preferred_skills": sorted(preferred_skills),

        "matched_required_skills": sorted(matched_required),
        "missing_required_skills": sorted(missing_required),

        "matched_preferred_skills": sorted(matched_preferred),
        "missing_preferred_skills": sorted(missing_preferred),

        "required_skill_score": round(
            required_skill_score, 2
        ),

        "preferred_skill_score": round(
            preferred_skill_score, 2
        ),

        # Effective requirement counts for app.py.
        "required_skill_count": required_result["total"],
        "matched_required_count": required_result["matched_count"],
        "missing_required_count": required_result["missing_count"],

        "preferred_skill_count": preferred_result["total"],
        "matched_preferred_count": preferred_result["matched_count"],
        "missing_preferred_count": preferred_result["missing_count"]
    }
