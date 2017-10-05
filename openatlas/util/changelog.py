# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict


class Changelog:
    """
        A big OrderedDict with changelog data, maybe not the best place and format to keep it.
    """

    versions = OrderedDict()
    versions['3.0.0'] = {
        'date': 'TBA',
        'data': OrderedDict(
            feature=OrderedDict([
                ('', 'Python Port')]))}
    versions['2.3.0'] = {
        'date': '2016-12-17',
        'data': OrderedDict(
            feature=OrderedDict([
                ('764', 'Improved hierarchy overview'),
                ('702', 'Improved settings'),
                ('707', 'Improved performance'),
                ('494', 'Newsletter and registration mails'),
                ('319', 'SMTP settings in admin interface'),
                ('693', 'Event overview: show event dates if available'),
                ('569', 'Previous and next buttons'),
                ('768', 'Show info column in main lists')]))}
    versions['2.2.0'] = {
        'date': '2016-09-11',
        'data': OrderedDict(
            feature=OrderedDict([
                ('547', 'Map: multiple points and areas for Places'),
                ('719', 'Favicon support for current systems')]))}
    versions['2.1.0'] = {
        'date': '2016-08-18',
        'data': OrderedDict(
            feature=OrderedDict([
                ('643', 'Performance improvements'),
                ('700', 'Improved frontend'),
                ('703', 'Add multiple actors, events and places to source')]),
            fix=OrderedDict([
                ('696', 'Add texts to source')]))}
    versions['2.0.0'] = {
        'date': '2016-06-19',
        'data': OrderedDict(
            feature=OrderedDict([
                ('428', 'Dynamic Types'),
                ('687', 'Remove required restriction from type fields')]),
            fix=OrderedDict([
                ('688', 'Translation errors'),
                ('689', 'Show/Hide buttons')]))}
    versions['1.6.0'] = {
        'date': '2016-05-04',
        'data': OrderedDict(
            feature=OrderedDict([
                ('340', 'Multi user capability'),
                ('672', 'Add multiple sources for event/actor/place'),
                ('679', 'Improved credits'),
                ('683', 'Tooltips for form fields and profile')]),
            fix=OrderedDict([
                ('674', 'Place error occurs during saving')]))}
    versions['1.5.0'] = {
        'date': '2016-04-01',
        'data': OrderedDict(
            feature=OrderedDict([
                ('564', 'Add multiple entries for relation, member and involvement'),
                ('586', 'Bookmarks'),
                ('671', 'Redmine links for changelog')]))}
    versions['1.4.0'] = {
        'date': '2016-03-26',
        'data': OrderedDict(
            feature=OrderedDict([
                ('528', 'jsTree views for hierarchies'),
                ('566', 'Enhanced profile and site settings'),
                ('580', 'Change menu and structure for easier access to types'),
                ('654', 'New map layers'),
                ('666', 'Added Credits')]))}
    versions['1.3.0'] = {
        'date': '2016-02-28',
        'data': OrderedDict(
            feature=OrderedDict([
                ('462', 'Actor - add member to group from actor view'),
                ('563', 'Actor - insert and continue for relations and members'),
                ('600', 'Update of JavaScript libraries (for jsTree)'),
                ('621', 'Revised and more compact schema')]),
            fix=OrderedDict([
                ('601', 'Application is very slow on some views'),
                ('638', 'Names with an apostrophe in a table not selectable')]))}
    versions['1.2.0'] = {
        'date': '2015-12-13',
        'data': OrderedDict(
            feature=OrderedDict([
                ('499', 'Actor - place tab with map'),
                ('511', 'Search - advanced features')]),
            fix=OrderedDict([
                ('547', 'Prevent double submit'),
                ('587', 'Support multiple email recipients')]))}
    versions['1.1.0'] = {
        'date': '2015-11-09',
        'data': OrderedDict(
            feature=OrderedDict([
                ('529', 'Reference - Information Carrier'),
                ('527', 'New user groups - manager and readonly'),
                ('540', 'Help and FAQ site'),
                ('555', 'Source - additional text type "Source Transliteration"'),
                ('556', 'Actor - function for member not required anymore'),
                ('560', 'Newsletter and show email option in profile')]),
            fix=OrderedDict([
                ('551', 'Model - Updating type bug'),
                ('544', 'Map - Form data lost after map search'),
                ('533', 'Map - Markers outside of Map')]))}
    versions['1.0.0'] = {
        'date': '2015-10-11',
        'data': OrderedDict(
            feature=OrderedDict([
                ('487', 'Event - Acquisition of places'),
                ('508', 'Reference - Editions'),
                ('504', 'Option to add comments for entities in texts tab'),
                ('495', 'Layout - new OpenAtlas logo'),
                ('412', 'Layout - improved layout and color scheme'),
                ('525', 'Layout - overlays for tables in forms')]))}
    versions['0.11.0'] = {
        'date': '2015-09-11',
        'data': OrderedDict(
            feature=OrderedDict([
                ('433', 'Search functions')]))}
    versions['0.10.0'] = {
        'date': '2015-09-01',
        'data': OrderedDict(
            feature=OrderedDict([
                ('429', 'Actor - member of'),
                ('472', 'Actor - activity for event relations'),
                ('483', 'Actor - update for relations and involvements'),
                ('486', 'Place - administrative units and historical places'),
                ('389', 'Reference - bibliography'),
                ('489', 'Layout - overwork, multiple possibilities to create and link entities'),
                ('421', 'CRM link checker')]))}
    versions['0.9.0'] = {
        'date': '2015-07-12',
        'data': OrderedDict(
            feature=OrderedDict([
                ('392', 'Event'),
                ('423', 'Map - advanced features'),
                ('474', 'Layout - new tab based layout for views')]))}
    versions['0.8.0'] = {
        'date': '2015-06-18',
        'data': OrderedDict(
            feature=OrderedDict([
                ('326', 'Map - search, show existing places'),
                ('425', 'Actor - added gender type'),
                ('425', 'Place - multiple evidences possible'),
                ('425', 'Forms - add multiple types with ajax (e.g. aliases)')]))}
    versions['0.7.0'] = {
        'date': '2015-05-29',
        'data': OrderedDict(
            feature=OrderedDict([
                ('403', 'Physical things - places'),
                ('403', 'Actor - residence, appears first and last places'),
                ('353', 'Maps - with Leaflet (GIS)'),
                ('420', 'First and last dates in list views (e.g. actor, place)')]))}
    versions['0.6.0'] = {
        'date': '2015-05-13',
        'data': OrderedDict(
            feature=OrderedDict([
                ('402', 'Begin, end, birth and death for actors (precise and range)'),
                ('402', 'Begin, end for relations (precise and range)'),
                ('346', 'CRM - link checker'),
                ('412', 'Layout - New color scheme')]),
            fix=OrderedDict([
                ('410', 'wrong domains for links')]))}
    versions['0.5.0'] = {
        'date': '2015-04-08',
        'data': OrderedDict(
            feature=OrderedDict([
                ('377', 'Type hierarchy (editable)'),
                ('377', 'Primary source type for documents'),
                ('391', 'Period hierarchy (editable)'),
                ('391', 'Periods for actors'),
                ('365', 'Actor to actor relations'),
                ('386', 'Filter for tables')]))}
    versions['0.4.0'] = {
        'date': '2015-02-23',
        'data': OrderedDict(
            feature=OrderedDict([
                ('362', 'Document - Insert, update, delete, add texts, link with actors'),
                ('354', 'Alternative names'),
                ('360', 'Layout - new default color theme'),
                ('359', 'Layout - options default and advanced'),
                ('358', 'Import CRM property hierarchy'),
                ('360', 'Layout - new default color theme')]),
            fix=OrderedDict([
                ('357', 'wrong range link in list view properties')]))}
    versions['0.3.0'] = {
        'date': '2015-02-10',
        'data': OrderedDict(
            feature=OrderedDict([
                ('348', 'Actor - begin and end dates'),
                ('307', 'Log user CRM data manipulation')]),
            fix=OrderedDict([
                ('344', 'tablesorter IE 11 bug')]))}
    versions['0.2.0'] = {
        'date': '2015-01-18',
        'data': OrderedDict(
            feature=OrderedDict([
                ('310', 'Actor - insert, update, delete, list, view'),
                ('337', 'CRM - new OpenAtlas shortcuts')]))}
    versions['0.1.0'] = {
        'date': '2014-12-30',
        'data': OrderedDict(
            feature=OrderedDict([
                ('318', 'CRM - classes'),
                ('318', 'CRM - properties'),
                ('318', 'CRM - relations (super/sub classes, domains, ranges'),
                ('318', 'OpenAtlas shortcuts')]))}
    versions['0.0.2'] = {
        'date': '2014-12-03',
        'data': OrderedDict(
            feature=OrderedDict([
                ('306', 'CIDOC classes'),
                ('308', 'Database design'),
                ('314', 'Feedback form and translations')]))}
    versions['0.0.1'] = {
        'date': '2014-11-05',
        'data': OrderedDict(
            feature=OrderedDict([
                ('', 'Initial version based on the "Zend Base" project from '
                     '<a target="_blank" href="http://craws.net">craws.net</a>')]))}
