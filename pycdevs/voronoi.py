from .models import Model, CellValues
import re

CURRENT_CELL_EXPRESSION_KEY = "${current_cell}"

DEFAULT_RULE = "rule : {(0,0)} 0 { t }\n"
ZERO_POSITION = (0, 0)
EXPRESSION_LOOKUP_PATTERN = "\${([a-zA-Z_]+)}"

DEFAULT_VORONOI_MODEL_TEMPLATE="""
[Top]
components: ${model_name}

[${model_name}]
type: cell
dim: ${initial_cell_values_dimension}
delay: transport
defaultDelayTime: 0
border: nowrapped
neighbors: ${neighbours}
initialvalue: 0
initialCellsValue: ${initial_cell_values_path}
localtransition: ${model_name}_site

[${model_name}_site]
${rule_set}
"""


def print_cell_position(position: tuple):
    return "({0},{1})".format(position[0], position[1])


class Neighbourhood:
    def __init__(self, neighbours_list):
        if len(neighbours_list) == 0:
            raise Exception('Cannot generate neighbourhood with an empty neighbours list')

        self.neighbours = neighbours_list

    def print_neighbours_list(self, parent_model):
        if ZERO_POSITION not in self.neighbours:
            self.neighbours.append(ZERO_POSITION)
        return " ".join([parent_model.name + str(neighbour).replace(' ', '') for neighbour in self.neighbours])

    def __iter__(self):
        return iter(self.neighbours)


class RulesetBuilder:
    def __init__(self, pattern : str, add_default_rule=True):
        self.rule_pattern = pattern
        self.should_apply_default_rule = add_default_rule
        self.append_new_line_to_rule_pattern()

    def append_new_line_to_rule_pattern(self):
        if not self.rule_pattern.endswith('\n'):
            self.rule_pattern = self.rule_pattern + '\n'

    def build(self, neighbourhood):
        rule_set = ""
        for neighbour in neighbourhood:
            rule_set = rule_set + self.rule_pattern.replace(CURRENT_CELL_EXPRESSION_KEY, print_cell_position(neighbour))
        if self.should_apply_default_rule:
            rule_set = rule_set + DEFAULT_RULE

        return rule_set


class VoronoiModel(Model):
    def __init__(self, name: str, neighbourhood: Neighbourhood, cell_values: CellValues, rule_builder: RulesetBuilder):
        super(VoronoiModel, self).__init__('', name)
        self.neighbourhood = neighbourhood
        self.initial_cell_values = cell_values
        self.rule_builder = rule_builder

        self.expression_register = {}
        self.register_initial_expressions()

    def register_initial_expressions(self):
        self.expression_register['model_name'] = self.name
        self.expression_register['initial_cell_values_dimension'] = self.initial_cell_values.get_printable_dimension()
        self.expression_register['initial_cell_values_path'] = self.initial_cell_values.write_to_file()
        self.expression_register['neighbours'] = self.neighbourhood.print_neighbours_list(self)
        self.expression_register['rule_set'] = self.rule_builder.build(self.neighbourhood)

    def build(self):
        self.source = DEFAULT_VORONOI_MODEL_TEMPLATE

        self.replace_expressions()
        return self

    def replace_expressions(self):
        expression_finder = re.compile(EXPRESSION_LOOKUP_PATTERN)
        non_replaced_source = self.source
        for expression_found in expression_finder.finditer(non_replaced_source):
            replaceable_expression = expression_found[0]
            expression_key = expression_found[1]

            try:
                resolved_value = self.expression_register[expression_key]
            except KeyError:
                raise Exception('Expression with key "{0}" was not found in expression register.'.format(expression_key))

            self.source = self.source.replace(replaceable_expression, resolved_value)







