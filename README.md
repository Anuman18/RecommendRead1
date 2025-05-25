# RecommRead API

A Flask-based API for a reading recommendation app with user authentication, story management, and bookmarking functionality.

## Features

- User registration and authentication
- Story creation and retrieval
- Story bookmarking
- Pagination for stories and bookmarks

## Tech Stack

- Flask (Web framework)
- SQLite (Database)
- SQLAlchemy (ORM)
- Flask-CORS (Cross-Origin Resource Sharing)
- Werkzeug.security (Password hashing)

## API Endpoints

### Authentication

- `POST /signup` - Register a new user
  - Request: `{"username": "string", "email": "string", "password": "string"}`
  - Response: User information and success message

- `POST /login` - Login a user
  - Request: `{"username": "string", "password": "string"}`
  - Response: User information and session token

- `POST /logout` - Logout the current user
  - Response: Success message

- `GET /user` - Get current logged-in user info
  - Response: User information

### Stories

- `GET /stories` - Get a list of stories (paginated)
  - Query Parameters: `page` (default: 1), `per_page` (default: 10, max: 50)
  - Response: List of stories with pagination metadata

- `GET /story/<id>` - Get a specific story by ID
  - Response: Story information

- `POST /stories` - Create a new story (requires authentication)
  - Request: `{"title": "string", "content": "string"}`
  - Response: Created story information

- `PUT /story/<id>` - Update a story (requires authentication and ownership)
  - Request: `{"title": "string", "content": "string"}`
  - Response: Updated story information

- `DELETE /story/<id>` - Delete a story (requires authentication and ownership)
  - Response: Success message

### Bookmarks

- `POST /bookmark/<story_id>` - Bookmark a story (requires authentication)
  - Response: Bookmark information

- `DELETE /bookmark/<story_id>` - Remove a bookmark (requires authentication)
  - Response: Success message

- `GET /bookmarks` - Get user's bookmarked stories (requires authentication, paginated)
  - Query Parameters: `page` (default: 1), `per_page` (default: 10, max: 50)
  - Response: List of bookmarked stories with pagination metadata

## Setup and Running

### Prerequisites

- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Werkzeug

### Running the App

1. Clone the repository
2. Install the required packages
3. Run the app:

```bash
python main.py
