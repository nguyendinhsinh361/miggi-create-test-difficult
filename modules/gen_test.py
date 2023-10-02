from modules.level.level_6 import Level_6_Service
from modules.level.level_5 import Level_5_Service
from modules.level.level_4 import Level_4_Service
from modules.level.level_3 import Level_3_Service
from modules.level.level_2 import Level_2_Service
from modules.level.level_1 import Level_1_Service
from helper import helper

DATA_RATE_DIFF = "data/db_rate_diff.json"
DATA_RATE_NOT_DIFF = "data/db_rate_not_diff.json"
KIND_FORMAT_PATH = "static/kind_format.json"
DATA_QUESTIONS_TEST_LEVEL_RATE_FINAL = "data/db_questions_test_level_rate_final.json"
HSK_FORMAT = "static/hsk_format.json"


def run():
    dict_question_diff = helper.get_raw_data(
        DATA_RATE_DIFF)

    dict_question_not_diff = helper.get_raw_data(
        DATA_RATE_NOT_DIFF)

    kind_format = helper.get_raw_data(
        KIND_FORMAT_PATH)

    hsk_format = helper.get_raw_data(
        HSK_FORMAT)

    dict_ques_diff_level = helper.get_raw_data(
        DATA_QUESTIONS_TEST_LEVEL_RATE_FINAL)
    list_question_diff = list(dict_question_diff.keys())
    list_question_not_diff = list(dict_question_not_diff.keys())

    for key, value in kind_format.items():
        if (key == "1"):
            obj = Level_1_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            obj.run()
        elif (key == "2"):
            obj = Level_2_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            obj.run()
        elif (key == "3"):
            obj = Level_3_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            obj.run()
        elif (key == "4"):
            obj = Level_4_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            obj.run()
        elif (key == "5"):
            obj = Level_5_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            obj.run()
        elif (key == "6"):
            obj = Level_6_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            obj.run()
        else:
            continue
