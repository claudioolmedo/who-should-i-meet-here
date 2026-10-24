#!/usr/bin/env python3
"""Load the seed graph into FalkorDB and run the demo query (Q1).

Prereqs: `pip install falkordb`, and a FalkorDB to connect to:
  - Local (default): docker run -d -p 6379:6379 falkordb/falkordb
  - Cloud: set FALKORDB_HOST / FALKORDB_PORT / FALKORDB_USERNAME / FALKORDB_PASSWORD
Usage:   python3 load.py
"""
import os

from falkordb import FalkorDB

GRAPH = "patchconf"

db = FalkorDB(
    host=os.environ.get("FALKORDB_HOST", "localhost"),
    port=int(os.environ.get("FALKORDB_PORT", "6379")),
    username=os.environ.get("FALKORDB_USERNAME") or None,
    password=os.environ.get("FALKORDB_PASSWORD") or None,
)
g = db.select_graph(GRAPH)

# Start clean so re-runs are safe.
try:
    g.delete()
except Exception:
    pass
g = db.select_graph(GRAPH)

# The seed is ONE Cypher query: its variables (you, p1..p10, t_*, talk*)
# are shared across all CREATE clauses, so it must run in a single call.
seed = "\n".join(
    line
    for line in open("seed.cypher").read().splitlines()
    if line.strip() and not line.strip().startswith("//")
)
g.query(seed)
n = g.query("MATCH (n) RETURN count(n)").result_set[0][0]
print(f"Seed loaded into graph '{GRAPH}': {n} nodes.")

print("\nQ1 — Who should Claudio meet?\n")
res = g.query(
    """
    MATCH (you:Person {name:'Claudio (You)'})-[:INTERESTED_IN]->(t:Topic)<-[:INTERESTED_IN]-(p:Person)
    WHERE p <> you AND NOT (you)-[:MET_WITH]->(p)
    RETURN p.name, p.role, p.org, count(t), collect(t.name)
    ORDER BY count(t) DESC LIMIT 5
    """
)
for row in res.result_set:
    print(f"- {row[0]} ({row[1]}, {row[2]}) — {row[3]} shared topics: {', '.join(row[4])}")
