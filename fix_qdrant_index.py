import os
from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "ai_tutor_docs")

def fix_index():
    print(f"Connecting to Qdrant at {QDRANT_URL}...")
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY or None,
        verify=False
    )
    
    print(f"Creating 'keyword' index for field 'subject' in collection '{QDRANT_COLLECTION}'...")
    try:
        client.create_payload_index(
            collection_name=QDRANT_COLLECTION,
            field_name="subject",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        print("✅ Index created successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_index()
