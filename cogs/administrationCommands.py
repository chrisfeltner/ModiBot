import discord
from discord.ext import commands
from discord import NotFound

class AdministrationCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Kick
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        """Kicks a member from the server.
        In order for this to work, the bot must have Kick Member permissions.
        To use this command you must have Kick Members permission.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'
        

        await ctx.guild.kick(member, reason = reason)
        await ctx.send(f'Kicked {member} for {reason}.')

    # Ban
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        """Bans a member from the server.
        You can also ban from ID to ban regardless whether they're
        in the server or not.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID:{ctx.author.id})'

        
        await ctx.guild.ban(member, reason = reason)
        await ctx.send(f'Banned {member} for {reason}.')

    #Multiban
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def multiban(self, ctx, members : commands.Greedy[discord.Member], *, reason = None):
        """Bans multiple members from the server.
        This only works through banning via ID.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID:{ctx.author.id})'
        
        total_members = len(members)
        if total_members == 0:
            return await ctx.send('Missing members to ban.')
        
        confirm = await ctx.prompt(f'This will ban **{plural(total_members):member}**. Are you sure?', reacquire = False)
        if not confirm:
            return await ctx.send('Aborting.')

        failed = 0
        for member in members:
            try:
                await ctx.guild.ban(member, reason = reason)
            except discord.HTTPException:
                failed += 1
        
        await ctx.send(f'Banned {total_members - failed}/{total_members} members.')

    # # Unban
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userID, reason = None):
        """Unbans a member from the server.
        You can pass either the ID of the banned member or the Name#Discrim
        combination of the member. Typically the ID is easiest to use.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permissions.
        """

        if not userID.isdigit():
            embed = discord.Embed(description = ":x: Input a Valid User ID.", color = 0xff0000)
            return await ctx.send(embed = embed)

        if reason is None:
            reason = f'Action done by {ctx.author} (ID:{ctx.author.id})'

        try:
            user = discord.Object(id = userID)
            await ctx.guild.unban(user, reason = reason)
            # await ctx.send(f'Unbanned {user}.')

            embed = discord.Embed(description = ":white_check_mark: **%s** has been unbanned."%userID.name, color = 0x00ff00)

            return await ctx.send(embed = embed)

        except (NameError, NotFound):
            embed = discord.Embed(description = ":x: Either this User ID is not valid or this user is not currently banned. Please input a valid user ID.", color = 0xff0000)
            return await ctx.send(embed = embed)

    # Clear messages
    @commands.command()
    @commands.has_guild_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 0):
        await ctx.channel.purge(limit = amount + 1)
        await ctx.send(f'Deleted {amount} messages.')

# Connect cog to bot
def setup(bot):
    bot.add_cog(AdministrationCommands(bot))