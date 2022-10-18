class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=MetaSingleton):

    def __init__(self):
       self.HELP_HUMAN_ABILITY = True
    
    def change_human_help_mode(self,is_enable):
        self.HELP_HUMAN_ABILITY = is_enable
    
    def get_human_ability(self):
        return self.HELP_HUMAN_ABILITY



# db1 = Settings()
# print(Settings().get_human_ability())
# db1.change_human_help_mode(False)
# db1.get_human_ability()

# print(Settings().get_human_ability())