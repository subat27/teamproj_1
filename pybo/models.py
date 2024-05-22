from pybo import db

class Conf_Age(db.Model):
    createDt = db.Column(db.String(20), primary_key=True)
    ageArea = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)
    
class Conf_Gender(db.Model):
    createDt = db.Column(db.String(20), primary_key=True)
    gender = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)
    
class Conf_Local(db.Model):
    createDt = db.Column(db.String(20), primary_key=True)
    localName = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    incDec = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)