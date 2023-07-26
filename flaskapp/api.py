from flask import Flask, jsonify, request, send_from_directory
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

from flaskapp.schemas import PostSchema

# Load Mock JSON Data
posts = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the first blog post.'},
    {'id': 2, 'title': 'Second Post', 'content': 'This is the second blog post.'}
]
# with open("static/mock_data.json", "r") as f:
#     posts = json.load(f)

# Initialize Flask App
app = Flask(__name__)

# Flask route definitions

# Create a blog post
@app.route('/posts', methods=['POST'])
def create_post():
    """create_post.
    ---
    post:
      summary: Create new post
      description: Create new post
      tags:
        - Posts
      requestBody: 
        required: true 
        content: 
          application/json:
            schema: PostRequestBody
      responses:
        200:
          content:
            application/json:
              schema: PostSchema
        201:
          content:
            application/json:
              schema: PostSchema
    """
    new_post = {'id': len(posts) + 1, 'title': request.json['title'], 'content': request.json['content']}
    posts.append(new_post)
    return jsonify(PostSchema().dump(new_post)), 201


# Retrieve all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    """get_posts.
    ---
    get:
      summary: Get all posts
      description: Get all posts
      tags:
        - Posts
      responses:
        200:
          content:
            application/json:
              schema: 
                type: array
                items: PostSchema
    """
    posts_schema = PostSchema(many=True)
    return jsonify(posts_schema.dump(posts))


# Retrieve a specific blog post
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """get_post.
    ---
    get:
      summary: Get post by post id
      description: Get post by post id
      tags:
        - Posts
      parameters:
      - in: path
        schema: PostParameter  
      responses:
        200:
          content:
            application/json:
              schema: PostSchema
        404:
          content:
            application/json:
              schema: 
                message: string
    """
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return PostSchema().dumps(post)
    return jsonify({'message': 'Post not found'}), 404


# Update a blog post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """update_post.
    ---
    put:
      summary: Update post with post id
      description: Update post with post id
      tags:
        - Posts
      parameters:
      - in: path
        schema: PostParameter  
      requestBody: 
        required: true 
        content: 
          application/json:
            schema: PostRequestBody
      responses:
        200:
          content:
            application/json:
              schema: PostSchema
        404:
          content:
            application/json:
              schema: 
                message: string
    """
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        req_body = request.json
        title = req_body.get('title')
        content = req_body.get('content')
        
        if title:
          post['title'] = title
        if content:
          post['content'] = content

        #post['content'] = req_body.get('content')
        return PostSchema().dumps(post)
    return jsonify({'message': 'Post not found'}), 404


# Delete a blog post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """delete_post.
    ---
    delete:
      summary: Delete post with post id
      description: Delete post with post id
      tags:
        - Posts
      parameters:
      - in: path
        schema: PostParameter  
      responses:
        200:
          content:
            application/json:
              schema: 
                message: string
        404:
          content:
            application/json:
              schema: 
                message: string
    """
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        posts.remove(post)
        return jsonify({'message': 'Post deleted'})
    return jsonify({'message': 'Post not found'}), 404


# Add more routes and functionality as needed

# SERVE OPENAPI3.0 JSON FILE
@app.route("/static/swagger.json")
def specs():
    return send_from_directory(os.getcwd(), "static/swagger.json")


with app.test_request_context():
    # Swagger blueprint config
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL
    )
    app.register_blueprint(swaggerui_blueprint)
    
    # APISpec config
    spec = APISpec(
        title="Posts API",
        version="1.0.0",
        openapi_version="3.0.0",
        info=dict(
            description="A simple API for posts",
        ),
        plugins=[FlaskPlugin(), MarshmallowPlugin()]
    )

    # Register route to swagger doc
    spec.path(view=create_post)
    spec.path(view=get_posts)
    spec.path(view=get_post)
    spec.path(view=update_post)
    spec.path(view=delete_post)
    
    # create swagger.json file
    json_data = spec.to_dict()
    with open("static/swagger.json", "w") as f:
        json.dump(json_data, f)

# Run the app locally
if __name__ == '__main__':
    app.run()