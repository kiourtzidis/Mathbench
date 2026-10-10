import math

def factorial(x):
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-10:
            x = int(round(x))

    return math.factorial(x)


def double_factorial(x):
    if x <= 0:
        return 1
    return x * double_factorial(x-2)


def frac(x):
    return _clean(x - math.floor(x))


def gamma(x):
    return _clean(math.gamma(x))


def lgamma(x):
    return _clean(math.lgamma(x))


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def factorize(number):

    if number == 0:
        return None
    elif number == 1:
        return 1
   
    if isinstance(number, float):
        if number.is_integer():
            number = int(number)
        else:
            return None
  
    if number < 0:
        number = abs(number)

    factors = []

    possible_factor = 2
    while number > 1:
        if number % possible_factor == 0:
            factors.append(f'{possible_factor}')
            number //= possible_factor
        else:
            possible_factor += 1

    return '×'.join(factors)


def cbrt(x):
    return _clean(math.cbrt(x))


def sin(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    return _clean(math.sin(x))


def cos(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    return _clean(math.cos(x))


def tan(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    c = math.cos(x)
    if abs(c) < 1e-12:
        raise ValueError('Error')
    return _clean(math.tan(x))


def csc(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    s = math.sin(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(1/s)


def sec(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    c = math.cos(x)
    if abs(c) < 1e-12:
        raise ValueError('Error')
    return _clean(1/c)


def cot(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    s = math.sin(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(math.cos(x)/s)


def sinh(x):
    return _clean(math.sinh(x))


def cosh(x):
    return _clean(math.cosh(x))


def tanh(x):
    return _clean(math.tanh(x))


def csch(x):
    s = math.sinh(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(1/s)


def sech(x):
    return _clean(1/math.cosh(x))


def coth(x):
    s = math.sinh(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(math.cosh(x)/s)


def arcsin(x, angle_mode):
    result = math.asin(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)    


def arccos(x, angle_mode):
    result = math.acos(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)    


def arctan(x, angle_mode):
    result = math.atan(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arccsc(x, angle_mode):
    if abs(x) < 1:
        raise ValueError('Error')
    result = math.asin(1/x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arcsec(x, angle_mode):
    if abs(x) < 1:
        raise ValueError('Error')
    result = math.acos(1/x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arccot(x, angle_mode):
    result = math.atan2(1, x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arcsinh(x):
    return _clean(math.asinh(x))


def arccosh(x):
    return _clean(math.acosh(x))


def arctanh(x):
    return _clean(math.atanh(x))


def arccsch(x):  
    if x == 0:  
        raise ValueError('Error')  
    return _clean(math.log(1/x+math.sqrt(1/(x**2)+1)))


def arcsech(x):  
    if x <= 0 or x > 1:  
        raise ValueError('Error')  
    return _clean(math.log((1+math.sqrt(1-x**2))/x))


def arccoth(x):  
    if abs(x) <= 1:  
        raise ValueError('Error')  
    return _clean(0.5*math.log((x+1)/(x-1)))


def _clean(x):
    if abs(x) < 1e-10:
        return 0
    elif abs(x - round(x)) < 1e-10:
        return int(round(x))
    return round(x, 12)