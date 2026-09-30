import math
from core import math_functions
from core.token import Token, TokenType
from core.lexer import Lexer
from core.parser import Parser
from core.exceptions import SyntaxError, MathError

ANGLE_DEPENDENT_FUNCTIONS = frozenset({
    'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 
    'arcsin', 'arccos', 'arctan', 'arccsc', 'arcsec', 'arccot'
    })

class CalculatorLogic:

    def __init__(self):

        self.raw_input = ''
        self.display_expression = ''

        self.calculated = False
        self.last_result = None

        self.angle_mode = 'DEG'
        self.angle_mode_used = None

        self.tokens = []
        self.lexer = Lexer()

        self.function_library = {
            **math.__dict__,
            **math_functions.__dict__,

            'abs': abs,
            'round': round,

            'phi': (1 + 5 ** 0.5) / 2,

            '%': lambda x: x * 0.01,
            '‰': lambda x: x * 0.001,

            '!': lambda x: math_functions.factorial(x),
            '!!': lambda x: math_functions.double_factorial(x),

            'sin': lambda x: math_functions.sin(x, self.angle_mode),
            'cos': lambda x: math_functions.cos(x, self.angle_mode),
            'tan': lambda x: math_functions.tan(x, self.angle_mode),
            'csc': lambda x: math_functions.csc(x, self.angle_mode),
            'sec': lambda x: math_functions.sec(x, self.angle_mode),
            'cot': lambda x: math_functions.cot(x, self.angle_mode),

            'arcsin': lambda x: math_functions.arcsin(x, self.angle_mode),
            'arccos': lambda x: math_functions.arccos(x, self.angle_mode),
            'arctan': lambda x: math_functions.arctan(x, self.angle_mode),
            'arccsc': lambda x: math_functions.arccsc(x, self.angle_mode),
            'arcsec': lambda x: math_functions.arcsec(x, self.angle_mode),
            'arccot': lambda x: math_functions.arccot(x, self.angle_mode)
            }


    def clear(self):
        self.tokens.clear()
        self.raw_input = ''
        self.display_expression = ''
        self.calculated = False


    def backspace(self):

        if not self.tokens:
            self.clear()
            return

        last = self.tokens[-1]

        if last.is_number() and len(last.key) > 1:
            trimmed = last.key[:-1]
            self.tokens[-1] = Token(TokenType.NUMBER, trimmed, trimmed, trimmed)
        else:
            self.tokens.pop()

        self.calculated = False

        print(self.tokens)
        self._update_expressions_from_tokens()


    def append(self, symbol):

        if self.display_expression == 'Error':
            self.clear()

        if self.calculated:
            incoming = self.lexer.tokenize(symbol)[0]
            if incoming.is_operator():
                self.tokens = [Token(TokenType.NUMBER, f'{self.last_result}', f'{self.last_result}', f'{self.last_result}')]
                self.raw_input = f'{self.last_result}'
            else:
                self.clear()

        self.calculated = False

        resolved = self._resolve_input(symbol)
        if resolved is None:
            return

        self.raw_input += resolved

        try:
            self.tokens = self.lexer.tokenize(self.raw_input)
            print(self.tokens)
            self._update_expressions_from_tokens()
        except SyntaxError:
            self.display_expression = self.raw_input


    def calculate(self):

        try:
            if not self.tokens:
                return None, None

            if any(token.type == TokenType.INVALID for token in self.tokens):
                raise SyntaxError('Invalid token')

            if not any(token.is_operator() or token.is_constant() or token.is_function() or token.is_special() for token in self.tokens):
                return None, None

            original_expression = self.display_expression

            uses_trig = any(token.eval_value in ANGLE_DEPENDENT_FUNCTIONS for token in self.tokens)
            self.angle_mode_used = self.angle_mode if uses_trig else None

            parser = Parser(self._expand_tokens(self.tokens))

            ast = parser.parse()
            scope = {
                **self.function_library,
                'Ans': self.last_result
            }
            result = ast.evaluate(scope)
            result = self._clean_result(result)

            if result < 0:
                positive_result = -result
                self.tokens = [Token(TokenType.INFIX_OPERATOR, '-', '-', '-'), 
                Token(TokenType.NUMBER, f'{positive_result}', f'{positive_result}', f'{positive_result}')]
            else:
                self.tokens = [Token(TokenType.NUMBER, f'{result}', f'{result}', f'{result}')]

            print(self.tokens)

            self.raw_input = ''
            self.display_expression = f'{result:.10g}'
            self.last_result = result

            self.calculated = True

            return original_expression, result

        except SyntaxError as e:
            print(f'Error: {e}')
            self.tokens.clear()
            self.raw_input = ''
            self.display_expression = 'Syntax Error'
            self.calculated = False 
            return None, 'Error'

        except MathError as e:
            print(f'Error: {e}')
            self.tokens.clear()
            self.raw_input = ''
            self.display_expression = 'Math Error'
            self.calculated = False 
            return None, 'Error'

        except Exception as e:
            print(f'Error: {e}')
            self.tokens.clear()
            self.raw_input = ''
            self.display_expression = 'Error'
            self.calculated = False 
            return None, 'Error'


    def negate(self):

        if not self.tokens:
            return
        
        for i in reversed(range(len(self.tokens))):
            token = self.tokens[i]
            if i > 0 and token.eval_value in ('+', '-'):
                new_sign = '-' if token.eval_value == '+' else '+'
                self.tokens[i] = Token(TokenType.INFIX_OPERATOR, new_sign, new_sign, new_sign)
                self._update_expressions_from_tokens()
                return

        if self.tokens[0].eval_value == '-':
            self.tokens.pop(0)
        else:
            self.tokens.insert(0, Token(TokenType.INFIX_OPERATOR, '-', '-', '-'))

        self.calculated = False

        print(self.tokens)
        self._update_expressions_from_tokens()


    def factorize(self):

        if not self.tokens:
            return

        token_values = []
        for token in self.tokens:
            if not isinstance(token.eval_value, list):
                token_values.append(token.eval_value)

        try:
            value = float(''.join(token_values))
        except ValueError:
            return

        self.calculated = False

        result = math_functions.factorize(int(value))
        if result:
            self.tokens = self.lexer.tokenize(result)
            print(self.tokens)
            self._update_expressions_from_tokens()


    def toggle_angle_mode(self):
        self.angle_mode = 'RAD' if self.angle_mode == 'DEG' else 'DEG'


    def _resolve_input(self, symbol):
        
        tokens = self.tokens
        last = tokens[-1] if tokens else None

        try:
            incoming_token = self.lexer.tokenize(symbol)[0]
        except ValueError:
            incoming_token = None

        if not tokens and symbol == '-':
            return '-'
        
        if not tokens and incoming_token and incoming_token.is_infix_operator():
            return None

        if last and last.display_value == '+' and symbol == '-':
            self.tokens.pop()
            self._update_expressions_from_tokens()
            return '-'

        if last and last.is_infix_operator() and symbol == '-':
            return None if last.eval_value == '-' else '-'

        if symbol == '.' and (not last or not last.is_value()):
            return '0.'

        if last and last.is_infix_operator() and incoming_token and incoming_token.is_infix_operator():
            return None
        
        if incoming_token and incoming_token.is_function():
            return symbol + '('

        if incoming_token and incoming_token.is_postfix_operator() and (last and last.eval_value in ('%', '‰') or not last.is_value()):
            return None

        if last and last.display_value[-1] in ('¹', '²', '³'):
            if incoming_token and (incoming_token.is_value() or incoming_token.is_function()):
                return '×' + symbol

        return symbol
    

    def _expand_tokens(self, tokens):
        result = []
        for token in tokens:
            if token.is_special():
                for sub in token.eval_value:
                    result.append(self.lexer._create_token_from_string(sub))
            else:
                result.append(token)
        return result


    def _update_expressions_from_tokens(self):
        self.raw_input = ''.join(token.key for token in self.tokens)
        self.display_expression = ''.join(token.display_value for token in self.tokens)


    def _clean_result(self, result):
        if isinstance(result, float):
            if abs(result) < 1e-10:
                return 0
            if abs(result - round(result)) < 1e-10:
                return int(round(result))
            if result.is_integer():
                return int(result)
            return round(result, 12)
        return result