from functools import partial


def stream(username):
    return f"my name is {username}"


new_func = partial(stream, "pss")
print(type(new_func))
print(new_func())
