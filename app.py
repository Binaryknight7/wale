from stryda import create_app
from stryda import db
from stryda.models import Admin_User, User
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import login_required, current_user, login_user, logout_user
from flask_admin import Admin, expose, BaseView, helpers, AdminIndexView, helpers
from flask_admin.contrib.sqla import ModelView
import flask_login
from flask_admin.contrib import sqla
from werkzeug.security import generate_password_hash, check_password_hash
from flask_basicauth import BasicAuth
from wtforms import form, fields, validators
import flask_admin as admin


app = create_app()
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['BASIC_AUTH_USERNAME'] = 'ADMIN'
app.config['BASIC_AUTH_PASSWORD'] = 'MATRIX'


toolbar = DebugToolbarExtension(app)
basic_auth = BasicAuth(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        print("new usr created")
        return redirect(url_for('home'))
    return render_template('home.html', user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        print("new usr created")
        return redirect(url_for('home'))
    return render_template('main_register.html', user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            print("permission denied, try again")

    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/mail")
def mail():
    return render_template('mail.html')


class stryda(ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('contact', next=request.url))


class stryda_admin(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

    @expose('/')
    def admin_index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('admin_login'))
        return super(stryda_admin, self).index()

    @expose('/admin_login/')
    def admin_login(self):
        return self.render('admin/admin_login.html')

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


admin = Admin(app, name='Dashboard', template_mode='bootstrap4',
              index_view=stryda_admin())
admin.add_view(stryda(User, db.session))


if __name__ == '__main__':
    app.run(debug=True)
