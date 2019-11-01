from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

from ba.settings import config, BASE_DIR

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
metadata = MetaData()

users_1 = Table('users_1', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('fullname', String),
              )

addresses = Table('addresses', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', None, ForeignKey('users_1.id')),
                  Column('email_address', String, nullable=False)
                  )


db_url = DSN.format(**config['postgres'])

engine = create_engine(db_url, echo=True)
metadata.create_all(engine)

ins = users_1.insert().values(name='zhan', fullname='Zhan Beshanov')
conn = engine.connect()
result = conn.execute(ins)
print(result)




