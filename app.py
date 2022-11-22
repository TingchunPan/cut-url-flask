
import uuid

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.sqlite3'
db = SQLAlchemy(app)
pwd_hash = db.Column(db.String(100),  nullable=False)


def create_tables():
    db.create_all()


class Urls(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    link = db.Column(db.String(1000))
    new_link = db.Column(db.String(100))

    def __init__(self, link, new_link):
        self.link = link
        self.new_link = new_link


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        got_link = request.form["link"]
        if got_link == '':
            flash('Oops! This form cannot be blank.')
            return render_template('index.html')
        else:
            found_link = Urls.query.filter_by(link=got_link).first()

            if found_link:
                if request.form["optional"]:
                    flash(
                        'Sorry, You have shorten this URL before. Cannot custimize.')

                return redirect(url_for("short_url_result", url=found_link.new_link))

            else:
                short = produce_shorten()
                print(short)
                new_link = Urls(got_link, short)
                # if new_link:
                #     flash(
                #         'Sorry, You have used the same optional words to custimize. Please change.')
                #     return redirect(url_for("short_url_result", url=found_link.new_link))
                # else:
                db.session.add(new_link)
                db.session.commit()
                return redirect(url_for("short_url_result", url=short))

    else:
        return render_template('index.html')


def produce_shorten():
    if request.form["optional"]:

        # if bool(Urls.query.filter_by(request.form["optional"]).first()) == True:
        #     flash(
        #         'Sorry, You have used the same optional words to custimize. Please change.')
        #     return render_template('index.html')

        # else:
        short = request.form["optional"]

    else:
        short = str(uuid.uuid4())[:5]
    return short


@app.route('/result/<url>')
def short_url_result(url):
    return render_template('result.html', short_present=url)


@app.route('/<short>')
def present(short):
    link = Urls.query.filter_by(new_link=short).first()
    return redirect(link.link)


if __name__ == "__main__":
    app.run(debug=True)
