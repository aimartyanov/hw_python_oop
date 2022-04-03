from typing import ClassVar
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    M_IN_H: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    COEF1: ClassVar[int] = 18
    COEF2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return ((self.COEF1 * self.get_mean_speed() - self.COEF2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.M_IN_H))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFW1: ClassVar[float] = 0.035
    COEFW2: ClassVar[float] = 0.029

    height: float

    def get_spent_calories(self) -> float:
        return ((self.COEFW1 * self.weight + (self.get_mean_speed() ** 2
                // self.height) * self.COEFW2 * self.weight)
                * (self.duration * self.M_IN_H))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFS1: ClassVar[float] = 1.1
    COEFS2: ClassVar[int] = 2

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFS1)
                * self.COEFS2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: dict = {
                           "RUN": Running,
                           "SWM": Swimming,
                           "WLK": SportsWalking
                           }
    if workout_type not in training_type:
        raise KeyError(
            "Некорректный тип тренировки."
            f"Тип {InfoMessage.training_type} отсутствует в базе")
    return training_type.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
