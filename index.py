from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from requests import post, get

from data import db_session, items
from data.add import AddForm
from data.users import User
from data.register import RegisterForm
from data.login import LoginForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
user = None


def main():
    db_session.global_init("db/db.sqlite")
    api.add_resource(items.ItemsListResource, '/api/items')

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return render_template("/main.html", title="Shoper", base_url="//127.0.0.1:8080", header=1)
        else:
            return render_template("/index.html", title="Shoper", base_url="//127.0.0.1:8080", header=0)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            global user
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect("//127.0.0.1:8080")
            return render_template('login.html', message="Неверный логин или пароль", form=form,
                                   base_url="//127.0.0.1:8080", header=1)
        return render_template('login.html', title='Войти | Shoper', form=form, base_url="//127.0.0.1:8080", header=1)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация | Shoper',
                                       form=form,
                                       message="Пароли не совпадают", base_url="//127.0.0.1:8080", header=1)
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация | Shoper',
                                       form=form,
                                       message="Такой пользователь уже есть", base_url="//127.0.0.1:8080", header=1)
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация | Shoper', form=form, base_url="//127.0.0.1:8080",
                               header=1)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route("/add", methods=['GET', 'POST'])
    @login_required
    def add():
        form = AddForm()
        if form.validate_on_submit():
            post('http://127.0.0.1:8080/api/items',
                 json={'name': form.name.data, 'image': form.image.data, 'user_id': user.id,
                       'buyer_id': -1}).json()
        return render_template("/add.html", title="Добавить товар | Shoper", base_url="//127.0.0.1:8080", header=1, form=form)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
