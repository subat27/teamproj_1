from pybo import db

class ConfAge(db.Model):
    __tablename__='confAge'
    createDt = db.Column(db.String(20), primary_key=True)
    ageArea = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)
    
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