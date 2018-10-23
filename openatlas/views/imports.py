# Created by Alexander Watzinger and others. Please see README.md for licensing information

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect, secure_filename
from wtforms import BooleanField, FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.models.imports import ImportMapper, Project
from openatlas.util.util import link, required_group, truncate_string


class ProjectForm(Form):
    project_id = None
    name = StringField(_('name'), [InputRequired()], render_kw={'autofocus': True})
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        project = ImportMapper.get_project_by_id(self.project_id) if self.project_id else Project()
        if project.name != self.name.data and ImportMapper.get_project_by_name(self.name.data):
            self.name.errors.append(str(_('error name exists')))
            valid = False
        return valid


@app.route('/import/index')
@required_group('editor')
def import_index():
    table = {'id': 'project', 'header': ['project', 'description'], 'data': []}
    for project in ImportMapper.get_all_projects():
        table['data'].append([
            link(project),
            truncate_string(project.description)])
    return render_template('import/index.html', table=table)


@app.route('/import/project/insert', methods=['POST', 'GET'])
@required_group('manager')
def import_project_insert():
    form = ProjectForm()
    if form.validate_on_submit():
        id_ = ImportMapper.insert_project(form.name.data, form.description.data)
        flash(_('project inserted'), 'info')
        return redirect(url_for('import_project_view', id_=id_))
    return render_template('import/project_insert.html', form=form)


@app.route('/import/project/view/<int:id_>')
@required_group('editor')
def import_project_view(id_):
    project = ImportMapper.get_project_by_id(id_)
    return render_template('import/project_view.html', project=project)


@app.route('/import/project/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def import_project_update(id_):
    project = ImportMapper.get_project_by_id(id_)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        ImportMapper.update_project(project)
        flash(_('Project updated'), 'info')
        return redirect(url_for('import_project_view', id_=project.id))
    return render_template('import/project_update.html', project=project, form=form)


@app.route('/import/project/delete/<int:id_>')
@required_group('manager')
def import_project_delete(id_):
    ImportMapper.delete_project(id_)
    flash(_('Project deleted'), 'info')
    return redirect(url_for('import_index'))


class PersonForm(Form):
    file = FileField(_('file'), [InputRequired()])
    preview = BooleanField(_('preview only'), default=True)
    save = SubmitField(_('import'))


@app.route('/import/person/<int:project_id>', methods=['POST', 'GET'])
@required_group('manager')
def import_person(project_id):
    project = ImportMapper.get_project_by_id(project_id)
    form = PersonForm()
    imported = None
    table = None
    columns = {'allowed': ['name', 'id', 'description'], 'valid': [], 'invalid': []}
    if form.validate_on_submit():
        file_ = request.files['file']
        if not file_:  # pragma: no cover
            flash(_('no file to upload'), 'error')
        elif not ('.' in file_.filename and file_.filename.rsplit('.', 1)[1].lower() == 'csv'):
            flash(_('file type not allowed'), 'error')
        else:
            filename = secure_filename(file_.filename)
            file_path = app.config['IMPORT_FOLDER_PATH'] + '/' + filename
            file_.save(file_path)
            import csv
            with open(file_path, newline='') as csv_file:
                data = csv.DictReader(csv_file)
                try:
                    for item in data.fieldnames:
                        if item in columns['allowed']:
                            columns['valid'].append(item)
                        else:
                            columns['invalid'].append(item)
                except Exception as e:  # pragma: no cover
                    logger.log('error', 'import', "invalid CSV file", e)
                    flash(_('error invalid csv file'), 'error')
                    return render_template('import/person.html', project=project, form=form,
                                           columns=columns)
                checked_data = []
                if 'name' not in columns['valid']:
                    flash(_('missing name column'), 'error')
                else:
                    table = {'id': 'import', 'header': columns['valid'], 'data': []}
                    table_data = []
                    for row in data:
                        table_row = []
                        checked_list = {}
                        for item in columns['valid']:
                            table_row.append(row[item])
                            checked_list[item] = row[item]
                        table_data.append(table_row)
                        checked_data.append(checked_list)
                    table['data'] = table_data
            if not form.preview.data and checked_data:
                g.cursor.execute('BEGIN')
                try:
                    ImportMapper.import_csv('person', checked_data)
                    g.cursor.execute('COMMIT')
                    logger.log('info', 'import', 'CSV import: ' + str(len(checked_data)))
                    flash(_('csv import of') + ': ' + str(len(checked_data)), 'info')
                    imported = True
                except Exception as e:  # pragma: no cover
                    g.cursor.execute('ROLLBACK')
                    logger.log('error', 'import', 'CSV import failed', e)
                    flash(_('error transaction'), 'error')
    return render_template('import/person.html', project=project, form=form,
                           table=table, columns=columns, imported=imported)
