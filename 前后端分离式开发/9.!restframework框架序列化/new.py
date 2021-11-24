class Foo(object):
    def __init__(self, a1):
        self.a = a1

    def __new__(cls, *args, **kwargs):
        """
        根据类创建对象，并返回.
        new方法返回了什么，就执行什么的构造方法__init__
        """
        # return 'xxx'
        return object.__new__(cls)  # 创建一个类对象


obj = Foo(123)
print(obj)  # xxx
