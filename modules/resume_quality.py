
import re


def check_resume_quality(resume_text):

    text = resume_text.lower()

    checks = {
        "Contact Information": {
            "found": bool(
                re.search(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", text)
                or re.search(r"\b\d{10}\b", text)
            ),
            "description": "Email address or phone number"
        },

        "Education": {
            "found": any(
                word in text
                for word in [
                    "education",
                    "bachelor",
                    "degree",
                    "university",
                    "college",
                    "b.tech",
                    "b.e."
                ]
            ),
            "description": "Education and qualification details"
        },

        "Technical Skills": {
            "found": any(
                word in text
                for word in [
                    "skills",
                    "python",
                    "java",
                    "sql",
                    "machine learning"
                ]
            ),
            "description": "Technical skills and technologies"
        },

        "Projects": {
            "found": any(
                word in text
                for word in [
                    "projects",
                    "project experience",
                    "academic project"
                ]
            ),
            "description": "Academic or personal projects"
        },

        "Work Experience": {
            "found": any(
                word in text
                for word in [
                    "experience",
                    "internship",
                    "employment",
                    "work history"
                ]
            ),
            "description": "Internship or work experience"
        },

        "Certifications": {
            "found": any(
                word in text
                for word in [
                    "certifications",
                    "certificates",
                    "certification"
                ]
            ),
            "description": "Professional certifications"
        }
    }

    total_sections = len(checks)

    completed_sections = sum(
        1 for item in checks.values()
        if item["found"]
    )

    quality_score = round(
        (completed_sections / total_sections) * 100,
        2
    )

    return {
        "checks": checks,
        "completed_sections": completed_sections,
        "total_sections": total_sections,
        "quality_score": quality_score
    }
