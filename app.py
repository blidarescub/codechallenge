from handlers import AdminHandler, MainHandler, UrlHandler

from models import Base as ModelsBase

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


PUBLIC_KEY = import_key('public_key.pem')
PRIVATE_KEY = import_key('private_key.pem')


class MyApplication(web.Application):
    """Main class for the application.
    We setup db and create or update tables here at startup."""

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session')
        super(MyApplication, self).__init__(*args, **kwargs)

    def create_database(self):
        ModelsBase.metadata.create_all(db_engine)

application = MyApplication([
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
    ioloop.IOLoop.instance().start()
