def Calc_block(left_value, oper, right_value):
    if oper  =='+':
        return sum(left_value, right_value)
    if   oper=='-':
        return sub(left_value, right_value)
    if   oper=='*':
        return mult(left_value, right_value)
    if (oper =='/') and (right_value != 0):
        return div(left_value, right_value)
    else:
        return 'Ошибка деления на 0!'

def sum(left_value, right_value):
    return left_value + right_value

def sub(left_value, right_value):
    return left_value - right_value

def mult(left_value, right_value):
    return left_value * right_value

def div(left_value, right_value):
    return left_value / right_value