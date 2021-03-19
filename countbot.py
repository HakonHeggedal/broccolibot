from discord.ext import commands


class Count(commands.Cog):

    def __init__(self):
        self.counter = 0

    @commands.command()
    async def add(self, ctx, *args):
        try:
            self.counter += int(args[0])
            await ctx.send("Sum: " + str(self.counter))
        except ValueError:
            await ctx.send("please give a number, like !add 5")
