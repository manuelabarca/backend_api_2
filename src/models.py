from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def getUser(email, password):
        user = User.query.filter_by(email=email, password=password).first()
        return user

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size
        }

    def getAll():
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.serialize(), planets))
        return planets
    
    def getPlanet(id):
        planet = Planet.query.get(id)
        if planet is None:
            return {"msg": "This planet doesn't exist"}
        planet = Planet.serialize(planet)
        return planet
    
    def deletePlanet(id):
        planet = Planet.query.get(id)
        db.session.delete(planet)
        db.session.commit()
        return {"msg": "Planet was delete"}