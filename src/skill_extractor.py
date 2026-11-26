import re


SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "SQL",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Data Analysis",
    "Data Visualization",
    "Tableau",
    "Power BI",
    "Excel",
    "AWS",
    "Azure",
    "Docker",
    "Git",
    "Linux",
    "PostgreSQL",
    "MongoDB",
    "REST API",
]

SKILL_ALIASES = {
    "JavaScript": ["JavaScript", "JS"],
    "Machine Learning": ["Machine Learning", "ML"],
    "PostgreSQL": ["PostgreSQL", "Postgres"],
    "REST API": ["REST API", "RESTful API", "RESTful APIs"],
    "Scikit-learn": ["Scikit-learn", "sklearn"],
    "Node.js": ["Node.js", "NodeJS"],
    "Artificial Intelligence": ["Artificial Intelligence", "AI"],
}

def extract_skills(text):
    """
    Extract technical skills while filtering some
    negated or aspirational skill mentions.
    """

    found_skills = set()

    exclusion_phrases = [
        "no experience with",
        "no knowledge of",
        "never used",
        "interested in learning",
        "planning to learn",
        "want to learn",
    ]

    for skill in SKILLS:
        aliases = SKILL_ALIASES.get(skill, [skill])

        for alias in aliases:
            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            for match in re.finditer(pattern, text, re.IGNORECASE):

                # Look at the words immediately before the skill
                preceding_text = text[max(0, match.start() - 80):match.start()]
                preceding_text = preceding_text.lower()

                # Check for exclusion phrases
                excluded = any(
                    phrase in preceding_text
                    for phrase in exclusion_phrases
                )

                if not excluded:
                    found_skills.add(skill)
                    break

            if skill in found_skills:
                break

    return sorted(found_skills)


def compare_skills(resume_skills, job_skills):
    """
    Compare resume skills with job requirements.
    """

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matching = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    if job_set:
        coverage = (
            len(matching) / len(job_set)
        ) * 100
    else:
        coverage = 0

    return matching, missing, coverage