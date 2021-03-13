from discord.ext import commands

from tictactoebot import TicTacToe

bot = commands.Bot(command_prefix='!')


bot.add_cog(TicTacToe(bot))


@bot.event
async def on_ready():
    print("broccolibot has started")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


@bot.command()
async def derp(ctx):
    await ctx.send("derp!")


@bot.command()
async def doubt(ctx):
    await ctx.message.add_reaction(bot.get_emoji(817367529957752894))

token = open('token.txt', 'r').readline()
bot.run(token)
