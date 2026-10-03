from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

# Railway/Heroku-style URLs use "postgres://", which SQLAlchemy 2 no longer accepts;
# also pin the psycopg (v3) driver explicitly
database_url = settings.database_url
for prefix in ("postgres://", "postgresql://"):
    if database_url.startswith(prefix):
        database_url = "postgresql+psycopg://" + database_url[len(prefix):]
        break

engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
