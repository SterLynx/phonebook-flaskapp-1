from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
# Import the SignUpForm, LoginForm, and PostForm classes from forms
from app.forms import SignUpForm, LoginForm, AddContact
# Import the User model from models
from app.models import User, Contact
# Create our first route
@app.route('/')
def index():
    # SELECT * FROM post ORDER BY date_created DESC;
    # posts = db.session.execute(db.select(Post).order_by(db.desc(Post.date_created))).scalars().all()
    return render_template('index.html')


# Sign up route
@app.route('/signup', methods=['GET','POST'])
def signup():
    # create instance of the signupform
    form = SignUpForm()
    if form.validate_on_submit():
        # Get the data from each of the fidls
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        phone_number = form.phone_number.data
        # print(first_name, last_name, username, email, password)
        
        # Create new instance of the User class with the data from the form
        new_user = User(first_name = first_name, last_name = last_name, address=address, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        
        # log the newly created user in
        login_user(new_user)
        
        # Redirect back to the home page
        return redirect(url_for('phonebook'))
    return render_template('signup.html', form=form)






@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = db.session.execute(db.select(User).where(User.username==username)).scalar()
        if user is not None and user.check_password(password):
            login_user(user, remember=remember_me)
            # log user in via Flask-Login
            flash(f'{user.username} has successfully logged in.')
            return redirect(url_for('phonebook'))
        else:
            flash('Incorrect username and/or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('index'))




@app.route('/phonebook')
@login_required
def phonebook():
    contacts = db.session.execute(db.select(User)).scalars().all()
    return render_template('phonebook.html', contacts=contacts)





# Add contact route
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_contact():
    form = AddContact()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        
        check_contact = db.session.execute(db.select(Contact).where( (Contact.phone_number==phone_number))).scalars().all()
        if check_contact:
            flash('A contact with that phone number already exists')
            return redirect(url_for('add_contact'))
        
        new_contact = Contact(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id=current_user.id)
        db.session.add(new_contact)
        db.session.commit()
        flash(f"{new_contact} has been added to your contacts")
        
        return redirect(url_for('phonebook'))
    return render_template('add.html', form=form)