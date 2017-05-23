from flask import render_template, session, redirect, url_for, current_app, abort, flash
from flask_login import current_user, login_required
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm ,EditProfileForm
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():

    """
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
        form.name.data = ''
        return redirect(url_for('index'))

    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())
    """

    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('You profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
