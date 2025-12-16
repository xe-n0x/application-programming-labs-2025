import os
import csv

class path_iterator:
    """Итератор по путям"""
    def __init__ (self, source: str) -> None:
        self.paths = []
        self.counter = 0
        if (source.endswith('.csv')):
            with open(source, mode='r', newline='', encoding='utf-8') as file:
             reader = csv.reader(file)
             next(reader)
             for row in reader:
               self.paths.append(row[0])
        else:
            for filename in os.listdir(source):
                self.paths.append(os.path.join(source,filename))

    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.counter < len (self.paths)):
            path = self.paths[self.counter]
            self.counter +=1
            return path
        else:
            self.counter = 0
            raise StopIteration