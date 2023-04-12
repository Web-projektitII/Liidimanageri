from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import Liidi,User

def liidit(count=25):
    fake = Faker(['fi_FI'])
    i = 0
    user_count = User.query.count()
    while i < count:
        user = User.query.offset(randint(0, user_count - 1)).first()
        liidi = Liidi(
                sahkoposti=fake.email(),
                puhelinnumero=fake.phone_number().replace(" ", ""),
                nimi=fake.name(),
                user_id=user.id,
                yksikko='IT',
                yhteinen=1,
                todennakoisyys=0.5)
        db.session.add(liidi)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

