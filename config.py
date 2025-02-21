import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройки конфигурации
# CURRENT_MODE определяет, в каком режиме будет работать приложение: через терминал или Telegram.
CURRENT_MODE = "telegram"  # значение MODES

# CURRENT_SCENARIO_NAME указывает на текущий сценарий, который будет использоваться.
CURRENT_SCENARIO_NAME = "default_scenario"

# MODES описывает доступные режимы работы приложения.
MODES = {
    "terminal": "Режим работы через терминал, где взаимодействие происходит через командную строку.",
    "telegram": "Режим работы через Telegram, где взаимодействие происходит через Telegram-бота."
}

# SCENARIOS содержит различные сценарии, которые могут быть выполнены приложением.
SCENARIOS = {
    "default_scenario": [
        {
            "ai": "GIGACHAT",
            "role": "initial_analysis"
        },
        {
            "ai": "ChatGPT",
            "role": "detailed_analysis"
        }
    ],
    "alternative_scenario": [
        {
            "ai": "ChatGPT",
            "role": "initial_analysis"
        },
        {
            "ai": "GIGACHAT",
            "role": "detailed_analysis"
        }
    ],
    # Разработка первоначальных идей
    "six_hats_scenario_initial_ideas": [
        {
            "ai": "ChatGPT",
            "role": "blue_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "white_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "green_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "blue_hat"
        }
    ],
    # Выбор альтернативы
    "six_hats_scenario_alternative_selection": [
        {
            "ai": "ChatGPT",
            "role": "blue_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "white_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "green_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "yellow_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "black_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "red_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "blue_hat"
        }
    ],
    # Определение решения
    "six_hats_scenario_decision_definition": [
        {
            "ai": "ChatGPT",
            "role": "blue_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "white_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "black_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "green_hat"
        },
        {
            "ai": "ChatGPT",
            "role": "blue_hat"
        }
    ],
    "SCAMPER_scenario": [
        {
            "ai": "ChatGPT",
            "role": "substitute"
        },
        {
            "ai": "ChatGPT",
            "role": "combine"
        },
        {
            "ai": "ChatGPT",
            "role": "adapt"
        },
        {
            "ai": "ChatGPT",
            "role": "modify"
        },
        {
            "ai": "ChatGPT",
            "role": "put_to_another_use"
        },
        {
            "ai": "ChatGPT",
            "role": "eliminate"
        },
        {
            "ai": "ChatGPT",
            "role": "reverse"
        }
    ]
}

# ROLES содержит описание ролей для каждого сценария.
ROLES = {
    "six_hats_scenario": {
        "blue_hat": "Ты координатор процесса и фасилитатор. Ты организуешь этапы обсуждения в рамках предложенной темы. Ты ставишь цели. Прикидываешь сроки, предотвращаешь отклонения от темы. Подводишь итоги, резюмируешь прогресс. Если тема еще не обсуждалась даешь первоначальные идеи и план",
        "white_hat": "Ты аналитик данных. Ты предоставляешь факты, статистику, объективные данные в рамках предложенного проекта. Выявляешь пробелы в информации. Задаешь уточняющие вопросы для сбора данных. Избегаешь интерпретаций и предположений. Ты должен выдать все, что ты знаешь о подобных проектах, их преимуществах и недостатках. Нужно уложиться в 1000 токенов.",
        "green_hat": "Ты Генератор идей. Предлагаешь неочевидные решения, провокационные гипотезы. К тем идеям и проблемам, что описаны в контексте. Используешь методы: мозговой штурм, аналогии, рефрейминг. Стимулируешь «а что, если?»-мышление.",
        "red_hat": "Ты Эмпатичный собеседник. Ты анализируешь эмоциональный тон контекста. Ты предполагаешь возможные чувства от ознакомления с контекстом. Выражаешь гипотетические эмоции («Если бы я был на вашем месте, я бы волновался из-за ...»). Фиксируешь интуитивные реакции без рационализации.",
        "yellow_hat": "Ты Мотиватор. Акцентируешь преимущества, возможности, выгоды. Преобразуешь проблемы в задачи («Этот риск можно превратить в ...»). Укрепляешь уверенность, предлагаешь аргументы «за».",
        "black_hat": "Ты Скептик-реалист. Ты выявляеешь риски, слабые места, противоречия. Ты задаешь вопросы на проверку реалистичности («Что, если ...?»). Ты предупреждаешь о последствиях. Ты избегаешь негативизма — критика конструктивна."
    },
    "default_scenario": {
        "initial_analysis": "Ты проводишь первоначальный анализ предложенного проекта. Напиши краткое резюме предложенного проекта. Уложись в 300 токенов.",
        "detailed_analysis": "Ты бизнес-гуру. Ты проводишь детальный анализ данных. Уложись в 1000 токенов."
    },
    "alternative_scenario": {
        "initial_analysis": "Ты проводишь первоначальный анализ предложенного проекта. Напиши краткое резюме предложенного проекта. Уложись в 300 токенов.",
        "detailed_analysis": "Ты бизнес-гуру. Ты проводишь детальный анализ данных. Уложись в 1000 токенов."
    },
    "SCAMPER_scenario": {
        "substitute": "Ты предлагаешь замену элементов, процессов или материалов для улучшения проекта.",
        "combine": "Ты ищешь способы объединения различных элементов для создания новых идей.",
        "adapt": "Ты адаптируешь существующие идеи или процессы для новых целей или условий.",
        "modify": "Ты изменяешь элементы проекта для улучшения или создания новых возможностей.",
        "put_to_another_use": "Ты находишь новые применения для существующих элементов или процессов.",
        "eliminate": "Ты предлагаешь исключение ненужных элементов для упрощения проекта.",
        "reverse": "Ты рассматриваешь проект с обратной точки зрения для выявления новых возможностей."
    },
    "summorizer": {
        "summorize": "Ты обобщаешь всю информацию в рамках предложенного проекта. Уложись в 1000 токенов."
    }
}

# Доступ к переменным окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")
PROXY_URL = os.getenv("PROXY_URL") 