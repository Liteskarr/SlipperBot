from flask import redirect, render_template, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash

import admin
import all_resources as resources
from app import app, login_manager
from forms import LoginForm
from models import all_models
from models.db_session import create_session, global_init


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/admin')
    else:
        return redirect('/login')


@app.route('/login', methods=['POST'])
def login_post():
    form = request.form
    login = form.get('login', None)
    password = form.get('password', None)
    session = create_session()
    user = session.query(all_models.User).filter_by(login=login).first()
    if user is None:
        flash('User does not exist!', 'danger')
        return redirect('/login')
    else:
        if check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            return redirect('/admin')
        else:
            flash('Incorrect password!', 'danger')
            return redirect('/login')


@app.route('/login', methods=['GET'])
def login_get():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@login_manager.user_loader
def user_loader(user_id):
    session = create_session()
    return session.query(all_models.User).get(user_id)


def main():
    global engine
    engine = global_init('D:\\Projects\\SlipperBot\\Server\\develop.sqlite3')
    admin.init()
    resources.init_all()
    app.run(host='localhost', port=5000, debug=True)


if __name__ == '__main__':
    main()
