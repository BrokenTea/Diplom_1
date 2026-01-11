import pytest
from unittest.mock import Mock, patch, call
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING

class TestBurgerInitialization:

#   def __init__(self):    
    def test_burger_bun_is_none_on_init(self, burger):
        """Тест: булка должна быть None при инициализации"""
        assert burger.bun is None

    def test_burger_ingredients_is_empty_list_on_init(self, burger):
        """Тест: список ингредиентов должен быть пустым при инициализации"""
        assert burger.ingredients == []

    def test_burger_ingredients_length_is_zero_on_init(self, burger):
        """Тест: длина списка ингредиентов должна быть 0 при инициализации"""
        assert len(burger.ingredients) == 0

#    def set_buns(self, bun: Bun):
    def test_set_buns_successfully_assigns_bun(self, burger, mock_bun):
        """Тест: Успешная установка булки"""
        mock_bun.get_name.return_value = "black bun"
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)

        assert burger.bun == mock_bun 

    def test_set_buns_replaces_existing(self, burger):
        """Тест: Замена существующей булки новой"""
        mock_bun1 = Mock(spec=Bun)
        mock_bun2 = Mock(spec=Bun)
        mock_bun1.get_name.return_value = "black bun"
        burger.set_buns(mock_bun1)
        burger.set_buns(mock_bun2)
    
        assert burger.bun != mock_bun1

#    def add_ingredient(self, ingredient: Ingredient):
    def test_add_ingredient_single(self, burger, mock_ingredient):
        """Тест: Добавление одного ингредиента"""   
        burger.add_ingredient(mock_ingredient)
        
        assert burger.ingredients[0] is mock_ingredient

    def test_add_multiple_different_ingredients(self, burger, three_different_ingredients):
        """Тест: Добавление трех разных ингредиентов"""
        for ingredient in three_different_ingredients:
            burger.add_ingredient(ingredient)

        assert burger.ingredients == three_different_ingredients

#    def remove_ingredient(self, index: int):
    def test_remove_ingredient_valid_index(self, burger, three_different_ingredients):
        """Тест: Ингредиент удалился (количество уменьшилось)"""
        burger.ingredients = three_different_ingredients.copy()
        initial_count = len(burger.ingredients)
        burger.remove_ingredient(1)
        
        assert len(burger.ingredients) == initial_count - 1
    
    def test_remove_ingredient_correct_item_removed(self, burger, three_different_ingredients):
        """Тест: Удаление именно выбранного ингредиента по индексу"""
        burger.ingredients = three_different_ingredients.copy()
        burger.remove_ingredient(1)
        
        assert burger.ingredients == [
            three_different_ingredients[0],
            three_different_ingredients[2],
            three_different_ingredients[3]
        ]

    def test_remove_ingredient_invalid_index_raises_error(self, burger, three_different_ingredients):
        """Тест: Удаление ингредиента по невалидному индексу """
        burger.ingredients = three_different_ingredients.copy()   
        with pytest.raises(IndexError):
            burger.remove_ingredient(5)
        
        assert burger.ingredients == three_different_ingredients

#    def move_ingredient(self, index: int, new_index: int):
    def test_element_changes_initial_position(self, burger, three_different_ingredients):
        """Тест: Элемент поменял исходное положение"""
        burger.ingredients = three_different_ingredients.copy()
        element_to_move  = burger.ingredients[2]
        burger.move_ingredient(2, 1)
        
        assert burger.ingredients[2] is not element_to_move 
    
    def test_element_position_is_updated(self, burger, three_different_ingredients):
        """Тест: Элемент переместился на указанный индекс"""
        burger.ingredients = three_different_ingredients.copy()
        element_to_move  = burger.ingredients[2]
        burger.move_ingredient(2, 1)
        
        assert burger.ingredients[1] is element_to_move

    def test_move_element_to_same_position(self, burger, three_different_ingredients):
        """Тест: Перемещение элемента на ту же позицию"""
        burger.ingredients = three_different_ingredients.copy()
        element_to_move  = burger.ingredients[2]
        burger.move_ingredient(2, 2)
        
        assert burger.ingredients[2] is element_to_move

    @pytest.mark.parametrize("from_index,to_index,", [
        (0, 3), #Перемещение первого элемента в конец
        (3, 0), #Перемещение последнего элемента в начало
        (2, 1), #Перемещение элемента из середины в другую позицию
        (1, 2), #Перемещение элемента из середины в другую позицию (обратное направление)
        (-1, 2), #Перемещение элемента с отрицательным индексмо
        (2, -1), #Перемещение элемента в отрицательный индекс
    ])
    def test_move_element_to_different_position(self, burger, three_different_ingredients, from_index, to_index):
        """Тест: Перемещение элемента на ту же позицию"""
        burger.ingredients = three_different_ingredients.copy()
        expected_order = three_different_ingredients

        expected_order.insert(to_index, expected_order.pop(from_index))
        
        burger.move_ingredient(from_index, to_index)
        
        assert burger.ingredients == expected_order

    def test_move_element_shift_elements_correctly(self, burger, three_different_ingredients):
        """Тест: Элементы справа занимают место перемещенного элемента"""
        burger.ingredients = three_different_ingredients.copy()
        moved_element = burger.ingredients[1]
        burger.move_ingredient(0, 3)

        assert burger.ingredients[0] is moved_element

    def test_move_displaces_target_element_left(self, burger, three_different_ingredients):
        """Тест: Элемент на индексе назначения перемещается в лева"""
        burger.ingredients = three_different_ingredients.copy()
        moved_element = burger.ingredients[3]
        burger.move_ingredient(0, 3)

        assert burger.ingredients[2] is moved_element

    def test_move_ingredient_original_object_preserved(self, burger, three_different_ingredients):
        """Тест: После перемещения остается тот же объект (не создается копия)"""
        burger.ingredients = three_different_ingredients.copy()
        element_to_move  = burger.ingredients[1]
        burger.move_ingredient(1, 3)

        assert sum(1 for ing in burger.ingredients if ing is element_to_move) == 1

    def test_move_ingredient_length_unchanged(self, burger, three_different_ingredients):
        """Тест: После перемещения длина списка остается прежней (не создаются новые элементы)"""
        burger.ingredients = three_different_ingredients.copy()
        original_length = len(burger.ingredients)
        burger.move_ingredient(1, 3)
        
        assert len(burger.ingredients) == original_length

    def test_move_ingredient_empty_list(self, burger):
        """Тест: Попытка перемещения в пустом списке"""
        burger.ingredients = []
        
        with pytest.raises(IndexError):
            burger.move_ingredient(0, 1)

    @pytest.mark.parametrize("from_index, to_index, expected_exception", [
        (10, 1, IndexError),  # индекс вне диапазона
        (None, 3, TypeError),  # None вместо int
        (1, None, TypeError),  # None вместо int
        (None, None, TypeError),  # None вместо int
    ])
    def test_move_with_invalid_index(self, burger, three_different_ingredients, 
                                    from_index, to_index, expected_exception):
        burger.ingredients = three_different_ingredients.copy()
        
        with pytest.raises(expected_exception):
            burger.move_ingredient(from_index, to_index)

#    def get_price(self) -> float:
    def test_get_price_with_bun_only(self, burger, mock_bun):
        """Тест: Цена бургера только с булками"""
        burger.set_buns(mock_bun)
        price = burger.get_price()
        
        assert price == 200
    
    def test_get_price_with_bun_and_one_ingredient(self, burger, mock_bun, mock_ingredient):
        """Тест: Цена бургера с булками и одним ингредиентом"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        price = burger.get_price()
        
        assert price == 250
    
    def test_get_price_with_multiple_ingredients(self, burger, mock_bun, three_different_ingredients):
        """Тест: Цена бургера с булками и несколькими ингредиентами"""
        burger.set_buns(mock_bun)
        for ingredient in three_different_ingredients:
            burger.add_ingredient(ingredient)

        expected_price = 0
        bun_price = mock_bun.get_price()
        expected_price += bun_price * 2
        for ingredient in three_different_ingredients:
            expected_price += ingredient.get_price() 
        
        assert burger.get_price() == expected_price

    def test_get_price_returns_float_or_int(self, burger, mock_bun, three_different_ingredients):
        """Простая проверка: get_price() возвращает float или int"""
        burger.set_buns(mock_bun)
        price = burger.get_price()
        assert isinstance(price, (int, float))

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected_total", [
        (50, [30, 20, 40], 190),           # Булка + 3 ингредиента
        (99.99, [49.99, 29.99], 279.96),   # Дробные числа
        (100, [49.99, 30], 279.99),        # Дробные числа и целые
        (0, [0, 0, 0], 0),                 # Нулевые цены
        (3, [50, 3, -1], 58),              # Отрицательные 
    ])
    def test_get_price_with_ingredients(self, burger, mock_bun, mock_ingredient, 
                                        bun_price, ingredient_prices, expected_total):
        """Тест: Параметризованный тест расчета цены с разными комбинациями"""
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        for price in ingredient_prices:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)
        
        assert burger.get_price() == expected_total

    def test_get_price_empty_burger(self, burger):
        """Тест: Цена пустого бургера (без булок) должна вызывать ошибку"""
        with pytest.raises(AttributeError):
            burger.get_price()

#    def get_receipt(self) -> str:

    def test_get_receipt_with_only_bun(self, burger, mock_bun, mock_price):
        """
        Тест чека для бургера только с булкой (без ингредиентов)
        """
        burger.set_buns(mock_bun)
        burger.get_price = Mock(return_value=mock_price)
        expected = (
            "(==== Test Bun ====)\n"
            "(==== Test Bun ====)\n"
            "\n"
            f"Price: {mock_price}"
        )
                
        assert burger.get_receipt() == expected

    def test_receipt_burger_with_bun_and_one_ingredient(self, burger, mock_bun, mock_ingredient, mock_price):
        """Тест чека для бургера с булкой и одним ингредиентом"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        burger.get_price = Mock(return_value=mock_price)
        expected = (
            "(==== Test Bun ====)\n"
            "= sauce Test Ingredient =\n"
            "(==== Test Bun ====)\n"
            "\n"
            f"Price: {mock_price}"
        )
        
        assert burger.get_receipt() == expected

    def test_receipt_burger_with_multiple_ingredients(self, burger, mock_bun, 
                                                    three_different_ingredients, mock_price):
        """Тест чека для бургера с несколькими ингредиентами"""
        burger.set_buns(mock_bun)
        
        expected_lines = ["(==== Test Bun ====)"]

        for ingredient in three_different_ingredients[:3]:
            burger.add_ingredient(ingredient)
            ingredient_type = ingredient.get_type().lower()
            ingredient_name = ingredient.get_name()
            expected_lines.append(f"= {ingredient_type} {ingredient_name} =")
        
        expected_lines.append("(==== Test Bun ====)\n")

        burger.get_price = Mock(return_value=mock_price)
        expected_lines.append(f"Price: {mock_price}")
        expected_receipt = "\n".join(expected_lines)

        assert burger.get_receipt() == expected_receipt

    def test_receipt_burger_with_different_ingredient_types(self, burger, mock_bun, 
                                                    three_different_ingredients, mock_price):
        """Тест чека для бургера с несколькими ингредиентами"""
        burger.set_buns(mock_bun)
        
        expected_lines = ["(==== Test Bun ====)"]
        
        for ingredient in three_different_ingredients:
            burger.add_ingredient(ingredient)
            ingredient_type = ingredient.get_type().lower()
            ingredient_name = ingredient.get_name()
            expected_lines.append(f"= {ingredient_type} {ingredient_name} =")
        
        expected_lines.append("(==== Test Bun ====)\n")

        burger.get_price = Mock(return_value=mock_price)
        expected_lines.append(f"Price: {mock_price}")
        expected_receipt = "\n".join(expected_lines)

        assert burger.get_receipt() == expected_receipt

    def test_receipt_burger_with_bun_and_one_ingredient(self, burger, mock_bun, mock_ingredient, mock_price):
        """Тест, что тип ингредиента в чеке пишется в нижнем регистре"""
        burger.set_buns(mock_bun)
        mock_ingredient.get_type.return_value = "SAUCE"
        burger.add_ingredient(mock_ingredient)

        assert "sauce" in burger.get_receipt()

    def test_receipt_ingredients_order_matches_addition_order(self, burger, mock_bun, 
                                                    three_different_ingredients, mock_price):
        """Тест порядка ингредиентов в чеке соответствует порядку добавления"""
        burger.set_buns(mock_bun)
        
        added_ingredients_order = []
        
        for ingredient in three_different_ingredients:
            burger.add_ingredient(ingredient)
            added_ingredients_order.append(ingredient.get_name())
        
        burger.get_price = Mock(return_value=mock_price)    
        
        receipt = burger.get_receipt()
        lines = receipt.split('\n')

        assert lines[0] == "(==== Test Bun ====)"
        assert lines[1] == "= filling Котлета ="
        assert lines[2] == "= filling Сыр ="
        assert lines[3] == "= filling Салат ="
        assert lines[4] == "= sauce Соус ="
        assert lines[5] == "(==== Test Bun ====)"
        assert lines[6] == ""
        assert lines[7] == f"Price: {mock_price}"

    def test_get_receipt_returns_string(self, burger_with_bun_and_ingredients, mock_price):
        """Тест get_receipt возвращает str"""
        burger, mock_bun, mock_ingredient = burger_with_bun_and_ingredients
        burger.get_price = Mock(return_value=mock_price)

        assert isinstance(burger.get_receipt(), str)

    def test_receipt_without_bun_raises_error(self, burger):
        """Тест формирования чека без булки вызывает AttributeError"""
        with pytest.raises(AttributeError):
            burger.get_receipt()
