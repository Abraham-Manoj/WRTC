from flask import Flask, render_template, request,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def redirectUser():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)