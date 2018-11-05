"""
webserver.py

File that is the central location of code for your webserver.
"""

from flask import Flask, render_template, request
import os
import requests
import json
import sqlite3


def get_connection():
	return sqlite3.connect('projects.db')

def create_shifts_table():
	conn = get_connection()
	c = conn.cursor()

	c.execute("CREATE TABLE IF NOT EXISTS shifts (shift_id integer PRIMARY KEY, slug text, shift_date text, shift_type text, quantity integer )")

	conn.commit()
	conn.close()

def create_completed_shifts_table():
	conn = get_connection()
	c = conn.cursor()

	c.execute("CREATE TABLE IF NOT EXISTS completed_shifts (shift_id integer, npi text, full_name text)")

	conn.commit()
	conn.close()


app = Flask(__name__)
create_shifts_table()
create_completed_shifts_table()

@app.route('/')
def load_default():
	return render_template("home.html")

@app.route('/index')
def load_index():
	"""
	If someone goes to the root of your website (i.e. http://localhost:5000/), run this function. The string that this
	returns will be sent to the browser
	"""
	return render_template("home.html") # Render the template located in "templates/index.html"

@app.route('/about')
def load_about():
	return render_template("about.html")

@app.route('/contact')
def load_contact():
	return render_template("contact.html")

# mailgun stuff
@app.route('/contact', methods=['POST'])
def send_contact():
	username = request.form.get("username")
	from_email = request.form.get("email")
	subject = request.form.get("subject")
	message = request.form.get("message")
	notifications = []

	data = {
		'from': from_email,
		'to': "muyingchen@berkeley.edu",
		'subject': subject,
		'text': message,
	}

	auth = (os.environ["INFO253_MAILGUN_USER"], os.environ["INFO253_MAILGUN_PASSWORD"])

	r = requests.post(
		'https://api.mailgun.net/v3/{}/messages'.format(os.environ["INFO253_MAILGUN_DOMAIN"]),
		auth=auth,
		data=data)

	if r.status_code == requests.codes.ok:
		response = "Thank you " + username + ", your email has been sent."
		notifications.append(response)
	else:
		response = "Sorry " + username + ", your email was not sent. Please try again."
		notifications.append(response)

	return render_template("contact.html", notifications=notifications)

@app.route('/volunteer', methods=['GET'])
def load_volunteer():
	return render_template("volunteer.html")


@app.route('/verify', methods=['POST'])
def verify_volunteer():
	npi = request.form.get("npi")

	api_response = requests.get(
		"https://api.betterdoctor.com/2016-03-01/doctors/npi/%s" % npi,
			params={"user_key": "0342b083731a904a7a774bb1b5b5a7a5",
			"fields": "licenses, profile(first_name, middle_name, last_name), specialties"})

	api_response = api_response.json()
	#print(api_response.get('data', {}).get('profile', {}).get('middle_name', {}))
	#print (api_response.get('data', {}).get('licenses', {}))
	#print (api_response['data']['profile']['first_name'])
	#print (api_response['data']['specialties'][0]['uid'])
	print("api response is :")
	print(api_response)

	if "http_status_code" in api_response['meta'] and api_response['meta']['http_status_code'] != 200:
		reason="Sorry, your license seems to be invalid and we are unable to proceed with your registration at this time."
		return render_template("NotEligibleVolunteer.html", Reason=reason)
	conn = get_connection()
	c = conn.cursor()

	data = api_response.get('data')
	specialties = data.get('specialties')
	specialty = specialties[0]['uid']
	profile = data.get('profile')
	first_name = profile.get('first_name')
	if profile.get('middle_name'):
		middle_name = profile.get('middle_name')
	last_name = profile.get('last_name')

	licenses = data.get('licenses')
	#specialty = api_response['data']['specialties'][0]['uid']

	if profile.get('middle_name'):
		full_name = first_name + " " + middle_name + " " + last_name
	else:
		full_name = first_name + " " + last_name

	c.execute("SELECT shift_id, slug, shift_date, shift_type, quantity FROM shifts WHERE shift_type = ?", [specialty])

	blogs = c.fetchall()

	return_data = list()
	if not blogs:
		reason="Sorry, there's no shifts available for your specialty. Thank you for visiting our site. "
		return render_template("NotEligibleVolunteer.html", Reason=reason)
	else:
		for blog in blogs:
			if blog[4] > 0:
				blog_dict = dict()
				blog_dict["shift_id"] = blog[0]
				blog_dict["slug"] = blog[1]
				blog_dict["shift_date"] = blog[2]
				blog_dict["shift_type"] = blog[3]
				blog_dict["quantity"] = blog[4]
				return_data.append(blog_dict)
		if len(licenses) > 0:
			return render_template("EligibleVolunteer.html",data=return_data, npi = npi, full_name = full_name)
		else:
			reason = "An error just occured. Please try again."
			return render_template("NotEligibleVolunteer.html", Reason=reason)

@app.route('/shift',methods=['POST'])
def volunteer_confirmed():
	shift_id = request.form.get("shift_id")
	print(shift_id)
	npi = request.form.get("npi")
	print(npi)
	full_name = request.form.get("full_name")
	print(full_name)
	quantity = request.form.get("quantity")
	print(quantity)
	conn = get_connection()
	c = conn.cursor()

	c.execute("SELECT shift_id, npi, full_name FROM completed_shifts WHERE shift_id = ? AND npi = ? AND full_name =?", [ shift_id, npi, full_name])

	blogs = c.fetchall()

	return_data = list()
	for blog in blogs:
		blog_dict = dict()

		return_data.append(blog_dict)
	if len(return_data) == 0:
		c.execute("INSERT INTO completed_shifts (shift_id, npi, full_name) VALUES (?, ?, ?)", [ shift_id, npi, full_name ])

		quantity = int(quantity) - 1
		if quantity < 0:
			quantity = 0

		c.execute("UPDATE shifts SET quantity = ? WHERE shift_id = ?", [ quantity, shift_id])
		conn.commit()
		conn.close()

		return render_template("VolunteerConfirmation.html")
	else:
		return render_template("VolunteerConfirmation.html")


@app.route('/shift', methods=['GET'])
def show_completed_shifts():
	conn = get_connection()
	c = conn.cursor()
	c.execute("SELECT shift_id, npi, full_name FROM completed_shifts")

	blogs = c.fetchall()

	return_data = list()
	for blog in blogs:
		blog_dict = dict()

		blog_dict["shift_id"] = blog[0]
		blog_dict["npi"] = blog[1]
		blog_dict["full_name"] = blog[2]

		return_data.append(blog_dict)

	return json.dumps(return_data)



@app.route('/organization')
def load_organizer():
	return render_template("organizer.html")

@app.route('/orgconfirm', methods=['GET','POST'])
def organization_confirmed():
	return render_template("OrganizationConfirmation.html")

@app.route('/schedule', methods=['POST'])
def load_schedule():
	print ('Parsing Request to JSON')
	#request_data = request.get_json()
	print ('Sucessfully parsed JSON')

	shift_id = None
	shift_date = request.form.get("shift_date")
	shift_type = request.form.get("shift_type")
	slug = shift_date + shift_type
	quantity = request.form.get("quantity")

	conn = get_connection()
	c = conn.cursor()
	c.execute("INSERT OR REPLACE INTO shifts (shift_id, slug, shift_date, shift_type, quantity) VALUES (?, ?, ?, ?, ?)", [ shift_id, slug, shift_date, shift_type, quantity ])
	conn.commit()
	conn.close()

	conn = get_connection()
	c = conn.cursor()

	c.execute("SELECT shift_id, slug, shift_date, shift_type, quantity FROM shifts")

	blogs = c.fetchall()

	return_data = list()
	for blog in blogs:
		blog_dict = dict()
		if blog[0] and blog[1] and blog[2] and blog[3] and blog[4] > 0:
			blog_dict["shift_id"] = blog[0]
			blog_dict["slug"] = blog[1]
			blog_dict["shift_date"] = blog[2]
			blog_dict["shift_type"] = blog[3]
			blog_dict["quantity"] = blog[4]
			return_data.append(blog_dict)

	return render_template("ScheduleViewer.html", data=return_data)


# View all'
@app.route('/schedule', methods=['GET'])
def get_schedule():
	print ('received', request)
	conn = get_connection()
	c = conn.cursor()

	c.execute("SELECT shift_id, slug, shift_date, shift_type, quantity FROM shifts")

	blogs = c.fetchall()

	return_data = list()
	for blog in blogs:
		blog_dict = dict()
		if blog[0] and blog[1] and blog[2] and blog[3] and blog[4] > 0:
			blog_dict["shift_id"] = blog[0]
			blog_dict["slug"] = blog[1]
			blog_dict["shift_date"] = blog[2]
			blog_dict["shift_type"] = blog[3]
			blog_dict["quantity"] = blog[4]

			c.execute("SELECT full_name FROM completed_shifts WHERE shift_id=?", [blog[0]])
			volunteers = c.fetchall()
			if volunteers:
				volunteer_str = ""
				for i in range(len(volunteers)):
					# v is a tuple
					volunteer_str += volunteers[i][0]
					if i < len(volunteers) - 1:
						volunteer_str += ", "
				blog_dict["volunteers"] = volunteer_str

			return_data.append(blog_dict)

	return render_template("ScheduleViewer.html", data=return_data)



#View shifts that still needs volunteers
@app.route('/schedulebyquantity', methods=['GET'])
def get_schedule_by_quantity():
	print ('received', request)
	conn = get_connection()
	c = conn.cursor()

	c.execute("SELECT shift_id, slug, shift_date, shift_type, quantity FROM shifts WHERE quantity>0")

	blogs = c.fetchall()

	return_data = list()
	for blog in blogs:
		blog_dict = dict()
		if blog[0] and blog[1] and blog[2] and blog[3] and blog[4] > 0:
			blog_dict["shift_id"] = blog[0]
			blog_dict["slug"] = blog[1]
			blog_dict["shift_date"] = blog[2]
			blog_dict["shift_type"] = blog[3]
			blog_dict["quantity"] = blog[4]

			c.execute("SELECT full_name FROM completed_shifts WHERE shift_id=?", [blog[0]])
			volunteers = c.fetchall()

			if volunteers:
				volunteer_str = ""
				for i in range(len(volunteers)):
					# v is a tuple
					volunteer_str += volunteers[i][0]
					if i < len(volunteers) - 1:
						volunteer_str += ", "
				blog_dict["volunteers"] = volunteer_str
			return_data.append(blog_dict)

	return render_template("ScheduleViewer.html", data=return_data)


#View schedule by specialty
@app.route('/schedulebyspecialty', methods=['GET'])
def get_schedule_by_specialty():
	print ('received', request)
	conn = get_connection()
	c = conn.cursor()

	shift_type = request.args.get("shift_type")
	print (shift_type)
	c.execute("SELECT shift_id, slug, shift_date, shift_type, quantity FROM shifts WHERE shift_type = ?", [shift_type ])


	blogs = c.fetchall()

	return_data = list()
	for blog in blogs:
		blog_dict = dict()
		if blog[0] and blog[1] and blog[2] and blog[3] and blog[4] > 0:
			blog_dict["shift_id"] = blog[0]
			blog_dict["slug"] = blog[1]
			blog_dict["shift_date"] = blog[2]
			blog_dict["shift_type"] = blog[3]
			blog_dict["quantity"] = blog[4]

			c.execute("SELECT full_name FROM completed_shifts WHERE shift_id=?", [blog[0]])
			volunteers = c.fetchall()
			if volunteers:
				volunteer_str = ""
				for i in range(len(volunteers)):
					# v is a tuple
					volunteer_str += volunteers[i][0]
					if i < len(volunteers) - 1:
						volunteer_str += ", "
				blog_dict["volunteers"] = volunteer_str
			return_data.append(blog_dict)

	return render_template("ScheduleViewer.html", data=return_data)
