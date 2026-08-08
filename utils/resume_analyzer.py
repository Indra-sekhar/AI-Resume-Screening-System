import re


SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "sql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "statistics",
    "statistical modeling",
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",
    "git",
    "github",
    "mysql",
    "oracle",
    "mongodb",
]


SECTIONS = [
    "professional summary",
    "summary",
    "objective",
    "education",
    "technical skills",
    "skills",
    "experience",
    "work experience",
    "projects",
    "certifications",
    "achievements",
]


def extract_skills(text):
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    return found_skills


def detect_sections(text):
    lines = [line.strip().lower() for line in text.splitlines()]

    section_aliases = {
        "summary": [
            "professional summary",
            "summary",
            "objective"
        ],
        "education": [
            "education"
        ],
        "skills": [
            "technical skills",
            "skills"
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience"
        ],
        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],
        "certifications": [
            "certifications",
            "certificates"
        ],
        "achievements": [
            "achievements",
            "accomplishments"
        ]
    }

    found_sections = []

    for section, aliases in section_aliases.items():
        for line in lines:
            if line in aliases:
                found_sections.append(section)
                break

    return found_sections

def check_contact_information(text):
    email = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    phone = re.search(
        r"\+?\d[\d\s()-]{8,}\d",
        text
    )

    return bool(email), bool(phone)


def calculate_ats_score(text):
    score = 0

    skills = extract_skills(text)
    sections = detect_sections(text)
    email_found, phone_found = check_contact_information(text)

    # Skills: 40 points
    skill_score = min(len(skills) * 2, 40)
    score += skill_score

    # Sections: 30 points
    section_score = min(len(sections) * 3, 30)
    score += section_score

    # Contact information: 20 points
    if email_found:
        score += 10

    if phone_found:
        score += 10

    # Resume length/content: 10 points
    word_count = len(text.split())

    if word_count >= 300:
        score += 10
    elif word_count >= 150:
        score += 5

    return min(score, 100)


def analyze_resume(text):

    skills = extract_skills(text)
    sections = detect_sections(text)

    email_found, phone_found = check_contact_information(text)

    score = calculate_ats_score(text)

    strengths = []
    improvements = []

    if len(skills) >= 10:
        strengths.append("Strong technical skill coverage.")
    elif len(skills) >= 5:
        strengths.append("Good technical skill coverage.")
    else:
        improvements.append("Add more relevant technical skills.")

    if len(sections) >= 6:
        strengths.append("Resume contains most important sections.")
    else:
        improvements.append("Add missing standard resume sections.")

    if email_found:
        strengths.append("Email address detected.")
    else:
        improvements.append("Add a professional email address.")

    if phone_found:
        strengths.append("Phone number detected.")
    else:
        improvements.append("Add a valid phone number.")

    if "projects" in sections:
        strengths.append("Projects section detected.")
    else:
        improvements.append("Add a projects section.")

    if "education" in sections:
        strengths.append("Education section detected.")
    else:
        improvements.append("Add an education section.")

    return {
        "score": score,
        "skills": skills,
        "sections": sections,
        "strengths": strengths,
        "improvements": improvements,
    }