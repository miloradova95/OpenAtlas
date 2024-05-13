from flask import Response, g, session
from flask_restful import Resource, marshal

from openatlas import app
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.parser import default, locale
from openatlas.api.resources.resolve_endpoints import download
from openatlas.api.resources.templates import (
    backend_details_template, class_mapping_template, class_overview_template,
    overview_template, properties_template)


class GetBackendDetails(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response:
        parser = default.parse_args()
        details = {
            'version': app.config['VERSION'],
            'apiVersions': app.config['API_VERSIONS'],
            'siteName': g.settings['site_name'],
            'imageProcessing': {
                'enabled': g.settings['image_processing'],
                'availableImageSizes':
                    app.config['IMAGE_SIZE']
                    if g.settings['image_processing'] else None},
            'IIIF': {
                'enabled': g.settings['iiif'],
                'url': g.settings['iiif_url'],
                'version': int(g.settings['iiif_version'])}}
        if parser['download']:
            return download(details, backend_details_template())
        return marshal(details, backend_details_template()), 200


class Classes(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response:
        return marshal([{
            "systemClass": item.name,
            "crmClass": item.cidoc_class.code if item.cidoc_class else None,
            "view": item.view,
            "standardTypeId": item.standard_type_id,
            "icon": item.icon,
            "en": item.label} for item in g.classes.values()],
            class_overview_template()), 200


class ClassMapping(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response:
        results = {
            "locale": session['language'],
            "results": [{
                "label": class_.label,
                "systemClass": class_.name,
                "crmClass":
                    class_.cidoc_class.code if class_.cidoc_class else None,
                "view": class_.view,
                "standardTypeId": class_.standard_type_id,
                "icon": class_.icon} for class_ in g.classes.values()]}
        if locale.parse_args()['download']:
            return download(results, class_mapping_template())
        return marshal(results, class_mapping_template()), 200


class GetProperties(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response:
        results = {}
        for property_code, property_ in g.properties.items():
            results[property_code] = {
                "id": property_.id,
                "name": property_.name,
                "nameInverse": property_.name_inverse,
                "code": property_.code,
                "domainClassCode": property_.domain_class_code,
                "rangeClassCode": property_.range_class_code,
                "count": property_.count,
                "sub": property_.sub,
                "super": property_.super,
                "i18n": property_.i18n,
                "i18nInverse": property_.i18n_inverse}
        if locale.parse_args()['download']:
            return download(results, properties_template(g.properties))
        return marshal(results, properties_template(g.properties)), 200


class SystemClassCount(Resource):
    @staticmethod
    def get() -> tuple[Resource, int] | Response:
        return marshal(
            ApiEntity.get_overview_counts(),
            overview_template()), 200
