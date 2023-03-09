# from revChatGPT.V1 import Chatbot
# import asyncio

# chatbot = Chatbot(config={
#   "email": "patrykszylin93@gmail.com",
#   "password": "Patryk#123"
# })


# def askBot(stock, content):
#   print("Chatbot: ")
#   prev_text = ""
#   for data in chatbot.ask(
#       """Summarise this article: """ + content,
#   ):
#       message = data["message"][len(prev_text) :]
#       print(message, end="", flush=True)
#       prev_text = data["message"]
#   print()

#   print("-------")
#   print(prev_text)

import os
from revChatGPT.V3 import Chatbot
chatbot = Chatbot(api_key=os.environ["OPENAI_API_KEY"])



# def summarise(stock, content):
#   for data in chatbot.ask("""Summarise this article: """ + content):
#       print(data, end="", flush=True)
#       # with open("test.json", "w") as testfile:
#       #   testfile.write(data)
#   # t1 = asyncio.create_task(askBot(stock, content))

#   # asyncio.gather(t1)



def summarise(stock, content):
  data = chatbot.ask("""Summarise this article: """ + content)
  print("----------------------------------------")
  return data

  
