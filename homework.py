
M_IN_KM: int = 1000


class InfoMessage:

    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.get_distance = distance
        self.get_mean_speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.get_distance:.3f} км; '
                f'Ср. скорость: {self.get_mean_speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

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
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                  * self.get_mean_speed()
                                  + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight / M_IN_KM
                                 * (self.duration * self.MIN_IN_H))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        spent_calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                  * self.weight
                                  + ((self.get_mean_speed()
                                      * self.KMH_IN_MSEC)**2
                                      / (self.height / self.CM_IN_M))
                                  * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                  * self.weight)
                                 * (self.duration * self.MIN_IN_H))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CONSTANT_1 = 1.1
    CONSTANT_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_speed = (self.length_pool
                      * self.count_pool / M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self):
        spent_calories = ((self.get_mean_speed() + self.CONSTANT_1)
                          * self.CONSTANT_2
                          * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_class: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    for type in type_class:
        if type == workout_type:
            return type_class[type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    into: InfoMessage = training.show_training_info()
    print(into.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
