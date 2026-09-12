import json
import os
import base64
import urllib.request
from pathlib import Path


NEO4J_HOST = "61d4045f.databases.neo4j.io"
NEO4J_DATABASE = "61d4045f"
NEO4J_USER = "61d4045f"


def main():

    result = json.loads(
        Path("result.json").read_text(
            encoding="utf-8"
        )
    )

    password = os.environ["NEO4J_PASSWORD"]

    statement = """
    MERGE (b:Bug {id:'GAME-BUG-001'})
    SET
        b.title = $bug,
        b.status = $status

    MERGE (t:Test {name:$test})

    MERGE (f:File {name:$file})

    MERGE (l:Log {id:'GAME-BUG-001-LOG'})
    SET l.message = $log

    MERGE (p:Patch {id:'GAME-BUG-001-PATCH'})
    SET p.code = $patch

    MERGE (b)-[:CAUSED_FAILURE_IN]->(t)

    MERGE (b)-[:FOUND_IN]->(f)

    MERGE (b)-[:PRODUCED]->(l)

    MERGE (b)-[:FIXED_BY]->(p)

    RETURN b
    """

    payload = json.dumps({
        "statement": statement,
        "parameters": result,
    }).encode("utf-8")

    credentials = (
        f"{NEO4J_USER}:{password}"
    )

    auth = base64.b64encode(
        credentials.encode()
    ).decode()

    url = (
        f"https://{NEO4J_HOST}"
        f"/db/{NEO4J_DATABASE}/query/v2"
    )

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(
        request,
        timeout=15,
    ) as response:

        response.read()

    print()
    print("Saved bug knowledge to Neo4j")


if __name__ == "__main__":
    main()