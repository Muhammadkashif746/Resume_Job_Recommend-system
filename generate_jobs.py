from pymongo import MongoClient
import random

# MongoDB Atlas Connection
client = MongoClient(
    "mongodb+srv://kashifcodes01_db_user:Kashif123456@cluster0.f4df4oo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    serverSelectionTimeoutMS=5000
)

db = client["resume_job_recommender"]
jobs = db["jobs"]

job_titles = [
    "Frontend Developer", "Backend Developer",
    "Python Developer", "Data Analyst",
    "Database Engineer", "Cloud Engineer",
    "Software Engineer", "AI Engineer",
    "Machine Learning Intern", "Full Stack Developer",
    "Web Developer", "Database Administrator",
    "DevOps Engineer", "Cyber Security Analyst",
    "Mobile App Developer", "UI UX Designer",
    "QA Engineer", "System Engineer",
    "Data Scientist", "IT Support Engineer"
]

companies = [
    "TechVision", "SoftSolutions", "CloudCore",
    "DataWorks", "NextGen Systems",
    "CodeCrafters", "Digital Hub",
    "InnovateX", "FutureByte", "SmartTech"
]

locations = [
    "Lahore", "Karachi", "Islamabad",
    "Faisalabad", "Multan",
    "Rawalpindi", "Bahawalpur"
]

skills_pool = [
    "HTML","CSS","JavaScript","React","NodeJS",
    "Python","Java","C++","MongoDB","SQL",
    "MySQL","AWS","Git","Docker","Linux",
    "Machine Learning","Data Analysis",
    "Cyber Security","Networking",
    "PHP","Laravel","Bootstrap"
]

employment_types = [
    "Full Time",
    "Part Time",
    "Internship",
    "Remote",
    "Contract"
]

job_data = []

for i in range(300):
    record = {
        "job_id": i + 1,
        "job_title": random.choice(job_titles),
        "company": random.choice(companies),
        "location": random.choice(locations),
        "required_skills": random.sample(
            skills_pool,
            random.randint(3,7)
        ),
        "salary": random.randint(30000,250000),
        "experience_required": random.randint(0,8),
        "employment_type": random.choice(
            employment_types
        ),
        "minimum_cgpa": round(
            random.uniform(2.0,4.0), 1
        )
    }
    job_data.append(record)

# Clear existing jobs and insert 300 fresh ones
jobs.delete_many({})
jobs.insert_many(job_data)

print("300 Enhanced Job Records Inserted into MongoDB Atlas!")