def metest(name, bases, dict):
    print name, bases, dict
    dict['__doc__'] = """New Doc"""
    cls = type(name+"_meta", bases, dict)
    return cls

class Test(object):
    "Old doc"
    __metaclass__ = metest

print Test
print Test.__doc__

t = Test()

print t.__doc__