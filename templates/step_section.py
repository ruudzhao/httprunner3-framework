

@pytest.fixture(scope="module")
def {{request_name}}(config_module):
    _svars = {{ variables }}
    svars = ObjectDotAccessWrapper(copy.deepcopy(_svars))
    svars.raw = _svars

    module_object = config_module
    _gvars = module_object.data
    gvars = ObjectDotAccessWrapper(copy.deepcopy(_gvars))
    gvars.raw = _gvars

    method = "{{ request_method }}"
    url = "{{ request_url }}"

    _data = {{ request_data }}
    data = ObjectDotAccessWrapper(copy.deepcopy(_data))
    data.raw = _data
    # __replace_parameters(data.raw, module_object.data)
    # ic(data)

    _headers = {{ request_headers }}
    headers = ObjectDotAccessWrapper(copy.deepcopy(_headers))
    headers.raw = _headers
    # __replace_parameters(headers.raw, module_object.data)
    # ic(headers)

    _message = module_object.http.act(method, url, _data, _headers)
    response = ObjectDotAccessWrapper(copy.deepcopy(_message))
    response.raw = _message

    # ic(full_message)
    extract_list = {{ extract_list }}
    for key in extract_list:
        _gvars[key] = jmespath.search(extract_list[key], response.raw)
    # ic(module_object.data)

    return response

