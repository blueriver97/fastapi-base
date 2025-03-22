from enum import Enum, auto


class StrEnum(str, Enum):
    @classmethod
    def _generate_next_value_(cls, name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class FallbackType(StrEnum):
    INIT_FAIL = auto()
    FINAL_FAIL = auto()
    PLUGIN_LOAD_FAIL = auto()
    SOCK_CONN_FAIL = auto()
    REQUEST_FAIL = auto()
    TRANSACTION_FAIL = auto()
    VALID_DATA_FAIL = auto()
    UNDEFINED_FAIL = auto()
