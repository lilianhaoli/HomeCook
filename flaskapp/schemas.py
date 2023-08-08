from marshmallow import Schema, fields

# Post Parameter
class PostParameter(Schema):
    post_id = fields.String()

# Post Request Body Schema
class PostRequestBody(Schema):
    title = fields.String()
    content = fields.String()

# Post Schema
class PostSchema(PostRequestBody):
    id = fields.String()
    # Add more fields as needed