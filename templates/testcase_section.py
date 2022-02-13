

def {{ testcase_name }}({{ request_name }}):
    r = {{ request_name }}
    testcase_dict = {{ testcase }}
    key, value = testcase_dict.popitem()
    key = key.lower()
    if key == "exp":
        assert eval(value)
    else:
        compare_express = __compose_compare_express(key, value, r.raw)
        # ic(compare_express)
        assert eval(compare_express)

