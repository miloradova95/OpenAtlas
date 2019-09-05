# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.gis import GisMapper
from openatlas.util.util import (required_group)


class OverlayForm(Form):
    top_left_latitude = FloatField('top left latitude', [InputRequired()], render_kw={'autofocus': True})
    top_left_longitude = FloatField('top left longitude', [InputRequired()])
    bottom_right_latitude = FloatField('bottom right latitude', [InputRequired()])
    bottom_right_longitude = FloatField('bottom right longitude', [InputRequired()])
    save = SubmitField(_('insert'))


@app.route('/overlay/insert/<int:file_id>/<int:place_id>', methods=['POST', 'GET'])
@required_group('editor')
def overlay_insert(file_id: int, place_id: int) -> str:
    place = EntityMapper.get_by_id(place_id)
    file = EntityMapper.get_by_id(file_id)
    form = OverlayForm()
    if form.validate_on_submit():
        GisMapper.insert_overlay(form=form, file=file, place=place)
        return redirect(url_for('place_view', id_=place.id) + '#tab-file')
    return render_template('overlay/insert.html', form=form, place=place, file=file)


def save(form, file, place) -> str:
    pass
