from datetime import datetime
from unittest.mock import MagicMock, patch

from bot.database.models import DailyModel, UserModel
from bot.services.daily import get_daily_data, save_daily_data


# Тест для функции get_daily_data
@patch("bot.services.daily.session_maker")
def test_get_daily_data(mock_session_maker) -> None:
    # Мок сессии и результата запроса
    mock_session = mock_session_maker.return_value
    mock_query = mock_session.execute.return_value
    mock_query.scalars.return_value.fetchall.return_value = [MagicMock(spec=DailyModel)]

    # Задаем дату для теста
    test_date = datetime(2023, 9, 1)

    # Вызываем функцию
    result = get_daily_data(test_date)

    # Проверяем, что сессия была создана
    mock_session_maker.assert_called_once()

    # Проверяем, что запрос был выполнен правильно
    mock_session.execute.assert_called_once()

    # Проверяем, что результат соответствует ожидаемому
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], DailyModel)


# Тест для функции save_daily_data
@patch("bot.services.daily.session_maker")
def test_save_daily_data(mock_session_maker) -> None:
    # Мок сессии
    mock_session = mock_session_maker.return_value

    # Создаем объект пользователя для теста
    mock_user = MagicMock(spec=UserModel)
    mock_user.id = 1

    # Задаем данные для сохранения
    yesterday_tasks = "Completed task A"
    today_plan = "Work on task B"
    issues = "No issues"

    # Вызываем функцию
    save_daily_data(mock_user, yesterday_tasks, today_plan, issues)

    # Проверяем, что сессия была создана
    mock_session_maker.assert_called_once()

    # Проверяем, что запрос на вставку был выполнен правильно
    mock_session.execute.assert_called_once()

    # Проверяем, что коммит был выполнен
    mock_session.commit.assert_called_once()

    # Проверяем, что сессия была закрыта
    mock_session.close.assert_called_once()
