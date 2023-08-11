from flask import Flask, jsonify, request, send_from_directory
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

from flaskapp.schemas import PostSchema
from flaskapp.mongodb import BlogManager

# Load Mock JSON Data
posts = []
with open("static/mock_data.json", "r") as f:
    posts = json.load(f)

mongodb_connection_string = 'mongodb://localhost:27017/'
# TODO: create client w/ mongodb_connection_string and pass to BlogManager
blog_manager = BlogManager(connection_str=mongodb_connection_string, database_name='test_database', collection_name='test_collection')

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
    post_schema = PostSchema()
    new_post = post_schema.dump({'title': request.json['title'], 'content': request.json['content']})
    new_post_resp = blog_manager.create_blog_post(new_post)
    if new_post_resp:
      return jsonify(post_schema.dump(new_post_resp)), 201
    return {}, 500


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
    posts = blog_manager.get_all_posts()
    return jsonify(posts_schema.dump(posts))


# Retrieve a specific blog post
@app.route('/posts/<string:post_id>', methods=['GET'])
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
    post = blog_manager.get_blog_post(post_id)
    if post:
        return PostSchema().dumps(post)
    return jsonify({'error': 'Post not found'}), 404


# Update a blog post
@app.route('/posts/<string:post_id>', methods=['PUT'])
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
    req_body = request.json
    updated_post = PostSchema().dump(req_body)
    post = blog_manager.update_blog_post(post_id, updated_post)
    if post:
      return PostSchema().dump(post)
    return jsonify({'error': 'Post not found'}), 404


# Delete a blog post
@app.route('/posts/<string:post_id>', methods=['DELETE'])
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
    delete_post = blog_manager.delete_blog_post(post_id)
    if delete_post:
        return jsonify({'message': 'Post deleted'})
    return jsonify({'error': 'Post not found'}), 404


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
    print("writing swagger JSON")
    json_data = spec.to_dict()
    with open("static/swagger.json", "w") as f:
        json.dump(json_data, f)

    # create swagger.yml file
    print("writing swagger YAML")
    with open('static/swagger.yml', 'w') as f:
        f.write(spec.to_yaml())

# Run the app locally
if __name__ == '__main__':
    app.run()