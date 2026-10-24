# Who Should I Meet Here?

A conference networking agent backed by a **FalkorDB** graph.

Built at **Patch the Conference Hackathon** (Bright Data HQ, San Francisco,
Oct 24, 2026) for the FalkorDB track.

## The problem

At a conference, meeting the right person is pure luck. An attendee list
never tells you who actually shares your interests — and by the time you
figure it out, the event is over.

## What it does

You ask one question: **"Who should I meet here — and why?"**

The agent ranks the other attendees by shared topics, using a multi-hop
Cypher query over a graph of the conference — people, talks and topics:

```
Person -[:INTERESTED_IN]-> Topic <-[:INTERESTED_IN]- Person
```

Every answer shows the **path through the graph** that produced it, so the
recommendation is explainable, never a black box. And when you mark
someone as met, the agent writes a `MET_WITH` edge back into the graph —
**the graph is the agent's memory**, so the next answer moves on to
someone new.

## How it works

- `seed.cypher` — the conference as a graph (people, talks, topics)
- `queries.cypher` — the three demo queries: rank, explain, remember
- `load.py` — loads the seed (as a single query — the graph's variables
  span all its CREATE clauses) and prints the top-5 answer
- `app.py` — a small Streamlit UI: the ranked answer, the why, and an
  "I met them" button that writes the memory back

## Run it

Local, with Docker:

```bash
docker run -d -p 6379:6379 -p 3000:3000 falkordb/falkordb
pip install falkordb streamlit
python3 load.py        # seed the graph, print the answer
streamlit run app.py   # the demo UI
# graph visual: http://localhost:3000
```

Or point it at a FalkorDB Cloud instance with `FALKORDB_HOST`,
`FALKORDB_PORT`, `FALKORDB_USERNAME` and `FALKORDB_PASSWORD`.

## Verified

Seed and all demo queries were verified live against FalkorDB Cloud:
21 nodes, 35 edges; the top-5 answer matches the graph; marking a person
as met removes them from the next answer.
