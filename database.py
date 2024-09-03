from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from utils import generate_unique_code

engine = create_engine("sqlite:///mydb")
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    original_link = Column(String(500), nullable=False)
    short_code = Column(String(5), nullable=False, unique=True)

    @classmethod
    def link_generation(cls, o_link):
        link = session.query(Link).filter(Link.original_link == o_link).one_or_none()
        if link:
            return link
        code = generate_unique_code()
        new_link = Link(original_link=o_link, short_code=code)
        session.add(new_link)
        session.commit()
        return new_link

    @classmethod
    def get_link_by_code(cls, code):
        link = session.query(Link).filter(Link.short_code == code).one_or_none()
        return link

    @classmethod
    def get_links_by_id(cls, id_lst):
        links = session.query(Link).filter(Link.id.in_(id_lst)).all()
        return links

    def to_json(self, host):
        return {'original_link': self.original_link, 'short_link': f'{host}/{self.short_code}'}
