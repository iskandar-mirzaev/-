import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Полные данные об электрических компонентах
ELECTRICAL_PARTS = {
    "🔋 Аккумулятор (LiPo)": {
        "description": (
            "Источник питания (например, 4S 1500mAh).\n\n"
            "📌 Параметры:\n"
            "- Напряжение: 14.8V\n"
            "- Емкость: 1500-2200mAh\n"
            "- Разъем: XT60\n\n"
            "⚠️ Не допускайте полного разряда!"
        ),
        "image": "https://i.ibb.co/4g1Q8NtD/image.jpg"
    },
    "🧠 Полетный контроллер": {
        "description": (
            "Основной процессор (например, Betaflight F7).\n\n"
            "📌 Функции:\n"
            "- Стабилизация полета\n"
            "- Обработка сигналов с пульта\n"
            "- Управление ESC\n\n"
            "💡 Прошивки: Betaflight, iNav, ArduPilot"
        ),
        "image": "https://i.ibb.co/rffz1tmH/image.jpg"
    },
      "Регуляторы (ESC)": {  # Исправленный компонент
        "description": (
            "4 ESC (например, BLHeli_32 35A).\n\n"
            "Задачи:\n"
            "- Контроль скорости моторов\n"
            "- Защита от перегрузок\n"
            "- Обратная связь по току\n\n"
            "Калибровка обязательна!"
        ),
        "image": "https://i.ibb.co/39JRmVd6/image.jpg"
    },
    "📡 Приемник (RX)": {
        "description": (
            "Получает сигналы с пульта (например, TBS Crossfire).\n\n"
            "📌 Протоколы:\n"
            "- SBUS\n"
            "- CRSF\n"
            "- PWM\n\n"
            "📶 Дальность: до 10+ км"
        ),
        "image": "https://i.ibb.co/fGtDMyPv/image.jpg"
    },
    "📷 Камера FPV": {
        "description": (
            "Аналоговая/цифровая (например, RunCam Phoenix 2).\n\n"
            "📌 Характеристики:\n"
            "- Разрешение: 1200TVL\n"
            "- Угол обзора: 170°\n"
            "- Формат: 4:3/16:9\n\n"
            "🌙 Ночная съемка: зависит от сенсора"
        ),
        "image": "https://i.ibb.co/xtb9kZNP/image.webp"
    },
    "📶 VTX (Передатчик видео)": {
        "description": (
            "Отправляет видео с камеры на очки/монитор.\n\n"
            "📌 Параметры:\n"
            "- Мощность: 25-800mW\n"
            "- Каналы: 5.8GHz\n"
            "- Антенна: MMCX/SMA\n\n"
            "⚖️ Законность: проверьте локальные ограничения"
        ),
        "image": "https://i.ibb.co/ymFBbL7J/vtx.jpg"
    },
    "🔄 Моторы": {
        "description": (
            "4 бесколлекторных мотора (например, 2207 1750KV).\n\n"
            "📌 Характеристики:\n"
            "- KV-рейтинг: 1500-2500\n"
            "- Крепление: M3/M5\n"
            "- Тип: Inrunner/Outrunner\n\n"
            "⚙️ Подбираются под вес коптера"
        ),
        "image": "https://i.ibb.co/c4sL5cK/image.jpg"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - показывает главное меню"""
    await show_components_menu(update)

async def show_components_menu(update: Update):
    """Показывает меню выбора компонентов"""
    keyboard = [
        [InlineKeyboardButton(part, callback_data=part)]
        for part in ELECTRICAL_PARTS.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🔌 *Электрическая схема квадрокоптера*:\nВыберите компонент:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def show_part(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает информацию о выбранном компоненте"""
    query = update.callback_query
    await query.answer()
    
    part_name = query.data
    part_data = ELECTRICAL_PARTS.get(part_name, {})
    
    # Кнопка "Назад"
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад к компонентам", callback_data="back_to_components")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"*{part_name}*\n\n{part_data['description']}\n\n[Фото]({part_data['image']})",
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=False
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех callback-запросов"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_to_components":
        await show_components_menu(update)
    elif query.data in ELECTRICAL_PARTS:
        await show_part(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /help"""
    await update.message.reply_text(
        "ℹ️ Доступные команды:\n"
        "/start - Показать компоненты\n"
        "/help - Справка",
        parse_mode="Markdown"
    )

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token("8153324226:AAHQfP2euZhUautClAmPuSVctI5cwExByz4").build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == "__main__":
    main()