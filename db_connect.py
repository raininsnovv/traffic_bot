from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///bot.db')
db = scoped_session(sessionmaker(bind=engine))

# db.execute(
#     text(
#         f'CREATE TABLE addresses ('
#         f'user_id INTEGER NOT NULL UNIQUE,'
#         f'home VARCHAR NOT NULL,'
#         f'job VARCHAR NOT NULL);'
#     )
# )
