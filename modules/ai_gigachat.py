import sys
import random
import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import GIGACHAT_API_KEY, SCENARIOS, ROLES

# Используйте ключ авторизации, полученный в личном кабинете, в проекте GigaChat API.
#   with GigaChat(credentials="ключ_авторизации", ca_bundle_file="russian_trusted_root_ca.cer") as giga:
#    response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
#    print(response.choices[0].message.content)

# Load environment variables from .env file
load_dotenv()

class GIGACHAT:
    def __init__(self):
        self.api_key = GIGACHAT_API_KEY
        self.ca_bundle_file = "modules/sert/russian_trusted_root_ca.cer"
        self.client = GigaChat(credentials=self.api_key, ca_bundle_file=self.ca_bundle_file, model="GigaChat-Max")
        self.message_history = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content=""
        ),
        
        Messages(
            role=MessagesRole.USER,
            content="Давай устроим мозговой штурм. Я дам тебе идею проекта, а ты будешь оценивать ее сильные и слабые стороны и предлагать интересные новые идеи в рамках этого проекта. На выходе должны получить хорошую крепкую концепцию. Хорошо продумывай свои ответы, чтобы они поместились в 1000 токенов."
        ),
    ],
    
    temperature=0.7,
    max_tokens=1000,
)
    
    
    def call_api(self, input_text, role_description):
        self.message_history.messages[0] = Messages(
            role=MessagesRole.SYSTEM,
            content=role_description
        )
        self.message_history.messages.append(Messages(role=MessagesRole.USER, content=input_text))
        try:
            resp = self.client.chat(self.message_history)
                
            # Добавление ответа от ChatGPT в историю сообщений
            self.message_history.messages.append(resp.choices[0].message)
            return resp.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
        

    def add_message_history(self, message):
        self.message_history.messages.append(Messages(role=MessagesRole.USER, content=message))

# Example usage
if __name__ == "__main__":
    
         
    gigachat = GIGACHAT()
    scenario = random.choice(list(SCENARIOS.keys()))
    role = random.choice(list(ROLES.get(scenario).keys()))
    question = input("Введите вопрос: ")
    result = gigachat.call_api(question, ROLES.get(scenario).get(role))
    print(f"Ответ {role}: {result}")