from sqlalchemy import create_engine, MetaData

from ba.settings import config, BASE_DIR
from ba.db import users


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[users])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(users.insert(), [
        {'name': 'zip1982b',
         'passwd': '12345',
         'role': 'admin'}
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)