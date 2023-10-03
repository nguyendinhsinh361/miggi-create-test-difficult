from config import database
from helper import helper
import json
from tqdm import tqdm
import numpy as np
import math

from models.hsk import QuestionModel

CONN = database.connect_db()

# DATA_NEW = "data/db_new.json"
# DATA_COM = "data/db_com.json"
# DATA_COM_EXIST_IN_QUESTIONS = "data/db_com_in_question.json"
DATA_RATE = "data/db_rate.json"
DATA_RATE_DIFF = "data/db_rate_diff.json"
DATA_RATE_NOT_DIFF = "data/db_rate_not_diff.json"
DATA_QUESTIONS_TEST = "data/db_questions_test.json"
DATA_QUESTIONS_TEST_LEVEL = "data/db_questions_test_level.json"
DATA_QUESTIONS_TEST_LEVEL_COMPARE = "data/db_questions_test_level_compare.json"
DATA_QUESTIONS_TEST_LEVEL_RATE = "data/db_questions_test_level_rate.json"
DATA_QUESTIONS_TEST_LEVEL_RATE_FINAL = "data/db_questions_test_level_rate_final.json"

KIND_FORMAT_PATH = "static/kind_format.json"
INCREATE_RATE = 1.4


def get_question_by_ids_kind_and_add_score(ids_diff, ids_not_diff, kind, score, total_ques, sub_count_question):
    cursor = CONN.cursor()

    all_question_in_kind = total_ques[0] + total_ques[1]
    result = []

    if all(x == sub_count_question[0] for x in sub_count_question):
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
    else:
        query_completed = ""
        for index, sub_question in enumerate(sub_count_question):
            if total_ques[1] >= index + 1:
                if (index == len(sub_count_question) - 1):
                    query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                        ','.join(map(str, ids_diff)))
                    query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)"""
                else:
                    query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                        ','.join(map(str, ids_diff)))
                    query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION ALL """
            else:
                if (index == len(sub_count_question) - 1):
                    query_1 = "SELECT * FROM questions WHERE id IN ({})".format(
                        ','.join(map(str, ids_diff)))
                    query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)"""
                else:
                    query_1 = "SELECT * FROM questions WHERE id IN ({})".format(
                        ','.join(map(str, ids_diff)))
                    query_completed += f"""({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION ALL """
        cursor.execute(query_completed)
        raw_data = cursor.fetchall()
        if (all_question_in_kind != len(raw_data)):
            for index, sub_question in enumerate(sub_count_question):
                if (index == len(sub_count_question) - 1):
                    query_exception = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                        ','.join(map(str, ids_not_diff)))
                    query_completed = f'({query_exception} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION ALL '
                else:
                    query_exception = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                        ','.join(map(str, ids_not_diff)))
                    query_completed = f'({query_exception} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)'
        cursor.execute(query_completed)
        raw_data = cursor.fetchall()

        if (all_question_in_kind != len(raw_data)):
            for index, sub_question in enumerate(sub_count_question):
                if (index == len(sub_count_question) - 1):
                    query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                        ','.join(map(str, ids_diff)))
                    query_completed = f'({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1) UNION ALL '
                else:
                    query_1 = "SELECT * FROM questions WHERE id NOT IN ({})".format(
                        ','.join(map(str, ids_diff)))
                    query_completed = f'({query_1} AND JSON_LENGTH(content) = {sub_question} AND kind = "{kind}" ORDER BY RAND() LIMIT 1)'

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


def get_question_exist(user_history_ids_com):
    question_ids_exist = list(user_history_ids_com.keys())
    question_ids_exist.remove('undefined')
    cursor = CONN.cursor()
    query = "SELECT id FROM questions WHERE id IN ({})".format(
        ','.join(map(str, question_ids_exist)))
    cursor.execute(query)
    result = cursor.fetchall()
    existing_question_ids = [row[0] for row in result]
    new_obj = {}
    for key in existing_question_ids:
        if str(key) in user_history_ids_com:
            new_obj[str(key)] = user_history_ids_com[str(key)]
    return new_obj


def get_user_history_ids_complete(user_history_ids_raw):
    user_history_ids_com = {}
    for id in tqdm(user_history_ids_raw):
        for key, value in id["history"].items():
            if key in user_history_ids_com:
                user_history_ids_com[key].extend(value)
            else:
                user_history_ids_com[key] = value
    return user_history_ids_com


def get_user_history_ids_rate(user_history_ids_com_exist):
    user_history_ids_rate = {}
    for key, values in tqdm(user_history_ids_com_exist.items()):
        if len(values) > 0:
            average_value = round(sum(values) / len(values), 4)
            user_history_ids_rate[key] = average_value
    return user_history_ids_rate


def get_user_history_ids_rate_result(user_history_ids_rate):
    user_history_ids_diff_result = {}
    user_history_ids_not_diff_result = {}
    for key, value in user_history_ids_rate.items():
        if value > 0.4:
            user_history_ids_diff_result[key] = value
        else:
            user_history_ids_not_diff_result[key] = value
    return user_history_ids_diff_result, user_history_ids_not_diff_result


def get_users_history():
    cursor = CONN.cursor()
    cursor.execute(
        f"SELECT * FROM users_history")
    raw_data = cursor.fetchall()
    user_history_ids_raw = []
    for index, record in tqdm(enumerate(raw_data)):
        user_history = {
            "id": record[0],
            "history": helper.simplify_input(json.loads(record[1]))
        }
        user_history_ids_raw.append(user_history)

    user_history_ids_com = get_user_history_ids_complete(user_history_ids_raw)
    user_history_ids_com_exist = get_question_exist(user_history_ids_com)

    user_history_ids_rate = get_user_history_ids_rate(
        user_history_ids_com_exist)
    user_history_ids_diff_result, user_history_ids_not_diff_result = get_user_history_ids_rate_result(
        user_history_ids_rate)

    # helper.save_data_to_json(user_history_ids_raw, DATA_NEW)
    # helper.save_data_to_json(user_history_ids_com, DATA_COM)
    # helper.save_data_to_json(user_history_ids_com_exist,
    #                          DATA_COM_EXIST_IN_QUESTIONS)
    # helper.save_data_to_json(user_history_ids_rate,
    #                          DATA_RATE)
    helper.save_data_to_json(
        user_history_ids_diff_result, DATA_RATE_DIFF)
    helper.save_data_to_json(
        user_history_ids_not_diff_result, DATA_RATE_NOT_DIFF)


def get_questions_test_by_level(questions_test):
    result = []
    for item in questions_test:
        level = item["level"]
        groups = item["groups"]
        found = False
        for new_item in result:
            if level in new_item:
                new_item[level].append(groups)
                found = True
                break
        if not found:
            new_dict = {level: [groups]}
            result.append(new_dict)
    return result


def get_questions_test_by_level_compare_rate_result(questions_test_level):
    result = []
    rate_diff_result = helper.get_raw_data(DATA_RATE_DIFF)
    for obj in questions_test_level:
        for key, value in obj.items():
            new_value = []
            for sub_array in value:
                new_sub_array = [
                    1 if str(item) in rate_diff_result else 0 for item in sub_array]
                new_value.append(new_sub_array)
            new_obj = {key: new_value}
            result.append(new_obj)
    return result


def get_questions_test_by_level_rate_output(questions_test_level_compare, rate_input=INCREATE_RATE):
    result = []
    kind_format = helper.get_raw_data(
        KIND_FORMAT_PATH)
    count_question_in_level = []
    for key, sub_obj in kind_format.items():
        total = sum(sub_obj.values())
        count_question_in_level.append(total)

    for obj in questions_test_level_compare:
        for key, value in obj.items():
            new_value = [round(sum(sub_array) / len(sub_array), 4)
                         for sub_array in value]
            new_obj = {key: new_value}
            result.append(new_obj)
    helper.save_data_to_json(
        result, DATA_QUESTIONS_TEST_LEVEL_RATE)
    result_caculate = []
    for obj, count_questions in zip(result, count_question_in_level):
        for key, value in obj.items():
            rate = sum(value) / len(value) * rate_input
            new_value = math.ceil(
                round(rate, 4)*count_questions) if rate >= 0.2 else math.ceil(0.2*count_questions)
            if (key == 101 or key == 102):
                new_value = math.ceil(round(rate, 4)*count_questions)
            new_obj = {key: new_value}
            result_caculate.append(new_obj)
    helper.save_data_to_json(
        result_caculate, DATA_QUESTIONS_TEST_LEVEL_RATE_FINAL)
    return result


def get_group_ids_of_question_test(data):
    all_ids = []
    for activity in data:
        for content in activity['content']:
            all_ids.extend([question['id']
                           for question in content['Questions']])
    return np.array(all_ids).tolist()


def get_questions_test_active():
    cursor = CONN.cursor()
    cursor.execute(
        f"SELECT * FROM questions_test WHERE active = 1")
    raw_data = cursor.fetchall()
    questions_test = []
    for record in tqdm(raw_data):
        questions_test_groups = {
            "level": record[3],
            "groups": get_group_ids_of_question_test(json.loads(record[2]))
        }
        questions_test.append(questions_test_groups)
    # helper.save_data_to_json(
    #     questions_test, DATA_QUESTIONS_TEST)
    return questions_test


def calculate_rate():
    questions_test = get_questions_test_active()
    questions_test_level = get_questions_test_by_level(questions_test)
    questions_test_level_compare = get_questions_test_by_level_compare_rate_result(
        questions_test_level)

    get_questions_test_by_level_rate_output(
        questions_test_level_compare, INCREATE_RATE)
    # helper.save_data_to_json(
    #     questions_test_level, DATA_QUESTIONS_TEST_LEVEL)
    # helper.save_data_to_json(
    #     questions_test_level_compare, DATA_QUESTIONS_TEST_LEVEL_COMPARE)
