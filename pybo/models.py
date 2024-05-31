from pybo import db

class ConfAge(db.Model):
    __tablename__='confAge'
    createDt = db.Column(db.String(20), primary_key=True)
    ageArea = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)

    @classmethod
    def getColumnList(cls, session):
        results = []
        for data in session.query(cls).all() :
            temp_dict = data.__dict__
            for key in temp_dict.keys():
                if type(temp_dict[key]) is bytes:
                    temp_dict[key] = int.from_bytes(temp_dict[key], byteorder="little")
            temp_dict.pop('_sa_instance_state')
            results.append(temp_dict)
        return results
                

    
class ConfGender(db.Model):
    __tablename__='confGender'
    createDt = db.Column(db.String(20), primary_key=True)
    gender = db.Column(db.String(20), primary_key=True)
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)
    
    @classmethod
    def getColumnList(cls, session):
        results = []
        for data in session.query(cls).all() :
            temp_dict = data.__dict__
            for key in temp_dict.keys():
                if type(temp_dict[key]) is bytes:
                    temp_dict[key] = int.from_bytes(temp_dict[key], byteorder="little")
            temp_dict.pop('_sa_instance_state')
            results.append(temp_dict)
        return results
    
class ConfLocal(db.Model):
    __tablename__='confLocal'
    createDt = db.Column(db.String(20), primary_key=True)
    localName = db.Column(db.String(20), primary_key=True)
    localNameEn = db.Column(db.String(30))
    confCase = db.Column(db.Integer)
    deathCnt = db.Column(db.Integer)


class ConfGlobal(db.Model):
    __tablename__='confGlobal'
    id = db.Column(db.Integer, primary_key=True)
    createDt = db.Column(db.String(20), unique=False)
    nation = db.Column(db.String(30), unique=False, nullable=True)
    confCase = db.Column(db.Integer, unique=False, nullable=True)
    deathCnt = db.Column(db.Integer, unique=False, nullable=True)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=True)
    hangeul = db.Column(db.String(50), unique=True, nullable=True)