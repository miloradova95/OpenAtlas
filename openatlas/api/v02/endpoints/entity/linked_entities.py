from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response
from flask_restful import Resource

from openatlas.api.v02.resources.enpoints_util import resolve_entities
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.api.v02.resources.util import get_all_links, get_all_links_inverse
from openatlas.models.entity import Entity


class GetLinkedEntities(Resource):  # type: ignore
    @swag_from("../swagger/linked_entities.yml", endpoint="api.entities_linked_to_entity")
    def get(self, id_: int) -> Union[Tuple[Resource, int], Response, Dict[str, Any]]:
        return resolve_entities(
            GetLinkedEntities.get_linked_entities(id_),
            entity_parser.parse_args(),
            'linkedEntities')

    @staticmethod
    def get_linked_entities(id_: int) -> List[Entity]:
        domain_ids = [link_.range for link_ in get_all_links(id_)]
        range_ids = [link_.domain for link_ in get_all_links_inverse(id_)]
        return range_ids + domain_ids
