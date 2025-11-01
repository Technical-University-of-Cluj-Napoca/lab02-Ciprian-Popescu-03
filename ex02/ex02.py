def multiply_all(*args: int) -> int:
    product = 1
    for num in args:
        product *= num
    return product

if __name__ == "__main__":
    test_cases = [
        (1, 2, 3, 4, 5),
        (),
        (7,)
    ]
    for case in test_cases:
        print(multiply_all(*case))