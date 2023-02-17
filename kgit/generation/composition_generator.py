import neomodel

from .generator import KBQAGenerator

class CompositionGenerator(KBQAGenerator):
    def __init__(self) -> None:
        super().__init__()
    
    def generate(self, r1_name: str, r2_name: str, limit:int=50000):
        out = []
        results, meta = neomodel.db.cypher_query(f"MATCH (a:Resource)-[r:{r1_name}]->(b:Resource) RETURN a, r, b LIMIT {limit}", resolve_objects=True)
        for ret in results:
            a, r1, b = ret
            results2, meta2 = neomodel.db.cypher_query(f"MATCH (b:Resource)-[r:{r2_name}]->(c:Resource) WHERE b.uri=\"{b.uri}\" RETURN b, r, c LIMIT 500", resolve_objects=True)
            for ret in results2:
                b, r2, c = ret
                out.append((a, b, c))
                break
        return out