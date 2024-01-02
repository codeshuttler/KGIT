import neomodel

from .generator import KBQAGenerator

# (A: Resource)-[r:R1]->(B: Resource)
# (B: Resource)-[r:R2]->(C: Resource)

# (A: Resource)-[r:sch__parent]->(B: Resource)：B是A的parent 
# (B: Resource)-[r:sch__gender]->(C: Resource)：B的性别是C
# 合成：A的parent的性别是什么？

# R1: 唯一性
# R2：任意

class InferGenerator(KBQAGenerator):
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
            # print(f"\"{end_node.label}\" is the parent of \"{start_node.label}\"")
        return out