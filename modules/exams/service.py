from config import database
import json
from models.hsk import HSKModel

CONN = database.connect_db()


def mapping_exams(total_parts_test, level):
    test_final = []
    for index, parts_test in enumerate(total_parts_test):
        time = 50
        if (level == "3"):
            time = 85
        elif (level == "4"):
            time = 100
        elif (level == "5"):
            time = 120
        elif (level == "6"):
            time = 135

        test: HSKModel = {
            "title": f'Test Diff {index + 1}',
            "parts": json.dumps(parts_test, ensure_ascii=False),
            "level": level,
            "groups": json.dumps([], ensure_ascii=False),
            "score": 200 if level == "1" or level == "2" else 300,
            "pass_score": None,
            "active": 1,
            "time": time
        }
        test_final.append(test)
    return test_final


def insert_exams(payload):
    cursor = CONN.cursor()
    query = f"INSERT INTO questions_test (title, parts, level, `groups`, score, active, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, [(d["title"], d["parts"], d["level"], d["groups"], d["score"], d["active"], d["time"]) for d in payload
                               ])
    CONN.commit()
