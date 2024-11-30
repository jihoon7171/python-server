from flask import Flask, Blueprint, jsonify, render_template, request, json
import urllib.request

endpoint = 'http://myback13:8888'

app = Flask(__name__)

# Blueprint 정의
bp = Blueprint('mybp', __name__, 
               static_folder='mybp/static',
               static_url_path='/pastebin/static',
               template_folder='templates',
) 

# @app.errorhandler(404)
# def handle_404(error):
#     return render_template("getpaste.html", paste=None), 404

@bp.route(f'/index.html/', methods=['GET'])
def get_index():
    count_users = 0
    url = f'{endpoint}/users/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_users = len(data)

    count_pastes = 0
    url = f'{endpoint}/users/pastes/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_pastes = len(data)

    return render_template('index.html', count_users=count_users, count_pastes = count_pastes)

@bp.route(f'/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = f'{endpoint}/users/'
        data = {'username': username, 'password': password}
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                return 'Created successfully'
            else:
                return 'Failed to create user', 400
    return render_template('createuser.html')

@bp.route(f'/createpaste', methods=['GET', 'POST'])
def create_paste():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        content = request.form['content']
        url = f'{endpoint}/users/{username}/pastes/'
        data = {'username': username, 'password': password, 'content': content}
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                return 'Paste created successfully!'
            else:
                return 'Failed to create paste', 400
    return render_template('createpaste.html')

def verify_user(username: str, password: str):
    url = f'{endpoint}/users/{username}/verify'
    headers = {'Content-Type': 'application/json'}
    data = {'username': username, 'password': password}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='POST')
    with urllib.request.urlopen(req) as f:
        user_data = json.loads(f.read())
        if user_data:
            return user_data
        else:
            return None




@bp.route(f'/pastes/<int:user_id>/', methods=['GET'])
def get_paste(user_id):
    paste_url = f'{endpoint}/pastes/{user_id}/'
    headers = {'Accept': 'application/json'}
    req = urllib.request.Request(paste_url, headers=headers, method='GET')
    with urllib.request.urlopen(req) as f:
        paste_data = json.loads(f.read())
        if paste_data:
            return render_template('getpaste.html',paste = paste_data)
        else:
            return jsonify({"detail": "Paste not found"}), 404
    return jsonify({"detail": "User verification failed"}), 403


# Blueprint 등록
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run('0.0.0.0', port=8888, debug=True)