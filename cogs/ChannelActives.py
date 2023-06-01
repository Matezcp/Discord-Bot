import nextcord
from nextcord.ext import commands

class ChannelActives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sair'])
    async def leave(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Não to em um canal de voz Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client
            
        await vc.disconnect()

def setup(bot):
    bot.add_cog(ChannelActives(bot))