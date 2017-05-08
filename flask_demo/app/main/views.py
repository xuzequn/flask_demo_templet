from flask import render_template,session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_mail
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    #name = None;
    form = NameForm()
    if form.validate_on_submit():
        '''
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('look like you have a change for your name')
        session['name'] = form.name.data
        return redirect(url_for('index'))
        '''

        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))

    return render_template('index.html',
                           form = form, name = session.get('name'),
                           known = session.get('known', False),
                           current_time=datetime.utcnow())