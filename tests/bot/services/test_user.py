from unittest.mock import MagicMock, patch

import pytest

from bot.database.models import UserModel
from bot.services.user import add_user, add_user_id_to_allow_access, get_user, get_users, is_allow_access


# Тест для функции get_user
@patch("bot.services.user.session_maker")
def test_get_user(mock_session_maker) -> None:
    # Создаем мок сессии
    mock_session = MagicMock()
    mock_session_maker.return_value = mock_session

    # Мокаем запрос и результат выполнения
    mock_query = MagicMock()
    mock_session.execute.return_value = mock_query
    mock_query.scalars.return_value.one_or_none.return_value = MagicMock(spec=UserModel)

    user_id = 123
    result = get_user(user_id)

    # Проверяем, что сессия и запрос выполнены корректно
    mock_session_maker.assert_called_once()
    mock_session.execute.assert_called_once()
    assert isinstance(result, UserModel)


# Тест для функции get_users
@patch("bot.services.user.session_maker")
def test_get_users(mock_session_maker) -> None:
    # Создаем мок сессии
    mock_session = MagicMock()
    mock_session_maker.return_value = mock_session

    # Мокаем запрос и результат выполнения
    mock_query = MagicMock()
    mock_session.execute.return_value = mock_query
    mock_query.scalars.return_value.all.return_value = [MagicMock(spec=UserModel)]

    result = get_users()

    # Проверяем, что функция вернула список пользователей
    mock_session_maker.assert_called_once()
    mock_session.execute.assert_called_once()
    assert isinstance(result, list)
    assert isinstance(result[0], UserModel)


# Тест для функции is_allow_access
@patch("bot.services.user.session_maker")
def test_is_allow_access(mock_session_maker) -> None:
    # Создаем мок сессии
    mock_session = MagicMock()
    mock_session_maker.return_value = mock_session

    # Мокаем запрос и результат выполнения
    mock_query = MagicMock()
    mock_session.execute.return_value = mock_query
    mock_query.fetchone.return_value = (True,)

    user_id = 123
    result = is_allow_access(user_id)

    # Проверяем, что функция корректно возвращает булево значение
    mock_session_maker.assert_called_once()
    mock_session.execute.assert_called_once()
    assert result is True


# Тест для функции add_user_id_to_allow_access
@patch("bot.services.user.session_maker")
def test_add_user_id_to_allow_access(mock_session_maker) -> None:
    # Создаем мок сессии
    mock_session = MagicMock()
    mock_session_maker.return_value = mock_session

    user_id = 123
    add_user_id_to_allow_access(user_id)

    # Проверяем, что запрос и коммит были вызваны
    mock_session_maker.assert_called_once()
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


# Тест для функции add_user
@patch("bot.services.user.session_maker")
@patch("core.config.settings")
def test_add_user(mock_settings, mock_session_maker) -> None:
    # Настраиваем мок настроек
    mock_settings.admin_user_ids = [123]

    # Создаем мок сессии
    mock_session = MagicMock()
    mock_session_maker.return_value = mock_session

    # Создаем мок модели UserModel с заданными атрибутами
    mock_user = MagicMock(spec=UserModel)
    mock_user.id = 123  # Устанавливаем значение id
    mock_user.username = "test_user"
    mock_user.first_name = "Test"
    mock_user.last_name = "User"

    # Мокаем результат выполнения запроса
    mock_query = MagicMock()
    mock_session.execute.return_value = mock_query
    mock_query.scalars.return_value.one.return_value = mock_user

    user_id = 123
    username = "test_user"
    first_name = "Test"
    last_name = "User"
    result = add_user(user_id, username, first_name, last_name)

    # Проверяем, что запрос и коммит были вызваны
    mock_session_maker.assert_called_once()
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

    # Проверяем результат
    assert result.id == user_id  # Здесь теперь сравниваем правильное значение
    assert result.username == username
    assert result.first_name == first_name
    assert result.last_name == last_name


# Фикстура для автоматического патчирования вызовов базы данных
@pytest.fixture(autouse=True)
def no_db_operations():
    with patch("bot.services.user.session_maker", new_callable=MagicMock):
        yield
