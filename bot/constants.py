from core.config import settings

START_TEXT = "Привет, вот доступные команды"

HELP_TEXT = (
    "Данный бот предназначен для проведения дейли команды.\n"
    "Бот пришлет сообщение с кнопкой для заполнения формы за 15 минут до дейлика.\n"
)

ID_TEXT = "Твой ID: %s"

DAILY_COMMAND_TEXT = (
    f"Место проведения дейли:\n\n{settings.daily_place}\n\n"
    f"Дейли проходит в {settings.daily_time.strftime('%H:%M %Z')}\n\n"
    f"Форма для заполнения будет прислана за 15 минут, до начала дейли."
)

DAILY_DATA_IS_EMPTY_TEXT = "Пока нечего показать, никто ничего не заполнил."
DAILY_DATA_TEXT = "Дейли отчет во вложении."

DAILY_DATA_SAVE_MESSAGE = "Ну, все. Сохранил."

NOT_ALLOWED_MESSAGE = "А-та-та, не положено товарищъ"

UNHANDLED_ERROR = "Произошла ошибка. Обратитесь к администратору бота."

ALLOW_ID_ADDED_SUCCESSFUL = "Добавил id=%s успешно"
