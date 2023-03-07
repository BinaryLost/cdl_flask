from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://hag:hagisgood@localhost/cdl')
Session = sessionmaker(bind=engine)
session = Session()

session.execute(text('TRUNCATE TABLE category_image'))

session.commit()
