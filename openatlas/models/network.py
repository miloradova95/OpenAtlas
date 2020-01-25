from typing import Any, Dict, Optional

from flask import g

from openatlas.util.util import truncate_string


class Network:

    properties = ['P107', 'P24', 'P23', 'P11', 'P14', 'P7', 'P74', 'P67', 'OA7', 'OA8', 'OA9']
    classes = ['E21', 'E7', 'E31', 'E33', 'E40', 'E74', 'E53', 'E18', 'E8', 'E84']
    sql_where = """
        AND (e.system_type IS NULL
            OR (e.system_type NOT IN ('file', 'source translation')
                AND e.system_type NOT LIKE 'external reference%%'));"""

    @staticmethod
    def get_edges():
        sql = """
            SELECT l.id, l.domain_id, l.range_id FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id
            WHERE property_code IN %(properties)s """ + Network.sql_where
        g.execute(sql, {'properties': tuple(Network.properties)})
        return g.cursor.fetchall()

    @staticmethod
    def get_entities():
        sql = """
            SELECT e.id, e.class_code, e.name
            FROM model.entity e
            WHERE class_code IN %(classes)s """ + Network.sql_where
        g.execute(sql, {'classes': tuple(Network.classes)})
        return g.cursor.fetchall()

    @staticmethod
    def get_network_json(params: Dict[str, Any]) -> Optional[str]:
        # Get object - location mapping
        sql = """
            SELECT e.id, l.range_id
            FROM model.entity e
            JOIN model.link l ON e.id = domain_id AND l.property_code = 'P53';"""
        g.execute(sql)
        object_mapping = {row.id: row.range_id for row in g.cursor.fetchall()}

        entities = set()
        edges = ''
        for row in Network.get_edges():
            edges += "{{'source':'{domain_id}','target':'{range_id}'}},".format(
                domain_id=row.domain_id, range_id=row.range_id)
            entities.update([row.domain_id, row.range_id])

        nodes = ''
        entities_already = set()
        for row in Network.get_entities():
            if params['options']['orphans'] or row.id in entities:
                entities_already.add(row.id)
                nodes += """{{'id':'{id}','name':'{name}','color':'{color}'}},""".format(
                    id=row.id,
                    name=truncate_string(row.name.replace("'", ""), span=False),
                    color=params['classes'][row.class_code]['color'])

        # Get entities of links which weren't present in class selection
        array_diff = [item for item in entities if item not in entities_already]
        if array_diff:
            sql = "SELECT id, class_code, name FROM model.entity WHERE id IN %(array_diff)s;"
            g.execute(sql, {'array_diff': tuple(array_diff)})
            result = g.cursor.fetchall()
            for row in result:
                color = ''
                if row.class_code in params['classes']:  # pragma: no cover
                    color = params['classes'][row.class_code]['color']
                nodes += """{{'id':'{id}','name':'{name}','color':'{color}'}},""".format(
                    id=row.id,
                    color=color,
                    name=truncate_string(row.name.replace("'", ""), span=False))

        return "graph = {'nodes': [" + nodes + "],  links: [" + edges + "]};" if nodes else None

    @staticmethod
    def get_network_json2(params: Dict[str, Any]) -> Optional[str]:
        entities = set()
        edges = ''
        for row in Network.get_edges():
            edges += "{{'source':'{d_id}', 'target':'{r_id}', 'id':'{l_id}'}},".format(
                d_id=row.domain_id, r_id=row.range_id, l_id=row.id)
            entities.update([row.domain_id, row.range_id])

        nodes = ''
        entities_already = set()
        for row in Network.get_entities():
            if params['options']['orphans'] or row.id in entities:
                entities_already.add(row.id)
                nodes += """{{'id':'{id}','label':'{name}','color':'{color}'}},""".format(
                    id=row.id,
                    name=truncate_string(row.name.replace("'", ""), span=False),
                    color=params['classes'][row.class_code]['color'])

        # Get entities of links which weren't present in class selection
        array_diff = [item for item in entities if item not in entities_already]
        if array_diff:
            sql = "SELECT id, class_code, name FROM model.entity WHERE id IN %(array_diff)s;"
            g.execute(sql, {'array_diff': tuple(array_diff)})
            result = g.cursor.fetchall()
            for row in result:
                color = ''
                if row.class_code in params['classes']:  # pragma: no cover
                    color = params['classes'][row.class_code]['color']
                nodes += """{{'id':'{id}','label':'{name}','color':'{color}'}},""".format(
                    id=row.id,
                    color=color,
                    name=truncate_string(row.name.replace("'", ""), span=False))

        return "{{nodes: [{nodes}], edges: [{edges}], types: {{nodes: [], edges: []}} }};".format(
            nodes=nodes, edges=edges)
