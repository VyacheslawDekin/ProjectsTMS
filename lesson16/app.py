from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    text = "index"
    return render_template('index.html', text=text)


@app.route('/menu/')
def menu():
    text = "menu"
    return render_template('menu.html', text=text)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
