from app.database.main import Database
from app.database.models import Products
from app.config.config import PLACEHOLDERS_DIR


def fill_database() -> None:
    session = Database().session
    session.add(Products(name='Рождественские пряники',
                         title='Рождественские имбирные пряники с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=25.7,
                         quantity=54,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('christmas.jpg')),
                         is_active=True))
    session.add(Products(name='Классические пряники',
                         title='Классические имбирные пряники с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=15.2,
                         quantity=13,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('classic.jpg')),
                         is_active=True))
    session.add(Products(name='Цветочные пряники',
                         title='Имбирные пряники в виде цветков с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=7,
                         quantity=13,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('flowers.jpg')),
                         is_active=True))
    session.add(Products(name='Пряники к 8 марту',
                         title='Имбирные пряники к 8 марту с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=21,
                         quantity=13,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('for_girls.jpg')),
                         is_active=True))
    session.add(Products(name='Пряничные человечки',
                         title='Имбирные пряничные человечки с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=35,
                         quantity=34,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('humans.jpg')),
                         is_active=True))
    session.add(Products(name='Волшебные зверюшки',
                         title='Имбирные волшебные зверюшки с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=40,
                         quantity=34,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('magical_animals.jpg')),
                         is_active=True))
    session.add(Products(name='Пряничные солдатики',
                         title='Имбирные пряничные солдатики с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=32,
                         quantity=34,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('soldiers.jpg')),
                         is_active=True))
    session.add(Products(name='Пряники на 23 февраля',
                         title='Имбирные пряничные солдатики с глазурью – пряные, ароматные, хрустящие и очень вкусные.',
                         price=23,
                         quantity=23,
                         img_path=str(PLACEHOLDERS_DIR.joinpath('war_theme.jpg')),
                         is_active=True))
    session.commit()