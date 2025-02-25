from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Index(db.Model):
    __tablename__ = 'indexes'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=True)
    icon = db.Column(db.String, nullable=True)
    office_id = db.Column(db.BigInteger, db.ForeignKey('offices.id'), nullable=False)
    is_kpi = db.Column(db.Boolean, default=False, nullable=False)
    alert = db.Column(db.Boolean, default=False, nullable=False)
    chart_type = db.Column(db.String, nullable=True)
    source = db.Column(db.String, nullable=True)
    news_feed_id = db.Column(db.String, nullable=True)

    # Relationships
    data = db.relationship('IndexData', backref='index', lazy=True)


class IndexData(db.Model):
    __tablename__ = 'indexes_data'
    id = db.Column(db.BigInteger, primary_key=True)
    index_id = db.Column(db.BigInteger, db.ForeignKey('indexes.id'), nullable=False)
    label = db.Column(db.String, nullable=False)
    value = db.Column(db.BigInteger, nullable=False)


class MinisterHistory(db.Model):
    __tablename__ = 'ministers_history'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    party = db.Column(db.String, nullable=True)
    start_date = db.Column(db.String, nullable=False)  
    office_id = db.Column(db.BigInteger, db.ForeignKey('offices.id'), nullable=False)
    image = db.Column(db.String, nullable=True)


class Office(db.Model):
    __tablename__ = 'offices'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=True)
    minister_id = db.Column(db.BigInteger, nullable=False)
    news_feed_id = db.Column(db.String, nullable=True)
    
    # Relationships
    indexes = db.relationship('Index', backref='office', lazy=True)
    ministers = db.relationship('MinisterHistory', backref='office', lazy=True)


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)  # Consider using Date
    time = db.Column(db.String, nullable=False)  # Consider using Time
    topic = db.Column(db.String, nullable=True)
    twitter_id = db.Column(db.BigInteger, nullable=False)
    image = db.Column(db.String, nullable=True)
    

class ParliamentMember(db.Model):
    __tablename__ = 'parliament_members'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    party = db.Column(db.String, nullable=True)
    additional_role = db.Column(db.String, nullable=True)
    is_km = db.Column(db.Boolean, default=False, nullable=False)
    is_coalition = db.Column(db.Boolean, default=False, nullable=False)
    image = db.Column(db.String, nullable=True)
    twitter_id = db.Column(db.String, nullable=True)
    twitter_feed_id = db.Column(db.String, nullable=True)


class NonParliamentMember(db.Model):
    __tablename__ = 'non_parliament_members'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    start_date = db.Column(db.String, nullable=True)
    finish_date = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    twitter_id = db.Column(db.String, nullable=True)
    appointed_by = db.Column(db.String, nullable=True)

class OfficeBranch(db.Model):
    __tablename__ = 'office_branches'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    office_id = db.Column(db.BigInteger, db.ForeignKey('offices.id'), nullable=False)
    image = db.Column(db.String, nullable=True)
