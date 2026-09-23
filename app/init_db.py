from app.database.connection import engine
from app.database.base import Base
from app.models.job import Job


Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")