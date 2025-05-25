from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'users'   # Add this line

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    # Relationships
    stories = db.relationship('Story', backref='author', lazy=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Story(db.Model):
    __tablename__ = 'stories'  # Add this line

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookmarks = db.relationship('Bookmark', backref='story', lazy=True)
    
    def __repr__(self):
        return f'<Story {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author_username': self.author.username,
            'created_at': self.created_at.isoformat()
        }

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'  # Add this line

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create a unique constraint to prevent duplicate bookmarks
    __table_args__ = (db.UniqueConstraint('user_id', 'story_id'),)
    
    def __repr__(self):
        return f'<Bookmark user_id={self.user_id} story_id={self.story_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'story_id': self.story_id,
            'story_title': self.story.title,
            'created_at': self.created_at.isoformat()
        }
