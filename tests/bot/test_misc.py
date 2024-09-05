from datetime import date
from unittest.mock import MagicMock, patch

from bot.misc import build_daily_result


def test_build_daily_result() -> None:
    # Мокирование данных
    mock_data = [
        MagicMock(
            user=MagicMock(first_name="John", last_name="Doe"),
            yesterday_tasks="Completed task A",
            today_plan="Work on task B",
            issues="No issues",
        )
    ]

    mock_date = date(2023, 9, 1)

    with patch("bot.misc.env.get_template") as mock_get_template:
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "<html>Mocked HTML</html>"

        result = build_daily_result(mock_date, mock_data)

        # Проверка вызова шаблона
        mock_get_template.assert_called_once_with("daily_report.html")
        mock_template.render.assert_called_once_with(
            data=[
                {
                    "name": "Doe John",
                    "yesterday_tasks": "Completed task A",
                    "today_plan": "Work on task B",
                    "issues": "No issues",
                }
            ],
            date=mock_date,
        )

        # Проверка результата
        assert result == "<html>Mocked HTML</html>"
