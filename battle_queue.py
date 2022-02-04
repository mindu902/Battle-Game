"""
The BattleQueue classes.

A BattleQueue is a queue that lets game know in what order various 
characters are going to attack.

"""
from typing import Union, List

class BattleQueue:
    """
    A class representing a BattleQueue.
    """
    
    def __init__(self) -> None:
        """
        Initialize this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._content = []
        self._p1 = None
        self._p2 = None
    
    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.
        
        >>> bq = BattleQueue()
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq.is_empty()
        False
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)
    
    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_empty()
        False
        """
        self._content.append(character)
        
        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy
    
    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        self._clean_queue()
        
        return self._content.pop(0)
    
    def is_empty(self) -> bool:
        """
        Return whether this BattleQueue is empty (i.e. has no players or
        has no players that can perform any actions).
        
        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._clean_queue()
        
        return self._content == []
    
    def peek(self) -> 'Character':
        """
        Return the character at the front of this BattleQueue but does not
        remove them.
        
        If this BattleQueue is empty, returns the first player who was added
        to this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.peek()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        False
        """
        self._clean_queue()
        
        if self._content:
            return self._content[0]

        return self._p1
    
    def is_over(self) -> bool:
        """
        Return whether the game being carried out in this BattleQueue is over 
        or not.
        
        A game is considered over if:
            - Both players have no skills that they can use.
            - One player has 0 HP
            or
            - The BattleQueue is empty.
            
        >>> bq = BattleQueue()
        >>> bq.is_over()
        True
        
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_over()
        False
        """
        if self.is_empty():
            return True
    
        if self._p1.get_hp() == 0 or self._p2.get_hp() == 0:
            return True
        
        return False
    
    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. Otherwise, return None.
        
        >>> bq = BattleQueue()
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.get_winner()
        """
        if not self.is_over():
            return None
        
        if self._p1.get_hp() == 0:
            return self._p2
        elif self._p2.get_hp() == 0:
            return self._p1
    
        return None
    
    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = BattleQueue()
        
        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy
        
        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()
        
        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)
        
        return new_battle_queue
    
    def __repr__(self) -> str:
        """
        Return a representation of this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> from characters import Rogue
        >>> from playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        return " -> ".join([repr(character) for character in self._content])


class RestrictedBattleQueue(BattleQueue):
    """
    A class representing a RestrictedBattleQueue.
    
    Rules for a RestrictedBattleQueue:
    - The first time each character is added to the RestrictedBattleQueue,
      they're able to add.
      
    For the below, you may assume that the character at the front of the
    RestrictedBattleQueue is the one adding:
    - Characters that are added to the RestrictedBattleQueue by a character
      other than themselves cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> B
      Able to add:     Y    Y
      
      Then if A tried to add B to the RestrictedBattleQueue, it would look like:
      Character order: A -> B -> B
      Able to add:     Y    Y    N
    - Characters that have 2 copies of themselves in the RestrictedBattleQueue
      already that can add cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> A -> B
      Able to add:     Y    Y    Y
      
      Then if A tried to add themselves in, the RestrictedBattleQueue would
      look like:
      Character order: A -> A -> B -> A
      Able to add:     Y    Y    Y    N
      
      If we removed from the RestrictedBattleQueue and tried to add A in again,
      then it would look like:
      Character order: A -> B -> A -> A
      Able to add:     Y    Y    N    Y
    """

    def __init__(self):
        super().__init__()
        self._restriction_lst = []
        self._seen = {}

    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.

        """
        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

        if character not in self._seen:
            self._seen[character] = 1
            self._content.append(character)
            self._restriction_lst.append("Y")
        elif self._content and character == self._content[0]:
            if self._restriction_lst[0] == "N":
                return
            else:
                count = self._content.count(character)
                if count >= 2:
                    self._content.append(character)
                    self._restriction_lst.append("N")
                else:
                    self._content.append(character)
                    self._restriction_lst.append("Y")
        else:
            if self._restriction_lst and self._restriction_lst[0] == "N":
                return
            self._content.append(character)
            self._restriction_lst.append("N")

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        """
        self._clean_queue()
        self._restriction_lst.pop(0)
        return self._content.pop(0)

    def clear_seen(self):
        self._seen.clear()

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        """
        new_battle_queue = RestrictedBattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()
            new_battle_queue.clear_seen()

        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)

        return new_battle_queue


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='pyta.txt')
