from flask import Flask, jsonify, request

app = Flask(__name__)



@app.route('/posts', methods=['POST'])
def create_post():
    new_post = {'id': len(posts) + 1, 'title': request.json['title'], 'content': request.json['content']}
    posts.append(new_post)
    return jsonify(new_post), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)
    
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post and request.json:
        post = request.json
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404
    
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        posts.remove(post)
        return jsonify({'message': 'Post deleted'})
    return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    app.run()