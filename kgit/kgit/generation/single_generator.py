import neomodel

from .generator import KBQAGenerator

# 单属性生成器
class SingleGenerator(KBQAGenerator):
    def __init__(self) -> None:
        super().__init__()
    
    def generate(self, r1_name: str, limit:int=150000):
        out = []
        results, meta = neomodel.db.cypher_query(
            f"MATCH (a:Resource)-[r1:{r1_name}]->(b:Resource) RETURN a, b LIMIT {limit}",
            resolve_objects=True
        )
        for ret in results:
            a, b = ret
            out.append((a, b))
        return out