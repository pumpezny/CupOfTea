import config
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from loguru import logger
from google_sheet_table import GoogleTable

logger.add(
    config.settings["LOG_FILE"],
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip",
)


class FreakTelegramBot(Bot):
    def __init__(
            self,
            token,
            parse_mode,
            google_table=None,
    ):
        super().__init__(token, parse_mode=parse_mode)
        self._google_table: GoogleTable = google_table

    @property
    def google_table(self):
        return self._google_table


bot = FreakTelegramBot(
    token=config.settings["TOKEN"],
    parse_mode=types.ParseMode.HTML,
    google_table=GoogleTable("cupoftea.json",
                             "https://docs.google.com/svoi_znachenia_vstavte"),
)
CupOfTea = Dispatcher(bot)

@CupOfTea.message_handler(filters.Regexp(regexp=r"(((|S|s)tart))"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")

    message: str = (
        f"Рад вас видеть)\n\n"
        f"Для того, чтобы получить список команд, отправьте: команды \n\n"
    )

    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@CupOfTea.message_handler(filters.Regexp(regexp=r"(((Ч|ч)ай)(\s)(\d+))"))
async def abonement_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command, number = text_msg.lower().split(' ')
    print(f"Вход: команда '{command}', опция '{number}'")

    values: int = bot.google_table.search_abonement(number)

    if values == -1:
        message = f'вы больше не можете приходить к нам на чай, купите абонемент 😰'
    else:
        end_date_value: datetime = values[0]
        balance_value: int = int(values[1])
        last_digit: int = balance_value % 10

        if last_digit == 1 and balance_value != 11:
            balance_value: str = f'{balance_value} посещение'
        elif last_digit in (2, 3, 4) and balance_value not in (12, 13, 14):
            balance_value: str = f'{balance_value} посещения'
        else:
            balance_value: str = f'{balance_value} посешений'

        message: str = f'🗓 приходите к нам на чай до: {end_date_value}\n💃 У Вас осталось {balance_value}'

    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return


@CupOfTea.message_handler(filters.Regexp(regexp=r"(((К|к)оманды))"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")

    message: str = (
        f"🤖 КОМАНДЫ ДЛЯ ЧАТ-БОТА: 🤖\n\n"
        f"❗ Команды ❗\n"
        f"--все доступные команды чат-бота 📣\n\n"
        f"🌿 Чай *** 🌿\n"
        f"--(*** - № абонемента) информация о Вашем абонементе (дата окончания абонемента и количество оставшихся посещений) 🔖\n\n"
        f"🔎 Как добраться 🔍\n"
        f"--наш адрес, карта и инструкция, как нас найти 🗺\n\n"
        f"💲 Цены 💲\n"
        f"-- цены на чай  💰\n\n"
        f"🗓 Расписание 🗓\n"
        f"-- расписание работы 📆\n\n"
        f"Если у Вас иной вопрос, напишите 'help' для связи с администратором 👤"
    )

    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@CupOfTea.message_handler(filters.Regexp(regexp=r"(((К|к)ак добраться))"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")

    message: str = (
        f"Нас легко найти в интернете,\n\n"
        f"для этого просто напишите в поисковике:\n\n"
        f"Pumpezny's House\n\n"
        f"вот ссылка: https://pumpeznys-house.business.site/\n"


    )

    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@CupOfTea.message_handler(filters.Regexp(regexp=r"(((Ц|ц)ены))"))
async def prices_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")
    try:
        with open('res/price.jpg', 'rb') as photo:
            await bot.send_photo(user_id, photo)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@CupOfTea.message_handler(filters.Regexp(regexp=r"(((Р|р)асписание))"))
async def schedule_adults_handler(message_from: types.Message) -> None:
  user_id: str = str(message_from.from_id)
  text_msg: str = message_from.md_text.strip(" @#")
  command:str = text_msg.lower()
  print(f"Вход: команда '{command}'")
  try:
    with open('res/timetable.jpg', 'rb') as photo:
        await bot.send_photo(user_id, photo)
  except Exception as send_error:
    logger.debug(f"{send_error.message}: Trouble id: {user_id}")
    return

@CupOfTea.message_handler(filters.Regexp(regexp=r"(((H|h)elp))"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")

    message: str = (
        f"Для обращения к администратору, перейдите по ссылке: @Saaaaaaaaaaaab \n\n"
        f"Хорошего дня!)\n\n"

    )

    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return


if __name__ == '__main__':
    executor.start_polling(CupOfTea, skip_updates=True)
