import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.session_logger import get_or_create_user, start_session, log_message, update_topic, end_session

def simulate():
    print("[Simulate] Generating sample data...")
    
    users = [
        {"username": "emma_study", "level": "beginner"},
        {"username": "alex_pro", "level": "advanced"},
    ]
    
    subjects = ["Physics", "Biology", "Chemistry"]
    topics = {
        "Physics": ["Gravity", "Newton's Laws", "Velocity", "Vectors"],
        "Biology": ["DNA", "Mitochondria", "Photosynthesis", "Cell Wall"],
        "Chemistry": ["Atoms", "Mole Concept", "Valency", "Isotopes"]
    }

    for u_info in users:
        user = get_or_create_user(u_info["username"], u_info["level"])
        user_id = user["id"]
        
        # Create 3 sessions per user
        for i in range(3):
            subject = random.choice(subjects)
            session_id = start_session(user_id, subject, u_info["level"], "normal")
            
            # log 3-5 messages per session
            num_msgs = random.randint(3, 5)
            for _ in range(num_msgs):
                topic = random.choice(topics[subject])
                log_message(session_id, "user", f"Tell me about {topic}")
                log_message(session_id, "assistant", f"Here is a brief overview of {topic} based on your level...")
                update_topic(user_id, subject, topic)
            
            end_session(session_id)
            print(f"  [User: {u_info['username']}] Created session for {subject}")

    print("\n✅ Simulation complete! You can now see other users' history in the DB.")

if __name__ == "__main__":
    simulate()
