'''
MIT License

Copyright (c) 2017 verixx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import discord
from discord.ext import commands
import datetime
import time
import random
import asyncio
import json

class Info():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=['s','serverinfo','si'], no_pm=True)
    async def server(self, ctx):
        '''See information about the server.'''
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle or
                      m.status == discord.Status.dnd])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))
        colour = ("#%06x" % random.randint(0, 0xFFFFFF))
        colour = int(colour[1:], 16)

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
            data.set_author(name=server.name, icon_url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)
            print(data.to_dict())

        try:
            await self.bot.say(embed=data)

        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True,no_pm=True,aliases=["ri","role"])
    async def roleinfo(self, ctx, *, role: discord.Role=None):
        '''Shows information about a role'''
        server = ctx.message.server

        if not role:
            role = server.default_role

        since_created = (ctx.message.timestamp - role.created_at).days
        role_created = role.created_at.strftime("%d %b %Y %H:%M")
        created_on = "{}\n({} days ago!)".format(role_created, since_created)

        users = len([x for x in server.members if role in x.roles])
        if str(role.colour) == "#000000":
            colour = "default"
            color = ("#%06x" % random.randint(0, 0xFFFFFF))
            color = int(colour[1:], 16)
        else:
            colour = "Hex: {}\nRGB: {}".format(str(role.colour).upper(),str(role.colour.to_tuple()))
            color = role.colour

        em = discord.Embed(colour=color)
        em.set_author(name=role.name)
        em.add_field(name="ID", value=role.id, inline=True)
        em.add_field(name="Users", value=users, inline=True)
        em.add_field(name="Mentionable", value=role.mentionable, inline=True)
        em.add_field(name="Hoist", value=role.hoist, inline=True)
        em.add_field(name="Position", value=role.position, inline=True)
        em.add_field(name="Managed", value=role.managed, inline=True)
        em.add_field(name="Colour", value=colour, inline=False)
        em.set_footer(text=created_on)

        try:
            await self.bot.say(embed=em)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")


    @commands.command(pass_context=True,aliases=['ui','user'],description='See user-info of someone.')
    async def userinfo(self,ctx, user: discord.Member = None):
        '''See information about a user or yourself.'''
        server = ctx.message.server
        user = user or ctx.message.author
        avi = user.avatar_url or user.default_avatar_url
        roles = sorted(user.roles, key=lambda c: c.position)
        roles = roles[::-1]
        for role in roles:
            if str(role.color) != "#000000":
                color = int(str(role.color)[1:], 16)
                break

        rolenamelist = []
        for role in roles:
            if role.name != "@everyone":
                rolenamelist.append(role.name)
        rolenames = ', '.join(rolenamelist) or 'None'

        time = ctx.message.timestamp
        desc = '{0} is chilling in {1} mode.'.format(user.name,user.status)
        member_number = sorted(server.members,key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(colour=color,description = desc,timestamp=time)
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name='Member No.',value=str(member_number),inline = True)
        em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Roles', value=rolenames, inline=True)
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url='http://site-449644.mozfiles.com/files/449644/logo-1.png')
        try:
            await self.bot.say(embed=em)

        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True,aliases=['av','dp'])
    async def avatar(self,ctx, user: discord.User = None):
        '''Returns ones avatar URL'''
        if not user:
            user = ctx.message.author
        avi = user.avatar_url or user.default_avatar_url
        if ".gif" in avi:
            avi+="&f=.gif"
        avi = avi.replace(".webp",".png").replace("?size=1024","?size=2048")
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.set_image(url=avi)
        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name
        em.set_author(name=name, url=avi)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def info(self, ctx):
        '''See bot information, uptime, servers etc.'''
        uptime = (datetime.datetime.now() - self.bot.uptime)
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)
        if days:
            time_ = '%s days, %s hours, %s minutes, and %s seconds' % (days, hours, minutes, seconds)
        else:
            time_ = '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)
        servers = len(self.bot.servers)
        version = '1.2.1'
        library = 'discord.py'
        time = ctx.message.timestamp
        emb = discord.Embed(colour=0x00FFFF)
        emb.set_author(name='selfbot.py', icon_url=self.bot.user.avatar_url)
        emb.add_field(name='Version',value='0.0.0')
        emb.add_field(name='Library',value='discord.py')
        emb.add_field(name='Creator',value='papaatje#0001(https://discord.gg/dbn78Kt)')
        emb.add_field(name='Servers',value=servers)
        emb.add_field(name='My crush:',value='the bot creator his crush is SECRET!')
        emb.add_field(name='Join my discord!',value='[Server:]()
        emb.add_field(name='Uptime',value=time_)
        emb.set_footer(text="ID: {}".format(self.bot.user.id))
        emb.set_thumbnail(url='https://cdn.discordapp.com/avatars/319395783847837696/349677f658e864c0a5247a658df61eb1.webp?width=80&height=80')
        await self.bot.say(embed=emb)

    @commands.command(pass_context=True)
    async def help(self, ctx, *, cmd = None):
        """Shows this message."""
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        pages = self.bot.formatter.format_help_for(ctx, self.bot)
        for page in pages:
            try:
                await self.bot.say(embed=page)
            except:
                await self.bot.say('I need the embed links perm.')

def setup(bot):
    bot.add_cog(Info(bot))
