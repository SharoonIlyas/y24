from y24 import DataStore

if __name__ == '__main__':
    data_store = DataStore('sample.json')
    print(data_store.get_all(limit=10, offset=0))
    print(data_store.query(value=12, limit=0, offset=0))

