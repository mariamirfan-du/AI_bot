import discord 
from discord.ext import commands 

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("messages are ready")
        
    @commands.command()
    async def embed(self,ctx):

        #creating an Embed object
        embed_msg = discord.Embed(title="description" , description="This is your description" , color=discord.Color.dark_green())

        # Using user's avatar URL for author and footer icons
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url     

        embed_msg.set_author(name=f"requested by {ctx.author.name}" , icon_url=avatar_url)
        '''dummy urls can be replaced with users one '''

        
        embed_msg.set_thumbnail(url=avatar_url)
        embed_msg.set_image(url="https://i.pinimg.com/564x/7d/51/6e/7d516e0572fcf7729d47e786725d3026.jpg")
        embed_msg.add_field(name="website" , value = "https://anything.com" , inline=False)
        embed_msg.set_footer(text="this is footer" , icon_url=avatar_url)
        
        await ctx.send(embed=embed_msg)
        

async def setup(client):
    await client.add_cog(Embed(client))