from tests.my_test_case import MyTestCase
from rule import Rule, get_context_regex
from feature_bundle import FeatureBundle
from segment_table import SegmentTable
from math import log, ceil

class TestRule(MyTestCase):
    def setUp(self):
        self.initialise_segment_table("plural_english_segment_table.txt")

        number_of_features = len(SegmentTable().features)
        self.rule_symbol_length = ceil(log(number_of_features + 6, 2))   # + 5 for 3 delimiters (feature, bundle, rule part), plus sign and minus sign, 1 for kleene


    def test_rule(self):
        rule_set = self.get_rule_set("plural_english_rule_set.json")
        self.write_to_dot_to_file(rule_set.get_transducer(), "plural_english_rule_set")

    def test_abnese_rules(self):
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], False)
        self.write_to_dot_to_file(rule.get_transducer(), "abnese_optional")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], True)
        self.write_to_dot_to_file(rule.get_transducer(), "abnese_obligatory")

    def test_word_boundary(self):
        from simulations import word_boundary
        self.initialise_simulation(word_boundary)
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+", 'WB': True}], True)
        print(rule)
        for _ in range(20):
            rule.repr = None
            a = rule.right_context_feature_bundle_list._change_existing_feature_bundle()
            print(a)
            print(rule)

        # self.initialise_segment_table("ab_segment_table.txt")

    def test_add_feature(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [{"low": "+"}], obligatory=True)
        #rule.add_feature_to_bundle(rule.target_feature_bundle_list)
        #self.assertEqual(len(rule.target_feature_bundle_list), )
        print(FeatureBundle.get_random_feature_bundle())

    def test_make_mutation(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [{"low": "+"}], obligatory=True)
        rule.make_mutation()
        print(rule)

    def test_make_mutation_from_empty(self):
        rule = Rule([], [], [], [], obligatory=True)
        rule.make_mutation()
        print(rule)

    def test_generate_random(self):
        from simulations import word_boundary
        self.initialise_simulation(word_boundary)
        for _ in range(20):
            rule = Rule.get_random_rule()
            print(rule)

    def test_get_segment_representation(self):
        rule = Rule([{"cons": "+", "voice": "-"}, {"cons": "+", "voice": "-"}], [], [], [], obligatory=True)
        representation = rule.get_segment_representation()
        print(representation)

    def test_encoding(self):
        print(self.rule_symbol_length)
        rule = Rule([{"cons": "+", "voice": "-"}, {"cons": "+", "voice": "-"}], [], [], [], obligatory=True)

        print(rule.get_encoding_length(self.rule_symbol_length))

    def test_encoding_kleene(self):
        print("Rule symbol length:", self.rule_symbol_length)
        rule = Rule([{"cons": "+", "voice": "-"}, {"cons": "+", "voice": "-"}], [], [], [], obligatory=True)
        rule_with_kleene = Rule([{"cons": "+", "voice": "-"}, {"cons": "+", "voice": "-", "kleene": True}], [], [], [], obligatory=True)

        regular_length = rule.get_encoding_length(self.rule_symbol_length)
        kleene_length = rule_with_kleene.get_encoding_length(self.rule_symbol_length)

        print("Regular rule encoding length: {}, rule with kleene encoding length: {}".format(regular_length, kleene_length))

    def test_penultimate_lengthening(self):
        rule = Rule([{"voice": "-"}], [{"voice": "-"}], [{"voice": "-"}], [{"low": "+"}], obligatory=True)
        print(rule.get_encoding_length(6))

    def test_get_context_regex(self):
        rule = Rule([{"voice": "-"}], [{"voice": "-"}], [{"cons": "+"}, {"voice": "-"}], [{"low": "+"}], obligatory=True)
        left_context_feature_bundle_list = rule.left_context_feature_bundle_list
        right_context_feature_bundle_list = rule.right_context_feature_bundle_list

        left_context_regex = get_context_regex(left_context_feature_bundle_list)
        right_context_regex = get_context_regex(right_context_feature_bundle_list)
        print(left_context_regex)
        print(right_context_regex)
