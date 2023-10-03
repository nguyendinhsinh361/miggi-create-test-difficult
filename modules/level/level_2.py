from models.hsk import ContentModel
from helper import helper
import copy
DATA_TEST = "test/level_2.json"
DATA_TEST_DISTRIBUTE = "test/level_2_distribute.json"


class Level_2_Service:
    def __init__(self, obj):
        self.obj = obj

    def gen_questions(self, kind_data):
        total_test = []
        total_distribute = []
        for i in range(kind_data["test_count"]):
            test_follow_level = copy.deepcopy(kind_data["level_format"])
            distribute_questions_diff = helper.distribute_total_question_diff(
                kind_data["questions"], kind_data["count_diff"])
            total_distribute.append(distribute_questions_diff)
            for index, tmp in enumerate(test_follow_level):
                test_follow_level[index]["content"] = []
            for key, value in kind_data["questions"].items():
                if (key.startswith("21")):
                    helper.gen_question_by_type_and_kind(
                        test_follow_level, 0, kind_data["ids_diff"], kind_data["ids_not_diff"], key, distribute_questions_diff[key])

                elif (key.startswith("22")):
                    helper.gen_question_by_type_and_kind(
                        test_follow_level, 1, kind_data["ids_diff"], kind_data["ids_not_diff"], key, distribute_questions_diff[key])
            for index, tmp in enumerate(test_follow_level):
                del test_follow_level[index]["parts"]
            total_test.append(test_follow_level)
        helper.save_data_to_json(
            total_distribute, DATA_TEST_DISTRIBUTE)
        helper.save_data_to_json(total_test, DATA_TEST)

    def run(self):
        kind_data = self.obj
        self.gen_questions(kind_data)
