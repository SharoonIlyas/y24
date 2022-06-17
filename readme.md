# y24 Python Library

- Minimum Python Version(3.10)

# Stack

Simple implementation of Stack datastructure in Python

### initialization

    stack = Stack()

### size()

return the size of the stack.

      stack.size()

### peek

return the last entered element in the stack or raise an exception if the stack is empty.

      stack.peek()

### pop

return the last entered element in the stack or raise an exception if the stack is empty.

      stack.pop()

### clear

deletes all elements in the stack.

      stack.pop()

### push

add an element to the stack or raise an exception if the element is None.

      stack.push(element)

# DataStore

Stores key value pair in the structured file. The file can be stored in various types.

### initialization

    data_store=DataStore()

### insert

Raise KeyError if the key already has been used, or insert the key value in the datastore

    data_store.insert(key,value)

### batch_insert

Takes a list of key,value tuples and perform the same functionality as insert method onto each element.

    data_store.batch_insert([(key,value),(key,value)])

### update

Raises Key error is the key does not exist and updated the value if key exist

    data_store.update(key, new_value)

### query

DataStore can be filtered with this, it takes the value, matches that value with the values of all the keys and
returns the object. Limit and offset can also be provided for pagination.
Returns Empty dictionary object, if the filtered values not found.

    data_store.query(value, limit, offset)

### get_all

It returns all the key values. Limit and offset can also be provided for pagination.

    data_store.get_all(value, limit, offset)

# Test

To perform the test, please install the libraries in the requirements.txt file

### command

run the following command in the project root directory

    pytest





