from config import database
import json

from models.hsk import QuestionModel

CONN = database.connect_db()


def get_question_if_all_sub_count_question_same(cursor, ids_diff, ids_not_diff, kind, score, total_ques):
    result = []
    all_question_in_kind = total_ques[0] + total_ques[1]
    query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
        ','.join(map(str, ids_diff)))
    query_completed_1 = f'{query_1} AND kind = "{kind}" ORDER BY RAND() LIMIT {total_ques[1]}'

    query_2 = "SELECT * FROM questions WHERE id IN ({})".format(
        ','.join(map(str, ids_diff)))
    query_completed_2 = f'{query_2} AND kind = "{kind}" ORDER BY RAND() LIMIT {total_ques[0]}'
    query_completed_final = f'({query_completed_1}) UNION ALL ({query_completed_2})'

    cursor.execute(query_completed_final)
    raw_data = cursor.fetchall()
    if (all_question_in_kind != len(raw_data)):
        query_exception = "SELECT * FROM questions WHERE id NOT IN ({})".format(
            ','.join(map(str, ids_not_diff)))
        query_completed_final = f'{query_exception} AND kind = "{kind}" ORDER BY RAND() LIMIT {all_question_in_kind}'

    cursor.execute(query_completed_final)
    raw_data = cursor.fetchall()
    # Nếu mảng không đủ độ dài chứng tỏ rằng có một số câu chưa được làm và đồng thời nó sẽ được xếp là câu khó vì chưa ai làm
    if (all_question_in_kind != len(raw_data)):
        query_completed_final = f'{query_1} AND kind = "{kind}" ORDER BY RAND() LIMIT {all_question_in_kind}'
    cursor.execute(query_completed_final)
    raw_data = cursor.fetchall()
    for tmp in raw_data:
        obj: QuestionModel = {
            "id": tmp[0],
            "kind": tmp[6],
            "general": json.loads(tmp[2]),
            "content": json.loads(tmp[3]),
            "scores": []
        }
        if (not obj['content']):
            obj["scores"] = [score]
        for i in range(len(obj['content'])):
            obj["scores"].extend([score])
        result.append(obj)
    return result


def get_question_if_all_sub_count_question_not_same(cursor, ids_diff, ids_not_diff, kind, score, total_ques, sub_count_question):
    all_question_in_kind = total_ques[0] + total_ques[1]
    query_completed = ""
    result = []
    for index, sub_question in enumerate(sub_count_question):
        if total_ques[1] >= index + 1:
            if (index == len(sub_count_question) - 1):
                query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                    ','.join(map(str, ids_diff)))
                query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)"""
            else:
                query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                    ','.join(map(str, ids_diff)))
                query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION """
        else:
            if (index == len(sub_count_question) - 1):
                query_1 = "SELECT * FROM questions WHERE id IN ({})".format(
                    ','.join(map(str, ids_diff)))
                query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)"""
            else:
                query_1 = "SELECT * FROM questions WHERE id IN ({})".format(
                    ','.join(map(str, ids_diff)))
                query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION """
    cursor.execute(query_completed)
    raw_data = cursor.fetchall()
    if (all_question_in_kind != len(raw_data)):
        for index, sub_question in enumerate(sub_count_question):
            if (index == len(sub_count_question) - 1):
                query_exception = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                    ','.join(map(str, ids_not_diff)))
                query_completed = f"""({query_exception} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)"""
            else:
                query_exception = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                    ','.join(map(str, ids_not_diff)))
                query_completed = f"""({query_exception} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION """
    cursor.execute(query_completed)
    raw_data = cursor.fetchall()

    if (all_question_in_kind != len(raw_data)):
        for index, sub_question in enumerate(sub_count_question):
            if (index == len(sub_count_question) - 1):
                query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                    ','.join(map(str, ids_diff)))
                query_completed = f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)"""
            else:
                query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                    ','.join(map(str, ids_diff)))
                query_completed = f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION """

    cursor.execute(query_completed)
    raw_data = cursor.fetchall()
    for tmp in raw_data:
        obj: QuestionModel = {
            "id": tmp[0],
            "kind": tmp[6],
            "general": json.loads(tmp[2]),
            "content": json.loads(tmp[3]),
            "scores": []
        }
        if (not obj['content']):
            obj["scores"] = [score]
        for i in range(len(obj['content'])):
            obj["scores"].extend([score])
        result.append(obj)
    return result


def get_question_by_ids_kind_and_add_score(ids_diff, ids_not_diff, kind, score, total_ques, sub_count_question):
    cursor = CONN.cursor()

    result = []
    if all(x == sub_count_question[0] for x in sub_count_question):
        result = get_question_if_all_sub_count_question_same(
            cursor, ids_diff, ids_not_diff, kind, score, total_ques)
    else:
        while len(result) != len(sub_count_question):
            result = get_question_if_all_sub_count_question_not_same(
                cursor, ids_diff, ids_not_diff, kind, score, total_ques, sub_count_question)
    return result
