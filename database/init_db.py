from database.db import engine, Base
import models  # important

def init_db():
    Base.metadata.create_all(bind=engine)