from core.exceptions import MathError

class Node:
    def evaluate(self, scope):
        raise NotImplementedError()


class NumberNode(Node):

    def __init__(self, value):
        self.value = value


    def evaluate(self, scope):
        return self.value


class NegNode(Node):

    def __init__(self, right):
        self.right = right


    def evaluate(self, scope):
        return -self.right.evaluate(scope)


class AddNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) + self.right.evaluate(scope)


class SubNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) - self.right.evaluate(scope)


class MulNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) * self.right.evaluate(scope)


class DivNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        try:
            return self.left.evaluate(scope) / self.right.evaluate(scope)
        except ZeroDivisionError:
            raise MathError('Division by zero')


class FloorDivNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        try:
            return self.left.evaluate(scope) // self.right.evaluate(scope)
        except ZeroDivisionError:
            raise MathError('Division by zero')


class ModNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        try:
            return self.left.evaluate(scope) % self.right.evaluate(scope)
        except ZeroDivisionError:
            raise MathError('Division by zero')


class PowerNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        try:
            result = self.left.evaluate(scope) ** self.right.evaluate(scope)
        except OverflowError:
            raise MathError('Result too large')
        except ZeroDivisionError:
            raise MathError('Division by zero')

        if isinstance(result, complex):
            raise MathError('Result is not a real number')

        return result


class PostfixNode(Node):

    def __init__(self, left, operator):
        self.left = left
        self.operator = operator.eval_value


    def evaluate(self, scope):
        try:
            return scope[self.operator](self.left.evaluate(scope))
        except (ValueError, OverflowError) as e:
            raise MathError(str(e))


class VariableNode(Node):

    def __init__(self, name):
        self.name = name


    def evaluate(self, scope):
        return scope[self.name]


class FunctionNode(Node):

    def __init__(self, function, arg):
        self.function = function
        self.arg = arg


    def evaluate(self, scope):
        try:
            return scope[self.function](self.arg.evaluate(scope))
        except (ValueError, OverflowError) as e:
            raise MathError(str(e))