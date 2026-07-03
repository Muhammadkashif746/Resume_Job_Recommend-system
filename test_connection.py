from pymongo import MongoClient

# MongoDB Atlas Connection
client = MongoClient(
    "mongodb+srv://kashifcodes01_db_user:Kashif123456@cluster0.f4df4oo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    serverSelectionTimeoutMS=5000
)

# Database
db = client["resume_job_recommender"]

try:
    # Trigger connection to verify
    client.admin.command('ping')
    print("MongoDB Atlas Connected Successfully!")
except Exception as e:
    print(f"MongoDB Atlas Connection Failed: {e}")