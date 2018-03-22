from flask import Flask, render_template, flash, redirect, url_for
import random
from oauth import OAuthSignIn
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:p@ssw0rd123@mysqlserver/db_name'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '205733200185301',
        'secret': '3d4cf797e215984bd3ad7935bc5ed335'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'

@app.route('/confirm_region/<region_id>')
def confirm_region(region_id):
    pass

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/maps')
def maps():

    points = [
              [{"lat": "50.5286636209", "lng": "27.8823074965"}],
              [{"lat": "48.4968544176", "lng": "32.241026259"}],
              [{"lat": "50.5854982987", "lng": "27.6051659533"}],
              [{"lat": "50.3980705737", "lng": "30.390864835"}],
              [{"lat": "49.9271527906", "lng": "36.3662432595"}],
              [{"lat": "49.9658315849", "lng": "36.1478684702"}],
              [{"lat": "50.9287142189", "lng": "34.7758232008"}],
              [{"lat": "49.3582859246", "lng": "35.4473162156"}],
              [{"lat": "50.5853395638", "lng": "26.3020379839"}],
              [{"lat": "49.9291614225", "lng": "36.4021826673"}],
              [{"lat": "48.2383133317", "lng": "22.6492120835"}],
              [{"lat": "48.3510482267", "lng": "33.5315966774"}],
              [{"lat": "49.3452186094", "lng": "23.5041836674"}],
              [{"lat": "48.7996180687", "lng": "26.7319851971"}],
              [{"lat": "50.0466492834", "lng": "36.2877128057"}],
              [{"lat": "49.5614750592", "lng": "27.9641169121"}],
              [{"lat": "51.4057539452", "lng": "31.3354803186"}],
              [{"lat": "50.3598350309", "lng": "30.9513242932"}],
                [{"lat": "49.0761454085", "lng": "33.4501271616"}],
                [{"lat": "50.9730806181", "lng": "28.6780608932"}],
                [{"lat": "49.5862518667", "lng": "34.4945589194"}],
                [{"lat": "48.3978545572", "lng": "35.0139510909"}],
                [{"lat": "50.3239670616", "lng": "30.3496480544"}],
                [{"lat": "47.8480415314", "lng": "35.1316017455"}],
                [{"lat": "50.7476736216", "lng": "33.4583446258"}],
                [{"lat": "46.4950586583", "lng": "30.7250566354"}],
                [{"lat": "51.5183878443", "lng": "31.3094931314"}],
                [{"lat": "48.0252278388", "lng": "37.8150244921"}],
                [{"lat": "48.3695463081", "lng": "30.2187413475"}],
                [{"lat": "49.9839620393", "lng": "36.4013645982"}],
                [{"lat": "50.3670364715", "lng": "30.4044865605"}],
                [{"lat": "49.5697511552", "lng": "34.5301580845"}],
                [{"lat": "49.840210639", "lng": "24.0776143302"}],
                [{"lat": "48.8140692913", "lng": "29.3664485637"}],
                [{"lat": "49.0970874615", "lng": "23.5883381159"}],
                [{"lat": "50.6348523058", "lng": "26.2524940491"}],
                [{"lat": "49.725473494", "lng": "33.3919146538"}],
                [{"lat": "49.7823478475", "lng": "30.1031072023"}],
                [{"lat": "49.4993739343", "lng": "25.8068696554"}],
                [{"lat": "48.8007427886", "lng": "36.0595092879"}],
                [{"lat": "49.9406889259", "lng": "36.2414505813"}],
                [{"lat": "48.2943198492", "lng": "25.8913767835"}],
                [{"lat": "48.4589549873", "lng": "35.0582260857"}],
                [{"lat": "50.728235853", "lng": "26.3742175335"}],
                [{"lat": "50.1135104805", "lng": "25.1991413869"}],
                [{"lat": "48.8718632165", "lng": "29.1005812595"}],
                [{"lat": "49.8578558092", "lng": "25.3424288654"}],
                [{"lat": "50.7430623785", "lng": "33.4538306007"}],
                [{"lat": "50.062588706", "lng": "26.3635918848"}],
                [{"lat": "49.7214011408", "lng": "24.5980069194"}],
                [{"lat": "49.8305577194", "lng": "23.8831750751"}],
                [{"lat": "49.9848465081", "lng": "36.2746998751"}],
                [{"lat": "48.4550365971", "lng": "35.0328941482"}],
                [{"lat": "51.4764671168", "lng": "30.740225656"}],
                 [{"lat": "49.023952179", "lng": "23.5147940234"}],
                [{"lat": "48.1981559517", "lng": "22.6565419883"}],
                [{"lat": "49.2105419391", "lng": "28.4164080996"}],
                [{"lat": "50.1572251893", "lng": "31.192456865"}],
                [{"lat": "49.0215084997", "lng": "24.8294825322"}],
                [{"lat": "50.3880296705", "lng": "30.2668759236"}],
                [{"lat": "47.757997875", "lng": "29.5156985901"}],
                [{"lat": "48.3750970552", "lng": "34.9213446837"}],
                [{"lat": "49.4438703422", "lng": "30.1473406837"}],
                [{"lat": "50.3596062931", "lng": "30.9729241243"}],

    ]
    data = random.choice(points)
    print(data)
    return render_template('maps.html', data=data)

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0')
