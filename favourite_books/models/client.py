import shortuuid
import uuid

from .base import db, BaseMixin


class Client(BaseMixin, db.Model):

	__tablename__ = 'api_client'

	name = db.Column(db.Unicode(255), nullable=False)
	client_id = db.Column(db.String(22), nullable=False, default=shortuuid.uuid)
	secret_key = db.Column(db.Unicode(), nullable=False, default=lambda: str(uuid.uuid4()))