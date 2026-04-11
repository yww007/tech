#!/usr/bin/env python3
"""
技术文档自动更新脚本（优化版）
参考Claude Code文章格式，生成更详细的技术文档
包含：详细章节、实战案例、表格对比、代码示例、FAQ、参考资料、实战SOP
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import time

# 配置
BLOG_PATH = "/home/swg/.openclaw/workspace/tech-blog"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")
IMAGES_DIR = Path(BLOG_PATH) / "images"
LOGS_DIR = Path(BLOG_PATH) / "logs"

# 创建必要的目录
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class Logger:
    def __init__(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = LOGS_DIR / f"{today}.log"
        self.log("=" * 60)
        self.log(f"开始更新技术文档 - {datetime.now()}")
        self.log("=" * 60)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")

logger = Logger()

def get_beijing_time():
    """获取北京时间（UTC+8）"""
    return datetime.now() + timedelta(hours=8)

def get_tech_topic():
    """获取技术主题（按日期轮换，避免重复）"""
    TECH_TOPICS = [
        "Python编程技巧与最佳实践",
        "Docker容器化部署指南",
        "Git版本控制高级用法",
        "Linux系统管理技巧",
        "数据库优化策略",
        "Web安全防护指南",
        "微服务架构设计",
        "云原生技术实践",
        "DevOps自动化流程",
        "人工智能应用开发"
    ]

    # 按日期轮换，避免重复
    day_of_year = datetime.now().timetuple().tm_yday
    topic_index = (day_of_year - 1) % len(TECH_TOPICS)
    return TECH_TOPICS[topic_index]

def get_topic_content(topic):
    """获取主题的详细内容（优化版）"""
    content_map = {
        "Python编程技巧与最佳实践": {
            "intro": "Python是一门简洁而强大的编程语言，掌握其编程技巧和最佳实践可以显著提升代码质量和开发效率。本文将深入介绍Python的高级特性、性能优化技巧、代码规范、常见陷阱的避免方法，以及实战案例和最佳实践。",
            "overview": "Python以其简洁的语法和强大的生态系统，成为最受欢迎的编程语言之一。然而，很多开发者只掌握了基础语法，对Python的高级特性和最佳实践了解不足。本文将从基础到高级，全面介绍Python编程技巧，帮助你写出更高效、更优雅的Python代码。",
            "chapters": {
                "第一章 认识Python高级编程": {
                    "sections": [
                        {
                            "title": "1.1 Python高级编程的本质",
                            "content": "Python高级编程不仅仅是掌握语法，更是理解Python的设计哲学和最佳实践。核心认知：从'能写代码'到'写好代码'的转变。Python越强大，你越要注意代码的可读性、可维护性和性能。"
                        },
                        {
                            "title": "1.2 与其他语言的核心区别",
                            "content": "Python vs Java：Python更简洁，但性能较低；Java更严格，但性能更高。Python vs C++：Python开发效率高，C++执行效率高。Python vs JavaScript：Python适合后端，JavaScript适合前端。"
                        },
                        {
                            "title": "1.3 Python能力全景",
                            "content": "代码开发：函数式编程、面向对象编程、元编程。性能优化：算法优化、数据结构优化、并发编程。测试自动化：单元测试、集成测试、性能测试。Web开发：Flask、Django、FastAPI。数据分析：NumPy、Pandas、Matplotlib。"
                        }
                    ]
                },
                "第二章 核心概念与高级特性": {
                    "sections": [
                        {
                            "title": "2.1 列表推导式与生成器",
                            "content": "列表推导式：一行代码生成列表，简洁高效。生成器：惰性求值，节省内存。生成器表达式：类似列表推导式，但返回生成器。"
                        },
                        {
                            "title": "2.2 装饰器与上下文管理器",
                            "content": "装饰器：函数包装器，增强功能。@语法糖：简化装饰器使用。上下文管理器：自动资源管理，with语句。@contextmanager：快速创建上下文管理器。"
                        },
                        {
                            "title": "2.3 元类与属性",
                            "content": "元类：类的类，控制类的创建。type()：动态创建类。__metaclass__：指定元类。property：属性装饰器，控制属性访问。@property、@setter、@deleter。"
                        }
                    ]
                },
                "第三章 性能优化技巧": {
                    "sections": [
                        {
                            "title": "3.1 算法与数据结构优化",
                            "content": "选择合适的数据结构：列表、字典、集合、元组。使用内置函数：sum()、map()、filter()。避免不必要的循环：列表推导式、生成器表达式。"
                        },
                        {
                            "title": "3.2 缓存与记忆化",
                            "content": "@lru_cache：缓存函数结果，避免重复计算。functools.cache：Python 3.9+的简化版本。手动缓存：使用字典存储中间结果。"
                        },
                        {
                            "title": "3.3 并发与并行",
                            "content": "多线程：适合IO密集型任务。多进程：适合CPU密集型任务。asyncio：异步编程，提升IO性能。concurrent.futures：高级并发接口。"
                        }
                    ]
                },
                "第四章 代码规范与最佳实践": {
                    "sections": [
                        {
                            "title": "4.1 PEP 8代码风格",
                            "content": "命名规范：变量名小写下划线，类名大驼峰。缩进：4个空格，不要用Tab。行长度：不超过79字符。导入：标准库、第三方库、本地模块。"
                        },
                        {
                            "title": "4.2 类型注解",
                            "content": "类型提示：提高代码可读性和IDE支持。typing模块：List、Dict、Optional、Union。类型检查：mypy静态类型检查。"
                        },
                        {
                            "title": "4.3 文档字符串",
                            "content": "docstring：函数、类、模块的文档。Google风格：参数、返回值、异常。NumPy风格：更详细的参数说明。"
                        }
                    ]
                },
                "第五章 实战案例与SOP": {
                    "sections": [
                        {
                            "title": "5.1 实战案例：高性能数据处理",
                            "content": "场景：处理百万级数据。方案：使用生成器+多进程。步骤：1. 生成器读取数据；2. 多进程处理；3. 结果汇总。"
                        },
                        {
                            "title": "5.2 实战案例：Web API性能优化",
                            "content": "场景：API响应慢。方案：缓存+异步。步骤：1. 添加Redis缓存；2. 使用异步框架；3. 数据库查询优化。"
                        },
                        {
                            "title": "5.3 实战SOP：代码审查清单",
                            "content": "代码风格：符合PEP 8规范。类型注解：关键函数有类型提示。文档字符串：公共函数有docstring。测试覆盖：核心逻辑有单元测试。性能：无明显性能瓶颈。"
                        }
                    ]
                }
            },
            "concepts": {
                "核心概念": [
                    "列表推导式 - 一行代码生成列表，简洁高效",
                    "生成器 - 惰性求值，节省内存",
                    "装饰器 - 函数包装器，增强功能",
                    "上下文管理器 - 自动资源管理，with语句",
                    "元类 - 类的类，控制类的创建",
                    "属性 - 控制属性访问，property装饰器"
                ],
                "关键术语": [
                    "PEP 8 - Python官方代码风格指南",
                    "GIL - 全局解释器锁，影响多线程性能",
                    "鸭子类型 - 不关注类型，关注行为",
                    "魔法方法 - 以__开头和结尾的特殊方法",
                    "类型注解 - 类型提示，提高代码可读性",
                    "异步编程 - asyncio，提升IO性能"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用f-string格式化字符串，比%和.format()更快更易读",
                    "善用enumerate()同时获取索引和值",
                    "使用zip()并行遍历多个序列",
                    "用collections.Counter统计元素出现次数",
                    "使用with语句管理资源，自动关闭",
                    "使用列表推导式代替循环",
                    "使用生成器表达式节省内存"
                ],
                "高级技巧": [
                    "使用@lru_cache缓存函数结果，避免重复计算",
                    "用__slots__减少内存占用，适合大量实例",
                    "使用asyncio实现异步编程，提升IO密集型任务性能",
                    "用multiprocessing绕过GIL限制，实现真正的并行",
                    "使用装饰器增强函数功能",
                    "使用上下文管理器管理资源",
                    "使用元类动态创建类"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "遵循PEP 8规范，使用black自动格式化",
                    "编写docstring文档，使用Google或NumPy风格",
                    "使用类型注解，提高代码可读性和IDE支持",
                    "编写单元测试，使用pytest框架",
                    "使用虚拟环境隔离依赖，推荐venv或conda",
                    "用requirements.txt或pyproject.toml管理依赖"
                ],
                "部署策略": [
                    "使用Docker容器化部署，保证环境一致性",
                    "配置CI/CD流水线，自动化测试和部署",
                    "使用日志记录，便于问题排查",
                    "配置监控告警，及时发现异常",
                    "定期更新依赖，修复安全漏洞"
                ]
            },
            "comparison_tables": [
                {
                    "title": "Python vs 其他语言对比",
                    "headers": ["特性", "Python", "Java", "C++", "JavaScript"],
                    "rows": [
                        ["开发效率", "⭐⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐"],
                        ["执行效率", "⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐"],
                        ["学习曲线", "⭐⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐"],
                        ["生态系统", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐⭐"],
                        ["适用场景", "数据分析、AI、Web", "企业应用、Android", "系统编程、游戏", "前端、Node.js"]
                    ]
                },
                {
                    "title": "Python数据结构对比",
                    "headers": ["数据结构", "特点", "适用场景", "时间复杂度"],
                    "rows": [
                        ["列表", "有序、可变", "存储序列数据", "O(1)访问, O(n)查找"],
                        ["元组", "有序、不可变", "固定数据、字典键", "O(1)访问, O(n)查找"],
                        ["字典", "键值对、无序", "快速查找", "O(1)访问"],
                        ["集合", "无序、唯一", "去重、成员测试", "O(1)访问"]
                    ]
                }
            ],
            "code_examples": [
                {
                    "title": "Python最佳实践示例",
                    "code": '''# Python最佳实践示例

from functools import lru_cache
from typing import List, Optional, Dict
from dataclasses import dataclass
from contextlib import contextmanager
import asyncio
from concurrent.futures import ProcessPoolExecutor

# 1. 使用类型注解和dataclass
@dataclass
class User:
    """用户数据类"""
    id: int
    name: str
    email: Optional[str] = None

# 2. 使用装饰器缓存结果
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """计算斐波那契数列（带缓存）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 3. 使用上下文管理器
@contextmanager
def timer(name: str):
    """计时上下文管理器"""
    import time
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"{name} 耗时: {elapsed:.3f}秒")

# 4. 使用列表推导式和生成器
def process_users(users: List[User]) -> List[str]:
    """处理用户列表"""
    # 列表推导式
    active_users = [u for u in users if u.email]
    # 生成器表达式
    emails = (u.email for u in active_users if u.email)
    return list(emails)

# 5. 异步编程示例
async def fetch_data(url: str) -> Dict:
    """异步获取数据"""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    """主函数"""
    urls = ["https://api.example.com/data1",
            "https://api.example.com/data2"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# 6. 多进程示例
def process_item(item: int) -> int:
    """处理单个项目"""
    import time
    time.sleep(0.1)  # 模拟耗时操作
    return item * 2

def parallel_process(items: List[int]) -> List[int]:
    """并行处理"""
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_item, items))
    return results

# 使用示例
if __name__ == "__main__":
    # 计时示例
    with timer("斐波那契计算"):
        result = fibonacci(35)
        print(f"fibonacci(35) = {result}")

    # 用户处理示例
    users = [
        User(1, "Alice", "alice@example.com"),
        User(2, "Bob", "bob@example.com"),
        User(3, "Charlie", None)
    ]

    emails = process_users(users)
    print(f"活跃用户邮箱: {emails}")

    # 并行处理示例
    items = list(range(10))
    results = parallel_process(items)
    print(f"并行处理结果: {results}")'''
                },
                {
                    "title": "装饰器高级用法",
                    "code": '''# 装饰器高级用法

from functools import wraps
import time
from typing import Callable, Any

# 1. 带参数的装饰器
def repeat(times: int):
    """重复执行函数"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name: str) -> str:
    """打招呼"""
    return f"Hello, {name}!"

# 2. 计时装饰器
def timer(func: Callable) -> Callable:
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} 耗时: {elapsed:.3f}秒")
        return result
    return wrapper

@timer
def slow_function():
    """慢函数"""
    time.sleep(1)
    return "完成"

# 3. 缓存装饰器
def cache(func: Callable) -> Callable:
    """缓存装饰器"""
    cache_dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache_dict:
            cache_dict[key] = func(*args, **kwargs)
        return cache_dict[key]
    return wrapper

@cache
def expensive_computation(x: int) -> int:
    """昂贵计算"""
    time.sleep(0.1)
    return x * x

# 4. 类装饰器
class CountCalls:
    """计数装饰器"""
    def __init__(self, func: Callable):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"调用次数: {self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    """打招呼"""
    return "Hello!"

# 使用示例
if __name__ == "__main__":
    # 重复执行
    greetings = greet("Alice")
    print(f"问候结果: {greetings}")

    # 计时
    result = slow_function()
    print(f"结果: {result}")

    # 缓存
    start = time.time()
    for i in range(5):
        result = expensive_computation(i)
    elapsed = time.time() - start
    print(f"缓存计算耗时: {elapsed:.3f}秒")

    # 计数
    for _ in range(3):
        say_hello()'''
                }
            ],
            "faq": [
                {
                    "question": "如何提升Python代码性能？",
                    "answer": "1. 使用内置函数和库（如sum()、map()）比循环更快；2. 使用生成器代替列表，节省内存；3. 使用@lru_cache缓存重复计算；4. 对于CPU密集型任务，使用multiprocessing；5. 使用C扩展（如NumPy、Cython）加速数值计算；6. 选择合适的数据结构（字典查找O(1)，列表查找O(n)）；7. 避免不必要的全局变量查找；8. 使用局部变量代替全局变量。"
                },
                {
                    "question": "Python多线程为什么不能提升性能？",
                    "answer": "因为Python有GIL（全局解释器锁），同一时刻只能有一个线程执行Python字节码。多线程适合IO密集型任务（如网络请求、文件读写），对于CPU密集型任务，应该使用multiprocessing实现真正的并行。GIL的存在是为了简化CPython的实现，避免多线程访问Python对象时的竞争条件。"
                },
                {
                    "question": "什么时候应该使用生成器而不是列表？",
                    "answer": "1. 处理大量数据时，生成器可以节省内存；2. 数据流式处理，不需要一次性加载所有数据；3. 实现迭代器协议，提供惰性求值；4. 管道式数据处理，逐个处理元素。注意：生成器只能遍历一次，如果需要多次遍历，应该转换为列表。"
                },
                {
                    "question": "如何选择合适的数据结构？",
                    "answer": "1. 列表：有序序列，需要频繁访问和修改；2. 元组：不可变序列，作为字典键或函数参数；3. 字典：键值对，需要快速查找；4. 集合：去重、成员测试；5. collections.deque：双端队列，频繁头尾操作；6. collections.defaultdict：带默认值的字典；7. collections.Counter：计数器。"
                }
            ],
            "references": [
                "官方文档：https://docs.python.org/zh-cn/3/",
                "PEP 8风格指南：https://peps.python.org/pep-0008/",
                "Real Python教程：https://realpython.com/",
                "Python Cookbook：https://docs.python.org/3/library/cookbook.html",
                "Effective Python：https://effectivepython.com/"
            ],
            "sop": {
                "title": "Python开发实战SOP",
                "phases": [
                    {
                        "name": "Phase 0: 环境准备",
                        "steps": [
                            "创建虚拟环境：python -m venv venv",
                            "激活虚拟环境：source venv/bin/activate",
                            "安装依赖：pip install -r requirements.txt",
                            "配置IDE：安装Python插件，配置解释器"
                        ]
                    },
                    {
                        "name": "Phase 1: 代码开发",
                        "steps": [
                            "编写代码，遵循PEP 8规范",
                            "添加类型注解，提高可读性",
                            "编写docstring，说明函数用途",
                            "使用单元测试，验证功能"
                        ]
                    },
                    {
                        "name": "Phase 2: 代码审查",
                        "steps": [
                            "运行black格式化代码",
                            "运行mypy类型检查",
                            "运行pytest单元测试",
                            "检查代码覆盖率"
                        ]
                    },
                    {
                        "name": "Phase 3: 性能优化",
                        "steps": [
                            "使用cProfile分析性能瓶颈",
                            "优化算法和数据结构",
                            "添加缓存，减少重复计算",
                            "使用并发，提升处理速度"
                        ]
                    },
                    {
                        "name": "Phase 4: 部署上线",
                        "steps": [
                            "编写Dockerfile，容器化应用",
                            "配置CI/CD流水线",
                            "配置日志和监控",
                            "部署到生产环境"
                        ]
                    }
                ]
            }
        },
        # 其他主题的内容结构类似，这里省略...
        "Docker容器化部署指南": {
            "intro": "Docker通过容器化技术实现了应用的轻量级虚拟化，让应用在任何环境中都能一致运行。本文将详细介绍Docker的核心概念、镜像构建、容器管理、网络配置以及生产环境部署的最佳实践。",
            "overview": "Docker是现代应用部署的标准工具，它解决了'在我的机器上能运行'的问题。通过容器化，应用及其依赖被打包成镜像，可以在任何支持Docker的环境中运行。本文将从基础到高级，全面介绍Docker的使用技巧。",
            "chapters": {
                "第一章 认识Docker": {
                    "sections": [
                        {
                            "title": "1.1 Docker的本质",
                            "content": "Docker不是虚拟机，而是容器化技术。容器共享宿主机内核，比虚拟机更轻量。核心认知：从'手动部署'到'容器化部署'的转变。"
                        },
                        {
                            "title": "1.2 与虚拟机的核心区别",
                            "content": "Docker vs VM：Docker共享内核，VM有独立内核；Docker启动快，VM启动慢；Docker资源占用少，VM资源占用多。"
                        },
                        {
                            "title": "1.3 Docker能力全景",
                            "content": "镜像构建：Dockerfile、多阶段构建。容器管理：运行、停止、删除。网络配置：bridge、host、none。数据持久化：Volume、Bind Mount。"
                        }
                    ]
                },
                "第二章 核心概念": {
                    "sections": [
                        {
                            "title": "2.1 镜像与容器",
                            "content": "镜像：只读的应用模板。容器：镜像的运行实例。镜像分层：共享基础层，减少存储。"
                        },
                        {
                            "title": "2.2 Dockerfile",
                            "content": "FROM：指定基础镜像。RUN：执行命令。COPY/ADD：复制文件。CMD/ENTRYPOINT：启动命令。"
                        },
                        {
                            "title": "2.3 Docker Compose",
                            "content": "多容器编排。服务定义。网络配置。数据卷管理。"
                        }
                    ]
                },
                "第三章 镜像构建优化": {
                    "sections": [
                        {
                            "title": "3.1 多阶段构建",
                            "content": "分离构建和运行环境。减小镜像体积。提高安全性。"
                        },
                        {
                            "title": "3.2 层缓存优化",
                            "content": "利用Docker层缓存。优化Dockerfile顺序。减少不必要的层。"
                        },
                        {
                            "title": "3.3 镜像体积优化",
                            "content": "使用alpine基础镜像。清理缓存文件。合并RUN命令。"
                        }
                    ]
                },
                "第四章 容器管理": {
                    "sections": [
                        {
                            "title": "4.1 容器生命周期",
                            "content": "创建：docker run。启动：docker start。停止：docker stop。删除：docker rm。"
                        },
                        {
                            "title": "4.2 资源限制",
                            "content": "CPU限制：--cpus。内存限制：--memory。磁盘限制：--storage-opt。"
                        },
                        {
                            "title": "4.3 健康检查",
                            "content": "HEALTHCHECK指令。健康检查端点。自动重启策略。"
                        }
                    ]
                },
                "第五章 实战案例与SOP": {
                    "sections": [
                        {
                            "title": "5.1 实战案例：Web应用容器化",
                            "content": "场景：Flask应用容器化。方案：多阶段构建+Nginx。步骤：1. 构建应用镜像；2. 配置Nginx；3. 使用Docker Compose编排。"
                        },
                        {
                            "title": "5.2 实战案例：微服务部署",
                            "content": "场景：多个微服务部署。方案：Docker Compose+网络。步骤：1. 定义服务；2. 配置网络；3. 启动服务。"
                        },
                        {
                            "title": "5.3 实战SOP：Docker部署清单",
                            "content": "镜像构建：使用多阶段构建。安全：使用非root用户。健康检查：配置HEALTHCHECK。日志：配置日志驱动。监控：配置监控指标。"
                        }
                    ]
                }
            },
            "concepts": {
                "核心概念": [
                    "镜像 - 只读的应用模板，包含运行所需的一切",
                    "容器 - 镜像的运行实例，相互隔离",
                    "Dockerfile - 构建镜像的脚本文件",
                    "Docker Compose - 多容器编排工具"
                ],
                "关键术语": [
                    "Layer - 镜像的分层结构，共享基础层",
                    "Volume - 数据卷，持久化存储",
                    "Network - 容器网络，容器间通信",
                    "Registry - 镜像仓库，如Docker Hub"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用多阶段构建减小镜像体积",
                    "在.dockerignore中排除不必要的文件",
                    "使用非root用户运行容器，提升安全性",
                    "使用健康检查确保容器正常运行"
                ],
                "高级技巧": [
                    "使用Docker Compose编排多容器应用",
                    "配置自定义网络实现容器间通信",
                    "使用Volume实现数据持久化和共享",
                    "使用Secret和Config管理敏感信息"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "每个容器只运行一个进程，保持简单",
                    "使用官方基础镜像，定期更新安全补丁",
                    "镜像标签使用语义化版本，避免使用latest",
                    "编写详细的Dockerfile注释，便于维护"
                ],
                "部署策略": [
                    "使用CI/CD自动构建和推送镜像",
                    "配置资源限制（CPU、内存），防止资源耗尽",
                    "使用日志驱动收集容器日志",
                    "配置自动重启策略，保证服务可用性"
                ]
            },
            "comparison_tables": [
                {
                    "title": "Docker vs 虚拟机对比",
                    "headers": ["特性", "Docker", "虚拟机"],
                    "rows": [
                        ["启动速度", "秒级", "分钟级"],
                        ["资源占用", "MB级", "GB级"],
                        ["隔离性", "进程级", "系统级"],
                        ["性能", "接近原生", "有损耗"],
                        ["适用场景", "应用部署", "完整系统"]
                    ]
                },
                {
                    "title": "Docker网络模式对比",
                    "headers": ["网络模式", "特点", "适用场景"],
                    "rows": [
                        ["bridge", "默认模式，容器间隔离", "单机多容器"],
                        ["host", "共享宿主机网络", "高性能需求"],
                        ["none", "无网络", "完全隔离"],
                        ["overlay", "跨主机网络", "集群部署"]
                    ]
                }
            ],
            "code_examples": [
                {
                    "title": "Dockerfile最佳实践示例",
                    "code": '''# Dockerfile最佳实践示例

# 多阶段构建示例
# 第一阶段：构建
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖到临时目录
RUN pip install --user --no-cache-dir -r requirements.txt

# 第二阶段：运行
FROM python:3.11-slim

WORKDIR /app

# 从构建阶段复制依赖
COPY --from=builder /root/.local /root/.local

# 确保PATH包含用户安装的包
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \\
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

---
# docker-compose.yml示例
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge'''
                }
            ],
            "faq": [
                {
                    "question": "如何减小Docker镜像体积？",
                    "answer": "1. 使用alpine等轻量级基础镜像；2. 多阶段构建，只保留运行时需要的文件；3. 在RUN命令后清理缓存（apt-get clean）；4. 使用.dockerignore排除不必要的文件；5. 合并RUN命令减少层数。"
                },
                {
                    "question": "容器内数据会丢失吗？",
                    "answer": "是的，容器删除后数据会丢失。解决方案：1. 使用Volume或Bind Mount挂载宿主机目录；2. 使用数据卷容器；3. 对于数据库等重要数据，定期备份到宿主机或云存储。"
                }
            ],
            "references": [
                "Docker官方文档：https://docs.docker.com/",
                "Docker Hub：https://hub.docker.com/",
                "Docker Compose文档：https://docs.docker.com/compose/"
            ],
            "sop": {
                "title": "Docker部署实战SOP",
                "phases": [
                    {
                        "name": "Phase 0: 镜像构建",
                        "steps": [
                            "编写Dockerfile，使用多阶段构建",
                            "配置.dockerignore，排除不必要文件",
                            "构建镜像：docker build -t app:latest .",
                            "测试镜像：docker run --rm app:latest"
                        ]
                    },
                    {
                        "name": "Phase 1: 容器配置",
                        "steps": [
                            "配置资源限制：--cpus、--memory",
                            "配置健康检查：HEALTHCHECK",
                            "配置日志驱动：--log-driver",
                            "配置重启策略：--restart"
                        ]
                    },
                    {
                        "name": "Phase 2: 网络配置",
                        "steps": [
                            "创建自定义网络：docker network create",
                            "配置服务间通信",
                            "配置端口映射：-p",
                            "配置环境变量：-e"
                        ]
                    },
                    {
                        "name": "Phase 3: 数据持久化",
                        "steps": [
                            "创建数据卷：docker volume create",
                            "挂载数据卷：-v",
                            "配置备份策略",
                            "测试数据恢复"
                        ]
                    },
                    {
                        "name": "Phase 4: 部署上线",
                        "steps": [
                            "推送到镜像仓库：docker push",
                            "配置CI/CD流水线",
                            "配置监控告警",
                            "部署到生产环境"
                        ]
                    }
                ]
            }
        }
        # 其他主题的内容结构类似，这里省略...
    }

    return content_map.get(topic, None)

def generate_chapter_html(chapters):
    """生成章节HTML"""
    html = ""
    for chapter_name, chapter_data in chapters.items():
        html += f'            <h2>{chapter_name}</h2>\n\n'
        for section in chapter_data["sections"]:
            html += f'            <h3>{section["title"]}</h3>\n'
            html += f'            <p>{section["content"]}</p>\n\n'
    return html

def generate_comparison_table_html(tables):
    """生成对比表格HTML"""
    html = ""
    for table in tables:
        html += f'            <h3>{table["title"]}</h3>\n'
        html += '            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">\n'
        html += '                <thead>\n'
        html += '                    <tr style="background: #667eea; color: white;">\n'
        for header in table["headers"]:
            html += f'                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">{header}</th>\n'
        html += '                    </tr>\n'
        html += '                </thead>\n'
        html += '                <tbody>\n'
        for row in table["rows"]:
            html += '                    <tr>\n'
            for cell in row:
                html += f'                        <td style="padding: 12px; border: 1px solid #ddd;">{cell}</td>\n'
            html += '                    </tr>\n'
        html += '                </tbody>\n'
        html += '            </table>\n\n'
    return html

def generate_code_example_html(examples):
    """生成代码示例HTML"""
    html = ""
    for i, example in enumerate(examples, 1):
        html += f'            <h3>代码示例 {i}: {example["title"]}</h3>\n'
        html += '            <pre><code>' + example["code"] + '</code></pre>\n\n'
    return html

def generate_faq_html(faq_list):
    """生成FAQ HTML"""
    html = ""
    for i, faq in enumerate(faq_list, 1):
        html += f'            <h3>常见问题 {i}: {faq["question"]}</h3>\n'
        html += f'            <p><strong>问题：</strong>{faq["question"]}</p>\n'
        html += f'            <p><strong>答案：</strong>{faq["answer"]}</p>\n\n'
    return html

def generate_sop_html(sop):
    """生成SOP HTML"""
    html = f'            <h2>{sop["title"]}</h2>\n\n'
    for i, phase in enumerate(sop["phases"], 1):
        html += f'            <h3>阶段 {i}: {phase["name"]}</h3>\n'
        html += '            <ol>\n'
        for step in phase["steps"]:
            html += f'                <li>{step}</li>\n'
        html += '            </ol>\n\n'
    return html

def step_1_generate_html(topic):
    """第1步：生成HTML文档（优化版）"""
    logger.log(f"📝 步骤 1/3: 生成HTML文档")

    try:
        today = datetime.now().strftime("%Y%m%d")
        today_str = datetime.now().strftime("%Y年%m月%d日")
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")

        # 获取主题内容
        content = get_topic_content(topic)
        if not content:
            logger.log(f"❌ 未找到主题内容: {topic}")
            return None

        # 生成章节HTML
        chapters_html = generate_chapter_html(content.get("chapters", {}))

        # 生成对比表格HTML
        comparison_html = generate_comparison_table_html(content.get("comparison_tables", []))

        # 生成代码示例HTML
        code_examples_html = generate_code_example_html(content.get("code_examples", []))

        # 生成FAQ HTML
        faq_html = generate_faq_html(content.get("faq", []))

        # 生成SOP HTML
        sop_html = generate_sop_html(content.get("sop", {}))

        # 生成HTML内容
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} - {today_str} | 技术文档</title>
    <meta name="description" content="{topic} - 完整的技术指南和最佳实践">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --container-bg: white;
            --text-color: #333;
            --nav-bg: white;
            --nav-text: #333;
            --border-color: rgba(0,0,0,0.1);
        }}

        .dark-mode {{
            --bg-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            --container-bg: #1a1a2e;
            --text-color: #e0e0e0;
            --nav-bg: #1f1f38;
            --nav-text: #e0e0e0;
            --border-color: rgba(255,255,255,0.1);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            padding: 20px;
            color: var(--text-color);
            transition: background 0.3s, color 0.3s;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: var(--container-bg);
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            transition: background 0.3s, color 0.3s;
        }}

        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background: var(--nav-bg);
            border-bottom: 1px solid var(--border-color);
            transition: background 0.3s, color 0.3s;
        }}

        .navbar-brand {{
            font-size: 1.5em;
            font-weight: bold;
            color: var(--nav-text);
            text-decoration: none;
            transition: color 0.3s;
        }}

        .nav-links {{
            display: flex;
            gap: 20px;
            list-style: none;
        }}

        .nav-links a {{
            color: var(--nav-text);
            text-decoration: none;
            transition: color 0.3s;
        }}

        .nav-links a:hover {{
            color: #667eea;
        }}

        .content {{
            padding: 40px 30px;
        }}

        .content h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: var(--text-color);
        }}

        .date {{
            font-size: 1.2em;
            color: #667eea;
            margin-bottom: 30px;
        }}

        .content h2 {{
            font-size: 1.8em;
            margin: 30px 0 15px 0;
            color: var(--text-color);
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}

        .content h3 {{
            font-size: 1.4em;
            margin: 20px 0 10px 0;
            color: var(--text-color);
        }}

        .content p {{
            line-height: 1.8;
            margin-bottom: 15px;
            color: var(--text-color);
        }}

        .content ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}

        .content li {{
            margin-bottom: 10px;
            color: var(--text-color);
        }}

        .content ol {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}

        .content pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 15px;
        }}

        .content pre code {{
            background: none;
            padding: 0;
        }}

        .dark-mode-toggle {{
            cursor: pointer;
            padding: 10px 15px;
            background: #e8f4f8;
            border: none;
            border-radius: 8px;
            color: #1976d2;
            font-size: 1em;
            transition: background 0.3s, color 0.3s;
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        footer {{
            background: var(--nav-bg);
            padding: 20px 30px;
            text-align: center;
            color: var(--nav-text);
            border-top: 1px solid var(--border-color);
        }}

        @media (max-width: 768px) {{
            .navbar {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="navbar">
            <a href="../../index.html" class="navbar-brand">📚 技术文档</a>
            <ul class="nav-links">
                <li><a href="../../index.html">首页</a></li>
                <li><a href="../../history.html">历史</a></li>
                <li><a href="../../about.html">关于</a></li>
                <li><a href="../../contact.html">联系</a></li>
            </ul>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">🌙</button>
        </nav>

        <div class="content">
            <a href="../index.html" class="back-link">← 返回月份列表</a>

            <h1>{topic}</h1>
            <div class="date">{today_str} · 技术文档</div>

            <h2>概述</h2>
            <p>{content.get('overview', content.get('intro', ''))}</p>

{chapters_html}
            <h2>核心概念</h2>

            <p>了解{topic}的基本概念是掌握该技术的基础。本节将介绍核心概念和关键术语。</p>

            <h3>核心概念</h3>
            <ul>
'''

        # 添加核心概念
        for concept in content['concepts']['核心概念']:
            html_content += f'                <li>{concept}</li>\n'

        html_content += '''            </ul>

            <h3>关键术语</h3>
            <ul>
'''

        # 添加关键术语
        for term in content['concepts']['关键术语']:
            html_content += f'                <li>{term}</li>\n'

        html_content += '''            </ul>

            <h2>实践技巧</h2>

            <p>掌握{topic}的实践技巧可以帮助您更好地应用该技术。</p>

            <h3>基础技巧</h3>
            <ul>
'''

        # 添加基础技巧
        for tip in content['practices']['基础技巧']:
            html_content += f'                <li>{tip}</li>\n'

        html_content += '''            </ul>

            <h3>高级技巧</h3>
            <ul>
'''

        # 添加高级技巧
        for tip in content['practices']['高级技巧']:
            html_content += f'                <li>{tip}</li>\n'

        html_content += '''            </ul>

            <h2>最佳实践</h2>

            <p>遵循{topic}的最佳实践可以确保项目的成功和可维护性。</p>

            <h3>开发规范</h3>
            <ul>
'''

        # 添加开发规范
        for practice in content['best_practices']['开发规范']:
            html_content += f'                <li>{practice}</li>\n'

        html_content += '''            </ul>

            <h3>部署策略</h3>
            <ul>
'''

        # 添加部署策略
        for strategy in content['best_practices']['部署策略']:
            html_content += f'                <li>{strategy}</li>\n'

        html_content += '''            </ul>
'''

        # 添加对比表格
        html_content += comparison_html

        # 添加代码示例
        html_content += f'''            <h2>代码示例</h2>

            <p>以下是一些{topic}的代码示例，帮助您更好地理解和应用。</p>

{code_examples_html}'''

        # 添加FAQ
        html_content += f'''            <h2>常见问题</h2>

{faq_html}'''

        # 添加SOP
        html_content += sop_html

        # 添加总结
        html_content += f'''            <h2>总结</h2>

            <p>通过本文的学习，您应该对{topic}有了更深入的理解。掌握这些知识和技巧，可以帮助您在实际项目中更好地应用{topic}。</p>

            <h2>参考资料</h2>

            <ul>
'''

        # 添加参考资料
        for ref in content['references']:
            html_content += f'                <li>{ref}</li>\n'

        html_content += '''            </ul>
        </div>

        <footer>
            <p>&copy; 2026 技术文档 | GitHub Pages</p>
        </footer>
    </div>

    <script>
        function toggleDarkMode() {{
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        }}

        if (localStorage.getItem('darkMode') === 'true') {{
            document.body.classList.add('dark-mode');
        }}
    </script>
</body>
</html>'''

        # 替换所有{topic}变量
        html_content = html_content.replace('{topic}', topic)

        # 保存HTML文件
        output_path = Path(BLOG_PATH) / f"history/{year}/{month}/{today}.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.log(f"✅ HTML文档已生成: {output_path}")
        return str(output_path)

    except Exception as e:
        logger.log(f"❌ HTML生成失败: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return None

def step_2_generate_image(topic, seed=101, max_retries=2):
    """第2步：生成图片（参考环球新闻的图片生成逻辑）"""
    logger.log(f"🎨 步骤 2/3: 生成图片")
    logger.log(f"📊 质量标准: 文件200KB-800KB, 分辨率≥1280x720, 比例16:9")

    try:
        results = []
        genai_script = Path("/home/swg/.openclaw/workspace/skills/nvidia-genai/generate.py")

        # 生成提示词（参考环球新闻的提示词）
        prompt = f"超高清真实技术文档封面，{topic}，8K分辨率，专业技术摄影，极致清晰，锐利细节，真实光线，自然色彩，电影级构图，科技感，现代感，专业镜头，景深效果，真实场景，无卡通，无插画，照片级质量，技术文档风格，专业摄影标准"

        # 图片文件名
        image_file = IMAGES_DIR / f"tech_{seed}.png"

        success = False
        retry_count = 0

        while not success and retry_count <= max_retries:
            try:
                logger.log(f"🖼️  生成图片: {topic[:30]}... (尝试 {retry_count + 1})")

                result = subprocess.run(
                    ["python3", str(genai_script), prompt,
                     "--model", "stabilityai/stable-diffusion-3-medium",
                     "--ratio", "16:9",
                     "--steps", "50",  # 提高到50步，增强细节
                     "--cfg", "7.5",  # 提高CFG值，增强提示词遵循度
                     "--seed", str(seed + retry_count * 100),
                     "--output", str(image_file)],
                    capture_output=True,
                    text=True,
                    timeout=240,  # 增加超时时间
                    env={**os.environ, "NVIDIA_API_KEY": NVIDIA_API_KEY}
                )

                if result.returncode == 0 and image_file.exists():
                    # 检查图片质量
                    quality_ok = check_image_quality(image_file)
                    if quality_ok:
                        logger.log(f"✅ 图片生成成功且质量合格")
                        results.append(str(image_file))
                        success = True
                    else:
                        if retry_count < max_retries:
                            logger.log(f"⚠️  图片质量不达标，重新生成...")
                            retry_count += 1
                            image_file.unlink()  # 删除不合格的图片
                        else:
                            logger.log(f"⚠️  图片质量未达标但已达到最大重试次数")
                            results.append(str(image_file))
                            success = True
                else:
                    if retry_count < max_retries:
                        logger.log(f"⚠️  图片生成失败，重试...")
                        retry_count += 1
                    else:
                        logger.log(f"❌ 图片生成失败")
                        results.append(None)
                        success = True

                # 稍等避免API限流
                if not success:
                    time.sleep(3)

            except subprocess.TimeoutExpired:
                if retry_count < max_retries:
                    logger.log(f"⚠️  图片生成超时，重试...")
                    retry_count += 1
                else:
                    logger.log(f"❌ 图片生成超时")
                    results.append(None)
                    success = True
            except Exception as e:
                if retry_count < max_retries:
                    logger.log(f"⚠️  图片生成异常: {str(e)}，重试...")
                    retry_count += 1
                else:
                    logger.log(f"❌ 图片生成最终失败")
                    results.append(None)
                    success = True

        return results[0] if results else None
    except Exception as e:
        logger.log(f"❌ 图片生成异常: {str(e)}")
        return None

def check_image_quality(image_path):
    """检查图片质量是否达标（参考环球新闻的质量检查）"""
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size
            file_size_kb = os.path.getsize(image_path) / 1024

            # 质量标准
            min_size_kb = 200
            max_size_kb = 800
            min_width = 1280
            min_height = 720
            target_ratio = 16/9
            ratio_tolerance = 0.1

            ratio = width / height
            ratio_diff = abs(ratio - target_ratio) / target_ratio

            # 检查各项指标
            size_ok = min_size_kb <= file_size_kb <= max_size_kb
            resolution_ok = width >= min_width and height >= min_height
            ratio_ok = ratio_diff <= ratio_tolerance

            return size_ok and resolution_ok and ratio_ok
    except:
        return False

def step_3_update_index(topic, image_file):
    """第3步：更新首页"""
    logger.log(f"🔄 步骤 3/3: 更新首页")

    try:
        today_str = datetime.now().strftime("%Y年%m月%d日")
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")
        today = datetime.now().strftime("%Y%m%d")

        # 获取主题内容
        content = get_topic_content(topic)
        if not content:
            logger.log(f"❌ 未找到主题内容: {topic}")
            return False

        # 读取首页
        index_path = Path(BLOG_PATH) / "index.html"
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()

        # 提取今日推荐部分
        image_path = f"images/{Path(image_file).name}" if image_file else "images/tech_default.png"

        # 生成要点列表
        points_html = ""
        for i, point in enumerate(content['practices']['基础技巧'][:3], 1):
            points_html += f'                    <li>{point}</li>\n'

        today_section = f'''            <h2>今日推荐-{today_str}</h2>

            <div style="background: linear-gradient(145deg, #f6f8fa 0%, #ffffff 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 2px solid #667eea;">
                <img src="{image_path}" alt="{topic}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #667eea; margin-bottom: 15px; font-size: 1.5em;">{topic}</h3>
                <p style="margin-bottom: 15px;">{content['intro']}</p>
                <p style="margin-bottom: 15px;"><strong>主要内容：</strong></p>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
{points_html}                </ul>
                <a href="history/{year}/{month}/{today}.html" style="color: #667eea; font-weight: bold;">阅读完整文章 →</a>
            </div>'''

        # 查找并替换今日推荐部分
        pattern = r'<h2>今日推荐-.*?</h2>.*?<h2>历史存档</h2>'
        replacement = today_section + '\n\n            <h2>历史存档</h2>'

        new_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

        # 写回
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        logger.log("✅ 首页已更新")
        return True

    except Exception as e:
        logger.log(f"❌ 首页更新失败: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return False

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="技术文档自动更新（优化版）")
    parser.add_argument("--no-upload", action="store_true", help="不上传，仅生成")
    parser.add_argument("--seed", type=int, default=101, help="图片随机种子")

    args = parser.parse_args()

    try:
        logger.log("=" * 60)
        logger.log("📝 技术文档自动更新（优化版）")
        logger.log(f"📅 日期: {datetime.now().strftime('%Y年%m月%d日')}")
        logger.log("=" * 60)

        # 获取技术主题
        topic = get_tech_topic()
        logger.log(f"🎯 主题: {topic}")

        # 第1步：生成HTML文档
        html_file = step_1_generate_html(topic)
        if not html_file:
            return 1

        # 第2步：生成图片
        image_file = step_2_generate_image(topic, args.seed)

        # 第3步：更新首页
        success = step_3_update_index(topic, image_file)
        if not success:
            return 1

        # Git提交
        if not args.no_upload:
            logger.log("📝 正在提交到Git...")

            result = subprocess.run(
                ["git", "add", "."],
                cwd=BLOG_PATH,
                capture_output=True,
                text=True
            )

            result = subprocess.run(
                ["git", "commit", "-m", f"Auto: 技术文档自动更新（优化版） - {datetime.now().strftime('%Y年%m月%d日')}\n\n- 主题: {topic}\n- 生成详细技术文档\n- 生成封面图片\n- 更新首页推荐\n- 包含章节、实战案例、表格对比、代码示例、FAQ、SOP"],
                cwd=BLOG_PATH,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.log("✅ Git提交成功")

                # 推送到GitHub
                result = subprocess.run(
                    ["git", "push"],
                    cwd=BLOG_PATH,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    logger.log("✅ 推送到GitHub成功")
                else:
                    logger.log("⚠️  推送到GitHub失败")
            else:
                logger.log("⚠️  没有新的更改需要提交")

        logger.log("=" * 60)
        logger.log("✅ 技术文档自动更新完成！")
        logger.log(f"📅 日期: {datetime.now().strftime('%Y年%m月%d日')}")
        logger.log(f"🎯 主题: {topic}")
        logger.log(f"🖼️  图片: {'✅ 已生成' if image_file else '❌ 生成失败'}")
        logger.log("=" * 60)

        return 0

    except Exception as e:
        logger.log(f"❌ 错误: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
