from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True

form = """
<!doctype html>
<html>
    <body>
        <form action="/hello">
            <label for="first-name">First Name</label>
            <input id="first-name" type="text" name="first_name" />
            <input type ="submit" />
        </form>
    </body>
</html>
"""

signup_form = """
    <style>
        .error {{ color: red; }}
        </style>
        <h1>Validate Signup</h1>
        <form method='Post'>
            <label>Username (3-20 characters)
                <input name="username" type="text" value='{username}' />
            </label>
            <p class="error">{username_error}</p>
            <label>Password (3-20 characters)
                <input name="password" type="password" value='{password}' />
            </label>
            <p class="error">{password_error}</p>
            <label>Retype Password
                <input name="re_password" type="password" value='{re_password}' />
            </label>
            <p class="error">{re_password_error}</p>
            <label>e-mail
                <input name="email" type="text" value='{email}' />
            </label>
            <p class="error">{email_error}</p>
            <input type="submit" value="Validate" />
        </form>
    """

@app.route("/")
def index():
    return form

@app.route('/validate-signup')
def display_signup_form():
    return signup_form.format(username='', username_error='',
        password='', password_error='', 
        re_password='', re_password_error='',
        email='', email_error='')

def is_integer(num):
    try: 
        int(num)
        return True
    except ValueError:
        return False

@app.route('/validate-signup', methods=['POST'])
def validate_signup():

    username = request.form['username']
    password = request.form['password']
    re_password = request.form['re_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    re_password_error = ''
    email_error = ''

    if not username:
        username_error = 'Missing username'
        username = '' 
    else:
        username = username
        if len(username) > 20 or len(username) < 3:
            username_error = 'Username length out of range (3-20)'
            username = ''
        if " " in username:
            username_error = 'Username should not contain spaces'
            username = ''
         
    if not password:
        password_error = 'Missing password'
        password = '' 
    else:
        password = password
        if len(password) > 20 or len(password) < 3:
            password_error = 'Password length out of range (3-20)'
            password = ''
        if " " in password:
            password_error = 'Password should not contain spaces'
            password = ''

    if not password_error:
        if password != re_password:
            re_password_error = 'Passwords do not match'
            re_password = ''

    if email:
        email = email
        if len(email) > 20 or len(email) < 3:
            email_error = 'E-mail length out of range (3-20)'
            email = ''
        if " " in email:
            email_error = 'invalid e-mail'
            email = ''
        if email.count(".") != 1:
            email_error = 'invalid e-mail'
        if email.count("@") != 1:
            email_error = 'invalid e-mail'

    if not password_error and not username_error and not re_password_error and not email_error:
        return "Welcome, " + str(username)
    else: 
        return signup_form.format(username_error=username_error, 
            password_error=password_error,
            re_password_error=re_password_error,
            email_error=email_error,
            username=username,
            password='',
            re_password='',
            email = email)

@app.route("/hello")
def hello():
    first_name = request.args.get('first_name') 
    #request.args.get argument is the input name in html above
    return '<h1>Hello, ' + first_name + '</h1>'


app.run()