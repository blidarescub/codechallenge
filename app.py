from handlers import AdminHandler, MainHandler, UrlHandler  # this is our main handler

from models import Base as ModelsBase  # get the declared sqlalchemy base
# from models import Url, Word, urls_table, words_table
from models import engine as models_engine

from security import import_key

from sqlalchemy.orm import sessionmaker

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line


define("port", default=8888, help="Port for webserver to run")
# get options from command line or use defaults
parse_command_line()

db_engine = models_engine
Session = sessionmaker(bind=db_engine)
db_session = Session()
# db = db_engine.connect()

# app_settings = {
#     debug: "True"
# }

PUBLIC_KEY = import_key('public_key.pem')
PRIVATE_KEY = import_key('private_key.pem')


class MyApplication(web.Application):
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session')
        # self.session.configure(bind=db_engine)
        super(MyApplication, self).__init__(*args, **kwargs)

    def create_database(self):
        ModelsBase.metadata.create_all(db_engine)

application = MyApplication([  # here is our url/handler mappings
    (r"/", MainHandler),
    (r"/submit_url", UrlHandler, dict(
        db_session=db_session, public_key=PUBLIC_KEY)),
    (r"/admin", AdminHandler, dict(
        db_session=db_session, private_key=PRIVATE_KEY)),
    (r"/content/(.*)", web.StaticFileHandler, {'path': './'})
], session=db_session)

if __name__ == "__main__":
    application.create_database()
    application.listen(options.port)
    # import ipdb; ipdb.set_trace()
    ioloop.IOLoop.instance().start()
