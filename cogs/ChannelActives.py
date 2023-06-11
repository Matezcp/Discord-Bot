import nextcord
import asyncio
from nextcord.ext import commands

class ChannelActives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if not member.id == self.bot.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == 600:
                    await voice.disconnect()
                if not voice.is_connected():
                    break

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