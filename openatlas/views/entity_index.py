from typing import Union

from flask import g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.image_processing import check_processed_image
from openatlas.display.table import Table
from openatlas.display.util import (
    button, format_date, get_base_table_data, get_file_path, is_authorized,
    link, manual, required_group)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis


@app.route('/index/<view>')
@required_group('readonly')
def index(view: str) -> Union[str, Response]:
    buttons = [manual(f'entity/{view}')]
    for name in g.view_class_mapping[view] if view != 'place' else ['place']:
        if is_authorized(g.classes[name].write_access):
            buttons.append(
                button(
                    g.classes[name].label,
                    url_for('insert', class_=name),
                    tooltip_text=g.classes[name].get_tooltip()))
    return render_template(
        'entity/index.html',
        class_=view,
        table=get_table(view),
        buttons=buttons,
        gis_data=Gis.get_all() if view == 'place' else None,
        title=_(view.replace('_', ' ')),
        crumbs=[[_('admin'), url_for('admin_index')], _('file')]
        if view == 'file' else [_(view).replace('_', ' ')])


def get_table(view: str) -> Table:
    table = Table(g.table_headers[view])
    if view == 'file':
        table.order = [[0, 'desc']]
        table.header = ['date'] + table.header
        if g.settings['image_processing'] \
                and current_user.settings['table_show_icons']:
            table.header.insert(1, _('icon'))
        for entity in Entity.get_by_class('file', types=True):
            data = [
                format_date(entity.created),
                link(entity),
                link(entity.standard_type),
                g.file_stats[entity.id]['size']
                if entity.id in g.file_stats else 'N/A',
                g.file_stats[entity.id]['ext']
                if entity.id in g.file_stats else 'N/A',
                entity.description]
            if g.settings['image_processing'] \
                    and current_user.settings['table_show_icons']:
                data.insert(1, file_preview(entity.id))
            table.rows.append(data)
    elif view == 'reference_system':
        for system in g.reference_systems.values():
            table.rows.append([
                link(system),
                system.count or '',
                link(system.website_url, system.website_url, external=True),
                link(system.resolver_url, system.resolver_url, external=True),
                system.placeholder,
                link(g.types[system.precision_default_id])
                if system.precision_default_id else '',
                system.description])
    else:
        classes = 'place' if view == 'place' else g.view_class_mapping[view]
        entities = Entity.get_by_class(classes, types=True, aliases=True)
        table.rows = [get_base_table_data(entity) for entity in entities]
    return table


def file_preview(entity_id: int) -> str:
    size = app.config['IMAGE_SIZE']['table']
    parameter = f"loading='lazy' alt='image' width='{size}'"
    if icon_path := get_file_path(
            entity_id,
            app.config['IMAGE_SIZE']['table']):
        url = url_for('display_file', filename=icon_path.name, size=size)
        return f"<img src='{url}' {parameter}>"
    path = get_file_path(entity_id)
    if path and check_processed_image(path.name):
        if icon := get_file_path(entity_id, app.config['IMAGE_SIZE']['table']):
            url = url_for('display_file', filename=icon.name, size=size)
            return f"<img src='{url}' {parameter}>"
    return ''
