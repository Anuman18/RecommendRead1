from flask import Blueprint, request, jsonify, session
from extensions import db
from models import Bookmark, Story
from utils import login_required
import logging
from sqlalchemy.exc import IntegrityError

bookmarks_bp = Blueprint('bookmarks', __name__)

@bookmarks_bp.route('/bookmark/<int:story_id>', methods=['POST'])
@login_required
def bookmark_story(story_id):
    user_id = session.get('user_id')
    
    try:
        # Check if story exists
        story = Story.query.get(story_id)
        if not story:
            return jsonify({'error': 'Story not found'}), 404
        
        # Check if bookmark already exists
        existing_bookmark = Bookmark.query.filter_by(
            user_id=user_id, 
            story_id=story_id
        ).first()
        
        if existing_bookmark:
            return jsonify({'message': 'Story already bookmarked', 'bookmark': existing_bookmark.to_dict()}), 200
        
        # Create new bookmark
        new_bookmark = Bookmark(
            user_id=user_id,
            story_id=story_id
        )
        
        db.session.add(new_bookmark)
        db.session.commit()
        
        return jsonify({
            'message': 'Story bookmarked successfully',
            'bookmark': new_bookmark.to_dict()
        }), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Story already bookmarked'}), 409
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error bookmarking story {story_id}: {str(e)}")
        return jsonify({'error': 'Failed to bookmark story'}), 500

@bookmarks_bp.route('/bookmark/<int:story_id>', methods=['DELETE'])
@login_required
def remove_bookmark(story_id):
    user_id = session.get('user_id')
    
    try:
        # Find the bookmark
        bookmark = Bookmark.query.filter_by(
            user_id=user_id, 
            story_id=story_id
        ).first()
        
        if not bookmark:
            return jsonify({'error': 'Bookmark not found'}), 404
        
        # Delete the bookmark
        db.session.delete(bookmark)
        db.session.commit()
        
        return jsonify({'message': 'Bookmark removed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error removing bookmark for story {story_id}: {str(e)}")
        return jsonify({'error': 'Failed to remove bookmark'}), 500

@bookmarks_bp.route('/bookmarks', methods=['GET'])
@login_required
def get_bookmarks():
    user_id = session.get('user_id')
    
    # Get pagination parameters with defaults
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limit per_page to prevent performance issues
    if per_page > 50:
        per_page = 50
    
    try:
        # Get user's bookmarks with pagination
        pagination = Bookmark.query.filter_by(user_id=user_id).order_by(
            Bookmark.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        # Get the stories from the bookmarks
        bookmarked_stories = []
        for bookmark in pagination.items:
            story_data = bookmark.story.to_dict()
            story_data['bookmark_id'] = bookmark.id
            story_data['bookmarked_at'] = bookmark.created_at.isoformat()
            bookmarked_stories.append(story_data)
        
        return jsonify({
            'bookmarks': bookmarked_stories,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        logging.error(f"Error retrieving bookmarks: {str(e)}")
        return jsonify({'error': 'Failed to retrieve bookmarks'}), 500
