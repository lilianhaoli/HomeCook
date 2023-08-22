from unittest.mock import MagicMock
import pytest
from pymongo import MongoClient
from flaskapp.mongodb import MongoDBClient



# Create a MagicMock instance for the MongoClient class, database and collection
mongo_client_mock = MagicMock(spec=MongoClient)
db_mock = MagicMock()
collection_mock = MagicMock()

# # Test POST ID
TEST_POST_ID = '64ac8e3cd923fe7823192d7d'

# Configure the collection_mock to return specific values for CRUD operations
test_document = {'_id': TEST_POST_ID, 'id': TEST_POST_ID, 'title': 'Test Post', 'content': 'Test content'}
test_collection = [test_document]

collection_mock.find.return_value = test_collection
collection_mock.insert_one.return_value.inserted_id = test_document['_id']
collection_mock.insert_one.return_value.inserted_count = len(test_collection)

collection_mock.find_one.return_value = test_document
collection_mock.update_one.return_value.modified_count = len(test_collection)
collection_mock.delete_one.return_value.deleted_count = len(test_collection)

db_mock.collection = collection_mock # Configure the db_mock to return the collection_mock for the 'collection' attribute
mongo_client_mock.db = db_mock # Configure the mongo_client_mock to return the db_mock for the 'db' attribute

blog_manager = MongoDBClient()
blog_manager.collection = mongo_client_mock.db.collection


# Test functions
def test_create_post():
    post = {'title': 'Test Post', 'content': 'Test content'}
    created_post = blog_manager.create_blog_post(post)
    assert len(blog_manager.get_all_posts()) == 1
    assert created_post['title'] == post['title']
    assert created_post['id'] == TEST_POST_ID
    assert created_post == test_document


def test_get_post():
    result = blog_manager.get_blog_post(TEST_POST_ID)
    assert result == test_document


def test_update_post():
    test_document['title'] =  'Updated Post'
    updated_post = blog_manager.update_blog_post(TEST_POST_ID, {'title': 'Updated Post'})
    assert updated_post['title'] == 'Updated Post'


def test_delete_post():
    blog_manager.delete_blog_post(TEST_POST_ID)
    assert len(mongo_client_mock.db.collection.documents) == 0


if __name__ == '__main__':
    pytest.main()



# import pytest
# from pymongo import MongoClient

# @pytest.fixture(scope='module')
# def mongo_client():
#     # Set up a MongoDB client connection
#     client = MongoClient('<mongodb_connection_string>')
#     yield client
#     # Teardown: Close the client connection
#     client.close()

# @pytest.fixture
# def blog_manager(mongo_client):
#     # Set up the blog manager with the MongoDB client
#     db = mongo_client['<database_name>']
#     collection = db['<collection_name>']
#     manager = BlogManager(collection)
#     yield manager
#     # Teardown: Clear the collection after each test
#     collection.delete_many({})


# def test_create_post(blog_manager):
#     # Test the create_post method of the blog manager
#     new_post = {'title': 'New Post', 'content': 'Test content', 'author': 'John Doe'}
#     blog_manager.create_post(new_post)
#     assert len(blog_manager.get_all_posts()) == 1

# def test_get_post(blog_manager):
#     # Test the get_post method of the blog manager
#     new_post = {'title': 'New Post', 'content': 'Test content', 'author': 'John Doe'}
#     blog_manager.create_post(new_post)
#     post = blog_manager.get_post(1)
#     assert post['title'] == 'New Post'

# # ... Additional test functions for update_post, delete_post, etc.