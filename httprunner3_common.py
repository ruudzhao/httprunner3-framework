import yaml
import yaml.loader
from icecream import ic
from jinja2 import Environment, select_autoescape, FileSystemLoader
from os import scandir, DirEntry
import os
import toml
import argparse
import pprint
from httprunner3_logging import logger


#
# def to_string(obj):
#     print("obj", obj)
#     if not obj:
#         # return '[!string %r with length %i!]' % (obj, len(obj))
#         return repr('')
#     return repr(obj)
#
#
# ic.configureOutput(argToStringFunction=to_string)
#  ic.disable()


class HttpRunner3Common(object):
    def __init__(self):
        _desc = """Testcase convertor from yaml to pytest."""
        _desc_yaml = """one yaml file or yaml files' source dir.
            Testcase's yaml file prefix is test_ and postfix is .yaml or .yml, 
            but can't end up with _partial.yaml or _partial.yml.        
            Because *_partial.yaml or *_partial.yml is used as a component, which refer by a include directive."""
        _desc_testcases = """one pytest file or pytest file's target dir. 
            If -y is a file, then -t must be a file.
            if -y is a dir, then -t must be a dir.
            -y and -t must be match with same target object."""
        _desc_yaml = _desc_yaml.replace("        ", "")
        _desc_testcases = _desc_testcases.replace("        ", "")
        parser = argparse.ArgumentParser(description=_desc, allow_abbrev=False,
                                         formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(help='commands')
        make_parser = subparsers.add_parser(
            'make', help='Create a pytest file from yaml file', formatter_class=argparse.RawTextHelpFormatter)
        make_parser.add_argument("-y", "--yaml", metavar="dir/someone.yaml", dest="yaml", action="store",
                                 default="yaml",
                                 help=_desc_yaml)
        make_parser.add_argument("-t", "--testcases", metavar="dir/test.py", dest="testcases", action="store",
                                 default="testcases",
                                 help=_desc_testcases)
        make_parser.add_argument("-c", "--clean", dest="clean", action="store_true", default=False,
                                 help="delete all files and sub dir in target testcases dir")
        make_parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
                                 help="show detail process information")

        verify_parser = subparsers.add_parser(
            'verify', help='Verify a yaml or toml file')
        verify_parser.add_argument("filepath", default="",
                                   help="verify whether one yaml or toml file is valid in syntax")
        verify_parser.add_argument("-ic", "--ice_cream", dest="ice_cream", action="store_true", default=False,
                                   help="show content int ice_cream format, otherwise in pprint format")
        verify_parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
                                   help="show detail process information")

        """
        parser.add_argument("-y", "--yaml", metavar="someone.yaml(.yml)", dest="v_yaml", action="store", default="",
                            help="verify whether one yaml file is valid in syntax")
        parser.add_argument("-t", "--toml", metavar="someone.toml", dest="v_toml", action="store", default="",
                            help="verify whether one toml file is valid in syntax")

        parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
                            help="show detail process information")
        """
        parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.8.0')

        args = parser.parse_args()
        # ic(argparse.Namespace)
        # ic(type(args))
        # ic(args)
        parameters_dict = {"make": False, "verify": False}
        if hasattr(args, "yaml"):
            # ic(args.yaml)
            # ic(args.testcases)
            # ic(args.clean)
            parameters_dict["make"] = True
            parameters_dict["yaml"] = args.yaml if len(args.yaml.strip()) > 0 else "yaml"
            parameters_dict["testcases"] = args.testcases if len(args.testcases.strip()) > 0 else "testcases"
            parameters_dict["clean"] = args.clean
            parameters_dict["verbose"] = args.verbose
        elif hasattr(args, "filepath"):
            # ic(args.filepath)
            parameters_dict["verify"] = True
            parameters_dict["filepath"] = args.filepath
            parameters_dict["ice_cream"] = args.ice_cream
            parameters_dict["verbose"] = args.verbose
        else:
            parser.parse_args(["--help"])
        self.cli_parameters = parameters_dict

    def load_yaml(self, _yaml_file_path):
        try:
            with open(_yaml_file_path, mode='r', encoding="utf-8") as fp:
                yaml_dict = yaml.load(fp, Loader=yaml.loader.FullLoader)
                # yaml_dict = yaml.unsafe_load(fp)
                fp.close()
                return yaml_dict
        except (Exception,) as e:
            _msg = f"open yaml file fail：{_yaml_file_path} , reason: {e}"
            logger.error(_msg)
            raise SystemExit(_msg)

    def load_template(self, _file_path):
        # ic(__file__)
        template_path = "{}{}{}".format(os.path.dirname(os.path.abspath(__file__)), os.path.sep, "templates")
        # config_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "config.toml"
        # ic(template_path)
        env = Environment(
            # loader=FileSystemLoader("templates"),
            loader=FileSystemLoader(template_path),
            autoescape=select_autoescape(disabled_extensions=(".py",))
        )
        return env.get_template(_file_path)

    def handle_template_python_express(self, _content):
        return _content.replace("'<%-", "").replace("-%>'", "")

    def request_data(self, data_dict, alias_data_dict, parameters_dict, is_data_base=True):
        # ic(parameters_dict)
        for parameter_key in parameters_dict:
            index = parameter_key.find("@")
            if index >= 0:
                parameter_alias = parameter_key[0:index]
                parameter_name = parameter_key[index + 1:]
            else:
                parameter_name = parameter_key
                parameter_alias = ""

            if len(parameter_alias) > 0:
                if is_data_base:
                    alias_data_dict[parameter_alias] = parameter_name
                else:
                    alias_data_dict[parameter_alias] = parameters_dict[parameter_key]

            if len(parameter_name) > 0:
                data_dict[parameter_name] = parameters_dict[parameter_key]

    def yaml_is_testcase(self, _file_name):
        if _file_name.startswith('test') and (_file_name.endswith(".yaml") or _file_name.endswith(".yml")) \
                and not _file_name.endswith("_partial.yaml") and not _file_name.endswith("_partial.yml"):
            return True
        else:
            return False

    def yaml_is_testcase_component(self, _file_name):
        if _file_name.startswith('test') and (
                _file_name.endswith("_partial.yaml") or _file_name.endswith("_partial.yml")):
            return True
        else:
            return False

    def file_is_pytest(self, _file_name):
        if _file_name.startswith('test') and _file_name.endswith(".py"):
            return True
        else:
            return False

    def file_is_toml(self, _file_name):
        if _file_name.endswith(".toml"):
            return True
        else:
            return False

    def file_is_yaml(self, _file_name):
        if _file_name.endswith(".yaml") or _file_name.endswith(".yml"):
            return True
        else:
            return False

    def yaml_discover(self, _search_path, _path_len):
        with scandir(_search_path) as it:
            for entry in list(it):
                if entry.is_file() and self.yaml_is_testcase(entry.name):
                    yield entry.path[_path_len + 1:]

                if entry.is_dir():
                    for one in list(self.yaml_discover(entry.path, _path_len)):
                        yield one

    def verify_yaml_or_toml_file(self):
        file_path = self.cli_parameters["filepath"]
        # ic(file_path)
        ice_cream = self.cli_parameters["ice_cream"]
        # ic(ice_cream)
        if not os.path.exists(file_path):
            _msg = f"file is not exists: {file_path}"
            logger.error(_msg)
            raise SystemExit(_msg)

        file_name = os.path.basename(file_path)
        if self.file_is_toml(file_name):
            try:
                toml_file_content = toml.load(file_path)
                logger.info(toml_file_content)
                if ice_cream:
                    ic(toml_file_content)
                else:
                    pprint.pp(toml_file_content)
            except (Exception,) as e:
                _msg = f"load toml error: {file_path}, reason: {e}"
                logger.error(_msg)
                raise SystemExit()
        elif self.file_is_yaml(file_name):
            yaml_file_content = self.load_yaml(file_path)
            logger.info(yaml_file_content)
            if ice_cream:
                ic(yaml_file_content)
            else:
                pprint.pp(yaml_file_content)
        else:
            _msg = f"is not a valid file: {file_path}"
            logger.error(_msg)
            raise SystemExit(_msg)


if __name__ == "__main__":
    obj_common = HttpRunner3Common()
    ic(obj_common.cli_parameters)
    obj_common.verify_yaml_or_toml_file()
    exit(100)
