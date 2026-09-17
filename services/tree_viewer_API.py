from pathlib import Path
from typing import Literal, overload

import logging
from core.config import logger
from database import DataBaseManager
from models import Relative  # noqa: F401
from pyvis.network import Network

script_dir = Path(__file__).resolve().parent
dtb_path = script_dir / "family_tree.db"


@overload
def true_int_input(text: str = "", allow_empty: Literal[False] = False) -> int: ...


@overload
def true_int_input(text: str = "", allow_empty: Literal[True] = True) -> int | None: ...


def true_int_input(text: str = "", allow_empty: bool = False):
    """Безопасный ввод чисел."""
    while True:
        try:
            user_input = input(text)

            if user_input == "":
                if allow_empty:
                    return None
                logger.warning("Пользователь оставил поле пустым при вводе числа.")
            else:
                return int(user_input)
        except ValueError:
            logger.error("Ошибка ввода: введено не число.")


def find_relative():
    """Поиск стартового родственника для построения дерева."""
    dtb = DataBaseManager(dtb_path)
    selected_relative = ()

    logger.info("Вы знаете ID родственника или хотите найти его по ФИО?")

    while True:
        choice_method = true_int_input(
            "Выберите метод введения родственника (1 - по ID, 2 - по Имени): "
        )
        if choice_method == 1:
            while True:
                num_id = true_int_input(
                    "Введите номер id или (9999) чтобы вернуться назад: "
                )
                if num_id == 9999:
                    logger.info("Возвращаемся обратно к выбору метода")
                    break
                selected_relative = dtb.get_relative_by_id(num_id)
                if selected_relative:
                    return selected_relative
                logger.warning("Родственник с таким ID не найден!")
        elif choice_method == 2:
            while True:
                name_rel = input(
                    "Введите имя родственника или (back) чтобы вернуться назад: "
                )
                if name_rel == "back":
                    logger.info("Возвращаемся обратно к выбору метода")
                    break
                selected_relative = dtb.get_relative_by_name(name_rel)
                if len(selected_relative) == 1:
                    return selected_relative[0]
                elif len(selected_relative) > 1:
                    for index, relative in enumerate(selected_relative, start=1):
                        logger.info(
                            f"{index}. ФИО: {relative.last_name} {relative.first_name} {relative.patronymic} Дата рождения: {relative.birth_date}"
                        )
                    choice_rel = true_int_input(
                        "Выберите одного из этих родственников: "
                    )
                    selected_relative = selected_relative[choice_rel - 1]
                    return selected_relative
                else:
                    logger.warning("Ни одного родственника с таким именем!")


def generate_family_tree(database):
    """Сгенерировать древо родственников с автоматическим расчётом уровней."""
    dict_levels = {}

    start_relative = find_relative()
    if not start_relative:
        logger.error("Стартовый родственник не выбран.")
        return

    key_id_rel = start_relative.id
    start_level = 10
    dict_levels[key_id_rel] = start_level

    all_relatives = database.get_all_relatives()
    queue_order = [key_id_rel]

    while len(queue_order) > 0:
        object_rel_now = database.get_relative_by_id(queue_order.pop(0))
        id_rel_now = object_rel_now.id
        level_rel_now = dict_levels[id_rel_now]

        father_id = object_rel_now.father_id
        mother_id = object_rel_now.mother_id
        spouse_id = object_rel_now.spouse_id

        if father_id and father_id not in dict_levels:
            queue_order.append(father_id)
            dict_levels[father_id] = level_rel_now - 1
        if mother_id and mother_id not in dict_levels:
            queue_order.append(mother_id)
            dict_levels[mother_id] = level_rel_now - 1
        if spouse_id and spouse_id not in dict_levels:
            queue_order.append(spouse_id)
            dict_levels[spouse_id] = level_rel_now

        for relative in all_relatives:
            if (
                relative.father_id == id_rel_now or relative.mother_id == id_rel_now
            ) and relative.id not in dict_levels:
                queue_order.append(relative.id)
                dict_levels[relative.id] = level_rel_now + 1

    # === ШАГ 2: НАСТРОЙКА ВИЗУАЛИЗАЦИИ PYVIS ===
    net = Network(height="750px", width="100%", bgcolor="#000000", directed=False)

    net.set_options("""
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed",
          "nodeSpacing": 250,
          "treeSpacing": 300
        }
      },
      "physics": {
        "enabled": false
      }
    }
    """)

    # === ШАГ 3: ОТРИСОВКА УЗЛОВ И СВЯЗЕЙ ===
    # Цикл 1: Добавляем людей (узлы) на экран
    for relative in all_relatives:
        if relative:
            if relative.gender == "М":
                node_color = "#1e90ff"  # Синий для мужчин
            elif relative.gender == "Ж":
                node_color = "#ff69b4"  # Розовый для женщин
            else:
                node_color = "#979797"  # Серый, если пол не указан

            # Безопасно берём уровень из словаря, для одиночек ставим 10 по умолчанию
            chosen_level = dict_levels.get(relative.id, 10)
            net.add_node(
                relative.id,
                relative.get_full_name(),
                color=node_color,
                level=chosen_level,
            )

    # Цикл 2: Рисуем кровные связи (Родители -> Дети)
    for relative in all_relatives:
        if relative:
            if relative.father_id:
                net.add_edge(relative.father_id, relative.id)
            if relative.mother_id:
                net.add_edge(relative.mother_id, relative.id)

    # Цикл 3: Рисуем брачные связи (Супруги)
    for relative in all_relatives:
        if relative:
            if relative.spouse_id:
                net.add_edge(
                    relative.spouse_id,
                    relative.id,
                    physics=False,  # Запрещаем влиять на иерархию
                    dashes=True,  # Делаем линию пунктирной
                    color="#ff1493",  # Розово-красный цвет для супругов
                    smooth={
                        "type": "curvedCW",
                        "roundness": 0.2,
                    },  # Легкий изгиб
                )

    # === ШАГ 4: СОХРАНЕНИЕ В HTML ===
    tree_html = script_dir / "family_tree.html"
    net.write_html(str(tree_html))
    logger.info(f"Древо успешно сгенерировано и сохранено в файл: {tree_html}")
