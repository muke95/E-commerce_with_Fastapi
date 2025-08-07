from db.database import engine
from model.models import  Base # this ensures all models are registered

Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully.")
