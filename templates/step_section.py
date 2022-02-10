

@pytest.fixture(scope="module")
def {{request_name}}(config_module):
    vars = ObjectDotAccessWrapper({{ variables }})
    module_object = config_module
    gvars = ObjectDotAccessWrapper(module_object.data)
    method = "{{ request_method }}"
    url = "{{ request_url }}"
    data = {{request_data}}
    __replace_parameters(data, module_object.data)
    # ic(data)
    headers = {{request_headers}}
    __replace_parameters(headers, module_object.data)
    # ic(headers)
    full_message = module_object.http.act(method, url, data, headers)
    # ic(full_message)
    extract_list = {{ extract_list }}
    for key in extract_list:
        module_object.data[key] = jmespath.search(extract_list[key], full_message)
    # ic(module_object.data)

    return full_message

