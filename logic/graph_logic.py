from logic.calculator_logic import CalculatorLogic
from core.parser import Parser
from core.exceptions import MathError

class GraphLogic(CalculatorLogic):

    def __init__(self):
        super().__init__()
        self.angle_mode = 'RAD'

    def evaluate_graph(self, x, tokens=None):
        try:
            parser = Parser(self._expand_tokens(tokens if tokens is not None else self.tokens))

            ast = parser.parse()
            scope = {
                  **self.function_library,
                  'x': x
            }
            return ast.evaluate(scope)

        except MathError:
            return None