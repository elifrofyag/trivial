from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from AnimalTracker import app
import pandas as pd
import os
import json
import csv
import random
import string
import smtplib
from email.mime.text import MIMEText
from flask import session
from email.mime.multipart import MIMEMultipart


app.secret_key = "your_secret_key"


# Function to read CSV and extract GPS coordinates
def get_gps_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "thing_gps.csv")
    df = pd.read_csv(file_path)
    gps_data = []
    for index, row in df.iterrows():
        timestamp = row["time"]
        lat = float(row["value"].split(":")[1])
        lon = float(row["Unnamed: 2"].split(":")[1].strip("}"))
        # Parse timestamp to extract date and time
        truncated_timestamp = timestamp[:26] + "Z"
        dt = datetime.strptime(truncated_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        date = dt.date()
        time = dt.time()

        gps_data.append(
            {
                "timestamp": timestamp,
                "date": str(date),
                "time": str(time),
                "lat": lat,
                "lng": lon,
            }
        )

    return gps_data


@app.route("/", methods=["GET", "POST"])
def index():
    gps_data = get_gps_data()
    return render_template("login.html")


# ---------------------------------------HOMEPAGE ROUTES-------------------------------------------------
lat_gb = None
lng_gb = None
rad_gb = None


@app.route("/homepage", methods=["POST"])
def home():
    global lat_gb, lng_gb, rad_gb

    gps_data = get_gps_data()

    email = request.form["email"]
    password = request.form["password"]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE_PATH = os.path.join(base_dir, "static", "data", "users_data.csv")

    # Check if the CSV file exists
    file_exists = os.path.isfile(CSV_FILE_PATH)

    if not file_exists:
        flash("User not found. Please sign up.")
        return redirect("/")

    user_found = False

    with open(CSV_FILE_PATH, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email and row[1] == password:
                user_found = True
                lat = row[2]
                lng = row[3]
                rad = row[4]
                lat_gb = lat
                lng_gb = lng
                rad_gb = rad
                break

    if user_found:
        return render_template(
            "homepage.html", gps_data=gps_data, lat=lat, lng=lng, rad=rad
        )

    else:
        flash("Invalid email or password. Please try again.")
        return redirect("/")


@app.route("/send_alert", methods=["POST"])
def send_alert():
    data = request.json
    message = data.get("message")
    timestamp = data.get("timestamp")
    print(f"Alert received: {message} at {timestamp}")
    return jsonify(success=True), 200


# ------------------------------------------SAFE ZONE ROUTES------------------------------------------------


@app.route("/set_safe_zone")
def set_safe_zone():
    return render_template("set_safe_zone.html")


@app.route("/update_safe_zone", methods=["POST"])
def update_safe_zone():
    global lat_gb, lng_gb, rad_gb

    gps_data = get_gps_data()

    lat = request.form["lat"]
    lng = request.form["lng"]
    rad = request.form["rad"]
    lat_gb = lat
    lng_gb = lng
    rad_gb = rad
    email = request.form["email"]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "static", "data", "users_data.csv")
    updated_rows = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == email:
                row[2] = lat
                row[3] = lng
                row[4] = rad
            updated_rows.append(row)
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(updated_rows)
    return render_template(
        "homepage.html", gps_data=gps_data, lat=lat, lng=lng, rad=rad
    )


# --------------------------------------------ABOUT-US ROUTES----------------------------------------------------------------
@app.route("/about_us", methods=["POST", "GET"])
def about():
    return render_template("about_us.html")


@app.route("/back", methods=["POST", "GET"])
def back():
    gps_data = get_gps_data()
    return render_template(
        "homepage.html", gps_data=gps_data, lat=lat_gb, lng=lng_gb, rad=rad_gb
    )


# --------------------------------------PASSWORD ROUTES -----------------------------------------------


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(base_dir, "static", "data", "users_data.csv")
        user_found = False
        with open(csv_file, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == email:
                    user_found = True
                    break
        if user_found:
            return render_template("reset_password_confirm.html", email=email)
        else:
            flash("Email not found. Please try again.")
            return redirect(url_for("reset_password"))
    return render_template("reset_password.html")


@app.route("/reset_password_confirm", methods=["POST"])
def reset_password_confirm():
    email = request.form.get("email")
    new_password = request.form.get("new_password")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "static", "data", "users_data.csv")
    updated_rows = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == email:
                row[1] = new_password
            updated_rows.append(row)
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(updated_rows)
    flash("Password reset successfully. Please log in with your new password.")
    session.pop("reset_code", None)
    session.pop("email", None)
    return redirect(url_for("index"))


# Create a code and check whether the user input matches the code
def generate_reset_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def send_email(to_email, subject, body):
    # Configure your SMTP server credentials
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "animaltrackergroup2@gmail.com"
    smtp_password = "vrrf amng oipk pabw"

    # Create a secure SMTP session
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start TLS for security
        server.login(smtp_user, smtp_password)

        # Prepare the message
        message = MIMEMultipart()
        message["From"] = smtp_user
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send the email
        server.send_message(message)


@app.route("/send_reset_code", methods=["POST"])
def send_reset_code():
    email = request.form.get("email")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "static", "data", "users_data.csv")
    user_found = False
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == email:
                user_found = True
                break
    if user_found:
        reset_code = generate_reset_code()
        session["reset_code"] = reset_code
        session["email"] = email
        send_email(
            email, "Password Reset Code", f"Your password reset code is: {reset_code}"
        )
        return render_template("enter_reset_code.html", email=email)
    else:
        flash("Email not found. Please try again.")
        return redirect(url_for("reset_password"))


@app.route("/verify_reset_code", methods=["POST"])
def verify_reset_code():
    email = request.form.get("email")
    reset_code = request.form.get("reset_code")
    if session.get("reset_code") == reset_code and session.get("email") == email:
        return render_template("reset_password_confirm.html", email=email)
    else:
        flash("Invalid code. Please try again.")
        return render_template("enter_reset_code.html", email=email)


# ------------------------------------SIGN-UP ROUTES---------------------------------------------------


@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("signup.html")


@app.route("/confirm_signup", methods=["POST"])
def answer():
    email = request.form["email"]
    password = request.form["create-password"]
    lat = request.form["lat"]
    lng = request.form["lng"]
    rad = request.form["rad"]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE_PATH = os.path.join(base_dir, "static", "data", "users_data.csv")

    # Check if the CSV file exists
    file_exists = os.path.isfile(CSV_FILE_PATH)

    # Open the CSV file in append mode
    with open(CSV_FILE_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Write the header if the file is new
        if not file_exists:
            writer.writerow(["Email", "Password", "lat", "lng", "rad"])
        # Write the user data
        writer.writerow([email, password, lat, lng, rad])

    return render_template("confirm_signup.html", email=email)
