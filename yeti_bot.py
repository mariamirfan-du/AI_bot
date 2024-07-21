import discord 
from discord.ext import commands , tasks
import random
from itertools import cycle
import os 
import asyncio
import csv  
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
Msgs = []
chat_history = []
file_path = "backup.csv"
load_dotenv()

Token = os.getenv("Discord_key")
'''------------------------------------------events -------------------------------------------'''
@client.event
async def on_ready():
    print("bot is connected to the server sucessfully")
    change_status.start()
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            
    
'''------------------------------------------------------------------------------------------------'''
  
'''------------------------------------------commands--------------------------------------------'''      
 
#for responses to questions
@client.command(aliases=["yeti","bot"] )
async def response(ctx , * , questions): 
       
       reply = chat_bot_response(questions)  #generate answers to questions through mistral ai 
       
       await ctx.send(reply) #sends the responses to the server 

'''-----------------------------------------------------------------------------------------------------'''

'''---------------------------------- Connection to Mistral Ai -----------------------------------------'''   
def get_mistral_bot():

    #Retrival of Mistral key 
    api_key = os.getenv("API_KEY")

    #Creation of client through api key       
    client = MistralClient(api_key=api_key)  
    
    return client 


'''--------------------------------------------------------------------------------------------------'''

'''--------------------------------------------Chat backup-------------------------------------------'''

def history_backup(q , reply):

    fields = ["Question", "Reply"]

    dict = {"Question": q, "Reply": reply}

    with open(file_path, "+a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(dict)


@client.command(aliases=["history"] )
async def display_chat_history(ctx):

    chat_list = chat_history
    for i in chat_history:
        await ctx.send(i)



'''-------------------------------------------------------------------------------------------------------'''
'''------------------------------------------LLM Training--------------------------------------------------'''
#it can be used for limited questions 
def tokenize_string(question):
    return_string = ""
    dict = chat_history

    for dictionary in dict:
        return_string += "<s>[INST] " + dictionary["Question"] + "[/INST]"+ dictionary["Reply"]+"</s>"

    return_string += f"[INST] {question} [/INST]"

    return return_string

def chat_bot_response(prompt):

    client = get_mistral_bot()
    
    #Specifying the model 
    model = "mistral-large-latest"

    #Retriving the questions 
    question = ChatMessage(role ="user" , content = prompt)
    Msgs.append(question)

    
    #Generating the response through mistral 
    chat_response = client.chat(
    model=model,
    messages=Msgs,
    )
    

    #prints the response through Mistral 
    response = chat_response.choices[0].message.content
    message = ChatMessage(role = "assistant", content = response)
    Msgs.append(message)
 

    chat_history.append({"Question": prompt, "Reply": response})
    history_backup(prompt , response)
    return response






'''-----------------------------------------------------------------------------------------------------'''   

'''------------------------------------------tasks--------------------------------------------------'''

bot_status =cycle(["/magicball", "/help" , "ping" ])

@tasks.loop(seconds= 7)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))


'''-------------------------------------------Main Fnction--------------------------------------------'''

async def main():
    async with client:
        await load()
        await client.start(Token)

    

'''------------------------------------------------------------------------------------------------------'''
asyncio.run(main())


