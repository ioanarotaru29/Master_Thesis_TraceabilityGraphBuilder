from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner


class GherkinParser:
    def __init__(self, location):
        self.__location = location
        self.__name = ''
        self.__keywords = []

    def __parse_scenario(self, scenario_hash):
        self.__keywords.append(scenario_hash.get('name'))
        self.__keywords.append(scenario_hash.get('description'))

        steps = scenario_hash.get('steps') or {}
        for step in steps:
            self.__parse_step(step)

    def __parse_step(self, step_hash):
        self.__keywords.append(step_hash.get('text'))
        data_table = step_hash.get('dataTable') or {}
        rows = data_table.get('rows') or []
        header_row = rows[0] if len(rows) > 0 else None
        if header_row:
            cells = header_row.get('cells') or {}
            for cell in cells:
                self.__keywords.append(cell.get('value'))

    def parse(self):
        parsed_hash = Parser().parse(TokenScanner(self.__location))

        content = parsed_hash.get('feature')
        if content:
            self.__name = content.get('name')
            self.__keywords.append(content.get('description'))

            scenarios = content.get('children') or {}
            for scenario in scenarios:
                if scenario.get('scenario'):
                    self.__parse_scenario(scenario.get('scenario'))

        return self.__name, self.__keywords
