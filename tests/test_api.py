import pytest
import json
from flaskapp.api import app
from flask.testing import FlaskClient

# Testing config
app.config['TESTING'] = True
client: FlaskClient = app.test_client()
posts = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the first blog post.'},
    {'id': 2, 'title': 'Second Post', 'content': 'This is the second blog post.'}
]
new_post_id = 3
new_post = {'id': new_post_id, 'title': 'Third Post', 'content': 'This is the third blog post.'}
expected_updated_post = {'id': new_post_id, 'title': 'Updated Title', 'content': 'This is the third blog post.'}


# test API endpoints
def test_get_all_posts():
    response = client.get('/posts')
    assert response.status_code == 200
    data = response.get_json()
    assert data == posts

def test_create_post():
    response = client.post('/posts', json=new_post)
    assert response.status_code == 201
    #print(response, response.data)
    data = response.data
    assert json.loads(data) == new_post

def test_get_post():
    response = client.get(f'/posts/{new_post_id}')
    assert response.status_code == 200
    data = response.data
    assert json.loads(data) == new_post
    
def test_update_post():
    response = client.put(f'/posts/{new_post_id}', json={'title': 'Updated Title'})
    assert response.status_code == 200
    data = response.data
    assert json.loads(data) == expected_updated_post
    
def test_delete_post():
    response = client.delete(f'/posts/{new_post_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {'message': 'Post deleted'}


if __name__ == '__main__':
    pytest.main()