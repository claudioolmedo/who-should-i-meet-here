// The 3 demo queries — the whole product in 3 questions.

// Q1 — WHO SHOULD I MEET? Ranked by shared topics; excludes people already met.
// Returns the person, the score, and the shared topics (the "why").
MATCH (you:Person {name:'Claudio (You)'})-[:INTERESTED_IN]->(t:Topic)<-[:INTERESTED_IN]-(p:Person)
WHERE p <> you AND NOT (you)-[:MET_WITH]->(p)
RETURN p.name AS person, p.role AS role, p.org AS org,
       count(t) AS shared_topics, collect(t.name) AS why
ORDER BY shared_topics DESC
LIMIT 5;

// Q2 — WHY THIS PERSON? The path through the graph (for the stage visual).
MATCH path = (you:Person {name:'Claudio (You)'})-[:INTERESTED_IN]->(t:Topic)<-[:INTERESTED_IN]-(p:Person {name:'Priya Nair'})
RETURN path;

// Q3 — MARK AS MET (memory). After a conversation, write MET_WITH so Q1 moves on.
MATCH (you:Person {name:'Claudio (You)'}), (p:Person {name:'Priya Nair'})
CREATE (you)-[:MET_WITH {at:'15:05'}]->(p);
