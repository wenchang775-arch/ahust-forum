from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import sqlite3
import os
import uuid

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'ahust-forum-secret-key-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 配置CORS，允许前端访问
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
})
jwt = JWTManager(app)

DATABASE = 'forum.db'
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            avatar TEXT DEFAULT '',
            signature TEXT DEFAULT '',
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 板块表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 帖子表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            board_id INTEGER NOT NULL,
            is_pinned INTEGER DEFAULT 0,
            is_essence INTEGER DEFAULT 0,
            view_count INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (board_id) REFERENCES boards (id)
        )
    ''')
    
    # 评论表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            parent_id INTEGER DEFAULT NULL,
            like_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (parent_id) REFERENCES comments (id)
        )
    ''')
    
    # 点赞表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER,
            comment_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (comment_id) REFERENCES comments (id),
            UNIQUE(user_id, post_id, comment_id)
        )
    ''')
    
    # 图片表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT,
            url TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            post_id INTEGER,
            comment_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (comment_id) REFERENCES comments (id)
        )
    ''')
    
    # 初始化板块数据
    cursor.execute('SELECT COUNT(*) FROM boards')
    if cursor.fetchone()[0] == 0:
        boards = [
            ('校园生活', '分享校园日常，交流生活点滴', 'school', 1),
            ('学习交流', '课程讨论、学习资料分享', 'book', 2),
            ('社团活动', '社团招新、活动预告', 'users', 3),
            ('二手交易', '闲置物品交换、转让', 'shopping', 4),
            ('求职招聘', '实习、兼职、就业信息', 'briefcase', 5),
            ('情感交流', '心情分享、情感咨询', 'heart', 6),
        ]
        cursor.executemany('INSERT INTO boards (name, description, icon, sort_order) VALUES (?, ?, ?, ?)', boards)
    
    conn.commit()
    conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': '请填写完整信息'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
    if cursor.fetchone():
        return jsonify({'error': '用户名或邮箱已存在'}), 400
    
    hashed_password = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (username, email, hashed_password))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    access_token = create_access_token(identity=str(user_id))
    return jsonify({'token': access_token, 'user_id': user_id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    access_token = create_access_token(identity=str(user['id']))
    return jsonify({
        'token': access_token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'avatar': user['avatar'],
            'signature': user['signature'],
            'is_admin': bool(user['is_admin'])
        }
    })

@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = int(get_jwt_identity())
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, avatar, signature, is_admin FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'avatar': user['avatar'],
        'signature': user['signature'],
        'is_admin': bool(user['is_admin'])
    })

@app.route('/api/boards', methods=['GET'])
def get_boards():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boards ORDER BY sort_order')
    boards = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': b['id'],
        'name': b['name'],
        'description': b['description'],
        'icon': b['icon']
    } for b in boards])

@app.route('/api/posts', methods=['GET'])
def get_posts():
    board_id = request.args.get('board_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    offset = (page - 1) * per_page
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = '''
        SELECT p.*, u.username, u.avatar, b.name as board_name
        FROM posts p
        JOIN users u ON p.user_id = u.id
        JOIN boards b ON p.board_id = b.id
        WHERE 1=1
    '''
    params = []
    
    if board_id:
        query += ' AND p.board_id = ?'
        params.append(board_id)
    
    query += ' ORDER BY p.is_pinned DESC, p.created_at DESC LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    
    cursor.execute(query, params)
    posts = cursor.fetchall()
    
    # 获取总数
    count_query = 'SELECT COUNT(*) FROM posts WHERE 1=1'
    count_params = []
    if board_id:
        count_query += ' AND board_id = ?'
        count_params.append(board_id)
    cursor.execute(count_query, count_params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'posts': [{
            'id': p['id'],
            'title': p['title'],
            'content': p['content'][:200] + '...' if len(p['content']) > 200 else p['content'],
            'user_id': p['user_id'],
            'username': p['username'],
            'avatar': p['avatar'],
            'board_id': p['board_id'],
            'board_name': p['board_name'],
            'is_pinned': bool(p['is_pinned']),
            'is_essence': bool(p['is_essence']),
            'view_count': p['view_count'],
            'like_count': p['like_count'],
            'comment_count': p['comment_count'],
            'created_at': p['created_at']
        } for p in posts],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # 更新浏览量
    cursor.execute('UPDATE posts SET view_count = view_count + 1 WHERE id = ?', (post_id,))
    conn.commit()
    
    cursor.execute('''
        SELECT p.*, u.username, u.avatar, u.signature, b.name as board_name
        FROM posts p
        JOIN users u ON p.user_id = u.id
        JOIN boards b ON p.board_id = b.id
        WHERE p.id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    
    # 获取评论
    cursor.execute('''
        SELECT c.*, u.username, u.avatar
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ? AND c.parent_id IS NULL
        ORDER BY c.created_at DESC
    ''', (post_id,))
    comments = cursor.fetchall()
    
    # 获取回复
    cursor.execute('''
        SELECT c.*, u.username, u.avatar
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ? AND c.parent_id IS NOT NULL
        ORDER BY c.created_at
    ''', (post_id,))
    replies = cursor.fetchall()
    
    conn.close()
    
    comments_data = []
    for c in comments:
        comment_replies = [{
            'id': r['id'],
            'content': r['content'],
            'username': r['username'],
            'avatar': r['avatar'],
            'like_count': r['like_count'],
            'created_at': r['created_at']
        } for r in replies if r['parent_id'] == c['id']]
        
        comments_data.append({
            'id': c['id'],
            'content': c['content'],
            'username': c['username'],
            'avatar': c['avatar'],
            'like_count': c['like_count'],
            'created_at': c['created_at'],
            'replies': comment_replies
        })
    
    return jsonify({
        'id': post['id'],
        'title': post['title'],
        'content': post['content'],
        'user_id': post['user_id'],
        'username': post['username'],
        'avatar': post['avatar'],
        'signature': post['signature'],
        'board_id': post['board_id'],
        'board_name': post['board_name'],
        'is_pinned': bool(post['is_pinned']),
        'is_essence': bool(post['is_essence']),
        'view_count': post['view_count'],
        'like_count': post['like_count'],
        'comment_count': post['comment_count'],
        'created_at': post['created_at'],
        'comments': comments_data
    })

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    title = data.get('title')
    content = data.get('content')
    board_id = data.get('board_id')
    
    if not all([title, content, board_id]):
        return jsonify({'error': '请填写完整信息'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (title, content, user_id, board_id)
        VALUES (?, ?, ?, ?)
    ''', (title, content, user_id, board_id))
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': post_id, 'message': '发布成功'}), 201

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    content = data.get('content')
    parent_id = data.get('parent_id')
    
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO comments (content, user_id, post_id, parent_id)
        VALUES (?, ?, ?, ?)
    ''', (content, user_id, post_id, parent_id))
    
    # 更新帖子评论数
    cursor.execute('UPDATE posts SET comment_count = comment_count + 1 WHERE id = ?', (post_id,))
    
    conn.commit()
    comment_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': comment_id, 'message': '评论成功'}), 201

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    user_id = int(get_jwt_identity())
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO likes (user_id, post_id) VALUES (?, ?)', (user_id, post_id))
        cursor.execute('UPDATE posts SET like_count = like_count + 1 WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': '点赞成功'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': '已经点赞过了'}), 400

@app.route('/api/search', methods=['GET'])
def search():
    keyword = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    offset = (page - 1) * per_page
    
    if not keyword:
        return jsonify({'posts': [], 'total': 0})
    
    conn = get_db()
    cursor = conn.cursor()
    
    search_pattern = f'%{keyword}%'
    
    cursor.execute('''
        SELECT p.*, u.username, u.avatar, b.name as board_name
        FROM posts p
        JOIN users u ON p.user_id = u.id
        JOIN boards b ON p.board_id = b.id
        WHERE p.title LIKE ? OR p.content LIKE ?
        ORDER BY p.created_at DESC
        LIMIT ? OFFSET ?
    ''', (search_pattern, search_pattern, per_page, offset))
    posts = cursor.fetchall()
    
    cursor.execute('''
        SELECT COUNT(*) FROM posts
        WHERE title LIKE ? OR content LIKE ?
    ''', (search_pattern, search_pattern))
    total = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'posts': [{
            'id': p['id'],
            'title': p['title'],
            'content': p['content'][:200] + '...' if len(p['content']) > 200 else p['content'],
            'username': p['username'],
            'avatar': p['avatar'],
            'board_name': p['board_name'],
            'is_essence': bool(p['is_essence']),
            'view_count': p['view_count'],
            'like_count': p['like_count'],
            'comment_count': p['comment_count'],
            'created_at': p['created_at']
        } for p in posts],
        'total': total,
        'page': page,
        'per_page': per_page
    })

# 图片上传API
@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        user_id = int(get_jwt_identity())
        
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # 保存文件
        file.save(filepath)
        
        # 获取可选的关联信息
        post_id = request.form.get('post_id', type=int)
        comment_id = request.form.get('comment_id', type=int)
        
        # 保存到数据库
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO images (filename, original_name, url, user_id, post_id, comment_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, file.filename, f'/uploads/{filename}', user_id, post_id, comment_id))
        conn.commit()
        image_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'id': image_id,
            'url': f'/uploads/{filename}',
            'filename': filename,
            'message': '上传成功'
        }), 201
    
    return jsonify({'error': '不支持的文件类型'}), 400

# 上传头像API
@app.route('/api/user/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        user_id = int(get_jwt_identity())
        
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"avatar_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # 保存文件
        file.save(filepath)
        
        # 更新用户头像
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET avatar = ? WHERE id = ?', (f'/uploads/{filename}', user_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'url': f'/uploads/{filename}',
            'message': '头像上传成功'
        })
    
    return jsonify({'error': '不支持的文件类型'}), 400

# 获取帖子图片
@app.route('/api/posts/<int:post_id>/images', methods=['GET'])
def get_post_images(post_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM images WHERE post_id = ?', (post_id,))
    images = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': img['id'],
        'url': img['url'],
        'filename': img['filename']
    } for img in images])

# 静态文件服务
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 初始化数据库
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
