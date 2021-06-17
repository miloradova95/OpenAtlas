from typing import List, Tuple, Union

from flask import Response
from flask_restful import Resource

from openatlas.api.v02.resources.error import InvalidLimitError
from openatlas.api.v02.resources.helpers import resolve_entity_parser
from openatlas.api.v02.resources.parser import entity_parser
from openatlas.models.entity import Entity


class GetLatest(Resource):  # type: ignore
    @staticmethod
    def get(latest: int) -> Union[Tuple[Resource, int], Response]:
        return resolve_entity_parser(
            GetLatest.get_latest(latest),
            entity_parser.parse_args(),
            latest)

    @staticmethod
    def get_latest(limit_: int) -> List[Entity]:
        if not (0 < limit_ < 101):
            raise InvalidLimitError
        return Entity.get_latest(limit_)
