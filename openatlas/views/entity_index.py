import datetime
from typing import List, Optional, Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.util.display import (button, convert_size, external_url, format_date,
                                    get_base_table_data, get_file_path, link)
from openatlas.util.table import Table
from openatlas.util.util import get_file_stats, is_authorized, required_group


@app.route('/index/<view>')
@app.route('/index/<view>/<int:delete_id>')
@required_group('readonly')
def index(view: str, delete_id: Optional[int] = None) -> Union[str, Response]:
    if delete_id:  # To prevent additional redirects deletion is done before showing index
        url = delete_entity(view, delete_id)
        if url:  # e.g. an error occurred and entry is shown again
            return redirect(url)
    return render_template('entity/index.html',
                           class_=view,
                           table=get_table(view),
                           buttons=get_buttons(view),
                           gis_data=Gis.get_all() if view == 'place' else None,
                           title=_(view.replace('_', ' ')),
                           crumbs=[[_('admin'), url_for('admin_index')], _('file')]
                           if view == 'file' else [_(view).replace('_', ' ')])


def get_buttons(view: str) -> List[str]:
    buttons = []
    class_names = [view] if view in ['artifact', 'place'] else g.view_class_mapping[view]
    for name in class_names:
        if is_authorized(g.classes[name].write_access):
            buttons.append(button(g.classes[name].label, url_for('insert', class_=name)))
    return buttons


def get_table(view: str) -> Table:
    table = Table(g.table_headers[view])
    if view == 'file':
        table.header = ['date'] + table.header
        file_stats = get_file_stats()
        for entity in Entity.get_by_system_class('file', nodes=True):
            date = 'N/A'
            if entity.id in file_stats:
                date = format_date(
                    datetime.datetime.utcfromtimestamp(file_stats[entity.id]['date']))
            table.rows.append([
                date,
                link(entity),
                entity.print_standard_type(),
                convert_size(file_stats[entity.id]['size']) if entity.id in file_stats else 'N/A',
                file_stats[entity.id]['ext'] if entity.id in file_stats else 'N/A',
                entity.description])
    elif view == 'reference_system':
        for entity in g.reference_systems.values():
            table.rows.append([
                link(entity),
                entity.count if entity.count else '',
                external_url(entity.website_url),
                external_url(entity.resolver_url),
                entity.placeholder,
                link(g.nodes[entity.precision_default_id]) if entity.precision_default_id else '',
                entity.description])
    else:
        classes = ['place'] if view == 'place' else g.view_class_mapping[view]
        entities = Entity.get_by_system_class(classes, nodes=True)
        table.rows = [get_base_table_data(item) for item in entities]
    return table


def delete_entity(class_: str, id_: int) -> Optional[str]:
    url = None
    if class_ == 'reference_system':
        entity = g.reference_systems[id_]
        if entity.system or not is_authorized('manager'):
            abort(403)
        if entity.forms:
            flash(_('Deletion not possible if forms are attached'), 'error')
            return url_for('entity_view', id_=id_)
    if class_ == 'place':
        entity = Entity.get_by_id(id_)
        parent = None if entity.class_.name == 'place' else entity.get_linked_entity('P46', True)
        if entity.get_linked_entities('P46'):
            flash(_('Deletion not possible if subunits exists'), 'error')
            return url_for('entity_view', id_=id_)
        entity.delete()
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
        if parent:
            tab = '#tab-' + entity.class_.name.replace('_', '-')
            url = url_for('entity_view', id_=parent.id) + tab
    else:
        Entity.delete_(id_)
        logger.log_user(id_, 'delete')
        flash(_('entity deleted'), 'info')
        if class_ == 'file':
            try:
                path = get_file_path(id_)
                if path:  # Only delete file on disk if it exists to prevent a missing file error
                    path.unlink()
            except Exception as e:  # pragma: no cover
                logger.log('error', 'file', 'file deletion failed', e)
                flash(_('error file delete'), 'error')
    return url
