import os
from dotenv import load_dotenv

# Load environmental variables from the local .env file into the application context
load_dotenv()

class Config:
    # Explicitly pull the OpenAI API credentials required for localized orchestration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Absolute filesystem path designating the local vector directory for ChromaDB
    VECTOR_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vector_db'))
    
    # Target directory routing path serving as a localized fallback/mock for AWS S3 object storage
    LOCAL_STORAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

    @classmethod
    def validate_config(cls):
        """
        Verify the presence of necessary runtime environmental parameters before bootstrapping the studio.
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "❌ Configuration Error: 'OPENAI_API_KEY' was not found within the active environment runtime or local .env file."
            )