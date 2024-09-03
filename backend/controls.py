from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask import current_app as app
from .models import *
import datetime
import hashlib as hash

def date_pack(item):
    date = datetime.datetime.strptime(item,'%Y-%m-%d')
    return date

def campaign_vis_pack(item):
    visibility = {
        '1':'Public',
        '2':'Private'
    }
    return visibility.get(item)

def inf_reach_pack(item):
    r = str(item)
    digits = len(r)
    if digits > 6:
        return r[:-6] + 'M'
    elif digits < 4:
        return r
    else:
        return r[:-3] + 'K'
    
def inf_platforms_pack(item):
    platforms = {
        "1":"Youtube",
        "2":"Twitch",
        "3":"Instagram",
        "4":"Twitter",
        "5":"Facebook",
        "6":"TikTok"
    }
    packed_platforms = [platforms.get(i) for i in item]
    return ";".join(packed_platforms)

def inf_niche_pack(item):
    niche_types = {
        "1":"Technology",
        "2":"Gaming",
        "3":"Beauty",
        "4":"Comedy",
        "5":"News",
        "6":"Music",
        "7":"Dance",
        "8":"Entertainment",
        "9":"Food",
        "10":"Visual Arts"
    }
    return niche_types.get(item)

def spn_industry_pack(item):
    industry_types = {
        "1":"Electronics",
        "2":"Gaming",
        "3":"Entertainment",
        "4":"Beauty",
        "5":"Finance",
        "6":"Food",
        "7":"Fashion",
        "8":"Tourism"
    }
    return industry_types.get(item)

def validate_empty(item):
    if not not item:
        return item
    return None

def sha_256(item):
    return hash.sha256(item.encode('utf-8')).hexdigest()

@app.route("/")
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session["user_id"][0] == "i":
        return redirect(url_for("inf_dashboard"))
    
    if session["user_id"][0] == "s":
        return redirect(url_for("spn_dashboard"))
    
    if session["user_id"][0] == "a":
        return redirect(url_for("adm_dashboard"))
    
    return redirect(url_for('login'))

@app.route("/login")
def login():
    if 'user_id' in session:
        print("here is the issue")
        return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def post_login():
    u_mail = validate_empty(request.form.get('u_mail'))
    u_pass = validate_empty(request.form.get('u_pass'))
    if None in [u_mail,u_pass]:
        flash('Invalid Input')
        return redirect(url_for('home'))
    
    user = User.query.filter_by(user_name=u_mail).first()

    if not bool(user):
        flash("This user is not Registered")
        return redirect(url_for('home'))

    u_hash = sha_256(u_pass)
    if u_hash != user.pass_hash:
        flash("This user is not Registered")
        return redirect(url_for('home'))

    session["user_id"] = user.user_id
    session["user_name"] = user.user_name    

    return redirect(url_for('home'))

@app.route("/logout", methods=['POST','GET'])
def Logout():
    print("here is the issue")
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    session.clear()
    print("here")
    return redirect(url_for('home'))

@app.route("/register/influencer")
def inf_register():
    if 'user_id' in session:
        print("here is the issue")
        return redirect(url_for('login'))
    return render_template("Influencerregistration.html")

@app.route("/register/influencer", methods=['POST'])
def post_inf_register():
    inf_name = validate_empty(request.form.get("infName"))
    inf_email = validate_empty(request.form.get("infEmail"))
    inf_platforms = validate_empty(request.form.getlist("infPlatform"))
    inf_niche = validate_empty(request.form.get("infNiche"))
    inf_pass1 = validate_empty(request.form.get("infPass1"))
    inf_pass2 = validate_empty(request.form.get("infPass2"))

    user = None
    influencer = None

    if None in [inf_name,inf_email,inf_platforms,inf_niche,inf_pass1,inf_pass2] or inf_pass1 != inf_pass2:
        flash('Invalid Input')
        return redirect(url_for('home'))
    
    user = User(user_id=f"i_{sha_256(inf_email)}",user_name=inf_email,pass_hash=sha_256(inf_pass1))
    db.session.add(user)
    db.session.commit()

    influencer = Influencer(influencer_id=f"i_{sha_256(inf_email)}",influencer_name=inf_name,influencer_niche=inf_niche_pack(inf_niche),influencer_platforms=inf_platforms_pack(inf_platforms))
    db.session.add(influencer)
    db.session.commit()

    session["user_id"] = user.user_id
    session["user_name"] = user.user_name

    return redirect(url_for("inf_dashboard"))

@app.route("/register/sponsor")
def spn_register():
    if 'user_id' in session:
        print("here is the issue")
        return redirect(url_for('login'))
    return render_template("sponsorregistration.html")

@app.route("/register/sponsor", methods=['POST'])
def post_spn_register():
    spn_name = validate_empty(request.form.get("orgName"))
    spn_industry = validate_empty(request.form.get("orgIndustry"))
    spn_email = validate_empty(request.form.get("orgEmail"))
    spn_pass1 = validate_empty(request.form.get("orgPass1"))
    spn_pass2 = validate_empty(request.form.get("orgPass2"))

    user = None
    sponsor = None

    if None in [spn_name,spn_email,spn_industry,spn_pass1,spn_pass2] or spn_pass1 != spn_pass2:
        flash('Invalid Input')
        return redirect(url_for('home'))
    
    user = User(user_id=f"s_{sha_256(spn_email)}",user_name=spn_email,pass_hash=sha_256(spn_pass1))
    db.session.add(user)
    db.session.commit()

    sponsor = Sponsor(sponsor_id=f"s_{sha_256(spn_email)}",sponsor_name=spn_name,sponsor_industry=spn_industry_pack(spn_industry))
    db.session.add(sponsor)
    db.session.commit()

    session["user_id"] = user.user_id
    session["user_name"] = user.user_name

    print(spn_name, spn_email, spn_industry, spn_pass1, spn_pass2)
    return redirect(url_for("spn_dashboard"))

@app.route("/dashboard/influencer")
def inf_dashboard():
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    
    inf_id = session["user_id"]
    influencer = Influencer.query.filter_by(influencer_id=inf_id).first()

    flash("You have logged in " + str(influencer.influencer_name))

    print(influencer.adverts)

    return render_template('Infuencerdashboard.html', nav=True, inf=influencer)

@app.route("/dashboard/sponsor")
def spn_dashboard():
    if 'user_id' not in session or session['user_id'][0] != 's':
        return redirect(url_for('home'))
    sponsor = Sponsor.query.filter_by(sponsor_id=session.get('user_id')).first()
    infDet = db.session.query(Influencer.influencer_id,Influencer.influencer_name).all()
    
    return render_template('sponsordashboard.html', nav = True, spn = sponsor, influencerdetails = infDet)

@app.route("/dashboard/admin")
def adm_dashboard():
    if 'user_id' not in session or session['user_id'][0] != 'a':
        return redirect(url_for('home'))
    return render_template('admindashboard.html')

@app.route("/profile/influencer")
def inf_profile():
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    
    flash("welcome to profile")
    influencer = Influencer.query.filter_by(influencer_id=session.get('user_id')).first()

    return render_template('influencerprofile.html',nav=True,inf=influencer)

@app.route("/profile/influencer", methods=['POST'])
def inf_profile_post():
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    inf_name = validate_empty(request.form.get("infName"))
    inf_niche = validate_empty(request.form.get("infNiche"))
    inf_platforms = validate_empty(request.form.getlist("infPlatform"))
    inf_reach = validate_empty(request.form.get("infReach"))
    inf_pic = request.files['profile_pic_input']

    print("here no shit:",inf_pic)

    if None in [inf_name,inf_niche,inf_platforms,inf_reach]:
        flash('Please Fill all the values')
        return redirect(url_for('spn_profile'))

    influencer = Influencer.query.filter_by(influencer_id=session.get('user_id')).first()
    influencer.influencer_name = inf_name
    influencer.influencer_niche = inf_niche_pack(inf_niche)
    influencer.influencer_platforms = inf_platforms_pack(inf_platforms)
    influencer.influencer_platform_reach = inf_reach_pack(inf_reach)
    influencer.influencer_image = inf_pic.read()
    
    db.session.commit()

    flash("Profile updated successfully")

    return redirect(url_for('home'))

@app.route("/profile/sponsor")
def spn_profile():
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    
    flash("welcome to profile")

    return render_template('sponsorprofile.html',nav=True)

@app.route("/profile/sponsor", methods=['POST'])
def spn_profile_post():
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    spn_name = validate_empty(request.form.get("orgName"))
    spn_indus = validate_empty(request.form.get("orgIndustry"))
    spn_budget = validate_empty(request.form.get("orgBudget"))
    spn_pic = request.files['profile_pic_input']

    if None in [spn_name,spn_indus,spn_budget,spn_pic]:
        flash('Please Fill all the values')
        return redirect(url_for('spn_profile'))
    
    sponsor = Sponsor.query.filter_by(sponsor_id=session.get('user_id')).first()

    sponsor.sponsor_name = spn_name
    sponsor.sponsor_industry = spn_industry_pack(spn_indus)
    sponsor.sponsor_budget = spn_budget
    sponsor.sponsor_image = spn_pic.read()

    print(sponsor.sponsor_name,sponsor.sponsor_industry,sponsor.sponsor_budget,sponsor.sponsor_image)

    db.session.commit()

    flash("Profile updated successfully")

    return redirect(url_for('home'))

@app.route("/search", methods=['POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    item = request.form.get('searchItem')
    if session.get('user_id')[0] == 'i':
        campaign = Campaign.query.filter(
            Campaign.campaign_name.contains(item)
            ).all() + Campaign.query.filter(
                Campaign.campaign_description.contains(item)
                ).all()

        return render_template('searchedcamp.html',nav=True, camps = set(campaign), item = item)
    if session.get('user_id')[0] == 's':
        inf = Influencer.query.filter(
            Influencer.influencer_name.contains(item)
        ).all() + Influencer.query.filter(
            Influencer.influencer_niche.contains(item)
        ).all() + Influencer.query.filter(
            Influencer.influencer_platform_reach.contains(inf_reach_pack(item))
        ).all()
        
        return render_template('searchedinfl.html', nav=True, infs = set(inf), item = item)

@app.route("/create/campaign", methods=['POST'])
def create_campaign():

    if 'user_id' not in session or session['user_id'][0] != 's':
        return redirect(url_for('home'))
    
    campaign_nam = request.form.get('campName')
    campaign_vis = campaign_vis_pack(request.form.get('campVis'))
    campaign_budg = request.form.get('campBudg')
    campaign_desc = request.form.get('campDesc')
    campaign_s_date = request.form.get('startDate')
    campaign_e_date = request.form.get('endDate')

    print(campaign_nam, campaign_vis, campaign_budg, campaign_desc, campaign_s_date, campaign_e_date)

    spn = Sponsor.query.filter_by(sponsor_id=session.get('user_id')).first()
    campaign = Campaign(
        campaign_id=f"c_{sha_256(spn.sponsor_id + campaign_nam)}",
        campaign_name=campaign_nam,
        campaign_description=campaign_desc,
        campaign_budget=int(campaign_budg),
        campaign_visibility=campaign_vis,
        campaign_start_date=date_pack(campaign_s_date),
        campaign_end_date=date_pack(campaign_e_date),
        sponsor=spn
    )
    
    db.session.add(campaign)
    db.session.commit()

    flash("welcome to influencer search")

    return redirect(url_for('home'))

@app.route("/delete/campaign/<camp_id>",methods=["GET"])
def delete_camp(camp_id):
    campaign = Campaign.query.filter_by(campaign_id=camp_id).first()

    if 'user_id' not in session or campaign.sponsor_id != session.get('user_id'):
        flash("invalid user")
        return redirect(url_for('home'))

    db.session.delete(campaign)
    db.session.commit()

    flash("A campaign was deleted")
    return redirect(url_for('home'))

@app.route("/create/ad", methods=['POST'])
def create_ad():
    if 'user_id' not in session or session['user_id'][0] != 's':
        return redirect(url_for('home'))
    
    camp_id = request.form.get('campId')
    ad_nam = request.form.get('adName')
    ad_budg = request.form.get('adBudg')
    ad_req = request.form.get('adReq')

    camp = Campaign.query.filter_by(campaign_id=camp_id).first()

    if camp.campaign_visibility == "Public":
        ad_stat = 'open'
    else:
        ad_stat = 'unsent'

    advert = Advert(
        ad_id = f'a_{sha_256(camp_id + ad_nam)}',
        ad_name = ad_nam,
        ad_budget = ad_budg,
        ad_requirements = ad_req,
        ad_accepted = ad_stat,

        campaign = camp
    )

    db.session.add(advert)
    db.session.commit()

    return redirect(url_for('home'))  

@app.route("/assign/ad",methods=['POST'])
def assign_ad():
    if 'user_id' not in session or session['user_id'][0] != 's':
        return redirect(url_for('home'))
    infId = request.form.get('adInf')
    adId = request.form.get('adId')

    inf = Influencer.query.filter_by(influencer_id = infId).first()
    ad = Advert.query.filter_by(ad_id = adId).first()
    ad.ad_accepted ='sent'

    inf.adverts.append(ad)
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/accept/ad/<adId>",methods=['GET'])
def accept_ad(adId):
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    ad = Advert.query.filter_by(ad_id=adId).first()
    if ad.influencer_id != session.get('user_id'):
        flash("Invalid input")
        return redirect(url_for('home'))
    ad.ad_accepted = 'accepted'
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/take/ad/<adId>",methods=['GET'])
def take_ad(adId):
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    ad = Advert.query.filter_by(ad_id=adId).first()

    inf = Influencer.query.filter_by(influencer_id=session.get("user_id")).first()

    inf.adverts.append(ad)
    ad.ad_accepted = 'accepted'
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/all/influencer")
def all_inf():
    if 'user_id' not in session or session['user_id'][0] != 's':
        return redirect(url_for('home'))
    
    influencer = Influencer.query.filter_by().all()
    
    return render_template('all_inf.html',nav = True, infs = influencer)

@app.route("/all/campaign")
def all_camp():
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    
    campaign = Campaign.query.filter_by().all()

    print(campaign)

    return render_template('all_camp.html',nav = True, camps = campaign)


@app.route("/statistics/influencer")
def stat_inf():
    if 'user_id' not in session or session['user_id'][0] != 'i':
        return redirect(url_for('home'))
    
    influencer = Influencer.query.filter_by(influencer_id = session.get('user_id')).first()
    # total ads accepted, total money

    ads = influencer.adverts

    ad_names = [ad.ad_name for ad in ads]
    ad_rev = [int(ad.ad_budget) for ad in ads]

    print(ad_names,ad_rev)
    
    
    return render_template('statsinf.html' , nav = True , datas = ad_rev , lables = ad_names)

@app.route("/statistics/sponsor")
def stat_spn():
    if 'user_id' not in session or session['user_id'][0] != 's':
        return redirect(url_for('home'))
    
    spn = Sponsor.query.filter_by(sponsor_id = session.get('user_id')).first()

    camp = spn.campaigns

    c_names = [c.campaign_name for c in camp]
    c_budget= [c.campaign_budget for c in camp]

    return render_template('statsspn.html' , nav = True , datas = c_budget , lables = c_names)