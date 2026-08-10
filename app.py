from flask import Flask, render_template, request
import os

from utils.pdf_parser import extract_text
from utils.resume_analyzer import analyze_resume


app = Flask(__name__)


UPLOAD_FOLDER = "resumes"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.route("/")
def home():
    print("HOME ROUTE: rendering index.html")
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("resume")

    job_description = request.form.get(
        "job_description",
        ""
    )

    if not file or file.filename == "":

        return "No file selected"


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )


    file.save(filepath)


    # Extract resume text
    resume_text = extract_text(
        filepath
    )


    # Analyze resume
    analysis = analyze_resume(
        resume_text,
        job_description
    )


    # Send results to result.html
    return render_template(
    "result.html",

    filename=file.filename,

    resume_text=resume_text,

    # Scores
    score=analysis["score"],
    base_score=analysis["base_score"],
    job_match=analysis["job_match"],
    skill_match=analysis["skill_match"],
    keyword_match=analysis["keyword_match"],

    # Requirement scores
    education_match=analysis["education_match"],
    experience_match=analysis["experience_match"],
    role_match=analysis["role_match"],

    # Skills
    skills=analysis["skills"],
    matched_skills=analysis["matched_skills"],
    missing_skills=analysis["missing_skills"],

    # Education
    matched_education=analysis["matched_education"],
    missing_education=analysis["missing_education"],

    # Experience
    matched_experience=analysis["matched_experience"],
    missing_experience=analysis["missing_experience"],

    # Role requirements
    matched_role=analysis["matched_role"],
    missing_role=analysis["missing_role"],

    # Resume analysis
    sections=analysis["sections"],
    strengths=analysis["strengths"],
    improvements=analysis["improvements"]
)


if __name__ == "__main__":

    app.run(
        debug=True
    )