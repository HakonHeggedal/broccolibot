from discord.ext import commands

from countbot import Count
from pibot import PiCommands
from searchbot import Search
from tictactoebot import TicTacToe

bot = commands.Bot(command_prefix='!')

bot.add_cog(TicTacToe(bot))
bot.add_cog(Count())
bot.add_cog(Search())
bot.add_cog(PiCommands())


@bot.event
async def on_ready():
    print("broccolibot has started")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


@bot.command()
async def doubt(ctx):
    kiasu_doubt = bot.get_emoji(817367529957752894)
    if kiasu_doubt:
        await ctx.message.add_reaction(kiasu_doubt)

token = open('token.txt', 'r').readline()
bot.run(token)
