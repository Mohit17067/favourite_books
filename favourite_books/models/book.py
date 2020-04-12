from .base import db, BaseMixin

__all__ = ['Book']


class Book(BaseMixin, db.Model):
  
  __tablename__ = 'book'
  
  title = db.Column(db.String(255), nullable=False)
  amazon_url = db.Column(db.Text, nullable=False)
  author = db.Column(db.Text, nullable=False)
  genre = db.Column(db.String(255), nullable=False)