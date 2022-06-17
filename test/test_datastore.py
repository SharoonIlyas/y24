import os
import pathlib

import pytest

from y24 import DataStore, load_json_file, write_to_json_file

path_test = f'{pathlib.Path(__file__).parent.resolve()}/files/test.json'
path_test_sample = f'{pathlib.Path(__file__).parent.resolve()}/files/sample_set.json'


class TestDataStore:
    """test cases to test datastore functionalities"""

    def test_load_to_json(self):
        dict_obj = {
            "first": 12,
            "second": "2",
            "third": 12,
            "fourth": 13,
            "fifth": 12
        }
        loaded_dict = load_json_file(path_test_sample)
        assert loaded_dict == dict_obj

    def test_write_to_json(self):
        dict_obj = {
            'first': 12,
            'second': 'string'
        }
        write_to_json_file(f'{pathlib.Path(__file__).parent.resolve()}/test_2.json', dict_obj)
        path_test2 = f'{pathlib.Path(__file__).parent.resolve()}/test_2.json'
        loaded_dict = load_json_file(path_test2)
        assert dict_obj == loaded_dict
        if os.path.exists(path_test2):
            os.remove(path_test2)

    @pytest.fixture
    def datastore_instance(self):
        data_store = DataStore(path_test)
        dict_obj = {
            "first": 12,
            "second": "2",
            "third": 12,
            "fourth": 13,
            "fifth": 12
        }
        write_to_json_file(path_test, dict_obj)
        return data_store

    def test_insert(self, datastore_instance):
        datastore_instance.insert('six', 6)
        assert {'six': 6} == datastore_instance.query(6, limit=1, offset=0)
        dict_obj = {
            "first": 12,
            "second": "2",
            "third": 12,
            "fourth": 13,
            "fifth": 12,
            "six": 6
        }
        assert load_json_file(path_test) == dict_obj

    def test_batch_insert(self, datastore_instance):
        datastore_instance.batch_insert([('seven', 7), ('eight', 8)])
        dict_obj = {
            "first": 12,
            "second": "2",
            "third": 12,
            "fourth": 13,
            "fifth": 12,
            "six": 6,
            "seven": 7,
            "eight": 8
        }
        assert load_json_file(path_test) == dict_obj

    def test_delete(self, datastore_instance):
        datastore_instance.delete('first')
        dict_obj = {
            "second": "2",
            "third": 12,
            "fourth": 13,
            "fifth": 12,
            "six": 6,
            "seven": 7,
            "eight": 8

        }
        assert load_json_file(path_test) == dict_obj

    def test_delete_not_exist(self, datastore_instance):
        with pytest.raises(KeyError):
            datastore_instance.delete('first')

    def test_update_non_exist(self, datastore_instance):
        with pytest.raises(KeyError):
            datastore_instance.update('eight', 88)

    def test_update_exist(self, datastore_instance):
        datastore_instance.update('second', 2)
        updated_file_dict = load_json_file(path_test)
        dict_obj_updated = {
            "first": 12,
            "second": 2,
            "third": 12,
            "fourth": 13,
            "fifth": 12
        }
        datastore_instance.update('second', "2")
        assert dict_obj_updated == updated_file_dict

    def test_get_all(self, datastore_instance):
        assert datastore_instance.get_all(1, 0) == {"first": 12}
        assert datastore_instance.get_all(2, 0) == {"first": 12, "second": "2", }
        assert datastore_instance.get_all(1, 1) == {"second": "2", }
        assert datastore_instance.get_all(0, 1) == {}

    def test_query(self, datastore_instance):
        assert datastore_instance.query(12, 1, 0) == {"first": 12}
        assert datastore_instance.query(12, 3, 0) == {"first": 12, "third": 12, "fifth": 12}
        assert datastore_instance.query(12, 4, 0) == {"first": 12, "third": 12, "fifth": 12}
        assert datastore_instance.query(12, 2, 0) == {"first": 12, "third": 12}
        assert datastore_instance.query(12, 1, 1) == {"third": 12}
        assert datastore_instance.query(12, 2, 1) == {"third": 12, 'fifth': 12}
        assert datastore_instance.query(12, 2, 2) == {'fifth': 12}
        assert datastore_instance.query(12, 2, 4) == {}
