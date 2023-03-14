from flask_sqlalchemy import SQLAlchemy
import redis
from rq import Queue

db = SQLAlchemy()

r = redis.Redis()
q = Queue(connection=r)