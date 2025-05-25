from flask import Blueprint, render_template, redirect, url_for

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/login')
def login():
    return render_template('login.html')

@web_bp.route('/signup')
def signup():
    return render_template('signup.html')

@web_bp.route('/stories')
def stories():
    return render_template('stories.html')

@web_bp.route('/story/<int:story_id>')
def story_detail(story_id):
    return render_template('story_detail.html')

@web_bp.route('/create-story')
def create_story():
    return render_template('create_story.html')

@web_bp.route('/edit-story/<int:story_id>')
def edit_story(story_id):
    return render_template('edit_story.html')

@web_bp.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')