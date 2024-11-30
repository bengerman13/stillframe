from collections import deque


class Popdeque(deque):
    def append(self, x):
        popped = None
        if len(self) == self.maxlen:
            popped = self[0]
        super().append(x)
        return popped

    def appendleft(self, x):
        popped = None
        if len(self) == self.maxlen:
            popped = self[-1]
        super().appendleft(x)
        return popped

    def extend(self, x):
        did_pop = False
        popped = []
        for i in x:
            if len(self) == self.maxlen:
                did_pop = True
                popped.append(self.append(i))
            else:
                self.append(i)
        if not did_pop:
            popped = None
        return popped

    def extendleft(self, x):
        did_pop = False
        popped = []
        for i in x:
            if len(self) == self.maxlen:
                did_pop = True
                popped.append(self.appendleft(i))
            else:
                self.appendleft(i)
        if not did_pop:
            popped = None
        return popped
