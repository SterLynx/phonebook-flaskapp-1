from flask import request
from . import api
from app import db
from app.models import Contact
from .auth import basic_auth, token_auth
from app.models import User
from flask import jsonify


# Endpoint to get token - requires username/password
@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token}

# Endpoint to get all posts
@api.route('/contacts', methods=["GET"])
def get_contact():
    contacts = db.session.execute(db.select(Contact)).scalars().all()
    return [post.to_dict() for post in contacts]

# Endpoint to get a post by ID
@api.route('/contacts/<contact_id>', methods=["GET"])
def get_contact(contact_id):
    contact = db.session.get(Contact, contact_id)
    if not contact:
        return {'error':f'Contact with an ID of {contact_id} does not exist'}, 404
    return contact.to_dict

# Endpoint to create a new post
@api.route('/contact', methods=['POST'])
@token_auth.login_required
def create_post():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    # Get data from the body
    title = data.get('title')
    body = data.get('body')
    image_url = data.get('image_url')
    # Get the user
    current_user = token_auth.current_user()
    
    # Create a new Post to add to the database
    new_post = Contact(title=title, body=body, image_url=image_url, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()
    return new_post.to_dict(), 201