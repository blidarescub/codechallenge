import Algorithmia

import hashlib

from operator import itemgetter

from models import Url, Word

from security import SALT, decrypt_w, encrypt_w

from tornado.web import RequestHandler

from word_cloud_processing import URLProcessing


class MainHandler(RequestHandler):
    def get(self, *args):
        self.write('<html><body><form action="/submit_url" method="POST">'
                   '<input type="text" name="url_text_input">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')


class UrlHandler(RequestHandler):
    def initialize(self, db_session, public_key):
        self.db_session = db_session
        self.public_key = public_key

    def post(self):
        url = self.get_body_argument("url_text_input")
        page = URLProcessing(url)
        client = Algorithmia.client('simScfOHIdEOdxcLMXQlYYx143/1')
        algo = client.algo('nlp/SentimentAnalysis/1.0.4')

        hash = hashlib.md5((SALT + url).encode('utf-8')).hexdigest()

        page.get_filtered_words()
        page.get_frequency()
        sentiment = algo.pipe({"document": page.text}).result[0]['sentiment']

        url_in_db = self.db_session.query(Url).filter(
            Url.hash == hash).one_or_none()

        if not url_in_db:
            url_entry = Url(hash=hash, url=url, sentiment=str(sentiment))
            self.db_session.add(url_entry)
            word_cloud = page.generate_word_cloud()
            word_cloud.to_file("%s.png" % hash)

        frequencies_top = page.get_top_100()

        for x in frequencies_top:
            word = self.db_session.query(Word).filter(
                Word.hash == hashlib.md5(
                    (
                        SALT + x[0]).encode('utf-8')).hexdigest()
            ).one_or_none()

            if not word:
                self.db_session.add(
                    Word(
                        hash=hashlib.md5(
                            (
                                SALT + x[0]).encode('utf-8')
                        ).hexdigest(),
                        value=encrypt_w(x[0], self.public_key),
                        frequency=x[1])
                )
            else:
                self.db_session.query(Word).filter(
                    Word.hash == word.hash
                ).update({"frequency": word.frequency + x[1]})

        self.db_session.commit()
        self.render(
            "template_wordcloud.html",
            url=url,
            image_file="%s.png" % hash
        )

    def options(self):
        pass


class AdminHandler(RequestHandler):
    def initialize(self, db_session, private_key):
        self.db_session = db_session
        self.private_key = private_key

    def get(self, *args):

        urls = list()
        words = list()

        for url_row in self.db_session.query(Url).all():
            urls.append(
                {
                    "value": url_row.url,
                    "sentiment": url_row.sentiment
                }
            )

        for word_row in self.db_session.query(Word).all():
            words.append(
                {
                    "value": decrypt_w(word_row.value, self.private_key),
                    "frequency": word_row.frequency
                }
            )

        words = sorted(words, key=itemgetter('frequency'), reverse=True)

        self.render(
            "admin_template.html",
            urls=urls,
            words=words
        )
