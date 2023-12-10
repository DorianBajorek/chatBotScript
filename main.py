import discord
from discord.ext import commands
import requests

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"


def make_request(user_message):
    payload = {
        "message": user_message,
        "sender": "user"
    }
    response = requests.post(rasa_server_url, json=payload)

    if response.status_code == 200:
        rasa_response = response.json()

        print("Rasa Response:", rasa_response)
        if isinstance(rasa_response, list) and len(rasa_response) > 0 and 'text' in rasa_response[0]:
            return rasa_response[0]['text']
        else:
            return "Sorry, I don't understand"
    else:
        print("Error:", response.status_code, response.text)
        return "Sorry, I don't understand"


intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send(f'{make_request(message.content)}')


bot.run("MTE4MTI1ODI3NTA2OTYyODQzNg.Gi1FOA.9tPiXWTiCxhRFrE1EFLqSX3UrSOuF4vgGHla7c")