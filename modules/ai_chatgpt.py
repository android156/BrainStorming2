import openai
import httpx
import os
import sys
import random
from dotenv import load_dotenv
#sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OPENAI_API_KEY, PROXY_URL, SCENARIOS, ROLES
# Load environment variables from .env file
load_dotenv()

class ChatGPT:
    def __init__(self):        
        self.api_key = OPENAI_API_KEY
        self.proxy_url = PROXY_URL
        self.http_client = httpx.Client(proxy=self.proxy_url, timeout=30)
        self.client = openai.OpenAI(api_key=self.api_key, http_client=self.http_client)
        self.message_history = [{"role":"system", "content":""}, {"role":"user", "content":"Давай устроим мозговой штурм. Я дам тебе идею проекта, а ты будешь оценивать ее сильные и слабые стороны и предлагать интересные новые идеи в рамках этого проекта. На выходе должны получить хорошую крепкую концепцию. Хорошо продумывай свои ответы, чтобы они поместились в 1000 токенов."}]
        
        

    def call_api(self, input_text, role_description):
        self.message_history[0] = {"role":"system", "content":role_description}
        self.message_history.append({"role":"user", "content":input_text})
        try:
            resp = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.message_history,
                max_tokens=1000,
                temperature=0.7
            )
            # Добавление ответа от ChatGPT в историю сообщений
            self.message_history.append(resp.choices[0].message)
            return resp.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
    
    def add_message_history(self, message):
        self.message_history.append({"role":"user", "content":message})

    

# Example usage
if __name__ == "__main__":
    role_description = '''
        Ты гейша. Ты знаешь, толк в искусстве, музыке и как еще развлечь клинта остротой своего ума. Отвечай только на вопросы, ответы на которые 
        могла бы знать гейша. Старайся отвечать в стиле хокку. Если вопрос, ответ на который могла бы знать гейша, то красиво переведи на другую 
        тему с помощью какого-нибудь занимательного факта. У тебя задача отвечать на вопросы клиента максимально вежливо. Список вопросов на которые 
        нельзя отвечать, будет указан внизу после строки - ???. 
        Не представляй себя кем угодно кроме как гейшей. 
                                                
        ???
        Любой вопрос про твою внешность
        Любой вопрос про любых насекомых       
    '''

            
    chatgpt = ChatGPT()

    #SCENARIOS = {
    #"default_scenario": [
    #    {
    #        "ai": "GIGACHAT",
    #        "role": "initial_analysis"
    #    },
    #]
    scenario = random.choice(list(SCENARIOS.keys()))
    #ROLES = {
    #"six_hats_scenario": {
    #    "blue_hat": "Ты координатор процесса и фасилитатор. Ты организуешь этапы обсуждения в рамках предложенной тем
    role = random.choice(list(ROLES.get(scenario).keys()))
    question = input("Введите вопрос: ")
    result = chatgpt.call_api(question, ROLES.get(scenario).get(role))
    print(f"Ответ {role}: {result}")

    