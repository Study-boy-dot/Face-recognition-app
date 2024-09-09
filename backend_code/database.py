import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load .env environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')  # This should be in the format: 'mysql+pymysql://username:password@host/dbname'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class InferenceResult(Base):
    __tablename__ = 'inference_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    boxes = Column(Text)
    keypoints = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def push_result_to_db(boxes, keypoints):
    try:
        new_result = InferenceResult(
            boxes=str(boxes),  # Converting to string for storage
            keypoints=str(keypoints)  # Converting to string for storage
        )
        session.add(new_result)
        session.commit()
        logger.info("Inference result saved to database successfully.")
    except Exception as e:
        logger.error(f"Error saving result to database: {e}")
        session.rollback()

