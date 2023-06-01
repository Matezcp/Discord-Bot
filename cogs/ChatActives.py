import nextcord
from nextcord.ext import commands

class ChatActives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #TO DO CHANGE TO THE CORRECT CHANNEL
        channel = bot.get_channel(1078848823767613504)
        await channel.send(f"{member.name}, bem vindo à tropa!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        #TO DO CHANGE TO THE CORRECT CHANNEL
        channel = bot.get_channel(1078848823767613504)
        await channel.send(f"{member.name}???????????????")

    @commands.command(aliases=['zao'])
    async def tropa(self, ctx: commands.Context):
        await ctx.send("Aiiiii zé da manga!")

def setup(bot):
    bot.add_cog(ChatActives(bot))