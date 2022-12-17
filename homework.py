
M_IN_KM: int = 1000

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def get_message():
        return (f'Тип тренировки: {training_type};'
                f'Длительность: {duration} ч.;'
                f'Дистанция: {distance} км;'
                f'Ср. скорость: {speed} км/ч;'
                f'Потрачено ккал: {calories}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight


    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        
        
        distance: int = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79 

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        spent_calories: float = ((*self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed + (*self.CALORIES_MEAN_SPEED_SHIFT))
                                  * self.weight / M_IN_KM * self.duration)
        return spent_calories

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height: int):
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self):
        spent_calories: float = ((0.035 * self.weight + (self.get_mean_speed**2 / self.height)
                                  * 0.029 * self.weight) * self.duration)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: int, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_speed = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self):
        spent_calories = (self.get_mean_speed + 1.1) * 2 * self.weight * self.duration
        return spent_calories
    

# В этой функции не сомневаюсь.
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_class = {
        'SWM' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking
    }
    for type in type_class:
        if type == workout_type:
            return type_class[type](data)
    


def main(training: Training) -> None:
    """Главная функция."""
    #return training_main = Training(training).
    pass
    


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

