from modules.level.level_6 import Level_6_Service
from modules.level.level_5 import Level_5_Service
from modules.level.level_4 import Level_4_Service
from modules.level.level_3 import Level_3_Service
from modules.level.level_2 import Level_2_Service
from modules.level.level_1 import Level_1_Service
from helper import helper
from modules.exams import service

DATA_RATE_DIFF = "rate/db_rate_diff.json"
DATA_RATE_NOT_DIFF = "rate/db_rate_not_diff.json"
DATA_QUESTIONS_TEST_LEVEL_RATE_FINAL = "rate/db_questions_test_level_rate_final.json"
HSK_FORMAT = "static/hsk_format.json"
KIND_FORMAT_PATH = "static/kind_format.json"


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
            total_parts_test = obj.run()
            service.insert_exams(service.mapping_exams(total_parts_test, key))
        elif (key == "2"):
            obj = Level_2_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            total_parts_test = obj.run()
            service.insert_exams(service.mapping_exams(total_parts_test, key))
        elif (key == "3"):
            obj = Level_3_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            total_parts_test = obj.run()
            service.insert_exams(service.mapping_exams(total_parts_test, key))
        elif (key == "4"):
            obj = Level_4_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            total_parts_test = obj.run()
            service.insert_exams(service.mapping_exams(total_parts_test, key))
        elif (key == "5"):
            obj = Level_5_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            total_parts_test = obj.run()
            service.insert_exams(service.mapping_exams(total_parts_test, key))
        elif (key == "6"):
            obj = Level_6_Service(
                {"ids_diff": list_question_diff, "ids_not_diff": list_question_not_diff, "level": key, "questions": value, "count_diff": helper.get_value_by_key(dict_ques_diff_level, key), "level_format": hsk_format[key], "test_count": 5})
            total_parts_test = obj.run()
            service.insert_exams(service.mapping_exams(total_parts_test, key))
        else:
            continue
