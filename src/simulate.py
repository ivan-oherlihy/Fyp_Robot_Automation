
from sever import server
from task import task
from random import randint
tasks ={}

for i in range(10):
    tasks[i] = task(i,location=(randint(-10,10),randint(-10,10)),time=randint(0,10),task="work",robotsRequired=randint(1,2))
print(tasks)
s = server("localhost",5005,tasks)
s.run()
