import requests
from flask import Flask, render_template, request, redirect
from twilio.rest import Client

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration():
    return render_template("Registration.html")


@app.route('/RegistrationDetails', methods=["POST", "GET"])
def registration_details():
    if request.method == "GET":
        print("No data found")
        return redirect('/')
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phonenumber = request.form['phonenumber']
    id_proof = request.form['idcard']
    date = request.form['date']
    full_name = first_name + " " + last_name
    print(full_name+" "+email_id+" "+source_st+" "+source_dt+" "+destination_st+" "+destination_dt+" "+phonenumber+" "+id_proof+" "+date)
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    try:
        cnt = json_data[destination_st]["districts"][destination_dt]["total"]["confirmed"]
        pop = json_data[destination_st]["districts"][destination_dt]["meta"]["population"]
        print("covid cases:",cnt)
        print("population:",pop)
    except KeyError:
        print("No data found")
        return render_template('registration.html')
    travel_pass = (cnt / pop) * 100
    print(travel_pass)
    if travel_pass < 30:
        status = 'CONFIRMED'
        print("status",status)
        client.messages.create(to="+91"+phonenumber, from_="",
                              body="Hello" + " " + full_name + " " + "Permission for your Travel From" + " " + source_dt + " " + destination_dt + " Is GRANTED")
        return render_template('Registration_Details.html', var1=full_name, var2=email_id, var3=id_proof,
                               var4=source_st, var5=source_dt, var6=destination_st, var7=destination_dt,
                               var8=phonenumber, var9=date, var10=status)
    else:
        status = 'NOT CONFIRMED'
        print("status:",status)
        client.messages.create(to="+91"+phonenumber, from_="",
                               body="Hello" + " " + full_name + " " + "Permission for your Travel From" + " " + source_dt + " " + destination_dt + " IS NOT GRANTED")
        return render_template('Registration_Details.html', var1=full_name, var2=email_id, var3=id_proof,
                               var4=source_st, var5=source_dt, var6=destination_st, var7=destination_dt,
                               var8=phonenumber, var9=date, var10=status)


if __name__ == "__main__":
    app.run()
