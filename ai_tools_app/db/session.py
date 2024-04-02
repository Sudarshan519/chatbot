 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

from ai_tools_app.core.config import settings
from typing import Generator            #new

SQLALCHEMY_DATABASE_URL = settings.SQLITE_URL
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_PYTHON
# SQLALCHEMY_DATABASE_URL=settings.POSTGRES_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread': False})#connect_args={'check_same_thread': False})
 

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
 


def get_db() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    except:
        pass
 
    else:
        pass
    finally:
        db.close()


async def commit_rollback():
    try:
        await get_db.commit()
    except Exception:
        await get_db.rollback()
        raise
db=SessionLocal()