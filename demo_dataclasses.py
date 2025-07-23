from dataclasses import dataclass, field
from datetime import datetime
from random import randint

# Демо классы просто чтобы был какой-то набор данных для демонстрации навигации по меню
# Итоговый функционал можно подогнать потом под реальные модели

@dataclass
class Warehouse:
    id: int
    address: str
    # Предполагаю, что ячейки будут стандартизованы по объему    
    number_of_1cub_m_boxes: int = 0
    number_of_2cub_m_boxes: int = 0
    number_of_3cub_m_boxes: int = 0
    number_of_4cub_m_boxes: int = 0
    
    def __post_init__(self):
        
        all_boxes = (
            self.number_of_1cub_m_boxes,
            self.number_of_2cub_m_boxes,
            self.number_of_3cub_m_boxes,
            self.number_of_4cub_m_boxes
        )
        
        self.total: int = sum(all_boxes)


@dataclass
class Box:
    id: int
    name: str
    dimensions: tuple
    address: str
    rented_from: datetime | None = None
    rented_till: datetime | None = None
    items_stored: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.volume: int = self.dimensions[0] * self.dimensions[1] * self.dimensions[2]
        self.height: int = self.dimensions[0]
        self.width: int = self.dimensions[1]
        self.length: int = self.dimensions[2]


@dataclass
class User:
    tg_id: str = ''
    phone: str = ''
    name: str = ''
    boxes_in_usage: list[Box] = field(default_factory=list)
    
    def find_box(self, id) -> Box | None:
        for box in self.boxes_in_usage:            
            if id == box.id:
                return box
        return None
    

#Имитация id в БД
def random_id():
    return randint(1, 99999)


def generate_demo_user():
    user = User(
        tg_id='12341231431234',
        phone='+79991111111',
        name='Иванов Иван Иванович',
        boxes_in_usage=get_demo_boxes()
    )
    
    return user


demouser: User = None


def get_demo_user():

    # Знаю, что так не принято делать, но это демо для данных
    # И мне надо где-то хранить пользователя, чтобы айди ячеек не менялись
    global demouser

    if not demouser:
        demouser = generate_demo_user()
    
    return demouser


def get_demo_boxes():
    boxes = [
        Box(
            id=random_id(),
            name='Ячейка №12',
            dimensions=(1, 1, 2),
            address='Склад 1',
            rented_from=datetime(year=2025, month=6, day=20),
            rented_till=datetime(year=2025, month=8, day=20),
            items_stored=['Сани', 'Лыжи', 'Куртка']
        ),
        Box(
            id=random_id(),
            name='Ячейка №22',
            dimensions=(1, 2, 2),
            address='Склад 1',
            rented_from=datetime(year=2025, month=5, day=20),
            rented_till=datetime(year=2025, month=9, day=20),
            items_stored=['Шины', 'Мелкие автозапчасти', 'Крыло автомобиля']
        ),
        Box(
            id=random_id(),
            name='Ячейка №33',
            dimensions=(1, 1, 2),
            address='Склад 2',
            rented_from=datetime(year=2025, month=4, day=20),
            rented_till=datetime(year=2025, month=7, day=20),
            items_stored=['Книги', 'Журналы', 'Газеты']
        ),
    ]
    
    return boxes


def get_demo_warehouses():
    warehouses = [
        Warehouse(
            id=1,
            address='Склад 1',
            number_of_1cub_m_boxes=12,
            number_of_2cub_m_boxes=4,
            number_of_3cub_m_boxes=2,
            number_of_4cub_m_boxes=3
        ),
        Warehouse(
            id=2,
            address='Склад 2',
            number_of_1cub_m_boxes=5,
            number_of_2cub_m_boxes=0,
            number_of_3cub_m_boxes=3,
            number_of_4cub_m_boxes=1
        ),
    ]
    
    return warehouses


def find_warehouse(id: int) -> Warehouse | None:
    for warehouse in get_demo_warehouses():
        if warehouse.id == id:
            return warehouse
    
    return None


if __name__ == '__main__':
    user = get_demo_user()
    print(user.boxes_in_usage)