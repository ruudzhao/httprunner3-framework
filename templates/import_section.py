# 引入当前目录作为模块导入的搜索目录
# 方法1：设置PYTHONPATH环境变量为%cd%
# print("PYTHONPATH", os.environ.get("PYTHONPATH", ""))
# 方法2：在程序中加入
# sys.path.append(os.path.curdir)
# if os.path.exists("ddt_analyse.py"):
#     import ddt_analyse as public
# 方法3：使用import_module函数
if os.path.exists("httprunner3_public.py"):
    public = importlib.import_module("httprunner3_public")

