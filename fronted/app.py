import time
import random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from backend.get_from_d2pt import get_all_heroes
from multiprocessing import Process
from backend.get_from_db_selenium import parse  #Заменить на get_from_db_selenium, если банит (спустя ~сутки все матчи будут добавляться)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///replays.db"
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_link = db.Column(db.String(100), nullable=False, unique=True)
    replay_id = db.Column(db.String(50), nullable=False)
    radiant_team = db.Column(db.String(100), nullable=False)
    dire_team = db.Column(db.String(100), nullable=False)
    victory = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Article %r>" % self.id


@app.route("/")
def index():
    all_heroes = get_all_heroes()
    return render_template("index.html", heroes=all_heroes)


@app.route('/matchup', methods=['POST'])
def process_form():
    selected_heroes = [request.form.get('hero1'), request.form.get('hero2'), request.form.get('hero3'),
                       request.form.get('hero4'), request.form.get('hero5'), request.form.get('hero6'),
                       request.form.get('hero7'), request.form.get('hero8'), request.form.get('hero9'),
                       request.form.get('hero10')]
    all_articles = Article.query.all()
    return render_template("matchup.html",articles=articles_filter(all_articles, selected_heroes))


def add_db(Replays):
    for i in Replays:
        existing_article = Article.query.filter_by(
            db_link=i.db_link()
        ).first()
        # Если запись не существует, добавляем её в базу данных
        if not existing_article:
            new_article = Article(
                db_link=str(i.db_link()),
                replay_id=str(i.replay_id()),
                radiant_team=str(' '.join(i.heroes()[:5])),
                dire_team=str(' '.join(i.heroes()[5:10])),
                victory=str(i.victory())
            )
            try:
                db.session.add(new_article)
                db.session.commit()
            except:
                print("Произошла ошибка")


def run_parser():
    while True:
        with app.app_context():
            Replays = parse()
            add_db(Replays)
            time.sleep(random.randint(3600, 4800))


def articles_filter(articles, heroes):
    filtred_articles = []
    filter_1 = []
    for i in range(5):
        if heroes[i] is not None:
            filter_1.append(heroes[i])
    filter_2 = []
    for i in range(5,10):
        if heroes[i] is not None:
            filter_2.append(heroes[i])

    for article in articles:
        skip = False
        for i in filter_1:
            if not(i in article.radiant_team):
                skip = True
                break
        else:
            for i in filter_2:
                if not (i in article.dire_team):
                    skip = True
                    break
        if not skip:
            filtred_articles.append(article)
            continue
        else:
            skip = False
            for i in filter_1:
                if not (i in article.dire_team):
                    skip = True
                    break
            else:
                for i in filter_2:
                    if not (i in article.radiant_team):
                        skip = True
                        break
        if not skip:
            filtred_articles.append(article)
    return filtred_articles


if __name__ == "__main__":
    parser_process = Process(target=run_parser)
    parser_process.start()
    app.run()
