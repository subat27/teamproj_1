from pybo import db

class ConfAge(db.Model):
    createDt = db.Column(db.String(20), primary_key=True)
    ageArea = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)
    
class ConfGender(db.Model):
    createDt = db.Column(db.String(20), primary_key=True)
    gender = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)
    
class ConfLocal(db.Model):
    createDt = db.Column(db.String(20), primary_key=True)
    localName = db.Column(db.String(20), primary_key=True)
    localNameEn = db.Column(db.String(30))
    confCase = db.Column(db.Integer)
    incDec = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)