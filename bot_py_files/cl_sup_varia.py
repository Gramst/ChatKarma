class PrintSearchinDict():

    def print_income(self, income, **kwargs ):
        indent = kwargs.get('indent', 0)
        res = kwargs.get("res", '')
        search = kwargs.get("search", False)
        spacer_begin = ''
        spacer_end = '\n'

        if isinstance(income, dict):
            spacer_begin = '\n' + ' '*indent + '{' + '\n'
            spacer_end = '\n' + ' '*indent + '}' + '\n'
        elif isinstance(income, list):
            spacer_begin = '\n' + ' '*indent + '[' + '\n'
            spacer_end = '\n' + ' '*indent + ']' + '\n'
        
        temp = spacer_begin 

        if isinstance(income, dict):
            for i in income:
                temp += (' '*indent + str(i) + ' : ') 
                temp += self.print_income(income[i], indent=(indent+2), search=search)
                
        elif isinstance(income, list):
            for i in income:
                temp += self.print_income(i, indent=(indent+2), search=search)
        else:
            temp += str(' '*indent + str(income))

        temp += spacer_end

        if search:
            if search in temp:
                res += temp
                return res 
            else:
                temp = ''
        
        res += temp
        return res


######################################################
#
#
#
######################################################



class Cashe():

    def __init__(self):
        self._cashe = {}

    def decorator_with_args(decorator_to_enhance):
        def decorator_maker(*args, **kwargs):
            def decorator_wrapper(func):
                return decorator_to_enhance(func, *args, **kwargs)
            return decorator_wrapper
        return decorator_maker

    @staticmethod
    @decorator_with_args
    def cashe_funct(func, *args, **kwargs):
        def wrapper(self, value=None):
            if kwargs.get('sett'):
                self._cashe[kwargs.get('name')] = func(self, value)
            else:       
                if kwargs.get('name') not in self._cashe:
                    self._cashe[kwargs.get('name')] = func(self)

            return self._cashe.get(kwargs.get('name'))
        return wrapper

    def clean_cashe(self):
        for  i in self._cashe.keys():
            self._cashe[i] = None