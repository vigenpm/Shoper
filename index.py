from flask import Flask, render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/db.sqlite")

    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("/index.html", title="Shoper", base_url="//127.0.0.1:8080", header=0)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
