from flask import Flask, render_template, request, redirect, session, flash
import random , re
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
app = Flask(__name__)
app.secret_key = "16E6A06CACB9C1E039541F7AE78714251422BC6A586310BED50639CAB4D32001"

@app.route('/')
def index():
    print(session)
    first_name,email,last_name= '','' ,'' 
    if 'email' in session:
        email = session['email']
    if 'first_name' in session: 
        first_name = session['first_name']
    if 'last_name' in session:
        last_name = session['last_name']
    return render_template("index.html", email = email, first_name = first_name , last_name = last_name)

@app.route('/submit', methods =["POST"])
def submit():
    session.clear()
    session['win'] = 0
    arr=['abc', '123','456','qwerty','789', 'pass','p@ss','$$', '00', '11', 'trustno1']
    for key in request.form:
# T1 Flag missing keys (bad)
        if request.form[key]=='':
            flash(key +" missing", 'error')
            session['win'] = 1
# T1 STORE ALL non-pw keys in session (good)
        if request.form[key] != ''and key!='password' and key!= 'confirm_password' :
            session[key] = request.form[key]
            if request.form[key] not in arr:
                arr.append(request.form[key])          
    # T2 regex on names if not blank (bad)
            if (key=='first_name' or key=='last_name') and not NAME_REGEX.match(request.form[key]):
                flash("Please use only english characters for "+key,'error' )
                session['win'] = 1
    # T2 regex on email (bad)
            if key=='email' and not EMAIL_REGEX.match(request.form[key]):
                flash("email is not valid" ,'error' )

# LOOP ENDED, START PW CHECKING (bad)
# check some common passwords + all name entry fields again
    for x in range(len(arr)):       
        if arr[x] in request.form['password']:
            flash("Your password is not secure. Please choose another password" ,'error' )
            session['win'] =1
            break
# check for password match (good)
    if 'password' in request.form and 'confirm_password' in request.form:
        if request.form['password'] != request.form['confirm_password']:
            flash(u'Your password do not match', 'error')
            session['win'] =1
# check for capital and number
    if not (any(x.isupper() for x in request.form['password'])and any(x.isdigit() for x in request.form['password'])):
        flash(u'You must have at least 1 number and 1 Capital letter in your password', 'error')
        session['win'] =1
# did you survive?
    if session['win'] == 0:
        session.clear()
        flash(u'Thanks for submitting your information.', 'success')
# remove pii
    arr=['abc', '123','456','qwerty','789', 'pass','p@ss','$$','w0rd', 'trustno1']
    return redirect ('/')
 

if __name__=="__main__":
    app.run(debug=True)
