from collections import Counter
class Header(Counter):
    '''like a Counter, but the the count is the number of 
        items in the counter
    '''    
    def __init__(self):
        self.count =1  
    def add(self,feature):
        feature = unicode(feature)
        if feature not in self:
            self[feature] = self.count
            self.count += 1

