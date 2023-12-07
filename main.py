from dotenv import dotenv_values
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
import os

cfg = dotenv_values(".env")

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['HTTPAUTH_USERNAME'] = cfg.get("auth_user")
app.config['HTTPAUTH_PASSWORD'] = cfg.get("auth_pass")

pids = {}

@auth.verify_password
def verify_password(username, password):
    if username == app.config['HTTPAUTH_USERNAME'] and password == app.config['HTTPAUTH_PASSWORD']:
        return username


@app.route('/')
@auth.login_required
def home():
    files = os.listdir('C:/Services')
    return render_template('home.html', files=files, pids=pids)


@app.route('/start_service', methods=['POST'])
@auth.login_required
def start_service():
    filename = request.form['filename']
    if filename in pids.keys():
        return
    os.system('chmod +x C:/Services/' + filename)
    pid = os.spawnl(os.P_NOWAIT, 'C:/Services/' + filename,)
    pids[filename] = pid
    return render_template('home.html')

@app.route('/stop_service', methods=['POST'])
@auth.login_required
def stop_service():
    filename = request.form['filename']
    pid = pids.get(filename)
    if pid is not None:
        os.kill(int(pid), 9)
        del pids[filename]
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host=cfg.get("host"), port=cfg.get("port"), debug=True)
