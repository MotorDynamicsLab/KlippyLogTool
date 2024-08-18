import inspect


def get_current_function_name():
    # 获取调用栈
    stack = inspect.stack()
    # 返回调用该函数的上一级函数的名称
    return stack[1].function


def example_function():
    function_name = get_current_function_name()
    print(f"当前函数的名称是: {function_name}")


example_function()
