
from app import app,db

from models import *

def seed_data():
    with app.app_context():
        # Drop existing tables and recreate
        db.drop_all()
        db.create_all()

        # Create some sample powers
        power1 = Power(name='Flight', description='Ability to fly and move through the air with great speed and agility')
        power2 = Power(name='Super Strength', description='Incredible strength')
        power3 = Power(name='Telepathy', description='Read minds')

        db.session.add_all([power1, power2, power3])
        db.session.commit()

        # Create some sample heroes
        hero1 = Hero(name='Superman', super_name='Clark Kent')
        hero2 = Hero(name='Wonder Woman', super_name='Diana Prince')
        hero3 = Hero(name='Professor X', super_name='Charles Xavier')

        db.session.add_all([hero1, hero2, hero3])
        db.session.commit()

        # Assign powers to heroes
        # hero1.powers.extend([power1, power2])
        # hero2.powers.append(power3)
        # hero3.powers.append(power3)

        # db.session.commit()

       # Create some hero powers
        hero_power1 = HeroPower(strength='Strong', hero_id=hero1.id, power_id=power1.id)
        hero_power2 = HeroPower(strength='Average', hero_id=hero2.id, power_id=power3.id)
        hero_power3 = HeroPower(strength='Weak', hero_id=hero3.id, power_id=power2.id)

        #print(vars(hero_power1))
        db.session.add_all([hero_power1, hero_power2, hero_power3])
        db.session.commit()


if __name__ == '__main__':
    seed_data()
    print("Database seeded successfully.")
