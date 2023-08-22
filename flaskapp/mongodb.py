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
    def create_blog_post(self, new_post):
        if new_post:
            result = self.collection.insert_one(new_post)
            if result:
                print(f"Inserted document ID: {result.inserted_id}")
                return self.get_blog_post(str(result.inserted_id))
        return {}

    # Retrieve all blog posts
    def get_all_posts(self):
        posts = self.collection.find()
        return list(posts)

    # Read (Retrieve) operation
    def get_blog_post(self, post_id):
        post = self.collection.find_one({'_id': ObjectId(post_id)})
        post['id'] = post_id
        return post

    # Update operation
    def update_blog_post(self, post_id, updated_post):
        result = self.collection.update_one({'_id': ObjectId(post_id)}, {'$set': updated_post})
        print(f"Matched count: {result.matched_count}, Modified count: {result.modified_count}")
        return self.get_blog_post(post_id)

    # Delete operation
    def delete_blog_post(self, post_id):
        result = self.collection.delete_one({'_id': ObjectId(post_id)})
        print(f"Deleted count: {result.deleted_count}")
        if result and result.deleted_count:
            return True
        return False
