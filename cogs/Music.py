import nextcord
from nextcord.ext import commands
import wavelink
from wavelink.ext import spotify
import datetime
from typing import Union

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: Union[wavelink.YouTubeTrack,spotify.SpotifyTrack], reason):    
        # ctx = player.ctx
        # vc: player = ctx.voice_client
        vc = player

        if vc.queue.is_empty:
            return

        # if vc.loop:
        #     return await vc.play(track)
        
        next_song = vc.queue.get()
        await vc.play(next_song)
        # await ctx.send(f"Tocando `{next_song.title}`")


    @commands.command(aliases=['tocar','zinho'])
    async def play(self, ctx: commands.Context, *, search: str):

        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return

        async def playTrack(vc, ctx, track: Union[wavelink.YouTubeTrack,spotify.SpotifyTrack]):
            if vc.queue.is_empty and not vc.is_playing():
                await vc.play(track)
                return True
            else:
                await vc.queue.put_wait(track)
                return False

        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        elif not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        if(search.startswith("https://open.spotify.com/")):
            decoded = spotify.decode_url(search)

            if decoded and decoded['type'] is spotify.SpotifySearchType.track:
                track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                print(f"Spotify Track: {track.title}")
                if(await playTrack(vc, ctx, track)):
                    await ctx.send(f"Tocando `{track.title}`")
                else:
                    await ctx.send(f"`{track.title}` adicionado à fila")
            elif decoded and decoded['type'] is spotify.SpotifySearchType.playlist:
                print(f"Spotify Playlist: {search}")
                await ctx.send(f"Adding musics from Spotify Playlist: {decoded}...")
                numMusicAdded = 0
                async for track in spotify.SpotifyTrack.iterator(query=search, type=spotify.SpotifySearchType.playlist):
                    print(f"Spotify Track: {track.title}")
                    numMusicAdded += 1
                    await playTrack(vc, ctx, track)
                await ctx.send(f"Added {numMusicAdded} musics from Spotify Playlist")
            elif decoded and decoded['type'] is spotify.SpotifySearchType.album:
                print(f"Adding musics from Spotify Album: {search}...")
                await ctx.send(f"Adding musics from Spotify Album: {search}...")
                numMusicAdded = 0
                async for track in spotify.SpotifyTrack.iterator(query=search, type=spotify.SpotifySearchType.album):
                    print(f"Spotify Track: {track.title}")
                    numMusicAdded += 1
                    await playTrack(vc, ctx, track)
                await ctx.send(f"Added {numMusicAdded} musics from Spotify Album")

        else:
            track = await wavelink.YouTubeTrack.search(query=search, return_first=True)
            print(f"Youtube Track: {track.title}")
            if(await playTrack(vc, ctx, track)):
                    await ctx.send(f"Tocando `{track.title}`")
            else:
                await ctx.send(f"`{track.title}` adicionado à fila")

    @commands.command()
    async def pause(self, ctx: commands.Context):
        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return

        if not ctx.voice_client:
            return await ctx.send("Nenhuma Música tocando Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client
            
        await vc.pause()
        await ctx.send("Música pausada!")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return

        if not ctx.voice_client:
            return await ctx.send("Nenhuma Música tocando Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client
            
        await vc.resume()
        await ctx.send("Toma a música de volta!")

    @commands.command(aliases=['queue'])
    async def fila(self, ctx: commands.Context):
        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return
        
        if not ctx.voice_client:
            return await ctx.send("Nenhuma Música tocando Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client
            
        if vc.queue.is_empty:
            return await ctx.send("Fila Vazia!")

        em = nextcord.Embed(title = "Músicas", color = nextcord.Color.green())
        queue = vc.queue.copy() 
        song_count = 0

        for song in queue:
            song_count += 1
            em.add_field(name = f"#{song_count}", value = f"{song.title}")

        await ctx.send(embed = em)

    @commands.command(aliases=['pular'])
    async def skip(self, ctx: commands.Context):
        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return

        if not ctx.voice_client:
            return await ctx.send("Nenhuma Música tocando Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.stop()
        await ctx.send("Música pulada!")

    @commands.command()
    async def remove(self, ctx: commands.Context, *, index: int):
        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return

        if not ctx.voice_client:
            return await ctx.send("Nenhuma Música tocando Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if(index > 0):
            del vc.queue._queue[index-1]
            await ctx.send(f"Música #{index} Removida da Fila!")

    @commands.command(aliases=['tocando'])
    async def playing(self, ctx: commands.Context):
        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return

        if not ctx.voice_client:
            return await ctx.send("Nenhuma Música tocando Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if not vc.is_playing():
            return await ctx.send("Nenhuma música tocando!")

        em = nextcord.Embed(title = f"Tocando {vc.track.title}",description= f"Por {vc.track.author}" , color = nextcord.Color.green())
        em.add_field(name = "Duração", value = f"{str(datetime.timedelta(seconds = vc.track.length))}")
        em.add_field(name = "Link", value = f"[Clique Aqui]({vc.track.uri})")

        await ctx.send(embed=em)
    
    @commands.command(aliases=['lume'])
    async def volume(self, ctx: commands.Context, volume: int = None):
        if(ctx.channel.id != 1117561338030465155):
            await ctx.send("Esse comando só pode ser usado no canal canto-do-cezar!")
            return

        if not ctx.voice_client:
            return await ctx.send("Nenhuma Música tocando Burro!")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Você não está em um canal de voz Burro!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if volume is None:
            return await ctx.send(f"Volume atual: {vc.volume}%")

        if volume >= 100:
            await ctx.send("Volume setado em 100%")
            return await vc.set_volume(100)
        elif volume <= 0:
            await ctx.send("Volume setado em 0%")
            return await vc.set_volume(0)

        await ctx.send(f"Volume setado em {volume}%")
        await vc.set_volume(volume)

    # @commands.command()
    # async def loop(ctx: commands.Context):
    #     if not ctx.voice_client:
    #         return await ctx.send("Nenhuma Música tocando Burro!")
    #     elif not getattr(ctx.author.voice, "channel", None):
    #         return await ctx.send("Você não está em um canal de voz Burro!")
    #     else:
    #         vc: wavelink.Player = ctx.voice_client
            
    #     try:
    #         vc.loop ^= True
    #     except:
    #         setattr(vc, "loop", False)
        
    #     if vc.loop:
    #         await ctx.send("Loop ativado!")
    #     else:
    #         await ctx.send("Loop desativado!")

def setup(bot):
    bot.add_cog(Music(bot))