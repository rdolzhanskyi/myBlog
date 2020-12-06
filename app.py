from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route("/")
@app.route("/home")
@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route("/posts/<int:id>")
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route("/posts/<int:id>/delete")
def post_delete(id):
    article = Article.query.get_or_404(id)
    
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error: Article '" + str(article.title) + "' wasn't deleted!"


@ app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error: Article '" + str(title) + "' wasn't created!"

    else:
        return render_template('create.html')


@ app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error: Article '" + str(article.title) + "' wasn't updated!"

    else:

        return render_template('/update.html', article=article)


if __name__ == "__main__":
    app.run()
