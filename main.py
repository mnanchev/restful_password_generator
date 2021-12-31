from loguru import logger
from sqlalchemy.exc import PendingRollbackError
from werkzeug.exceptions import InternalServerError

from config import create_app
from db import db

app = create_app()
db.init_app(app)


@app.before_first_request
def init_request():
    db.create_all()


@app.after_request
def _conclude_request(resp):
    try:
        db.session.commit()
    except PendingRollbackError as pending_rollback_exception:
        db.session.rollback()
        logger.error("Pending rollback exception", pending_rollback_exception)
    except Exception:
        raise InternalServerError("Server is unavailable. Please try again later")
    finally:
        db.session.close()
    return resp


if __name__ == "__main__":
    app.run()
