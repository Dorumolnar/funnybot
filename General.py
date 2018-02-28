import asyncio
import discord
from random import randint
from chat_formatting import esape_mass_mentions, italics, pagify
from random import choice
from discord.ext import commands
import datetime
import time
import aiohttp

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def choose(self, *choices):
        """Chooses between multiple choices."""
        choices = [escape_mass_mentions(c) for c in choices]
        if len(choices) < 2:
            await self.bot.say('Not enough choices to pick from.')
        else:
            await self.bot.say(choice(choices))

    @commands.command
    async def roll(self, ctx, number : int = 100):
        """Rolls random number"""
        author = ctx.message.author
        if number > 1:
            n = randint(1, number)
            await self.bot.say("You rolled : {}".format(n))
        else:
            await self.bot.say("Higher than 1!")

    @commands.command()
    async def lmgtfy(self, *, search_terms : str):
        """Creates a lmgtfy link"""
        search_terms = escape_mass_mentions(search_terms.replace(" ", "+"))
        await self.bot.say("https://lmgtfy.com/?q={}".format(search_terms))

    @commands.command(pass_context=True, no_pm=True)
    async def userinfo(self, ctx, *, user: discord.Member=None):
        """Shows users's informations"""
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = self.fetch_joined_at(user, server)
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(server.members,
                               key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "Playing {}".format(user.game)
        else:
            game = "Streaming: [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="Member #{} | User ID:{}"
                             "".format(member_number, user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows server's informations"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.voice])
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

def setup(bot):
    bot.add_cog(General(bot))
    print('General is loaded')
