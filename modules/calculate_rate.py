# Step 2
from config import database
from helper import helper
import json
from tqdm import tqdm
import numpy as np
import math

CONN = database.connect_db()
INCREATE_RATE = 1.4
DATA_RATE_DIFF = "rate/db_rate_diff.json"
DATA_RATE_NOT_DIFF = "rate/db_rate_not_diff.json"
DATA_QUESTIONS_TEST_LEVEL_RATE = "rate/db_questions_test_level_rate.json"
DATA_QUESTIONS_TEST_LEVEL_RATE_FINAL = "rate/db_questions_test_level_rate_final.json"
KIND_FORMAT_PATH = "static/kind_format.json"


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


def calculate_rate():
    questions_test = get_questions_test_active()
    questions_test_level = get_questions_test_by_level(questions_test)
    questions_test_level_compare = get_questions_test_by_level_compare_rate_result(
        questions_test_level)

    get_questions_test_by_level_rate_output(
        questions_test_level_compare, INCREATE_RATE)


def run():
    calculate_rate()
