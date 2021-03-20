from discord.ext import commands


class PiCommands(commands.Cog):
    pi_2000 = open('pi.txt', 'r').readline()

    @commands.command()
    async def pi(self, ctx, *args):

        try:
            digits = int(args[0])
            if digits > 1998:
                digits = 1998
            elif digits < 0:
                digits = 0
        except (IndexError, ArithmeticError, ValueError):
            digits = 16
        await ctx.send(self.pi_2000[:digits+2])