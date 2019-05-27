from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:python@localhost:3306/flask_test1')
#获取Base
Base = declarative_base()

#创建模型类
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String(50), nullable=False)
    user_name = Column(String(50), nullable=False)
    head_img = Column(String(200), nullable=True)
    short_description = Column(String(300), nullable=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100))

