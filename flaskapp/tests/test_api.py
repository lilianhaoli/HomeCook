import pytest
from flaskapp.api import app
from flask.testing import FlaskClient
import json

# API endpoint tests

class APIConfig:
    def __init__(self):
        app.config['TESTING'] = True
        self.client: FlaskClient = app.test_client()
        self.new_post_id = ""


test_config = APIConfig()
client = test_config.client

def test_get_all_posts():
    response = client.get('/posts')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_create_post():
    new_post = {'title': 'New Post', 'content': 'New post content'}
    response = client.post('/posts', json=new_post)
    assert response.status_code == 201
    data = response.get_json()
    test_config.new_post_id = response.json['id']
    assert data['title'] == new_post['title']
    assert data['content'] == new_post['content']

def test_get_post():
    new_post_id = test_config.new_post_id
    response = client.get(f'/posts/{new_post_id}')
    # print('response',)
    assert response.status_code == 200
    data = json.loads(response.data)
    print('data', data)
    assert data == {'id': new_post_id, 'title': 'New Post', 'content': 'New post content'}
    
def test_update_post():
    new_post_id = test_config.new_post_id
    updated_post = {'title': 'Updated Title'}
    response = client.put(f'/posts/{new_post_id}', json=updated_post)
    assert response.status_code == 200
    data = response.get_json()
    assert data == {'id': new_post_id, 'title': 'Updated Title', 'content': 'New post content'}

def test_delete_post():
    new_post_id = test_config.new_post_id
    response = client.delete(f'/posts/{new_post_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {'message': 'Post deleted'}


if __name__ == '__main__':
    pytest.main()