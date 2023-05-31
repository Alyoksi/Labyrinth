# Игра "Лабиринт"

## Описание проекта 
`Цель:`создание игры, в которой игрок будет помещен в лабиринт, из которого ему надо будет выбраться. Игрок может видеть только в фиксированном радиусе вокруг себя.

`Мотивация:`более глубокое изучение библиотек Python для создания игр, алгоритмов создания лабиринтов и нахождение путей выхода из них.

## Перечень функциональностей проекта
1. Пользователь должен иметь возможность играть за персонажа, помещенного в правильно сгенерированный лабиринт (т.е. тот, из которого точно есть выход). 
2. Приложение должно предоставлять пользователю возможность выбрать сложность лабиринта (т.е. его размеры) 
3. Приложение должно предоставлять пользователю возможности:
   1. Управлять персонажем `стрелочками` или при помощи клавиш `WASD`.
   2. При нажатии на клавишу `Q` пустить после персонажа след.
   3. При нажатии на клавишу `R` начать прохождение лабиринта заново.
   4. При нажатии на клавишу `E` вернуть персонажа в начальную позицию.
4. Приложение должно показывать маршрут выхода из лабиринта в случае, если пользователь не смог найти его самостоятельно. 

## Описание сценария использования
1. Пользователь запускает программу - программа генерирует лабиринт и запускает игру.
2. Пользователь запускает программу - программа создает меню, в котором можно выбрать сложность(3 варианта) -
пользователь кликает на выбранный вариант - программа изменяет стандартные показатели ширины и длины поля.
3. Разветвление:
   1. Пользователь нажимает на `стрелочку` или на одну из клавиш `WASD` - программа запускает соотвествующую функцию,
которая меняет координаты персонажа.
   2. Пользователь нажимает на клавишу `Q` - программа запускает функцию, которая меняет значение переменной `trace`
на `True`, чтобы метод delete_player рисовал след после изменения положения игрока.
   3. Пользователь нажимает на клавишу `R` - программа запускает метод `start_game`, который обнуляет время прохождения
лабиринта и помещает персонажа в стартовую позицию.
   4. Пользователь нажимает на клавишу `E` - программа помещает персонажа в стартовую позицию.
4. Пользователь не смогу до конца времени пройти лабиринт - программа останавливает игру и прорисовывает на экране 
правльный путь.