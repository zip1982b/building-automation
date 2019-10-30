from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('fullname', String),
              )

addresses = Table('addresses', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', None, ForeignKey('users.id')),
                  Column('email_address', String, nullable=False)
                  )


engine = create_engine('sqlite:///:memory:', echo=True)
metadata.create_all(engine)

ins = users.insert().values(name='zhan', fullname='Zhan Beshanov')
conn = engine.connect()
result = conn.execute(ins)





