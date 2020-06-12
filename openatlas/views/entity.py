import sys
from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.forms.forms import build_table_form
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.util.table import Table
from openatlas.util.util import (display_remove_link, get_base_table_data, get_entity_data,
                                 get_profile_image_table_link, is_authorized, link, required_group,
                                 uc_first)
from openatlas.views.reference import AddReferenceForm


@app.route('/entity/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_file(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string('P67', request.form['checkbox_values'], inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-file')
    form = build_table_form('file', entity.get_linked_entities('P67', inverse=True))
    return render_template('entity/add_file.html', entity=entity, form=form)


@app.route('/entity/add/source/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_source(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    property_code = 'P128' if entity.class_.code == 'E84' else 'P67'
    inverse = False if entity.class_.code == 'E84' else True
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(property_code, request.form['checkbox_values'], inverse=inverse)
        return redirect(url_for('entity_view', id_=id_) + '#tab-source')
    form = build_table_form('source', entity.get_linked_entities(property_code, inverse=inverse))
    return render_template('entity/add_source.html', entity=entity, form=form)


@app.route('/entity/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_reference(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    form = AddReferenceForm()
    if form.validate_on_submit():
        entity.link_string('P67', form.reference.data, description=form.page.data, inverse=True)
        return redirect(url_for('entity_view', id_=id_) + '#tab-reference')
    form.page.label.text = uc_first(_('page / link text'))
    return render_template('entity/add_reference.html', entity=entity, form=form)


@app.route('/entity/<int:id_>')
@required_group('readonly')
def entity_view(id_: int) -> Union[str, Response]:
    if id_ in g.nodes:
        node = g.nodes[id_]
        if node.root:
            return node_view(node)
        else:  # pragma: no cover
            if node.class_.code == 'E53':
                tab_hash = '#menu-tab-places_collapse-'
            elif node.standard:
                tab_hash = '#menu-tab-standard_collapse-'
            elif node.value_type:
                tab_hash = '#menu-tab-value_collapse-'
            else:
                tab_hash = '#menu-tab-custom_collapse-'
            return redirect(url_for('node_index') + tab_hash + str(id_))
    try:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)
    except AttributeError:
        abort(418)
        return ''  # pragma: no cover
    if not entity.view_name:  # pragma: no cover
        flash(_("This entity can't be viewed directly."), 'error')
        abort(400)
    # remove this after finished tab refactor
    if entity.view_name in ['node']:
        return getattr(sys.modules[__name__], '{name}_view'.format(name=entity.view_name))(entity)
    return getattr(sys.modules['openatlas.views.' + entity.view_name],
                   '{name}_view'.format(name=entity.view_name))(entity)


def node_view(node: Node) -> str:
    root = g.nodes[node.root[-1]] if node.root else None
    super_ = g.nodes[node.root[0]] if node.root else None
    header = [_('name'), _('class'), _('info')]
    if root and root.value_type:  # pragma: no cover
        header = [_('name'), _('value'), _('class'), _('info')]
    tables = {'entities': Table(header), 'file': Table(Table.HEADERS['file'] + [_('main image')])}
    profile_image_id = node.get_profile_image_id()
    for entity in node.get_linked_entities(['P2', 'P89'], inverse=True, nodes=True):
        if node.class_.code == 'E53':  # pragma: no cover
            object_ = entity.get_linked_entity('P53', inverse=True)
            if not object_:  # If it's a location show the object, continue otherwise
                continue
            entity = object_
        data = [link(entity)]
        if root and root.value_type:  # pragma: no cover
            data.append(format_number(entity.nodes[node]))
        data.append(g.classes[entity.class_.code].name)
        data.append(entity.description)
        tables['entities'].rows.append(data)
    tables['link_entities'] = Table([_('domain'), _('range')])
    for link_ in node.get_links('P67', inverse=True):
        domain = link_.domain
        data = get_base_table_data(domain)
        if domain.view_name == 'file':  # pragma: no cover
            extension = data[3].replace('.', '')
            data.append(get_profile_image_table_link(domain, node, extension, profile_image_id))
            if not profile_image_id and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                profile_image_id = domain.id
        if is_authorized('contributor'):
            url = url_for('link_delete', id_=link_.id, origin_id=node.id)
            data.append(display_remove_link(url + '#tab-' + domain.view_name, domain.name))
        tables[domain.view_name].rows.append(data)

    for row in Link.get_entities_by_node(node):
        tables['link_entities'].rows.append([link(Entity.get_by_id(row.domain_id)),
                                             link(Entity.get_by_id(row.range_id))])
    tables['subs'] = Table([_('name'), _('count'), _('info')])
    for sub_id in node.subs:
        sub = g.nodes[sub_id]
        tables['subs'].rows.append([link(sub), sub.count, sub.description])
    return render_template('types/view.html',
                           node=node,
                           super_=super_,
                           tables=tables,
                           root=root,
                           info=get_entity_data(node),
                           profile_image_id=profile_image_id)
