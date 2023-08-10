# Web App_Otto Buddies

<img align="center" src="/static/pics/screenshots/homepage.png">

Welcome to **Otto Buddies**, a dynamic and engaging social media web application designed to connect people, foster friendships, and promote meaningful interactions in the digital world. Whether you're looking to stay connected with friends, share your thoughts and experiences, or discover new connections with like-minded individuals, **Otto Buddies** provides the perfect platform to do it all. Join **Otto Buddies** today and discover a world of connections, and friendships. Together, let's make the virtual world a little more meaningful and engaging!

## Table of Contents

1. [Features](#features)
2. [User guide](#userguide)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Authors](#authors)


## <a name="features"></a>1. Features

All below features are deployed successfully.

| Essential | Necessary | Nice to have |
|-----------|-----------|--------------|
| Create account | Add DOB to profile | Add workplace to profile |
| Display profile | Add gender to profile | Add education to profile |
| Search for users | Make admin accounts | Add marriage status to profile |
| Add friends | Admins can edit anything, block users from log in and search, set a user to be an admin | Add sexual orientation to profile |
| Add profile picture | Post/ edit/ delete stories | Captcha when log in and register |
|                     | Reset password | Available to dating status |
|                     | Limit who can see profile and posts | Script password       |


## <a name="userguide"></a>2. User guide for Otto buddies

To get started with **Otto Buddies**, simply sign up for an account on the website and create a unique profile. Once you're in, explore the various features and start connecting with friends and like-minded individuals.

The opening page of Otto buddies looks like below: 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-11_155148.png">

The existing users can log in to their profiles while new users can create an account to use Otto buddies. 
To prevent unauthorized entry of bots, we have implemented captcha. Also, in case user forgets the password, he can reset the password with a help of e-mail.

In case, the user does not have an account he can register with his email and password. The registration page for the website looks like below:

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-11_165418.png">

Once registered, the homepage for user looks like below:

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-11_165804.png">

On the Top-bar, the user can see few tabs.

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_120129.png">

#### Home Page

On clicking Otto-buddies, the user can go to the Home-page. Currently the home page looks empty. The user have to add friends, to see their posts on the Home page. The home page would look like below:

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-11_162401.png">

#### Search Friends

Just adjacent to that we have a search bar where user can search for other users. The user has to know the Usernames of other users to search them. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_152017.png">

If the username is incorrect, the user will get below message. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_152302.png">

From here, the user can view their profiles and send them a friend request or restrict them. 
User needs to click on the Username, in order to see the profile. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_152836.png">

Here the user have 2 options currently- 
1) Add friend - To connect to other users, user have to send them a friend request. Once you click this button, the status of the friend request changes to "Request Pending" and you have an option to "Cancel Request"

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_153608.png">

2) Restrict - With this button, you can limit who can view your account. If the user is restricted, your profile will not be visible to him.


#### Navigation bar functions
On the right-side of the Top-bar, we have 4 tabs. 

**1) Create new post**
New post- By clicking here, you are redirected to a page to create a post. A post could have a Title, a text content and/or an image. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_154527.png">

Once the user clicks on "Post" button, the post is available to view by other users. This post will be available on the the profile page as well as home page friends. 

**2) Friends**
This tab is used to view user's friends. The are two tabs, one for existing friends and other for friend requests. When a new friend request has arrived, the user can see the number of pending friend requests on the 
notification badge on the Top-bar. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_164309.png">

If you switch the tab to Friend Requests, you get an option to comfirm or remove the friend requests. You can also click on the Username to go the user-profile. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_165247.png">

**3) Profile page**
This tab redirects user to his own profile page. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_170115.png">

The top section of profile page shows user details. The user can click on the Edit button next to tje username, to edit profile details like Username, date of birth, Gender, Marital status, Sexual Orientation, Workplace and Education and even profile image. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_171605.png">

If the user is interested in dating,  a red heart appears on the profile image to let other users know.  

Further, on profile page, the user sees posts made in past. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_172025.png">

For each post, there is an edit option for user. User can click on this button, to either update the post or delete the post. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_172202.png">

**4) Logout** 

Clicking here, you can logout from your account. You will be redirected to Login page from here. 

#### Reset password

If the user forgets the password or wishes to reset it, he can use "Forgot password?" functionality available on Login page. After clicking on this option, the user has to enter the Email-ID used for the account. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-17_153124.png">

Once submitted, the user will receive an email with a link to reset the password. This link cannot be shared with others in order to avoid misuse. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-17_154042.png">

Once the password is reset, the user can login with the new password. 

#### Admin control

To maintain control over users, there was a request for setting up admin accounts. The admin users are differentiated with additional "Admin" tab on their Top-bar. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_174440.png">

Once you click on this tab, you can see a dashboard listing all users. The admin has authority to view and edit the profile. The Admin can also block users from logging in the app and set other users as admin. 

<img align="center" src="/static/pics/screenshots/Screenshot_2023-07-13_175844.png">


## <a name="technologies"></a>3. Technologies

**Front-end:** [HTML5](https://www.w3schools.com/html/), [CSS](https://www.w3schools.com/css/), [Bootstrap](https://getbootstrap.com)

**Back-end:** [Python](https://www.python.org/), [Flask](https://flask.pocoo.org/), [Jinja2](https://jinja.pocoo.org/docs/dev/), [SQLite](https://www.sqlite.org/index.html), [SQLAlchemy](https://www.sqlalchemy.org/)

**Captcha:** [Google captcha](https://www.google.com/recaptcha/about/)


## <a name="installation"></a>4. Installation

Clone this repository:

```$ git clone https://code.ovgu.de/ohyh83oc/web-app_otto-buddies.git```

Create a virtual environment and activate it:

```
$ virtualenv env
$ cd env/Scripts
$ .\activate
$ cd ..
$ cd ..
```

Install the dependencies:

```$ pip install -r requirements.txt```

Create database if database is not available

```
$ python
>>> from app import app, db
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

Finally, to run the app, start the server:

```$ python app.py```

Go to `localhost:5000` in your browser to start using Otto Buddies!


## <a name="authors"></a>5. Authors

**Duy Quoc Vo**  | Back-end | Operations Research and Business Analytics | [Email](mailto:duy.vo@st.ovgu.de) <br/>
**Darshana Sakpal** | Front-end | Digital Engineering | [Email](mailto:darshana.sakpal@st.ovgu.de) <br/>
**Md Jahidul Islam** | Testing and Project management | Operations Research and Business Analytics | [Email](mailto:md2.islam@st.ovgu.de) <br/>
**Rajesh Bhandari** | Design and Testing | Digital Engineering | [Email](mailto:rajesh.bhandari@st.ovgu.de) <br/>
