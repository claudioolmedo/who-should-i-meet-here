#!/usr/bin/env python3
"""Patch the Conference — networking agent (FalkorDB track).

One question, answered by the graph: "Who should I meet here — and why?"
Run:  streamlit run app.py    (FalkorDB must be running; run load.py first)
"""
import os

import streamlit as st
from falkordb import FalkorDB

YOU = "Claudio (You)"
GRAPH = "patchconf"

st.set_page_config(page_title="Who should I meet?", layout="centered")
st.title("Who should I meet here — and why?")
st.caption("A conference networking agent. The graph decides; the path explains.")

g = FalkorDB(
    host=os.environ.get("FALKORDB_HOST", "localhost"),
    port=int(os.environ.get("FALKORDB_PORT", "6379")),
    username=os.environ.get("FALKORDB_USERNAME") or None,
    password=os.environ.get("FALKORDB_PASSWORD") or None,
).select_graph(GRAPH)

res = g.query(
    """
    MATCH (you:Person {name:$you})-[:INTERESTED_IN]->(t:Topic)<-[:INTERESTED_IN]-(p:Person)
    WHERE p <> you AND NOT (you)-[:MET_WITH]->(p)
    RETURN p.name, p.role, p.org, count(t), collect(t.name)
    ORDER BY count(t) DESC LIMIT 5
    """,
    params={"you": YOU},
)

rows = res.result_set
if not rows:
    st.success("You have met everyone the graph recommends. Time to enjoy the conference.")
for name, role, org, shared, topics in rows:
    with st.container(border=True):
        st.subheader(name)
        st.write(f"{role} · {org}")
        st.write(f"**Why:** you both care about {', '.join(topics)} ({shared} shared topics).")
        st.write(f"Path: You → INTERESTED_IN → {topics[0]} ← INTERESTED_IN ← {name}")
        if st.button(f"I met {name.split()[0]}", key=f"met-{name}"):
            g.query(
                "MATCH (you:Person {name:$you}), (p:Person {name:$p}) CREATE (you)-[:MET_WITH]->(p)",
                params={"you": YOU, "p": name},
            )
            st.rerun()
