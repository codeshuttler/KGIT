import neomodel

from .generator import KBQAGenerator

# (A: Resource {sch__alternateName: C}): A的别名是C
# (A: Resource)-[r:R1]->(B: Resource): A的R1是B

# 问 C的R1是B吗？

class AlternativeGenerator(KBQAGenerator):
    def __init__(self) -> None:
        super().__init__()
    
    def generate(self, r1_name: str, limit:int=50000):
        out = []
        results, meta = neomodel.db.cypher_query(
            f"MATCH (a:Resource)-[r:{r1_name}]->(b:Resource) WHERE a.sch__alternateName IS NOT NULL RETURN a, r, b LIMIT {limit}",
            resolve_objects=True
        )
        for ret in results:
            a, r1, b = ret
            out.append((a, a.alternateName, b))
        return out