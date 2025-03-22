# Note. Color Final Vars
class Color:
    RED = "\033[31m"
    ORANGE = "\033[38:5:208m"
    GREEN = "\033[32m"
    YELLOW = "\033[38:5:226m"
    DEFAULT = "\033[0m"

    @classmethod
    def colorize_bool(cls, v):
        return f"{cls.GREEN}{v}{cls.DEFAULT}" if v else f"{cls.RED}{v}{cls.DEFAULT}"
