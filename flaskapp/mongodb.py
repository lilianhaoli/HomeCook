from pymongo import MongoClient
from bson import ObjectId

class MongoDBClient:
    def __init__(self, connection_str=None, database_name=None, collection_name=None):
        self.client = None
        self.db = None
        self.collection = None
        if connection_str and database_name and collection_name:
            self.client = MongoClient(connection_str) # Connect to MongoDB
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]

    # Create (Insert) operation
    def create_blog_post(self, post):
        result = self.collection.insert_one(post)
        print(f"Inserted document ID: {result.inserted_id}")
        return self.get_blog_post(result.inserted_id)

    # Retrieve all blog posts
    def get_all_posts(self):
        posts = self.collection.find()
        #print(list(posts))
        for document in self.collection.find({}, {'_id': 1}):
            print(document['_id'])
        return list(posts)

    # Read (Retrieve) operation
    def get_blog_post(self, post_id):
        print(post_id)
        post = self.collection.find_one({'_id': post_id})
        return post

    # Update operation
    def update_blog_post(self, post_id, new_content):
        result = self.collection.update_one({'_id': post_id}, {'$set': {'content': new_content}})
        print(f"Matched count: {result.matched_count}, Modified count: {result.modified_count}")
        return True

    # Delete operation
    def delete_blog_post(self, post_id):
        result = self.collection.delete_one({'_id': post_id})
        print(f"Deleted count: {result.deleted_count}")
        return True
    

# # Example usage of the CRUD operations
# # Database Config
#mongodb_client = MongoDBClient(connection_str='<mongodb_connection_string>', database_name='<database_name>', collection_name='<collection_name>')

# # Create a blog post
#mongodb_client.create_blog_post(title="Introduction to MongoDB", content="MongoDB is a NoSQL database...", author="John Doe")

# # Get all blog posts
#posts = mongodb_client.get_all_posts()
#print(posts)

# # Get a blog post
#post = mongodb_client.get_blog_post(post_id='<post_id>')
#print(post)

# # Update a blog post
#mongodb_client.update_blog_post(post_id='<post_id>', new_content="Updated content goes here...")

# # Delete a blog post
#mongodb_client.delete_blog_post(post_id='<post_id>')