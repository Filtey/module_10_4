import time
import random
from queue import Queue
from threading import Thread


class Table:
    def __init__(self, numb):
        self.number = numb
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        return time.sleep(random.randint(3,10))

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            flag = False
            for table in self.tables:
                if(table.guest is None):
                    table.guest = guest
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    flag = True
                    guest.start()
                    break
            if(flag == False):
                print(f"{guest.name} в очереди") #не посадили
                self.queue.put(guest)



    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if (table.guest and not table.guest.is_alive()):
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                if (table.guest is None and not self.queue.empty()):
                    guest = self.queue.get()
                    table.guest = guest
                    guest.start()
                    print(f"{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")



# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
