import discord
import requests
from discord.ext import commands


class Search(commands.Cog):

    @commands.command()
    async def d(self, ctx, *args):
        if not args:
            return
        query = " ".join(args)
        url = "https://api.duckduckgo.com/?q=" + query + "&format=json"
        try:
            result = requests.get(url).json()["RelatedTopics"][0]["Text"]
            embed = discord.Embed()
            embed.add_field(name="DuckDuckGo search: " + query, value=result)
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("no duckduckgo result for: " + query)



