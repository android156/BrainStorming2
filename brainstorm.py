import os
from modules.ai_chatgpt import ChatGPT
from modules.ai_gigachat import GIGACHAT
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT, COMMAND
from config import CURRENT_MODE, CURRENT_SCENARIO_NAME, SCENARIOS, ROLES, TELEGRAM_BOT_TOKEN

# Загрузка переменных окружения из файла .env
load_dotenv()

def init_and_get_ai_dict(ai_set):
    """
    Инициализирует и возвращает словарь с экземплярами AI моделей.
    :param ai_set: множество имен AI моделей, которые необходимо инициализировать.
    :return: словарь с экземплярами AI моделей.
    """
    ai_dict = dict()
    for ai in ai_set:
        if ai == "ChatGPT":
            chatgpt = ChatGPT()
            ai_dict[ai] = chatgpt
        elif ai == "GIGACHAT":
            gigachat = GIGACHAT()
            ai_dict[ai] = gigachat
        else:
            print(f"Unknown AI model: {ai}")
    return ai_dict

def run_terminal_mode(current_scenario, roles):
    """
    Запускает сценарий в режиме терминала.
    :param current_scenario: текущий сценарий, который необходимо выполнить.
    :param roles: словарь ролей для AI моделей.
    """
    ai_set = set([sc_step["ai"] for sc_step in current_scenario])
    ai_dict = init_and_get_ai_dict(ai_set)
    
    scenario_name = current_scenario[0].get("scenario_name", "default_scenario")
    
    question = input("Введите идею проекта: ")
    
    for i, step in enumerate(current_scenario, 1):
        role = step.get("role")
        ai_name = step.get("ai")
        current_ai = ai_dict.get(ai_name)              
        role_description = roles.get(scenario_name, {}).get(role, "")
        
        # Вызов API для текущей AI модели
        result = current_ai.call_api(question, role_description)
        for ai in ai_dict.values():
            if ai is not current_ai:
                ai.add_message_history(result)
        question = "Дай заключение по вышеизложенному"
        
        print(f"\n\nОтвет {i}. {ai_name}[{role}]: {result}")

async def list_scenarios(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a list of available scenarios to the user.
    """
    scenarios = SCENARIOS.keys()
    scenarios_list = "\n".join(scenarios)
    await update.message.reply_text(f"Доступные сценарии:\n{scenarios_list}")

async def select_scenario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Allows the user to select a scenario.
    """
    if context.args:
        selected_scenario = context.args[0]
        if selected_scenario in SCENARIOS:
            global CURRENT_SCENARIO_NAME
            CURRENT_SCENARIO_NAME = selected_scenario
            await update.message.reply_text(f"Сценарий '{selected_scenario}' выбран.")
        else:
            await update.message.reply_text("Неверный сценарий. Используйте /list_scenarios для просмотра доступных сценариев.")
    else:
        await update.message.reply_text("Пожалуйста, укажите сценарий. Пример: /select_scenario <название_сценария>")

async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a list of available commands to the user.
    """
    commands = [
        "/start - Начать взаимодействие с ботом",
        "/list_scenarios - Показать доступные сценарии",
        "/select_scenario <название_сценария> - Выбрать сценарий",
        "/list_commands - Показать список команд"
    ]
    commands_list = "\n".join(commands)
    await update.message.reply_text(f"Доступные команды:\n{commands_list}")

def run_telegram_mode(current_scenario, roles):
    """
    Запускает сценарий в режиме Telegram.
    :param current_scenario: текущий сценарий, который необходимо выполнить.
    :param roles: словарь ролей для AI моделей.
    """
    ai_set = set([sc_step["ai"] for sc_step in current_scenario])
    ai_dict = init_and_get_ai_dict(ai_set)
    
    scenario_name = current_scenario[0].get("scenario_name", "default_scenario")

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Введите идею проекта:')

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        question = update.message.text
        for i, step in enumerate(current_scenario, 1):
            role = step.get("role")
            ai_name = step.get("ai")
            current_ai = ai_dict.get(ai_name)
            role_description = roles.get(scenario_name, {}).get(role, "")
            
            # Вызов API для текущей AI модели
            result = current_ai.call_api(question, role_description)
            for ai in ai_dict.values():
                if ai is not current_ai:
                    ai.add_message_history(result)
            question = "Дай заключение по вышеизложенному"
            
            await update.message.reply_text(f"Ответ {i}. {ai_name}[{role}]: {result}")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list_scenarios", list_scenarios))
    application.add_handler(CommandHandler("select_scenario", select_scenario))
    application.add_handler(CommandHandler("list_commands", list_commands))
    application.add_handler(MessageHandler(TEXT, handle_message))

    application.run_polling()

def run_scenario():
    """
    Загружает конфигурацию и запускает сценарий в зависимости от текущего режима.
    """
    current_scenario = SCENARIOS.get(CURRENT_SCENARIO_NAME, [])
    
    if CURRENT_MODE == "terminal":
        run_terminal_mode(current_scenario, ROLES)
    elif CURRENT_MODE == "telegram":
        run_telegram_mode(current_scenario, ROLES)

if __name__ == "__main__":
    run_scenario()
