import pytest
from unittest.mock import Mock, call
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING
from praktikum.bun import Bun

@pytest.fixture
def burger():
    return Burger()

@pytest.fixture
def mock_bun():
    """Mock для булки"""
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "Test Bun"
    bun.get_price.return_value = 100
    return bun

@pytest.fixture
def mock_ingredient():
    """Mock для ингредиента"""
    ingredient = Mock(spec=Ingredient)
    ingredient.get_name.return_value = "Test Ingredient"
    ingredient.get_price.return_value = 50
    ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
    return ingredient

@pytest.fixture
def three_different_ingredients():
    """Фикстура возвращает 4 разных ингредиента"""
    ingredients_data = [
        {
            "name": "Котлета",
            "price": 150,
            "type": INGREDIENT_TYPE_FILLING
        },
        {
            "name": "Сыр",
            "price": 100,
            "type": INGREDIENT_TYPE_FILLING
        },
        {
            "name": "Салат",
            "price": 50,
            "type": INGREDIENT_TYPE_FILLING
        },
        {
            "name": "Соус",
            "price": 30,
            "type": INGREDIENT_TYPE_SAUCE
        }
    ]
    
    ingredients = []
    for data in ingredients_data:
        mock = Mock(spec=Ingredient)
        mock.get_name.return_value = data["name"]
        mock.get_price.return_value = data["price"]
        mock.get_type.return_value = data["type"]
        ingredients.append(mock)
    
    return ingredients

@pytest.fixture
def burger_with_bun_and_ingredients(burger, mock_bun, mock_ingredient):
    """Бургер с булкой и ингредиентами"""
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingredient)
    return burger, mock_bun, mock_ingredient

@pytest.fixture
def mock_price():
    """Mock для метода get_price бургера"""
    return 500.0