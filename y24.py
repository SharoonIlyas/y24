import json
import threading
from dataclasses import dataclass, field
from itertools import islice
from typing import Dict, Tuple, List


@dataclass
class EmptyStackException(Exception):
    """custom error"""
    pass


@dataclass
class Stack:
    """stack root class with all the methods"""
    __stack_list: List[str | float | int | bool] = field(default_factory=lambda: [])

    @property
    def size(self) -> int:
        return len(self.__stack_list)

    @property
    def peek(self) -> str | float | int | bool:
        if len(self.__stack_list) == 0:
            raise EmptyStackException
        return self.__stack_list[-1]

    @property
    def empty(self) -> bool:
        if len(self.__stack_list) > 0:
            return False
        return True

    def push(self, element) -> None:
        if element is None:
            raise EmptyStackException
        self.__stack_list.append(element)

    def pop(self) -> str | float | int | bool | EmptyStackException:
        if len(self.__stack_list) > 0:
            element = self.__stack_list.pop()
            return element
        raise EmptyStackException

    def clear(self) -> None:
        if len(self.__stack_list) > 0:
            self.__stack_list = []


def check_value_type(key, value) -> None:
    if type(key) != str:
        raise ValueError("key must be of type string")
    if type(value) not in [str, float, bool, int]:
        raise ValueError("value must be of type string, integer, float. boolean")


def load_json_file(file: str) -> Dict[str, str | float | int | bool]:
    with open(file, "r") as json_file:
        dict_object = json.load(json_file)
        return dict_object


def write_to_json_file(file_path: str, dictionary: dict) -> None:
    json_object = json.dumps(dictionary, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_object)


@dataclass
class DataStore:
    """DataStore class with all the methods"""
    _instance = None
    _lock = threading.Lock()
    __file_path: str
    __data_object: Dict[str, str | float | int | bool] = field(
        default_factory=lambda: {})

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(DataStore, cls).__new__(cls)
        return cls._instance

    def __post_init__(self):
        self.__data_object = load_json_file(file=self.__file_path)

    def insert(self, key: str, value: str | float | int | bool) -> None:
        check_value_type(key, value)
        if self.__data_object.__contains__(key):
            raise KeyError(f"{key} already exist, if you wish to change, use update function")
        self.__data_object[key] = value
        write_to_json_file(file_path=self.__file_path, dictionary=self.__data_object)

    def batch_insert(self, key_value_lst: List[Tuple[str, str | float | int | bool]]) -> None:
        for key_value in key_value_lst:
            check_value_type(key=key_value[0], value=key_value[1])
            if self.__data_object.__contains__(key_value[0]):
                raise KeyError(f"{key_value[0]} already exist, if you wish to change, use update function")
        for key_value in key_value_lst:
            self.__data_object[key_value[0]] = key_value[1]
            write_to_json_file(file_path=self.__file_path, dictionary=self.__data_object)

    def update(self, key, value) -> None:
        if not self.__data_object.__contains__(key):
            raise KeyError(f"{key} does not exist")
        check_value_type(key, value)
        self.__data_object[key] = value
        write_to_json_file(file_path=self.__file_path, dictionary=self.__data_object)

    def delete(self, key) -> None:
        if not self.__data_object.__contains__(key):
            raise KeyError(f"{key} does not exist")
        self.__data_object.pop(key)
        write_to_json_file(file_path=self.__file_path, dictionary=self.__data_object)

    def query(self, value: str | float | int | bool, limit: int, offset: int) -> Dict[str, str | float | int | bool]:
        all_dict = {k: v for (k, v) in self.__data_object.items() if v == value}
        sliced = dict(islice(islice(all_dict.items(), offset, None), limit))
        return sliced

    def get_all(self, limit: int, offset: int) -> Dict[str, str | float | int | bool]:
        sliced = dict(islice(islice({k: v for (k, v) in self.__data_object.items()}.items(), offset, None), limit))
        return sliced
