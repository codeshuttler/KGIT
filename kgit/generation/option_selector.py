
import neomodel
from typing import List, Optional
from functools import lru_cache

class OptionSelector(object):
    def __init__(self) -> None:
        pass

    def get_option_list(self, relation_name: str, source_not: List[str]=[], limit: Optional[int]=50000):
        results = self.get_option_list_inner(relation_name, limit)
        ret = []
        for a, b in results:
            if a.label not in source_not:
                ret.append(b)
        return ret
    
    def get_option_list_source_not(self, relation_name: str, source_not: List[str]=[], limit: Optional[int]=50000):
        results = self.get_option_list_inner(relation_name, limit)
        ret = []
        for a, b in results:
            if a.label not in source_not:
                ret.append(b)
        return ret
    
    def get_option_list_target_not(self, relation_name: str, target_not: List[str]=[], limit: Optional[int]=50000):
        results = self.get_option_list_inner(relation_name, limit)
        ret = []
        for a, b in results:
            if b.label not in target_not:
                ret.append(a)
        return ret
    
    @lru_cache(maxsize=128)
    def get_option_list_inner(self, relation_name: str, limit: Optional[int]=50000):
        out = []
        results, meta = neomodel.db.cypher_query(
            f"MATCH (a:Resource)-[r1:{relation_name}]->(b:Resource) WHERE a.rdfs__label IS NOT NULL AND b.rdfs__label IS NOT NULL RETURN a, b LIMIT {limit}",
            resolve_objects=True
        )
        for ret in results:
            a, b = ret
            out.append((a, b))
        return out

    def get_option_list_slow(self, relation_name: str, source_not: List[str]=[], limit: Optional[int]=50000):
        out = []
        escaped_source_not = [s.replace('\"', '\\\"') for s in source_not]
        filter_string = " AND ".join([f"a.rdfs__label <> \"{s}\"" for s in escaped_source_not])
        results, meta = neomodel.db.cypher_query(
            f"MATCH (a:Resource)-[r1:{relation_name}]->(b:Resource) WHERE {filter_string} RETURN a, b LIMIT {limit}",
            resolve_objects=True
        )
        for ret in results:
            a, b = ret
            out.append((a.label, b.label))
        return out