from flask import Flask, render_template

app = Flask(__name__, template_folder='src/user_interface/templates')

@app.route('/')
def index():
    return render_template('base0.html')

if __name__ == '__main__':
    app.run(debug=True)
