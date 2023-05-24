from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

from models.nodes.requirement import Requirement
from models.nodes.test_case import TestCase


class GherkinParser:
    def __init__(self, location):
        self.__location = location

    def __parse_step(self, step_hash):
        keywords = [step_hash.get('text')]
        data_table = step_hash.get('dataTable') or {}
        rows = data_table.get('rows') or []
        header_row = rows[0] if len(rows) > 0 else None
        if header_row:
            cells = header_row.get('cells') or {}
            for cell in cells:
                keywords.append(cell.get('value'))
        return keywords

    def __parse_scenarios(self, scenarios):
        test_cases = []
        background_sentences = []
        for scenario in scenarios:
            sentences = []

            _, scenario_hash = list(scenario.items())[0]
            steps = scenario_hash.get('steps') or {}
            for step in steps:
                sentences += self.__parse_step(step)

            if scenario_hash.get('keyword') == 'Background':
                background_sentences = sentences
            elif scenario_hash.get('keyword') == 'Scenario':
                test_cases.append(TestCase(self.__location, scenario_hash.get('name'), background_sentences + sentences))
        return test_cases

    def parse(self):
        parsed_hash = Parser().parse(TokenScanner(self.__location))

        content = parsed_hash.get('feature')
        if content:
            req = Requirement(self.__location,
                              content.get('name'),
                              content.get('description')
                              )
            test_cases = self.__parse_scenarios(content.get('children') or {})
            return req, test_cases
        return None, []
