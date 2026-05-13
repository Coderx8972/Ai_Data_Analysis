from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
# Create A Engine
engine = create_engine("sqlite:///library.db",echo= True)

# Create A Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False
)

# Function to create the database
def init_db():
    Base.metadata.create_all(bind=engine)