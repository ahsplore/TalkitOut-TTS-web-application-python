from application import utils
from . import db
import os
import secrets
import cv2
import pytesseract
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Flask
import numpy as np
from gtts import gTTS
from application import app
from application.forms import MyForm
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route("/")
def home():
    return render_template('home.html')


@auth.route('/dictionary')
def dictionary():
    return render_template('dictionary.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@app.route('/upload', methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        sentence = ""
        f = request.files.get('file')
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(20) + f".{extension}"
        file_location = os.path.join(app.config["UPLOADED_PATH"], generated_filename)
        f.save(file_location)
        pytesseract.pytesseract.tesseract_cmd = r"full path to the exe file"
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        img = cv2.imread(file_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = pytesseract.image_to_data(img)
        for i, box in enumerate(boxes.splitlines()):
            if i == 0:
                continue
            box = box.split()
            if len(box) == 12:
                sentence += box[11] + " "
        session['sentence'] = sentence
        os.remove(file_location)
        return redirect('/decoded/')
    else:
        return render_template("upload.html", user=current_user)


@auth.route('/decoded', methods=['POST', 'GET'])
def decoded():
    sentence = session.get("sentence")
    form = MyForm()
    if request.method == "POST":
        generated_audio_filename = secrets.token_hex(10) + ".mp4"
        text_data = form.text_field.data
        translate_to = form.language_field.data
        translated_text = utils.translate_text(text_data, dest=translate_to)
        form.text_field.data = translated_text

        tts = gTTS(translated_text, lang=translate_to)
        file_location = os.path.join(app.config["AUDIO_FILE_UPLOAD"], generated_audio_filename)
        tts.save(file_location)
        return render_template("decoded.html", form=form, user=current_user, audio=True, file=generated_audio_filename)
    else:
        form.text_field.data = sentence
        session['sentence'] = ""
        return render_template("decoded.html", form=form, user=current_user, audio=False)
