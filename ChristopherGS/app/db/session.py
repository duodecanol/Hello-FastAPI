from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    # necessary to work with SQLite -
    # this is a common gotcha because FastAPI can access the database
    # with multiple threads during a single request,
    # so SQLite needs to be configured to allow that.
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)