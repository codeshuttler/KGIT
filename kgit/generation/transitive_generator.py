import neomodel

from .generator import KBQAGenerator

class TransitiveGenerator(KBQAGenerator):
    def __init__(self) -> None:
        super().__init__()
    
    def generate(self, r1_name: str, limit:int=150000):
        out = []
        results, meta = neomodel.db.cypher_query(
            f"MATCH (a:Resource)-[r1:{r1_name}]->(b:Resource)-[r2:{r1_name}]->(c:Resource) RETURN a, b, c LIMIT {limit}",
            resolve_objects=True
        )
        for ret in results:
            a, b, c = ret
            out.append((a, b, c))
        return out