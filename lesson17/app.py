from flask import Flask
# from views.posts import posts_bp
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = '4hklh46-d436-f6456199dfgbzcb0-n,'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

# app.register_blueprint(posts_bp)


if __name__ == "__main__":
    from views.posts_orm import posts
    app.register_blueprint(posts)

    app.run()