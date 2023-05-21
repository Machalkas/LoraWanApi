from app_energy_meters import models
from database_clients.postgres_client import engine

models.Base.metadata.create_all(bind=engine)
