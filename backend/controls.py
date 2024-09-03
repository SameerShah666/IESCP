from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask import current_app as app
from .models import *

import json as j
import hashlib as hash


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
        print("here is the issue")
        return redirect(url_for('login'))
    
    if session["user_id"][0] == "i":
        return redirect(url_for("inf_dashboard"))
    
    if session["user_id"][0] == "s":
        return redirect(url_for("spn_dashboard"))
    
    return redirect(url_for('login'))

@app.route("/trial", methods=['POST'])
def trial():
    data = request.get_json()
    return {"result":data["value"]}

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

    return render_template("login.html")

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
    return render_template("sponsorregistration.html")

@app.route("/dashboard/sponsor")
def spn_dashboard():
    if 'user_id' not in session:
        print("here is the issue")
        return redirect(url_for('login'))
    return render_template('admindashboard')

@app.route("/dashboard/influencer")
def inf_dashboard():
    if 'user_id' not in session:
        print("here is the issue")
        return redirect(url_for('login'))
    
    inf_id = session["user_id"]
    influencer = Influencer.query.filter_by(influencer_id=inf_id).first()

    return render_template('Infuencerdashboard.html',name=influencer.influencer_name,email=influencer.influencer_email)

@app.route("/dashboard/admin")
def adm_dashboard():
    if 'user_id' not in session:
        print("here is the issue")
        return redirect(url_for('login'))
    return render_template('admindashboard.html')