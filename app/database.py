from sqlalchemy import create_engine
# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings



# this changes with each project - rest is copy and paste
SQLalchemy_Database_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLalchemy_Database_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect( host='localhost', database='fastapi',user='postgres',
#                                 password='Aberdeen12', cursor_factory=RealDictCursor )
#         cursor=conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)
#         exit        


