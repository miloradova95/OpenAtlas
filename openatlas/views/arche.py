from flask import render_template, url_for

from openatlas import app
from openatlas.util.tab import Tab
from openatlas.util.util import required_group, display_info, button, \
    is_authorized
from flask_babel import lazy_gettext as _


@app.route('/arche')
@required_group('readonly')
def arche_index() -> str:
    content = {
        'ARCHE ID': app.config['ARCHE_ID'],
        'ARCHE URL': app.config['ARCHE_BASE_URL']}
    if is_authorized('manager'):
        content['Fetch data'] = button(_('fetch'), url_for('arche_fetch'))
    return render_template(
        'tabs.html',
        tabs={'info': Tab('info', content=display_info(content))},
        crumbs=['ARCHE'])


@app.route('/arche/fetch')
@required_group('manager')
def arche_fetch() -> str:
    return render_template(
        'tabs.html',
        tabs={'info': Tab('info', content='This is ARCHEEEE')},
        crumbs=[['ARCHE', url_for('arche_index')], _('fetch')])
