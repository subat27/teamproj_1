from pybo import db

class ConfAge(db.Model):
    __tablename__='confAge'
    createDt = db.Column(db.String(20), primary_key=True)
    ageArea = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)

    @classmethod
    def getColumnList(cls, session):
        results = session.query(cls.createDt, cls.ageArea, cls.confCase, cls.deathCnt).all()
        return [row.__dict__ for row in results]

    
class ConfGender(db.Model):
    __tablename__='confGender'
    createDt = db.Column(db.String(20), primary_key=True)
    gender = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)
    
class ConfLocal(db.Model):
    __tablename__='confLocal'
    createDt = db.Column(db.String(20), primary_key=True)
    localName = db.Column(db.String(20), primary_key=True)
    localNameEn = db.Column(db.String(30))
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)


class ConfGlobal(db.Model):
    __tablename__='confGlobal'
    createDt = db.Column(db.String(20), primary_key=True)
    ageArea = db.Column(db.String(20), primary_key=True)
    gender = db.Column(db.String(20), primary_key=True)
    nation = db.Column(db.String(30))
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)