from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.String,primary_key=True)
    user_name = db.Column(db.String,unique=True)
    pass_hash = db.Column(db.String,nullable=False)

class Influencer(db.Model):
    influencer_id = db.Column(db.String,primary_key=True)
    influencer_name = db.Column(db.String,nullable=False)
    influencer_niche = db.Column(db.String,nullable=False)
    influencer_platforms = db.Column(db.String,nullable=False)
    influencer_platform_reach = db.Column(db.String,nullable=True)
    influencer_image = db.Column(db.LargeBinary, nullable=True)

    adverts = db.relationship('Advert',backref='influencer')

class Sponsor(db.Model):
    sponsor_id = db.Column(db.String,primary_key=True)
    sponsor_name = db.Column(db.String,nullable=False)
    sponsor_industry = db.Column(db.String,nullable=False)
    sponsor_budget = db.Column(db.Integer)
    sponsor_image = db.Column(db.BLOB, nullable=True)

    campaigns = db.relationship('Campaign',backref='sponsor')

class Admin(db.Model):
    admin_id = db.Column(db.String,primary_key=True)
    admin_name = db.Column(db.String)

class Campaign(db.Model):
    campaign_id = db.Column(db.String,primary_key=True)
    campaign_name = db.Column(db.String,nullable=False)
    campaign_description = db.Column(db.String,nullable=False)
    campaign_budget = db.Column(db.Integer,nullable=False)
    campaign_visibility = db.Column(db.String,nullable=False)
    campaign_start_date = db.Column(db.Date,nullable=False)
    campaign_end_date = db.Column(db.Date,nullable=False)

    sponsor_id = db.Column(db.String,db.ForeignKey('sponsor.sponsor_id'))

    adverts = db.relationship('Advert',backref='campaign')


class Advert(db.Model):
    ad_id = db.Column(db.String,primary_key=True)
    ad_name = db.Column(db.String,nullable=False)
    ad_budget = db.Column(db.Integer,nullable=False)
    ad_requirements = db.Column(db.String,nullable=False)
    ad_accepted = db.Column(db.String,nullable=False)

    influencer_id = db.Column(db.String,db.ForeignKey('influencer.influencer_id'))
    campaign_id = db.Column(db.String,db.ForeignKey('campaign.campaign_id'))


class Negotiation(db.Model):
    neg_id = db.Column(db.String,primary_key=True)
    neg_amount = db.Column(db.Integer,nullable=False)

    neg_init = db.Column(db.String,nullable=False)
    spn_id = db.Column(db.String,nullable=False)