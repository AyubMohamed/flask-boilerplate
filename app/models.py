from mongoengine import *
from datetime import datetime

class Comment(EmbeddedDocument):
    content = StringField()

class User(EmbeddedDocument):
    name = StringField()
    email = StringField()

class Ticket(Document):
    title = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    closed_at = DateTimeField()
    deleted_at = DateTimeField()
    status = StringField(default='New')
    created_by = EmbeddedDocumentField(User)
    assigned_to = EmbeddedDocumentField(User)
    comments = EmbeddedDocumentListField(Comment)

    def add_or_replace_comment(self, comment):
        existing = self.comments
        existing.append(comment)