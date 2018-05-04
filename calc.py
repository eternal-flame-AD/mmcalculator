import sys

# 定义优先级
PRIORITY = "^,*,/,+,-"


def main(expression):
    exp_list = list("".join(expression))
    format_list = format(exp_list)
    res = calculate(format_list)
    print(res)
    #输出结果


#按照优先级进行计算
def priority_compute(format_list):
    _format_list = format_list
    for oper in PRIORITY.split(","):
        _format_list = compute(_format_list, oper)
    return _format_list


#格式化表达式
def format(single_list):
    temp_list = []
    temp_num = ""
    for index, i in enumerate(single_list):

        if (isNumber(i)): temp_num += i

        if (isOperator(i)):
            if (temp_num != ""): temp_list.append(temp_num)
            temp_list.append(i)
            temp_num = ""

        if (len(single_list) - 1 == index):
            if (temp_num != ""): temp_list.append(temp_num)

    return temp_list


#计算带括号的表达式
def calculate(format_list):
    expression = "".join(format_list)

    if expression.find("(") == -1:
        return priority_compute(format_list)

    parathesis = []  #做符号栈检查括号匹配
    for i in range(len(expression)):
        if expression[i] == '(':  #遇到左括号, 表达式起点
            parathesis.append(i)  #保存左括号的下标
        elif expression[i] == ')':  #遇到右括号, 表达式终点, 遇到完整的一段表达式则递归计算
            if len(parathesis) != 0:
                subexp = expression[parathesis[-1]:i + 1][1:-1]  #截取子表达式
                if subexp.find("(") == -1:  #如果子表达式不含有括号了则计算
                    result = priority_compute(format(subexp))[0]  #计算子表达式的结果
                    pre = expression[0:parathesis[-1]]  #括号前面的表达式
                    post = expression[i + 1:]  #括号后面的表达式
                    expression = pre + str(result) + post  #拼接为新的表达式
                    return calculate(expression)  #递归计算
                parathesis.pop()  #删除一个左括号


#计算表达式
def compute(format_list, operator):
    timer = 0
    for index, i in enumerate(format_list):
        if (isOperator(i) and i == operator):
            timer += 1
            left = float(format_list[index - 1])
            right = float(format_list[index + 1])
            if operator == "^": format_list[index - 1] = left**right
            if operator == "*": format_list[index - 1] = left * right
            if operator == "/": format_list[index - 1] = left / right
            if operator == "+": format_list[index - 1] = left + right
            if operator == "-": format_list[index - 1] = left - right
            del format_list[index]
            del format_list[index]

    if (timer):
        return compute(format_list, operator)
    else:
        return format_list


# 判断是否是运算符
def isOperator(str):
    return True if str in PRIORITY.split(",") else False


# 判断是否是数字
def isNumber(str):
    return True if str.isdigit() or str == "." else False


if __name__ == "__main__":
    main(sys.argv[1:])
