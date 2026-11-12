
import re


ACTION_VERBS = [
    "developed",
    "designed",
    "implemented",
    "created",
    "built",
    "analyzed",
    "automated",
    "managed",
    "optimized",
    "integrated",
    "tested",
    "deployed",
    "contributed",
    "implemented",
    "applied",
    "configured",
    "maintained",
    "evaluated",
    "processed"
]


def enhance_bullet_point(original_text):

    original_text = original_text.strip()

    if not original_text:
        return {
            "original": "",
            "enhanced": "",
            "tips": ["Please enter a resume bullet point."]
        }

    cleaned_text = re.sub(
        r"\s+",
        " ",
        original_text
    ).strip()

    enhanced_text = cleaned_text

    # 1. IMPROVE COMMON WEAK PHRASES

    replacements = [
        (
            r"^worked on a project using ",
            "Contributed to a project using "
        ),
        (
            r"^worked on ",
            "Contributed to "
        ),
        (
            r"^used ",
            "Applied "
        ),
        (
            r"^made ",
            "Created "
        ),
        (
            r"^helped with ",
            "Assisted with "
        ),
        (
            r"^did ",
            "Performed "
        ),
        (
            r"^was responsible for ",
            "Managed "
        ),
        (
            r"^responsible for ",
            "Managed "
        )
    ]

    for pattern, replacement in replacements:

        if re.search(pattern, enhanced_text, re.IGNORECASE):

            enhanced_text = re.sub(
                pattern,
                replacement,
                enhanced_text,
                count=1,
                flags=re.IGNORECASE
            )

            break

    # 2. CHECK ACTION VERBS

    first_word = enhanced_text.split()[0].lower().strip(".,:")

    has_action_verb = first_word in ACTION_VERBS

    # 3. GENERATE IMPROVEMENT TIPS

    tips = []

    words = cleaned_text.split()

    if len(words) < 8:

        tips.append(
            "Add more details about your responsibilities and technologies."
        )

    if not re.search(r"\b\d+(?:\.\d+)?%?\b", cleaned_text):

        tips.append(
            "Include measurable results if you have genuine figures."
        )

    if not has_action_verb:

        tips.append(
            "Start your bullet point with a strong action verb."
        )

    if not re.search(
        r"\b(using|with|through|in|for)\b",
        cleaned_text,
        re.IGNORECASE
    ):

        tips.append(
            "Mention the tools, programming languages or technologies used."
        )

    tips.append(
        "Explain your actual contribution and the outcome of your work."
    )

    # REMOVE DUPLICATE TIPS

    tips = list(dict.fromkeys(tips))

    return {
        "original": original_text,
        "enhanced": enhanced_text,
        "tips": tips
    }
