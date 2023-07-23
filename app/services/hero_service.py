from sqlmodel import create_engine, Session, select, update

from ..models.heroes import Hero

# localhostと書くと繋がらない
engine = create_engine('mysql://yoshima:yoshima@127.0.0.1:3306/study_fastapi_db')


def get_all_hero():
    with Session(engine) as session:
        stmt = select(Hero)
    heroes = session.exec(stmt).all()
    return heroes


def get_by_id(hero_id: int):
    with Session(engine) as session:
        stmt = select(Hero).where(Hero.id == hero_id)
    result = session.exec(stmt).one()
    return result


def update_hero(hero_id: int):
    with Session(engine) as session:
        stmt = select(Hero).where(Hero.id == hero_id)
    result = session.exec(stmt).one()
    result.name = "updated name"
    session.add(result)
    session.commit()
    session.refresh(result)


def create_hero(hero: Hero):
    with Session(engine) as session:
        print(f"追加前ID：{hero.id}")
        session.add(hero)
        print(f"追加後ID：{hero.id}")

        print(f"コミット前ID：{hero.id}")
        session.commit()
        print(f"コミット後ID：{hero.id}")

        # コミット後でIDは最新の状態になっているので，不要な気がする．．．
        print(f"反映前ID：{hero.id}")
        session.refresh(hero)
        print(f"反映後ID：{hero.id}")


def bulk_update():
    with Session(engine) as session:
        heroes = session.query(Hero).filter(Hero.name == "yoshima").all()

    session.execute(
        update(Hero).where(Hero.name == "yoshima").values(age=45)
    )
    session.commit()

    for hero in heroes:
        session.refresh(hero)


def delete(hero_id: int):
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == hero_id)
    result = session.exec(statement).one()

    session.delete(result)
    session.commit()
