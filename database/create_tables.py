from database.connection import engine, Base
from database.models import Question, Variation


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")