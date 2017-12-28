from flask import Flask, url_for,  render_template

uimgmt = Flask(__name__)


@uimgmt.route('/')
def home_page():
    return render_template("index.html")



if __name__ == "__main__":
    uimgmt.run('10.11.59.156', 80, debug=True)
