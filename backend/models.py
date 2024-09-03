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

class Sponsor(db.Model):
    sponsor_id = db.Column(db.String,primary_key=True)
    sponsor_name = db.Column(db.String,nullable=False)
    sponsor_industry = db.Column(db.String,nullable=False)
    sponsor_budget = db.Column(db.Integer)

# class Admin(db.Model):
#     admin_name = db.Column(db.String)

# class Campaign(db.Model):
#     campaign_id = db.Column(db.String,primary_key=True)
#     campaign_name = db.Column(db.String,nullable=False)
#     campaign_description = db.Column(db.String,nullable=False)
#     campaign_budget = db.Column(db.Integer,nullable=False)
#     campaign_visibility = db.Column(db.String,nullable=False)
#     campaign_start_date = db.Column(db.Date,nullable=False)
#     campaign_end_date = db.Column(db.Date,nullable=False)

# class Advert(db.Model):
#     ad_id = db.Column(db.String,primary_key=True)
#     campaign_id = db.Column(db.String,foreign_key=True)
#     influencer_id = db.Column(db.String,foreign_key=True)
#     ad_name = db.Column(db.String,nullable=False)
#     ad_description = db.Column(db.String,nullable=False)
#     ad_budget = db.Column(db.Integer,nullable=False)
#     ad_visibility = db.Column(db.String,nullable=False)
#     ad_start_date = db.Column(db.Date,nullable=False)
#     ad_end_date = db.Column(db.Date,nullable=False)
    # def __srt__():


# class Advert(db.Model):
#     ad_id = db.Column(db.String,primary_key=True)
#     campaign_id = db.Column(db.String,foreign_key=True)
#     influencer_id = db.Column(db.String,foreign_key=True)
#     ad_name = db.Column(db.String,nullable=False)
#     ad_description = db.Column(db.String,nullable=False)
#     ad_budget = db.Column(db.Integer,nullable=False)
#     ad_visibility = db.Column(db.String,nullable=False)
#     ad_start_date = db.Column(db.Date,nullable=False)
#     ad_end_date = db.Column(db.Date,nullable=False)