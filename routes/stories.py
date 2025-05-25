from flask import Blueprint, request, jsonify, session
from extensions import db
from utils import login_required
import logging

stories_bp = Blueprint('stories', __name__)

@stories_bp.route('/stories', methods=['GET'])
def get_stories():
    from models import Story  # Import inside function
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    if per_page > 50:
        per_page = 50
    
    try:
        pagination = Story.query.order_by(Story.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        stories = [story.to_dict() for story in pagination.items]
        
        return jsonify({
            'stories': stories,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        logging.error(f"Error retrieving stories: {str(e)}")
        return jsonify({'error': 'Failed to retrieve stories'}), 500

@stories_bp.route('/story/<int:story_id>', methods=['GET'])
def get_story(story_id):
    from models import Story  # Import inside function
    
    try:
        story = Story.query.get(story_id)
        if not story:
            return jsonify({'error': 'Story not found'}), 404
        return jsonify(story.to_dict()), 200
    
    except Exception as e:
        logging.error(f"Error retrieving story {story_id}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve story'}), 500

@stories_bp.route('/stories', methods=['POST'])
@login_required
def create_story():
    from models import Story  # Import inside function
    
    data = request.get_json()
    user_id = session.get('user_id')
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400
    
    try:
        new_story = Story(
            title=data['title'],
            content=data['content'],
            author_id=user_id
        )
        db.session.add(new_story)
        db.session.commit()
        
        return jsonify({
            'message': 'Story created successfully',
            'story': new_story.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating story: {str(e)}")
        return jsonify({'error': 'Failed to create story'}), 500

@stories_bp.route('/story/<int:story_id>', methods=['PUT'])
@login_required
def update_story(story_id):
    from models import Story  # Import inside function
    
    data = request.get_json()
    user_id = session.get('user_id')
    
    try:
        story = Story.query.get(story_id)
        if not story:
            return jsonify({'error': 'Story not found'}), 404
        
        if story.author_id != user_id:
            return jsonify({'error': 'Not authorized to update this story'}), 403
        
        if data.get('title'):
            story.title = data['title']
        if data.get('content'):
            story.content = data['content']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Story updated successfully',
            'story': story.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating story {story_id}: {str(e)}")
        return jsonify({'error': 'Failed to update story'}), 500

@stories_bp.route('/story/<int:story_id>', methods=['DELETE'])
@login_required
def delete_story(story_id):
    from models import Story  # Import inside function
    
    user_id = session.get('user_id')
    
    try:
        story = Story.query.get(story_id)
        if not story:
            return jsonify({'error': 'Story not found'}), 404
        
        if story.author_id != user_id:
            return jsonify({'error': 'Not authorized to delete this story'}), 403
        
        db.session.delete(story)
        db.session.commit()
        
        return jsonify({'message': 'Story deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting story {story_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete story'}), 500
