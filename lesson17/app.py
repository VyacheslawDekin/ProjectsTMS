from flask import Flask
# from views.posts import posts_bp
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = '4hklh46-d436-f6456199dfgbzcb0-n,'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# app.register_blueprint(posts_bp)


if __name__ == "__main__":
    from views.posts_orm import posts
    app.register_blueprint(posts)

    from views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.run()