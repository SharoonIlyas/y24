import pytest

from y24 import Stack, EmptyStackException


class TestStack:
    """test cases to test stack functionalities"""

    @pytest.fixture
    def stack_instance(self):
        stack = Stack()
        return stack

    def test_push(self, stack_instance):
        stack_instance.push(1)
        assert 1 == stack_instance.peek

    def test_none_push(self, stack_instance):
        with pytest.raises(EmptyStackException):
            stack_instance.push(None)

    def test_peek(self, stack_instance):
        stack_instance.push(1)
        assert False == stack_instance.empty

    def test_peek_empty(self, stack_instance):
        stack_instance.clear()
        with pytest.raises(EmptyStackException):
            stack_instance.peek()

    def test_pop_empty(self, stack_instance):
        stack_instance.clear()
        with pytest.raises(EmptyStackException):
            stack_instance.pop()

    def test_pop_non_empty(self, stack_instance):
        stack_instance.push(1)
        stack_instance.push(2)
        popped_element = stack_instance.pop()
        assert 2 == popped_element

    def test_clear(self, stack_instance):
        stack_instance.clear()
        assert stack_instance.empty == True
