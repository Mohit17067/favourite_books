from kim import field

from .base import BaseMapper

from favourite_books.models import Book


class BookMapper(BaseMapper):

    __type__ = Book

    title = field.String()
    amazon_url = field.String()
    author = field.String()
    genre = field.String()