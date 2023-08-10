from flask import Flask, render_template, redirect, url_for, request , session, current_app, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import union_all, or_
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField, RadioField
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, InputRequired
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_mail import Message, Mail
from flask_migrate import Migrate
import os
import secrets
from PIL import Image


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba249'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfDaOcmAAAAAOm0GX1fYcjF2aWPAP8gjeIsTt71'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfDaOcmAAAAANAt0I-HNQArCQJwlqFiYQAdEAGa'
app.config["RECAPTCHA_USE_SSL"] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ottobuddies@gmail.com'
app.config['MAIL_PASSWORD'] = 'xvauafngxzvvwjbo'
mail = Mail(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthday = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(120), nullable=True)
    marriage_status = db.Column(db.String(120), nullable=True)
    sexual_orientation = db.Column(db.String(120), nullable=True)
    workplace = db.Column(db.String(120), nullable=True)
    education = db.Column(db.String(120), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)
    dating = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expiration=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expiration)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    post_image = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Connection(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref("sent_connections"))
    followed = db.relationship('User', foreign_keys=[followed_id], backref=db.backref("received_connections"))

    def __repr__(self):
        return f"Connection('{self.follower_id}', '{self.followed_id}', '{self.status}')"


class ViewBlock(db.Model):
    blocker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    blocked_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.Boolean, default=False)
    blocker = db.relationship('User', foreign_keys=[blocker_id], backref=db.backref("block"))
    blocked = db.relationship('User', foreign_keys=[blocked_id], backref=db.backref("be_blocked"))

    def __repr__(self):
        return f"ViewBlock('{self.blocker_id}', '{self.blocked_id}', '{self.status}')"
    

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    captcha = RecaptchaField()
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    captcha = RecaptchaField()
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    dob = DateField('Date of birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[(None, 'Choose'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    marriage_status = SelectField('Marriage status', choices=[(None, 'Choose'), ('single', 'Single'),('engaged', 'Engaged'), 
                                                              ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')])
    sexual_orientation = StringField('Sexual orientation', validators=[Length(min=0, max=20)])
    dating = SelectField('Available and interested in dating', choices=[(None, 'Choose'), ('yes', 'Yes'), ('no', 'No')])
    workplace = StringField('Workplace', validators=[Length(min=0, max=20)])
    edu = StringField('Education', validators=[Length(min=0, max=20)])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if not current_user.is_admin:
            if username.data != current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if not current_user.is_admin:
            if email.data != current_user.email:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    image = FileField('Post Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

    def validate_on_submit(self):	
        if not super().validate_on_submit():	
            return False	
        # Perform the custom validation	
        if not self.title.data and not self.content.data and not self.image.data:	
            self.title.errors.append('At least one field is required: Title, Content, or Image')	
            return False	
        return True	

class SearchFriendForm(FlaskForm):
    searched = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

@app.context_processor
def inject_friend_request_count():
    if current_user.is_authenticated:
        received_friend_requests, sent_friend_requests = get_friend_requests(current_user.id)
        num_total_requests = len(received_friend_requests)
        return dict(num_total_requests=num_total_requests, received_friend_requests=received_friend_requests)
    return dict()

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.blocked == False:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and user.blocked == True:
            flash('Login unsuccessful. You are blocked.', 'danger')
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        if current_user.is_admin:
            posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
            return render_template('home.html', posts=posts)
        else:
            friends = get_friends(current_user.id)
            blocked_users = get_blocked(current_user.id)
            user_ids = [current_user.id] + [friend.id for friend in friends if friend.id not in [blocked_user.id for blocked_user in blocked_users]]
            posts = Post.query.filter(Post.user_id.in_(user_ids)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
            return render_template('home.html', posts=posts)
    return render_template('home.html', posts=None)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_cnt = db.session.query(User).count()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=True if user_cnt == 0 else False)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! You are now able to use Otto Buddies.', 'success')
        flash('Update your profile and search for your friends!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture_profile(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pics/profile_pics',  picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/profile")
@login_required
def profile():
    image_file = url_for('static', filename='pics/profile_pics/' + current_user.image_file)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.user_id == current_user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('profile.html', title='Profile', image_file=image_file, posts=posts)



@app.route("/setting/", methods=['GET', 'POST'])
@login_required
def setting():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_profile(form.picture.data)
            current_user.image_file = picture_file
        if form.username.data:
            current_user.username = form.username.data
        if form.email.data:
            current_user.email = form.email.data
        if form.dob.data:
            current_user.birthday = form.dob.data
        if form.gender.data != 'None':
            current_user.gender = form.gender.data
        else:
            current_user.gender = None
        if form.marriage_status.data != 'None':
            current_user.marriage_status = form.marriage_status.data
        else:
            current_user.marriage_status = None
        if form.sexual_orientation.data:
            current_user.sexual_orientation = form.sexual_orientation.data
        if form.dating.data != 'yes':
            current_user.dating = False
        else:
            current_user.dating = True
        if form.workplace.data:
            current_user.workplace = form.workplace.data
        if form.edu.data:
            current_user.education = form.edu.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.birthday:
            form.dob.data = datetime.strptime(current_user.birthday, '%Y-%m-%d')
        form.gender.data = current_user.gender
        form.marriage_status.data = current_user.marriage_status
        form.sexual_orientation.data = current_user.sexual_orientation
        form.workplace.data = current_user.workplace
        form.edu.data = current_user.education
        if current_user.dating is True:
            form.dating.data = "yes"
        else:
            form.dating.data = "no"
    image_file = url_for('static', filename='pics/profile_pics/' + current_user.image_file)
    return render_template('setting.html', title='Setting', image_file=image_file, form=form)

def save_picture_post(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pics/post_pics',  picture_fn)

    output_size = (500, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture_post(form.image.data)
            post = Post(title=form.title.data, content=form.content.data, author=current_user, post_image=picture_file)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture_post(form.image.data)
            post.post_image = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/search", methods=['POST'])
def search():
    form = SearchFriendForm()
    if form.validate_on_submit():
        searched_username = form.searched.data
        user = User.query.filter(User.username.ilike(f'%{searched_username}%'), User.blocked == False).first()
        if user:
            return render_template('search.html', form=form, searched=searched_username, user=user)
        else:
            flash("User not found.", 'not_found')
            return redirect(url_for('home'))

@app.context_processor
def layout():
    form = SearchFriendForm()
    return dict(form=form)


@app.route("/user/<string:username>")
def user_profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter(Post.user_id == user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='pics/profile_pics/' + user.image_file)
    follower_id = current_user.id
    followed_id = user.id
    friends, pending_request = is_friends_or_pending(follower_id, followed_id)
    be_blocked = is_blocked(follower_id, followed_id)
    check_blocked = is_blocked(followed_id, follower_id)
    received_requests = Connection.query.filter_by(follower_id=followed_id, followed_id=follower_id, status = "Requested").all()
    return render_template('user_profile.html', title='User_profile', image_file=image_file, user=user, friends=friends, pending_request=pending_request, posts=posts, is_blocked=be_blocked, check_blocked=check_blocked, received_requests=received_requests)

def is_friends_or_pending(follower_id, followed_id):
    is_friends = db.session.query(Connection).filter(or_(
        (Connection.follower_id == follower_id) & (Connection.followed_id == followed_id),
        (Connection.follower_id == followed_id) & (Connection.followed_id == follower_id)
        ),Connection.status == "Accepted").first()

    is_pending = db.session.query(Connection).filter(Connection.follower_id == follower_id,
                                                     Connection.followed_id == followed_id,
                                                     Connection.status == "Requested").first()
    
    return is_friends, is_pending


def get_friend_requests(user_id):
    received_friend_requests = db.session.query(User).filter(Connection.followed_id == user_id,
                                                             Connection.status == "Requested").join(Connection,
                                                                                                    Connection.follower_id == User.id).all()

    sent_friend_requests = db.session.query(User).filter(Connection.follower_id == user_id,
                                                         Connection.status == "Requested").join(Connection,
                                                                                                Connection.followed_id == User.id).all()

    return received_friend_requests, sent_friend_requests


def get_friends(user_id):
    friends_1 = db.session.query(User).filter(Connection.follower_id == user_id,
                                            Connection.status == "Accepted").join(Connection,
                                                                                  Connection.followed_id == User.id)
    friends_2 = db.session.query(User).filter(Connection.followed_id == user_id,
                                            Connection.status == "Accepted").join(Connection,
                                                                                  Connection.follower_id == User.id)
    merged_friends = union_all(friends_1, friends_2)
    friends = db.session.query(User).from_statement(merged_friends)
    return friends

@app.route("/friends")
@login_required
def show_friends_and_requests():
    received_friend_requests, sent_friend_requests = get_friend_requests(current_user.id)
    friends= get_friends(current_user.id)
    num_total_requests = len(received_friend_requests)
    return render_template("friends.html",
                           num_total_requests=num_total_requests,
                           received_friend_requests=received_friend_requests,
                           friends=friends)


@app.route("/add-friend", methods=["POST"])
def add_friend():
    follower_id = current_user.id
    followed_id = request.form.get('user_id')
    user = User.query.filter_by(id=followed_id).first_or_404()
    is_friends, is_pending = is_friends_or_pending(follower_id, followed_id)

    if follower_id == followed_id:
        flash("You cannot add yourself as a friend.", 'cannot')
    elif is_friends:
        flash("You are already friends.", 'already')
    elif is_pending:
        flash("Your friend request is pending.", 'pending')
    else:
        requested_connection = Connection(follower_id=follower_id, followed_id=followed_id, status="Requested")
        db.session.add(requested_connection)
        db.session.commit()
        flash("Request Sent", 'success')
    return redirect(url_for('user_profile', username=user.username))

@app.route("/cancel-friend", methods=["POST"])
def cancel_friend():
    follower_id = current_user.id
    followed_id = request.form.get('user_id')
    user = User.query.filter_by(id=followed_id).first_or_404()
    is_friends, is_pending = is_friends_or_pending(follower_id, followed_id)

    if is_friends or is_pending:
        cancel_connection = Connection.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        db.session.delete(cancel_connection)
        db.session.commit()
        flash("Cancel friend request.", 'success')
    return redirect(url_for('user_profile', username=user.username))

@app.route("/accept-friend", methods=["POST"])
def accept_friend():
    follower_id = request.form.get('user_id')
    followed_id = current_user.id
    user = User.query.filter_by(id=follower_id).first_or_404()
    is_friends, is_pending = is_friends_or_pending(follower_id, followed_id)

    if is_friends:
        flash("You are already friends.", 'already')
    else:
        accept_connection_1 = Connection.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        accept_connection_1.status="Accepted"
        accept_connection_2 = Connection.query.filter_by(follower_id=followed_id, followed_id=follower_id).first()
        if accept_connection_2:
            accept_connection_2.status="Accepted"
        db.session.commit()
        flash("Accept friend request.", 'success')
    return redirect(url_for('user_profile', username=user.username))

@app.route("/delete-friend", methods=["POST"])
def delete_friend():
    follower_id = request.form.get('user_id')
    followed_id = current_user.id
    user = User.query.filter_by(id=follower_id).first_or_404()
    is_friends, is_pending = is_friends_or_pending(follower_id, followed_id)

    if is_friends or is_pending:
        delete_connection = Connection.query.filter(or_(
            (Connection.follower_id == follower_id) & (Connection.followed_id == followed_id),
            (Connection.follower_id == followed_id) & (Connection.followed_id == follower_id)
            )).first()
        db.session.delete(delete_connection)
        db.session.commit()
        flash("Delete friend request.", 'success')
    return redirect(url_for('user_profile', username=user.username))

def is_blocked(blocker_id, blocked_id):
    is_blocked = db.session.query(ViewBlock).filter(
        ViewBlock.blocker_id == blocker_id, ViewBlock.blocked_id == blocked_id, ViewBlock.status == True).first()
    return is_blocked

def get_blocked(user_id):
    blocked_list_1 = db.session.query(User).filter(ViewBlock.blocker_id == user_id,
                                            ViewBlock.status == True).join(ViewBlock,
                                                                                  ViewBlock.blocked_id == User.id)
    blocked_list_2 = db.session.query(User).filter(ViewBlock.blocked_id == user_id,
                                            ViewBlock.status == True).join(ViewBlock,
                                                                                  ViewBlock.blocker_id == User.id)
    blocked_list = union_all(blocked_list_1, blocked_list_2)
    blocked_users = db.session.query(User).from_statement(blocked_list)
    return blocked_users

@app.route("/block-view", methods=["POST"])
def block_view():
    blocker_id = current_user.id
    blocked_id = request.form.get('user_id')
    user = User.query.filter_by(id=blocked_id).first_or_404()
    be_blocked = is_blocked(blocker_id, blocked_id)

    if blocker_id == blocked_id:
        flash("You cannot block yourself.", 'cannot')
    elif be_blocked:
        unblock_view = ViewBlock.query.filter_by(blocker_id=blocker_id, blocked_id=blocked_id).first()
        unblock_view.status = False
        db.session.commit()
        flash("This user can view your profile now.", 'already')
    else:
        already_blocked = db.session.query(ViewBlock).filter(ViewBlock.blocker_id == blocker_id, ViewBlock.blocked_id == blocked_id, ViewBlock.status == False).first()
        if already_blocked:
            already_blocked.status = True
            db.session.commit()
            flash("You have restricted this user. He cannot view your profile now", 'already')
        else:
            block_view = ViewBlock(blocker_id=blocker_id, blocked_id=blocked_id, status=True)
            db.session.add(block_view)
            db.session.commit()
            flash("You have restricted this user. He cannot view your profile now.", 'success')
    return redirect(url_for('user_profile', username=user.username))

@app.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route("/admin/block_user/<int:user_id>")
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    user = User.query.get(user_id)
    if user:
        user.blocked = not user.blocked
        db.session.commit()
    return redirect(url_for('admin'))

@app.route("/admin/admin_user/<int:user_id>")
@login_required
def admin_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    user = User.query.get(user_id)
    if user:
        user.is_admin = not user.is_admin
        db.session.commit()
    return redirect(url_for('admin'))

@app.route("/admin/edit_user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    user = User.query.get(user_id)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_profile(form.picture.data)
            user.image_file = picture_file
        if form.username.data:
            user.username = form.username.data
        if form.email.data:
            user.email = form.email.data
        if form.dob.data:
            user.birthday = form.dob.data
        if form.gender.data != 'None':
            user.gender = form.gender.data
        else:
            user.gender = None
        if form.marriage_status.data != 'None':
            user.marriage_status = form.marriage_status.data
        else:
            user.marriage_status = None
        if form.sexual_orientation.data:
            user.sexual_orientation = form.sexual_orientation.data
        if form.dating.data != 'yes':
            user.dating = False
        else:
            user.dating = True
        if form.workplace.data:
            user.workplace = form.workplace.data
        if form.edu.data:
            user.education = form.edu.data
        db.session.commit()
        flash('Account has been updated!', 'success')
        return redirect(url_for('user_profile', username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        if user.birthday:
            form.dob.data = datetime.strptime(user.birthday, '%Y-%m-%d')
        form.gender.data = user.gender
        form.marriage_status.data = user.marriage_status
        form.sexual_orientation.data = user.sexual_orientation
        form.workplace.data = user.workplace
        form.edu.data = user.education
        if user.dating is True:
            form.dating.data = "yes"
        else:
            form.dating.data = "no"
    image_file = url_for('static', filename='pics/profile_pics/' + user.image_file)
    return render_template('edit_user.html', title='Edit_user', image_file=image_file, form=form, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='ottobuddies@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


if __name__ == "__main__":
    app.run(debug=True)
