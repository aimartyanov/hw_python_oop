class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        info = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')
        return info


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60
    """Базовый класс тренировки."""

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
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
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
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    workout = "RUN"
    coef1: int = 18
    coef2: int = 20
    """Тренировка: бег."""

    def __init__(self, action, duration, weight) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories = (self.coef1 * self.get_mean_speed() - self.coef2) *(
                self.weight / self.M_IN_KM * (self.duration * self.M_IN_H))
        return calories


class SportsWalking(Training):
    coefw1: float = 0.035
    coefw2: float = 0.029
    workout = "WLK"
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = (self.coefw1 * self.weight + (
                self.get_mean_speed() ** 2 // self.height) * (
                self.coefw2 * self.weight) * (self.duration * self.M_IN_H))
        return calories


class Swimming(Training):
    LEN_STEP: float = 1.38
    coefs1: float = 1.1
    coefs2: int = 2
    workout = "SWM"
    """Тренировка: плавание."""

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = self.length_pool * self.count_pool / (
                self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        calories = (Swimming.get_mean_speed(self) + self.coefs1) * (
                self.coefs2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary: dict = {"RUN": Running, "SWM": Swimming, "WLK": SportsWalking}
    if workout_type == "RUN" and len(data) == 3:
        return dictionary.get(workout_type)(*data)
    elif workout_type == "WLK" and len(data) == 4:
        return dictionary.get(workout_type)(*data)
    elif workout_type == "SWM" and len(data) == 5:
        return dictionary.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
