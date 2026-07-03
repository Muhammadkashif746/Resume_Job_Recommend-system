from flask import Flask, render_template, request
from pymongo import MongoClient
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# MongoDB Atlas Connection
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://kashifcodes01_db_user:Kashif123456@cluster0.f4df4oo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Database
db = client["resume_job_recommender"]

# Collections
jobs_collection = db["jobs"]

# Upload Folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# HOME PAGE
@app.route('/')
def home():
    return render_template("index.html")


# SEARCH PAGE
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        skill = request.form['skill'].strip()
        results = jobs_collection.find({
            "required_skills": {
                "$regex": skill,
                "$options": "i"
            }
        }).limit(10)
    return render_template(
        "search.html",
        jobs=results
    )


# RESUME UPLOAD
@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file = request.files['resume']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Extract text from PDF
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        # Skills List
        skills_list = [
            "python", "java", "html", "css", "javascript",
            "react", "nodejs", "sql", "mongodb", "flask",
            "django", "aws", "docker", "git", "github",
            "c++", "php", "bootstrap", "tailwind", "mysql"
        ]

        extracted_skills = []
        for skill in skills_list:
            if skill.lower() in text.lower():
                extracted_skills.append(skill)

        print("\n=== DEBUG: RESUME SKILLS EXTRACTION ===")
        print(f"Extracted Resume Skills: {extracted_skills}")
        print("========================================\n")

        recommendations = []
        resume_skills = [skill.lower() for skill in extracted_skills]

        for job in jobs_collection.find():
            job_skills = [
                skill.lower()
                for skill in job.get("required_skills", [])
            ]

            matched = set(resume_skills) & set(job_skills)

            if len(job_skills) > 0:
                score = int((len(matched) / len(job_skills)) * 100)
            else:
                score = 0

            # Debugging prints for each job as requested
            print("--- DEBUG: JOB EVALUATION ---")
            print(f"Complete Job Document: {job}")
            print(f"Required Skills: {job_skills}")
            print(f"Matched Skills: {list(matched)}")
            print(f"Score: {score}%")
            print("-----------------------------\n")

            if score > 0:
                recommendations.append({
                    "job_title": job.get("job_title", "N/A"),
                    "company": job.get("company", "N/A"),
                    "score": score,
                    "matched_skills": list(matched),
                    "location": job.get("location", "N/A"),
                    "salary": job.get("salary", "N/A"),
                    "employment_type": job.get("employment_type", "N/A")
                })

        recommendations = sorted(
            recommendations,
            key=lambda x: x["score"],
            reverse=True
        )

        print("=== DEBUG: RECOMMENDATION SUMMARY ===")
        print(f"Total Recommendations Found: {len(recommendations)}")
        print("======================================\n")

        return render_template(
            "recommend.html",
            student={
                "name": "Resume User",
                "skills": extracted_skills
            },
            recommendations=recommendations[:10]
        )

    return render_template("upload_resume.html")


# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)