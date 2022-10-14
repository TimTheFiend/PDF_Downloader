def hello():
    return 1, 2, 3


if __name__ == "__main__":
    foo, bar, baz = hello()

    print(foo + bar + baz)