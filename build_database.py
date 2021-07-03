import os
from config import db

if os.path.exists("test.db"):
    os.remove("test.db")
db.create_all()

db.session.commit()

print('ok...')
