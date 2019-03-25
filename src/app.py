from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_cors import CORS
import boto3
import os
import json
from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import PasswordType

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(12)

postgress_pass = os.environ['POSTGRES_PASSWORD']
key_id = os.environ["KEY_ID"]
secret_key = os.environ["SECRET_KEY"]
bucket = os.environ["BUCKET"]

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]

engine = create_engine(f'postgresql://usr:{postgress_pass}@postgres:5432/photos_website')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512'
        ]
    ))

    def __init__(self, username, password):
        self.username = username
        self.password = password


Base.metadata.create_all(engine)
db_session = Session()


@app.before_first_request
def check_db_table():
    try:
        users = db_session.query(User).all()
        if not users:
            test_user = User(db_user, db_pass)
            db_session.add(test_user)
            db_session.commit()
            db_session.close()
        else:
            for user in users:
                print(user.username)

    except Exception as e:
        print(e)
        raise


def generate_urls(bucket, keys, token):
    client = boto3.client(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        region_name='eu-west-1'
        )

    urls = []

    for key in keys:
        url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': key
            },
            ExpiresIn=60
        )
        urls.append(url)

    resp = {
        "urls": urls,
        "token": token
    }

    return resp


def get_keys(token):
    keys = []
    client = boto3.client(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        region_name='eu-west-1'
    )

    if token:
        objects = client.list_objects_v2(
            Bucket=bucket,
            MaxKeys=10,
            ContinuationToken=token
        )
    else:
        objects = client.list_objects_v2(
            Bucket=bucket,
            MaxKeys=10,
        )

    for key in objects['Contents']:
        keys.append(key['Key'])

    if 'NextContinuationToken' in objects:
        return generate_urls(bucket, keys, objects['NextContinuationToken'])
    else:
        return generate_urls(bucket, keys, "")


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    username = request.form['username']

    users = db_session.query(User).filter(User.username == username).first()

    if users is not None and users.password == password:
        session['logged_in'] = True
        session['username'] = username
        return redirect('/')
    else:
        flash('wrong username or password!')
        return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route('/urls', methods=['POST'])
def get_photos():
    token = request.get_json()
    if token is not None:
        token = token["token"]
    else:
        token = ""
    
    return json.dumps(get_keys(token))


if __name__ == "__main__":
    app.run(debug=True)

# "SELECT * FROM users WHERE username = 'dsfjdsfjdf' AND password = '' OR '1' = '1'"
