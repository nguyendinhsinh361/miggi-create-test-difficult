# Step 1
from helper import helper
from tqdm import tqdm
import json

DATA_RATE_DIFF = "rate/db_rate_diff.json"
DATA_RATE_NOT_DIFF = "rate/db_rate_not_diff.json"


def get_user_history_ids_rate_result(user_history_ids_rate):
    user_history_ids_diff_result = {}
    user_history_ids_not_diff_result = {}
    for key, value in user_history_ids_rate.items():
        if value > 0.4:
            user_history_ids_diff_result[key] = value
        else:
            user_history_ids_not_diff_result[key] = value
    return user_history_ids_diff_result, user_history_ids_not_diff_result


def get_question_exist(cursor, user_history_ids_com):
    question_ids_exist = list(user_history_ids_com.keys())
    question_ids_exist.remove('undefined')
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


def get_user_history_ids_rate(user_history_ids_com_exist):
    user_history_ids_rate = {}
    for key, values in tqdm(user_history_ids_com_exist.items()):
        if len(values) > 0:
            average_value = round(sum(values) / len(values), 4)
            user_history_ids_rate[key] = average_value
    return user_history_ids_rate


def get_user_history_ids_complete(user_history_ids_raw):
    user_history_ids_com = {}
    for id in tqdm(user_history_ids_raw):
        for key, value in id["history"].items():
            if key in user_history_ids_com:
                user_history_ids_com[key].extend(value)
            else:
                user_history_ids_com[key] = value
    return user_history_ids_com


def statistics_question(cursor):
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
    user_history_ids_com_exist = get_question_exist(
        cursor, user_history_ids_com)

    user_history_ids_rate = get_user_history_ids_rate(
        user_history_ids_com_exist)
    user_history_ids_diff_result, user_history_ids_not_diff_result = get_user_history_ids_rate_result(
        user_history_ids_rate)

    helper.save_data_to_json(
        user_history_ids_diff_result, DATA_RATE_DIFF)
    helper.save_data_to_json(
        user_history_ids_not_diff_result, DATA_RATE_NOT_DIFF)


def run(cursor):
    statistics_question(cursor)
