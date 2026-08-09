import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# TECHNICAL SKILLS
# =========================================================

SKILLS = [
    "python",
    "r",
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
    "statistical analysis",
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
    "flask",
    "django",
    "fastapi",
    "docker",
    "aws",
    "azure",
    "gcp",
    "react",
    "node.js",
    "express",
    "html",
    "css",
    "javascript",
    "typescript",
    "linux",
    "rest api",
    "api",
    "gitlab",
]


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {

    "statistics": [
        "statistics",
        "statistical modeling",
        "statistical analysis",
        "statistical methods"
    ],

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "data analysis": [
        "data analysis",
        "data analytics"
    ],

    "data science": [
        "data science",
        "data scientist"
    ],

    "python": [
        "python",
        "python programming"
    ],

    "scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ]
}


# =========================================================
# EDUCATION REQUIREMENTS
# =========================================================

EDUCATION_TERMS = [

    "bachelor's degree",
    "bachelors degree",
    "bachelor degree",
    "advanced degree",
    "computer science",
    "statistics",
    "mathematics",
    "related discipline"
]


# =========================================================
# ROLE / SOFT-SKILL REQUIREMENTS
# =========================================================

ROLE_REQUIREMENTS = [

    "analytical",
    "analytical skills",
    "problem solving",
    "problem-solving",
    "cross-functional",
    "cross functional",
    "actionable insights",
    "data-driven",
    "data driven",
    "strategic thinking",
    "mentorship",
    "mentor",
    "business problems"
]


# =========================================================
# PROJECT / EXPERIENCE TERMS
# =========================================================

EXPERIENCE_TERMS = [

    "data science projects",
    "data science project",
    "machine learning projects",
    "machine learning project",
    "data science",
    "machine learning",
    "statistical modeling",
    "data analysis",
    "actionable insights",
    "analytical solutions"
]


# =========================================================
# TEXT MATCHING HELPER
# =========================================================

def contains_term(text, term):

    pattern = (
        r"(?<!\w)"
        + re.escape(term.lower())
        + r"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            text.lower()
        )
    )


# =========================================================
# SKILL EXTRACTION
# =========================================================

def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        if contains_term(text, skill):

            found_skills.append(skill)

    return found_skills


# =========================================================
# NORMALIZED SKILL EXTRACTION
# =========================================================

def extract_normalized_skills(text):

    found_skills = set()

    # Check aliases first
    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_term(text, alias):

                found_skills.add(
                    canonical_skill
                )

                break

    # Check normal skills
    for skill in SKILLS:

        if contains_term(text, skill):

            found_skills.add(skill)

    return sorted(found_skills)


# =========================================================
# SECTION DETECTION
# =========================================================

def detect_sections(text):

    lines = [
        line.strip().lower()
        for line in text.splitlines()
    ]

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
            "skills",
            "technical skill"
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

                found_sections.append(
                    section
                )

                break

    return found_sections


# =========================================================
# CONTACT INFORMATION
# =========================================================

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


# =========================================================
# BASE RESUME QUALITY
# =========================================================

def calculate_ats_score(text):

    score = 0

    skills = extract_skills(text)

    sections = detect_sections(text)

    email_found, phone_found = (
        check_contact_information(text)
    )

    # Skills = 40
    score += min(
        len(skills) * 2,
        40
    )

    # Sections = 30
    score += min(
        len(sections) * 3,
        30
    )

    # Contact = 20
    if email_found:
        score += 10

    if phone_found:
        score += 10

    # Content = 10
    word_count = len(text.split())

    if word_count >= 300:

        score += 10

    elif word_count >= 150:

        score += 5

    return min(score, 100)


# =========================================================
# TF-IDF SIMILARITY
# =========================================================

def calculate_job_match(
    resume_text,
    job_description
):

    if not job_description.strip():

        return 0

    documents = [

        resume_text.lower(),

        job_description.lower()
    ]

    vectorizer = TfidfVectorizer(

        stop_words="english",

        ngram_range=(1, 2),

        max_features=5000,

        sublinear_tf=True
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(

        matrix[0:1],

        matrix[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


# =========================================================
# REQUIREMENT MATCHING
# =========================================================

def match_requirements(
    resume_text,
    job_description,
    requirements
):

    matched = []

    missing = []

    for requirement in requirements:

        if contains_term(
            job_description,
            requirement
        ):

            if contains_term(
                resume_text,
                requirement
            ):

                matched.append(
                    requirement
                )

            else:

                missing.append(
                    requirement
                )

    return matched, missing


# =========================================================
# TECHNICAL SKILL MATCH
# =========================================================

def analyze_technical_skills(
    resume_text,
    job_description
):

    resume_skills = set(
        extract_normalized_skills(
            resume_text
        )
    )

    job_skills = set(
        extract_normalized_skills(
            job_description
        )
    )

    matched = sorted(
        resume_skills.intersection(
            job_skills
        )
    )

    missing = sorted(
        job_skills - resume_skills
    )

    if job_skills:

        score = (
            len(matched)
            / len(job_skills)
        ) * 100

    else:

        score = 0

    return {

        "resume_skills":
            sorted(resume_skills),

        "job_skills":
            sorted(job_skills),

        "matched":
            matched,

        "missing":
            missing,

        "score":
            round(score, 2)
    }


# =========================================================
# EDUCATION MATCH
# =========================================================

def calculate_education_match(
    resume_text,
    job_description
):

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    matched = []
    missing = []

    # -------------------------------------------------
    # Degree requirement
    # -------------------------------------------------

    degree_terms = [
        "bachelor's degree",
        "bachelors degree",
        "bachelor degree",
        "b.tech",
        "btech",
        "b.e",
        "b.e.",
        "undergraduate"
    ]

    has_degree_requirement = any(
        contains_term(job_description, term)
        for term in degree_terms
    )

    degree_match = any(
        contains_term(resume_text, term)
        for term in degree_terms
    )

    if has_degree_requirement:

        if degree_match:
            matched.append(
                "Bachelor's degree"
            )
        else:
            missing.append(
                "Bachelor's degree"
            )

    # -------------------------------------------------
    # Field of study
    # -------------------------------------------------

    field_terms = [
        "computer science",
        "statistics",
        "mathematics"
    ]

    job_fields = [
        term
        for term in field_terms
        if contains_term(
            job_description,
            term
        )
    ]

    matched_fields = [
        term
        for term in job_fields
        if contains_term(
            resume_text,
            term
        )
    ]

    if matched_fields:

        matched.extend(
            matched_fields
        )

    elif job_fields:

        missing.append(
            "Relevant degree field"
        )

    # -------------------------------------------------
    # Calculate score
    # -------------------------------------------------

    total_requirements = 0

    satisfied = 0

    if has_degree_requirement:

        total_requirements += 1

        if degree_match:
            satisfied += 1

    if job_fields:

        total_requirements += 1

        if matched_fields:
            satisfied += 1

    if total_requirements == 0:

        return 0, [], []

    score = (
        satisfied /
        total_requirements
    ) * 100

    return (
        round(score, 2),
        matched,
        missing
    )
# =========================================================
# EXPERIENCE / PROJECT MATCH
# =========================================================

def calculate_experience_match(
    resume_text,
    job_description
):

    job_terms = [

        term

        for term in EXPERIENCE_TERMS

        if contains_term(
            job_description,
            term
        )
    ]

    if not job_terms:

        return 0, [], []

    matched = [

        term

        for term in job_terms

        if contains_term(
            resume_text,
            term
        )
    ]

    missing = [

        term

        for term in job_terms

        if term not in matched
    ]

    score = (
        len(matched)
        / len(job_terms)
    ) * 100

    return (
        round(score, 2),
        matched,
        missing
    )


# =========================================================
# ROLE / SOFT SKILL MATCH
# =========================================================

def calculate_role_match(
    resume_text,
    job_description
):

    job_terms = [

        term

        for term in ROLE_REQUIREMENTS

        if contains_term(
            job_description,
            term
        )
    ]

    if not job_terms:

        return 0, [], []

    matched = [

        term

        for term in job_terms

        if contains_term(
            resume_text,
            term
        )
    ]

    missing = [

        term

        for term in job_terms

        if term not in matched
    ]

    score = (
        len(matched)
        / len(job_terms)
    ) * 100

    return (
        round(score, 2),
        matched,
        missing
    )


# =========================================================
# KEYWORD MATCH
# =========================================================

def calculate_keyword_match(
    resume_text,
    job_description
):

    important_terms = [

        "python",

        "r",

        "machine learning",

        "statistical modeling",

        "statistics",

        "data analysis",

        "data science",

        "problem solving",

        "analytical",

        "computer science",

        "mathematics",

        "cross-functional",

        "projects",

        "actionable insights"
    ]

    job_terms = [

        term

        for term in important_terms

        if contains_term(
            job_description,
            term
        )
    ]

    if not job_terms:

        return 0

    matched = [

        term

        for term in job_terms

        if contains_term(
            resume_text,
            term
        )
    ]

    return round(
        (
            len(matched)
            / len(job_terms)
        ) * 100,
        2
    )


# =========================================================
# V4 FINAL SCORE
# =========================================================

def calculate_final_score(

    resume_quality,

    technical_score,

    education_score,

    experience_score,

    role_score,

    keyword_score,

    semantic_score
):

    final_score = (

    resume_quality * 0.15

    + technical_score * 0.30

    + education_score * 0.15

    + experience_score * 0.15

    + role_score * 0.05

    + keyword_score * 0.10

    + semantic_score * 0.10
)

    return round(
        final_score,
        2
    )


# =========================================================
# MAIN ANALYZER
# =========================================================

def analyze_resume(
    text,
    job_description=""
):

    # =====================================================
    # BASIC RESUME ANALYSIS
    # =====================================================

    skills = extract_skills(text)

    sections = detect_sections(text)

    email_found, phone_found = (
        check_contact_information(text)
    )

    base_score = calculate_ats_score(text)

    strengths = []

    improvements = []

    # Skills
    if len(skills) >= 10:

        strengths.append(
            "Strong technical skill coverage."
        )

    elif len(skills) >= 5:

        strengths.append(
            "Good technical skill coverage."
        )

    else:

        improvements.append(
            "Add more relevant technical skills."
        )

    # Sections
    if len(sections) >= 6:

        strengths.append(
            "Resume contains most important sections."
        )

    else:

        improvements.append(
            "Add missing standard resume sections."
        )

    # Email
    if email_found:

        strengths.append(
            "Email address detected."
        )

    else:

        improvements.append(
            "Add a professional email address."
        )

    # Phone
    if phone_found:

        strengths.append(
            "Phone number detected."
        )

    else:

        improvements.append(
            "Add a valid phone number."
        )

    # Projects
    if "projects" in sections:

        strengths.append(
            "Projects section detected."
        )

    else:

        improvements.append(
            "Add a projects section."
        )

    # Education
    if "education" in sections:

        strengths.append(
            "Education section detected."
        )

    else:

        improvements.append(
            "Add an education section."
        )


    # =====================================================
    # DEFAULT JOB RESULTS
    # =====================================================

    job_match = 0

    technical_score = 0

    education_score = 0

    experience_score = 0

    role_score = 0

    keyword_score = 0

    matched_skills = []

    missing_skills = []

    matched_education = []

    missing_education = []

    matched_experience = []

    missing_experience = []

    matched_role = []

    missing_role = []


    # =====================================================
    # JOB ANALYSIS
    # =====================================================

    if job_description.strip():

        # TF-IDF
        job_match = calculate_job_match(

            text,

            job_description
        )


        # Technical skills
        technical = analyze_technical_skills(

            text,

            job_description
        )

        technical_score = technical["score"]

        matched_skills = technical["matched"]

        missing_skills = technical["missing"]


        # Education
        (
            education_score,
            matched_education,
            missing_education
        ) = calculate_education_match(

            text,

            job_description
        )


        # Experience / projects
        (
            experience_score,
            matched_experience,
            missing_experience
        ) = calculate_experience_match(

            text,

            job_description
        )


        # Role requirements
        (
            role_score,
            matched_role,
            missing_role
        ) = calculate_role_match(

            text,

            job_description
        )


        # Keywords
        keyword_score = calculate_keyword_match(

            text,

            job_description
        )


        # Final score
        final_score = calculate_final_score(

            base_score,

            technical_score,

            education_score,

            experience_score,

            role_score,

            keyword_score,

            job_match
        )

    else:

        final_score = base_score


    # =====================================================
    # RETURN RESULTS
    # =====================================================

    return {

        # Overall
        "score":
            final_score,

        "base_score":
            base_score,

        # Existing
        "skills":
            skills,

        "sections":
            sections,

        "strengths":
            strengths,

        "improvements":
            improvements,

        # Job similarity
        "job_match":
            job_match,

        # Technical
        "skill_match":
            technical_score,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        # Education
        "education_match":
            education_score,

        "matched_education":
            matched_education,

        "missing_education":
            missing_education,

        # Experience
        "experience_match":
            experience_score,

        "matched_experience":
            matched_experience,

        "missing_experience":
            missing_experience,

        # Role
        "role_match":
            role_score,

        "matched_role":
            matched_role,

        "missing_role":
            missing_role,

        # Keywords
        "keyword_match":
            keyword_score
    }