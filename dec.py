from functools import wraps

class magic:
    def __init__(self):
        self.functions = {}

    def dec(self, name):
        def decorator(func):
            self.functions[name] = func
            @wraps(func)
            def wrapper():
                # Wrapper Code
                func()
            return(wrapper)
        return(decorator)

    def run(self):
        self.functions["Init"]()
        self.functions["View"]()
 

