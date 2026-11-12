
def generate_suggestions(results):
    """
    Generate concise and personalized resume improvement suggestions
    using skill matching and ATS analysis results.

    Each recommendation section contains a maximum of 5 actions.
    """

    if not isinstance(results, dict):
        results = {}

    # --------------------------------------------------
    # GET SKILL INFORMATION
    # --------------------------------------------------

    matched_skills = results.get(
        "matched_skills",
        results.get("matched_required_skills", [])
    )

    missing_skills = results.get(
        "missing_skills",
        results.get("missing_required_skills", [])
    )

    extra_skills = results.get("extra_skills", [])

    def clean_list(items):
        if not items:
            return []

        if isinstance(items, str):
            return [items.strip()] if items.strip() else []

        return sorted(
            set(
                str(item).strip()
                for item in items
                if str(item).strip()
            )
        )

    matched_skills = clean_list(matched_skills)
    missing_skills = clean_list(missing_skills)
    extra_skills = clean_list(extra_skills)

    suggestions = []

    # ATS information
    ats_score = results.get("ats_score")
    action_verb_score = results.get("action_verb_score")
    has_achievements = results.get("has_quantified_achievements")
    length_status = results.get("length_status")

    # --------------------------------------------------
    # 1. TECHNICAL SKILLS IMPROVEMENT
    # --------------------------------------------------

    if missing_skills:

        priority_skills = missing_skills[:3]

        skill_actions = [
            "Prioritize important missing skills: "
            + ", ".join(priority_skills) + ".",

            "Practise these skills through small hands-on exercises.",

            "Build a mini-project using one or more of the missing technologies.",

            "Prepare technical interview questions related to these skills.",

            "Add skills to your resume only after gaining practical knowledge."
        ]

        suggestions.append({
            "title": "Improve Your Technical Skills",
            "description": (
                f"Your resume is missing {len(missing_skills)} "
                "recognized job-related skills. Focus on the most "
                "important gaps to improve your job relevance."
            ),
            "actions": skill_actions
        })

    else:

        suggestions.append({
            "title": "Great Technical Skill Match!",
            "description": (
                "Your resume contains all recognized technical "
                "skills required by the job description."
            ),
            "actions": [
                "Keep your technical skills section updated.",
                "Demonstrate your skills through practical projects.",
                "Prepare real examples of how you used these technologies.",
                "Practise technical interview questions related to the role."
            ]
        })

    # --------------------------------------------------
    # 2. PROJECT EXPERIENCE IMPROVEMENT
    # --------------------------------------------------

    project_actions = [
        "Include at least two relevant academic or personal projects.",
        "Mention the technologies and frameworks used in each project.",
        "Clearly explain your individual contribution and implementation.",
        "Describe the problem your project solves and its outcome."
    ]

    if missing_skills:
        project_actions.append(
            "Build a project using "
            + ", ".join(missing_skills[:3])
            + " to demonstrate your newly acquired skills."
        )
    else:
        project_actions.append(
            "Include GitHub links or project demonstrations where available."
        )

    suggestions.append({
        "title": "Strengthen Your Project Experience",
        "description": (
            "Projects help recruiters understand how you apply "
            "technical knowledge to solve practical problems."
        ),
        "actions": project_actions
    })

    # --------------------------------------------------
    # 3. HIGHLIGHT MATCHING SKILLS
    # --------------------------------------------------

    if matched_skills:

        highlight_actions = [
            "Highlight your strongest matching technical skills "
            "in the skills section.",

            "Mention relevant technologies naturally in project descriptions.",

            "Explain how you applied these skills in real projects.",

            "Place your most relevant projects near the top of your resume.",

            "Use job-related terminology where it accurately describes your experience."
        ]

        suggestions.append({
            "title": "Highlight Your Relevant Skills",
            "description": (
                f"Your resume already contains {len(matched_skills)} "
                "recognized matching skills. Make these strengths "
                "easy for recruiters to identify."
            ),
            "actions": highlight_actions
        })

    else:

        suggestions.append({
            "title": "Improve Job Relevance",
            "description": (
                "Your resume currently has no recognized technical "
                "skills matching the supplied job description."
            ),
            "actions": [
                "Identify the main technical requirements in the job description.",
                "Review your existing skills and academic experience.",
                "Include relevant projects that demonstrate your abilities.",
                "Update your resume using accurate job-related terminology."
            ]
        })

    # --------------------------------------------------
    # 4. ADDITIONAL SKILLS
    # --------------------------------------------------

    if extra_skills:

        additional_actions = [
            "Highlight useful additional skills such as "
            + ", ".join(extra_skills[:4]) + ".",

            "Explain how you have practically used these technologies.",

            "Connect additional skills to relevant job responsibilities.",

            "Include them in project descriptions where appropriate.",

            "Avoid listing technologies without supporting experience."
        ]

        suggestions.append({
            "title": "Make Use of Your Additional Skills",
            "description": (
                "Your resume contains additional technical skills "
                "that may provide value beyond the direct job requirements."
            ),
            "actions": additional_actions
        })

    else:

        suggestions.append({
            "title": "Expand Your Technical Profile",
            "description": (
                "No additional technical skills were detected "
                "outside the recognized job requirements."
            ),
            "actions": [
                "Explore technologies related to your target job role.",
                "Practise using relevant tools and frameworks.",
                "Build small projects to gain practical experience.",
                "Add newly acquired skills to your resume after practising them."
            ]
        })

    # --------------------------------------------------
    # 5. ATS COMPATIBILITY IMPROVEMENT
    # --------------------------------------------------

    ats_actions = []

    if action_verb_score is not None and action_verb_score < 60:
        ats_actions.append(
            "Start bullet points with strong action verbs such as "
            "Developed, Implemented, Designed and Optimized."
        )
    else:
        ats_actions.append(
            "Continue using clear action verbs to describe your work."
        )

    if has_achievements is False:
        ats_actions.append(
            "Include accurate measurable achievements such as "
            "improvements in accuracy, processing time or project performance."
        )

    if length_status == "Too Short":
        ats_actions.append(
            "Add relevant projects, experience and achievements "
            "without including unnecessary information."
        )

    elif length_status == "Too Long":
        ats_actions.append(
            "Remove repeated information and prioritize content "
            "relevant to the target job."
        )

    if ats_score is not None and ats_score < 75:
        ats_actions.append(
            "Improve missing job-related skills and strengthen "
            "your project descriptions."
        )
    elif ats_score is not None:
        ats_actions.append(
            "Continue tailoring your resume to individual job descriptions."
        )

    ats_actions.append(
        "Use standard headings and a simple ATS-friendly single-column layout."
    )

    suggestions.append({
        "title": "Improve ATS Compatibility",
        "description": (
            "Improve your resume structure, keywords and achievement "
            "descriptions to make important information easier to identify."
        ),
        "actions": ats_actions[:5]
    })

    # --------------------------------------------------
    # 6. RESUME PRESENTATION
    # --------------------------------------------------

    presentation_actions = [
        "Use clear headings such as Education, Skills, Projects and Experience.",
        "Maintain consistent fonts, spacing and formatting.",
        "Keep bullet points short, clear and professionally written.",
        "Check spelling, grammar and contact information.",
        "Use a simple ATS-friendly single-column resume layout."
    ]

    suggestions.append({
        "title": "Improve Resume Presentation",
        "description": (
            "A clear and professional resume helps recruiters "
            "quickly understand your qualifications and experience."
        ),
        "actions": presentation_actions
    })

    return suggestions
