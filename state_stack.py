"""

This includes the Stack, Queue, and an abstract parent class (Container)

"""
from playstyle import *

class Container:
    """
    An abstract Container class.
    """
    
    def __init__(self) -> None:
        """
        Initialize this Container.
        """
        raise NotImplementedError

    def add(self, value) -> None:
        """
        Add value this Container.
        """
        raise NotImplementedError

    def remove(self) -> object:
        """
        Remove an item from this Container.
        """
        raise NotImplementedError
    
    def is_empty(self) -> bool:
        """
        Return whether this container is empty or not (whether there's nothing
        left to remove.)
        """
        raise NotImplementedError


class StateStack(Container):
    """
    An implementation of Stack.
    """
    
    def __init__(self) -> None:
        """
        Initialize this Stack.
        
        >>> s = StateStack()
        >>> s.is_empty()
        True
        """
        self._content = []

    def add(self, value: 'State') -> None:
        """
        Add value this Stack.

        >>> from battle_queue import *
        >>> s = StateStack()
        >>> bq = BattleQueue()
        >>> state = State(1, bq)
        >>> s.add(state)
        >>> s.is_empty()
        False
        """
        self._content.append(value)

    def remove(self) -> 'State':
        """
        Remove an item from the top of this Stack.

        >>> from battle_queue import *
        >>> s = StateStack()
        >>> bq = BattleQueue()
        >>> state = State(1, bq)
        >>> s.add(state)
        >>> s.remove()
        State: 1, Score: None
        """
        return self._content.pop()
    
    def is_empty(self) -> bool:
        """
        Return whether this Stack is empty or not (whether there's nothing
        left to remove.)
        
        >>> from battle_queue import *
        >>> s = StateStack()
        >>> bq = BattleQueue()
        >>> state = State(1, bq)
        >>> s.add(state)
        >>> s.is_empty()
        False
        """
        return self._content == []

if __name__ == "__main__":
    import doctest
    doctest.testmod()