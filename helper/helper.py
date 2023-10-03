import random
import json
from models.hsk import ContentModel
from modules.questions import service


KIND_FORMAT_PATH = "static/kind_format.json"
TEST_PATH = "test/test_distribute_kind.json"


def save_data_to_json(data, path):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def flatten_recursive(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_recursive(item))
        else:
            result.append(item)
    return result


def get_raw_data(path):
    data = []
    with open(path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def simplify_input(input_obj):
    output_obj = {}

    for value1 in input_obj.values():
        for value2 in value1.values():
            for key3, value3 in value2["process"].items():
                if key3 not in output_obj:
                    output_obj[key3] = [
                        round((1-item[1])/2, 4) if item[1] <= 1 else 0 for item in value3 if item[1] is not None]
                else:
                    output_obj[key3].extend(round((1-item[1])/2, 4)
                                            for item in value3 if item[1] is not None)
    return output_obj


def distribute_total_question_diff(ques_in_level, total_diff):
    kind_detal = list(ques_in_level.keys())
    kind_rand_count = {item: 0 for item in kind_detal}

    while total_diff > 0:
        item = random.choice(kind_detal)
        increment = random.randint(
            0, min(ques_in_level[item] - kind_rand_count[item], total_diff))
        kind_rand_count[item] += increment
        total_diff -= increment

    result = {}
    for key in kind_rand_count.keys():
        new_value = [kind_rand_count[key],
                     ques_in_level[key] - kind_rand_count[key]]
        result[key] = new_value

    return result


def get_value_by_key(array, key):
    for item in array:
        if key in item:
            return item[key]
    return None


def gen_question_by_type_and_kind(test_follow_level, type_index, ids_diff, ids_not_diff, key, distribute_questions_diff_key):
    obj = next((item for item in test_follow_level[type_index]["parts"] if item.get(
        "kind") == key), None)
    kind_gen_result = service.get_question_by_ids_kind_and_add_score(
        ids_diff, ids_not_diff, key, obj["score"], distribute_questions_diff_key, obj["sub_count_question"])
    content_model: ContentModel = {
        "kind": key,
        "Questions": kind_gen_result
    }
    test_follow_level[type_index]["content"].append(content_model)
