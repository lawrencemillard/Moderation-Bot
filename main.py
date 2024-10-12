import discord, json, os, base64
from discord.ext import commands, tasks
from colorama import Fore
from discord import app_commands, utils, File
import os
import sys
import os.path
import hashlib
from time import sleep
import time
import win32security
import json as jsond
import platform
import binascii
from uuid import uuid4
import requests
import logging
import sqlite3
import datetime
from datetime import datetime, timedelta
import asyncio
import traceback
import wcwidth
import shutil

logging.getLogger("discord.client").setLevel(logging.WARNING)
logging.getLogger("discord.gateway").setLevel(logging.WARNING)

class aclient(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(intents = intents)
        self.synced = False
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await bot.sync(guild = discord.Object(id=guild_id))
            self.synced = True
        if not self.added:
            self.added = True
    async def  on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await bot.sync()
            self.synced = True
        print(f''' 

{Fore.WHITE}

                            ███╗░░░███╗░██████╗░██████╗░░░░░██████╗░░██████╗░████████╗
                            ████╗░████║██╔═══██╗██╔══██╗░░░░██╔══██╗██╔═══██╗╚══██╔══╝
                            ██╔████╔██║██║░░░██║██║░░██║░░░░██████╔╝██║░░░██║░░░██║░░░
                            ██║╚██╔╝██║██║░░░██║██║░░██║░░░░██╔══██╗██║░░░██║░░░██║░░░
                            ██║░╚═╝░██║╚██████╔╝██████╔╝░░░░██████╔╝╚██████╔╝░░░██║░░░
                            ╚═╝░░░░░╚═╝░╚═════╝░╚═════╝░░░░░╚═════╝░░╚═════╝░░░░╚═╝░░░
''')
        print(f"We have logged in as {self.user}.")
        activity = activity=discord.Activity(type=3, name=botstatus)
        await client.change_presence(status=discord.Status.idle, activity=activity)

##Config###
with open('Data\Config.json', 'r') as file:
    config = json.load(file)
    
    token = config['Bot_Token']
    botstatus = config['Bot_Status']
    guild_id = config['Guild_Id']
    logs_channel = config['Logs_Channel_Id']
    welcome_channel = config['Welcome_Channel_Id']
    welcome_message_thumbnail = config['Welcome_Message_Thumbnail_Url']
    welcome_message_banner = config['Welcome_Message_Banner_Url']
    departure_message_thumbnail = config['Departure_Message_Thumbnail_Url']
    departure_message_banner = config['Departure_Message_Banner_Url']
    departure_channel = config['Departure_Channel_Id']
    terms_of_service_channel = config['Terms_Of_Service_Channel_Id']
    community_rules = config['Community_Rules_Channel_Id']
    ticket_system_channel = config['Ticket_System_Channel_Id']
    products_channel = config['Products_Channel_Id']
    report_message_channel = config['Report_Message_Channel_Id']
    server_name = config['Server_Name']
    muted_role = config['Muted_Role_Name']
    member_role = config['Member_Role_Name']

client = aclient()
bot = app_commands.CommandTree(client)

data_folder = "Data"
db_file = os.path.join(data_folder, "warning_system.db")

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

db = sqlite3.connect(db_file)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS warns(warning_id INTEGER PRIMARY KEY, user INTEGER, reason TEXT, time INTEGER, guild INTEGER, timestamp REAL)")

#####################################################################################
#                                  Kick Command                                     #
#####################################################################################

@bot.command(name="kick", description="This allows you to kick a person from the server")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.User, reason: str = None):
    if reason == None:
        reason='Reason not specified'
    
    embed=discord.Embed(
        title=f"**Moderation Bot | Kick Command**",
        color=0x313338,
        description=f'''
{member.mention} has been kicked by {interaction.user.mention}, and for the reason:
``{reason}``
        ''')

    await interaction.guild.kick(member)
    await interaction.response.send_message(embed=embed)

#####################################################################################
#                                   Ban Command                                     #
#####################################################################################

@bot.command(name="ban", description="This allows you to ban a person from the server")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.User, reason: str = None):
    if reason == None:
        reason='Reason not specified'
    
    embed=discord.Embed(
        title=f"**Moderation Bot | Ban Command**",
        color=0x313338,
        description=f'''
{member.mention} has been banned by {interaction.user.mention}, and for the reason:
``{reason}``
        ''')

    await interaction.guild.ban(member)
    await interaction.response.send_message(embed=embed)

#####################################################################################
#                                  Unban Command                                    #
#####################################################################################

@bot.command(name="unban", description="This allows you to unban a person from the ban list")
@app_commands.default_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    user = await client.fetch_user(user_id)
    
    embed=discord.Embed(
        title=f"**Moderation Bot | Unban Command**",
        color=0x313338,
        description=f'''
{user.mention} has been unbanned by {interaction.user.mention}
        ''')

    await interaction.guild.unban(user)
    await interaction.response.send_message(embed=embed)

#####################################################################################
#                                  Timeout Command                                  #
#####################################################################################

@bot.command(name="timeout", description="This allows you to timout a person for a duration of time")
@app_commands.default_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    
    if reason == None:
        reason='Reason not specified'
    
    embed=discord.Embed(
        title=f"**Moderation Bot | Timeout Command**",
        color=0x313338,
        description=f'''
{member.mention} has been put to timeout
### Reason:
``{reason}``
### Time:
``{duration}``
        ''')

    await member.timeout(duration, reason=reason)
    await interaction.response.send_message(embed=embed)

#####################################################################################
#                                  Add Role Command                                 #
#####################################################################################

@bot.command(name="add_role", description="This allows you to add roles to a person")
@app_commands.default_permissions(manage_roles=True)
async def giverole(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    await user.add_roles(role)

#####################################################################################
#                              Enable Slowmode Command                              #
#####################################################################################

@bot.command(name="enable_slowmode", description="This allows you to enable slowmode for a channel")
@app_commands.default_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction,  seconds: int = 0):
    embed=discord.Embed(
        title=f"**Moderation Bot | Enambe Slowmode Command**",
        color=0x313338,
        description=f'''
A slowmode was added to this channel.
### Time:
``{seconds}``
        ''')
    
    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(embed=embed)

#####################################################################################
#                             Disable Slowmode Command                              #
#####################################################################################

@bot.command(name="disable_slowmode", description="This allows you to disable slowmode for a channel")
@app_commands.default_permissions(manage_channels=True)
async def disable_slowmode(interaction: discord.Interaction):
    embed=discord.Embed(
        title=f"**Moderation Bot | Disable Slowmode Command**",
        color=0x313338,
        description=f'''
The slowmode was disabled for this channel.
        ''')
    
    await interaction.channel.edit(slowmode_delay=None)
    await interaction.response.send_message(embed=embed)

#####################################################################################
#                                   Purge Command                                   #
#####################################################################################

@bot.command(name='purge', description='Deletes a specified number of messages from the current channel')
@app_commands.default_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, limit: int):
    time = datetime.now()
    time_str1 = time.strftime("%I:%M")

    time_meridian_part = time.strftime("%p")

    await interaction.channel.purge(limit=limit)
    purge_embed = discord.Embed(title='Moderation Bot | Purge Command', description=f'Successfully purged {limit} messages. \n Command executed by {interaction.user.mention}.', color=0x313338)
    purge_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
    await interaction.channel.send(embed=purge_embed, delete_after=10)

#####################################################################################
#                                   Report Command                                  #
#####################################################################################

report_message_channel = 1132520224353165312

class timeoutthr34564(discord.ui.Modal, title='Timeout Person'):
    def __init__(self):
        super().__init__(timeout=None)
        
    quick111 = discord.ui.TextInput(
        label="What is the person's user id?",
        style=discord.TextStyle.short,
        placeholder='Type here...',
        required=True,
        max_length=34,
    )

    timequestion = discord.ui.TextInput(
        label="How much time? (Minutes only)",
        style=discord.TextStyle.short,
        placeholder='Type here...',
        required=True,
        max_length=6,
    )

    banquestion1321 = discord.ui.TextInput(
        label='Reason for timeout.',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=True,
        max_length=1000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(int(self.quick111.value))
        reason = f'{self.banquestion1321.value}'
        time = self.timequestion.value

        duration = discord.utils.utcnow() + timedelta(minutes=int(time))
        await member.timeout(duration, reason=reason)

        embed = discord.Embed(
            title=f"**Moderation Bot | Timeout Button**",
            timestamp = datetime.now(),
            color=0x313338,
            description=f'''
{member.mention} has been put to timeout by {interaction.user.mention}, and for the reason:
``{reason}``
        ''')

        view = reportbuttclear()
        await interaction.message.edit(view=view)

        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

class kick34(discord.ui.Modal, title='Kick Person'):
    def __init__(self):
        super().__init__(timeout=None)
        
    quick111 = discord.ui.TextInput(
        label="What is the person's user id?",
        style=discord.TextStyle.short,
        placeholder='Type here...',
        required=True,
        max_length=34,
    )
    banquestion1321 = discord.ui.TextInput(
        label='Reason for kick.',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=True,
        max_length=1000,
    )

    async def on_submit(self, interaction: discord.Interaction):

        user = await client.fetch_user(self.quick111.value)
        
        reason=f'{self.banquestion1321.value}'
        
        embed=discord.Embed(
            title=f"**Moderation Bot | Kick Button**",
            timestamp = datetime.now(),
            color=0x313338,
            description=f'''
{user.mention} has been kicked by {interaction.user.mention}, and for the reason:
``{reason}``
        ''')
        
        view = reportbuttclear()

        await interaction.message.edit(view=view)
        
        await interaction.guild.kick(user, reason=reason)
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        traceback.print_exception(type(error), error, error.__traceback__)

class ban34(discord.ui.Modal, title='Ban Person'):
    def __init__(self):
        super().__init__(timeout=None)
        
    quick111 = discord.ui.TextInput(
        label="What is the person's user id?",
        style=discord.TextStyle.short,
        placeholder='Type here...',
        required=True,
        max_length=34,
    )
    banquestion1321 = discord.ui.TextInput(
        label='Reason for ban.',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=True,
        max_length=1000,
    )

    async def on_submit(self, interaction: discord.Interaction):

        user = await client.fetch_user(self.quick111.value)
        
        reason=f'{self.banquestion1321.value}'
        
        embed=discord.Embed(
            title=f"**Moderation Bot | Ban Button**",
            timestamp = datetime.now(),
            color=0x313338,
            description=f'''
{user.mention} has been banned by {interaction.user.mention}, and for the reason:
``{reason}``
        ''')
        
        view = reportbuttclear()

        await interaction.message.edit(view=view)
        
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        traceback.print_exception(type(error), error, error.__traceback__)
        
class reportbuttclear(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Ban", custom_id="ban342", style=discord.ButtonStyle.gray, emoji="<:ban_hammer:1133477744836096010>", disabled=True)
    async def banbutt(self, interaction: discord.Interaction, button):

        await interaction.response.send_modal(ban34())
    
    @discord.ui.button(label='Kick', custom_id='kick342', style=discord.ButtonStyle.gray, emoji="<:DiscordKickIcon:1133459906939322368>", disabled=True)
    async def kickbutt(self, interaction: discord.Interaction, button):
        
        await interaction.response.send_modal(kick34())
    
    @discord.ui.button(label='Timeout', custom_id='timeout342', style=discord.ButtonStyle.gray, emoji="<:timeout_clock:1133464252162785311>", disabled=True)
    async def timeoutbutt(self, interaction: discord.Interaction, button):
        
        await interaction.response.send_modal(timeoutthr34564())
        
    @discord.ui.button(label='Cancel', custom_id='cancel342', style=discord.ButtonStyle.gray, emoji="<:Cancel:1133464880222048318>", disabled=True)
    async def cancelbutt(self, interaction: discord.Interaction, button):
        
        view = reportbuttclear()
        await interaction.message.edit(view=view)

class makesure(discord.ui.View):
    def __intit__(self):
        super().__init__(timout=None)
        
    @discord.ui.button(label='Cancel', custom_id='cancel23342', style=discord.ButtonStyle.gray, emoji="<:Cancel:1133464880222048318>")
    async def cancelbutt(self, interaction: discord.Interaction, button):
        
        view = reportbuttclear()

        await interaction.message.edit(view=view)
        await interaction.response.send_message('Buttons have been disabled', ephemeral=True)
    
    @discord.ui.button(label='Nevermind', custom_id='cancel3423342', style=discord.ButtonStyle.gray, emoji="<:w98_approve:1133478256318885888>")
    async def nvmbutt(self, interaction: discord.Interaction, button):
        view = reportbutt()

        await interaction.message.edit(view=view)

class reportbutt(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ban", custom_id="ban342", style=discord.ButtonStyle.gray, emoji="<:ban_hammer:1133477744836096010>")
    async def banbutt(self, interaction: discord.Interaction, button):

        await interaction.response.send_modal(ban34())
    
    @discord.ui.button(label='Kick', custom_id='kick342', style=discord.ButtonStyle.gray, emoji="<:DiscordKickIcon:1133459906939322368>")
    async def kickbutt(self, interaction: discord.Interaction, button):
        
        await interaction.response.send_modal(kick34())
    
    @discord.ui.button(label='Timeout', custom_id='timeout342', style=discord.ButtonStyle.gray, emoji="<:timeout_clock:1133464252162785311>")
    async def timeoutbutt(self, interaction: discord.Interaction, button):
        
        await interaction.response.send_modal(timeoutthr34564())
        
    @discord.ui.button(label='Cancel', custom_id='cancel342', style=discord.ButtonStyle.gray, emoji="<:Cancel:1133464880222048318>")
    async def cancelbutt(self, interaction: discord.Interaction, button):
        
        view = makesure()
        await interaction.message.edit(view=view)

    async def interaction_check(self, interaction: discord.MessageInteraction) -> None:
        role = discord.utils.get(interaction.guild.roles, name=f"Bal")
        if role not in interaction.user.roles:
            await interaction.response.send_message(content="You don't have permission to press this button.", ephemeral=True)
            return False
        return True
        
@bot.command(name='report', description='This allows people to report a user for misbehavior')
async def report(interaction:discord.Interaction, member: discord.Member, reason: str=None):
    
    if reason == None:
        reason='Reason not specified'
    
    time = datetime.now()
    time_str1 = time.strftime("%I:%M")

    time_meridian_part = time.strftime("%p")

    report_embed = discord.Embed(title='Moderation Bot | Report Command', description=f'{member.mention} was reported for the reason:\n\n ``{reason}``. \n\n Report sent by {interaction.user.mention}.', timestamp = datetime.now(), color=0x313338)
    thankyou_embed = discord.Embed(title='Moderation Bot | Report Command', description=f'Thank you for sending a report {interaction.user.mention}.', timestamp = datetime.now(), color=0x313338)
    thankyou_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
    guild = member.guild
    channel = guild.get_channel(int(report_message_channel))
    await interaction.response.send_message(embed = thankyou_embed, ephemeral=True)
    await channel.send(embed=report_embed, view=reportbutt())

#####################################################################################
#                                 Lockdown Command                                  #
#####################################################################################

@bot.command(name='lockdown', description='This allows you to lockdown a channel')
@app_commands.default_permissions(manage_channels=True)
async def lockdown(interaction: discord.Interaction, role: discord.Role=None, reason: str=None):
    
    role = role or interaction.guild.default_role
    
    time = datetime.now()
    time_str1 = time.strftime("%I:%M")

    time_meridian_part = time.strftime("%p")
    
    await interaction.channel.set_permissions(role, send_messages=False)
    lockdown_embed = discord.Embed(title='Moderation Bot | Lockdown Command', description=f'The channel {interaction.channel.mention} has been locked down by {interaction.user.mention} and for the reason: \n\n ``{reason}``\n\n The role that is not able to send a message is {role.mention}', color=0x313338)
    lockdown_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
    await interaction.response.send_message(embed=lockdown_embed)

#####################################################################################
#                                   Unlock Command                                  #
#####################################################################################

@bot.command(name='unlock', description='This allows you to unlock a channel that has been locked')
@app_commands.default_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction, role: discord.Role=None):
    
    role = role or interaction.guild.default_role
    
    time = datetime.now()
    time_str1 = time.strftime("%I:%M")

    time_meridian_part = time.strftime("%p")
    
    await interaction.channel.set_permissions(role, send_messages=True)
    unlock_embed = discord.Embed(title='Moderation Bot | Unlock Command', description=f'The channel {interaction.channel.mention} has been unlocked by {interaction.user.mention}', color=0x313338)
    unlock_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
    await interaction.response.send_message(embed=unlock_embed)

#####################################################################################
#                                       Logs                                        #
#####################################################################################

Logs = logs_channel

@client.event
async def on_message_delete(message):
    channel_id = Logs  # Replace with your desired channel ID
    Baller2345 = client.get_channel(channel_id)
    embed = discord.Embed(title = f"{message.author}'s Message was Deleted", description = f"Deleted Message: ``{message.content}``\nAuthor: {message.author.mention}\nLocation: {message.channel.mention}", timestamp = datetime.now(), colour=0x313338)
    embed.set_author(name = message.author.name, icon_url = message.author.display_avatar)
    await Baller2345.send(embed = embed)
    
@client.event
async def on_message_edit(before, after):
    Baller2345 = client.get_channel(Logs)
    embed = discord.Embed(title = f"{before.author} Edited Their Message", description = f"Before: {before.content}\nAfter: {after.content}\nAuthor: {before.author.mention}\nLocation: {before.channel.mention}", timestamp = datetime.now(), colour=0x313338)
    embed.set_author(name = after.author.name, icon_url = after.author.display_avatar)
    await Baller2345.send(embed = embed)
    
@client.event
async def on_member_update(before, after):
    Baller2345 = client.get_channel(Logs)
    if len(before.roles) > len(after.roles):
        role = next(role for role in before.roles if role not in after.roles)
        embed = discord.Embed(title = f"{before}'s Role has Been Removed", description = f"{role.name} was removed from {before.mention}.",  timestamp = datetime.now(), colour=0x313338)
    elif len(after.roles) > len(before.roles):
        role = next(role for role in after.roles if role not in before.roles)
        embed = discord.Embed(title = f"{before} Got a New Role", description = f"{role.name} was added to {before.mention}.",  timestamp = datetime.now(), colour=0x313338)
    elif before.nick != after.nick:
        embed = discord.Embed(title = f"{before}'s Nickname Changed", description = f"Before: {before.nick}\nAfter: {after.nick}",  timestamp = datetime.now(), colour=0x313338)
    else:
        return
    embed.set_author(name = after.name, icon_url = after.display_avatar)
    await Baller2345.send(embed = embed)
    
@client.event
async def on_guild_channel_create(channel):
    Baller2345 = client.get_channel(Logs)
    embed = discord.Embed(title = f"{channel.name} was Created", description = channel.mention, timestamp = datetime.now(), colour=0x313338)
    await Baller2345.send(embed = embed)
    
@client.event
async def on_guild_channel_delete(channel):
    z = client.get_channel(logs_channel)
    embed = discord.Embed(title = f"{channel.name} was Deleted", timestamp = datetime.now(), colour=0x313338)
    await z.send(embed = embed)

#####################################################################################
#                                  Welcome Events                                   #
#####################################################################################

##Join Event##
@client.event
async def on_member_join(member):
    guild = member.guild
    mc = guild.member_count
    channel = guild.get_channel(int(welcome_channel))
    avatar_url = member.avatar if member.avatar else member.default_avatar
    embed=discord.Embed(title=f"New Arrival",
    description=f'''
    Welcome {member.mention} to {server_name}. Below is some information to help navigate you around the server.

    **->** **Guild Information**
    <#{terms_of_service_channel}> = *Terms Of Service*
    <#{community_rules}> = *Community Rules*
    <#{ticket_system_channel}> = *Ticket System*
    <#{products_channel}> = *Products & Prices*
    
    **->** **Account Information**
    > UserName: ``{member.name}#{member.discriminator}``
    > User ID: ``{member.id}``
    ''',
    colour=0xEB1F2A)
    embed.set_image(url=f"{welcome_message_banner}")
    embed.set_thumbnail(url=f"{welcome_message_thumbnail}")
    embed.set_footer(text=f'You are our {mc} member')
    await channel.send(embed=embed)
  
##Leave Event##
@client.event
async def on_member_remove(member):
    guild = member.guild
    mc = guild.member_count
    channel = guild.get_channel(int(departure_channel))
    embed = discord.Embed(title=f"New Depature",
    description=f'''Goodbye {member.mention}
    
It looks like {member.mention} has decided to leave the community...
They will be missed
    ''',
    colour=0xEB1F2A)
    embed.set_image(url=f"{departure_message_banner}")
    embed.set_footer(text=f'We are now at {mc} members')
    embed.set_thumbnail(url=f"{departure_message_thumbnail}")
    await channel.send(embed=embed)

#####################################################################################
#                                  Warn command                                     #
#####################################################################################
   
data_folder = "Data"
db_file = os.path.join(data_folder, "warning_system.db")

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

db = sqlite3.connect(db_file)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS warns(warning_id INTEGER PRIMARY KEY, user INTEGER, reason TEXT, time INTEGER, guild INTEGER, timestamp REAL)")

async def get_warnings(interaction: discord.Interaction, member: discord.Member, messages, channel_name):
    user = member
    
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM warns WHERE user = ? AND guild = ?", (member.id, interaction.guild.id))
    data = cursor.fetchall()
    if data:
        embed = discord.Embed(title="User Warnings", color=0x313338)
        embed.set_author(name=user.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        for warn in data:
            warn_id, user_id, reason, time, guild_id = warn
            warn_time = datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
            embed.add_field(name=f"Warning ID: {warn_id}", value=f"Reason: {reason}\nTime: {warn_time}", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title="User Warnings", color=0x313338)
        embed.set_author(name=user.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="No Warnings", value=f"{member.mention} has no warnings.")
        await interaction.response.send_message(embed=embed)

@bot.command(name='warn', description='This is a warning command')
@app_commands.default_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason"):
    user = member
    channel = interaction.channel
    
    time = datetime.now()
    time_str1 = time.strftime("%I:%M")

    time_meridian_part = time.strftime("%p")
    
    embed = discord.Embed(title="Warning", color=0x313338)
    embed.set_author(name=user.display_name, icon_url=member.avatar.url)
    embed.add_field(name="Member:", value=member.mention)
    embed.add_field(name="Reason:", value=reason)
    embed.set_footer(text=f'{time_str1} {time_meridian_part}')
    await channel.send(embed=embed)

    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    
    try:
        timestamp = time.time()
        cursor.execute("INSERT INTO warns (user, guild, timestamp, reason) VALUES (?, ?, ?, ?)",
                       (member.id, interaction.guild.id, timestamp, reason))
        db.commit()
        
        cursor.execute("SELECT * FROM warns WHERE user = ? AND guild = ?", (member.id, interaction.guild.id))
        data = cursor.fetchall()
        
        if len(data) == 9:
            mute_message = f"{member.mention} has been warned {len(data)} times and is now temporarily muted."
            mute_embed = discord.Embed(title="Mute", description=mute_message, color=0x313338)
            await channel.send(embed=kick_message)
            await member.kick(reason="Exceeded warning limit")
            kick_message = f"{member.mention} has been kicked for not following rules."
            kick_embed = discord.Embed(title="Kick", description=kick_message, color=0x313338)
            kick_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
            await channel.send(embed=kick_embed)
        elif len(data) == 6:
            muteRole = discord.utils.get(interaction.guild.roles, name=f"{muted_role}")
            mute_message = f"{member.mention} has been warned {len(data)} times and is now temporarily muted."
            mute_embed = discord.Embed(title="Mute", description=mute_message, color=0x313338)
            mute_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
            await member.add_roles(muteRole)
            await member.remove_roles(MemberRole)
            await channel.send(embed=mute_embed)
            await asyncio.sleep(3600)
            await member.remove_roles(muteRole)
            await member.add_roles(MemberRole)
            unmute_message = f"{member.mention} You have been unmuted."
            unmute_embed = discord.Embed(title="Unmute", description=unmute_message, color=discord.Color.red)
            unmute_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
            await channel.send(embed=unmute_embed)
        elif len(data) == 3:
            muteRole = discord.utils.get(interaction.guild.roles, name=f"{muted_role}")
            MemberRole = discord.utils.get(interaction.guild.roles, name=f"{member_role}")
            mute_message = f"{member.mention} has been warned {len(data)} times and is now temporarily muted."
            mute_embed = discord.Embed(title="Mute", description=mute_message, color=0x313338)
            mute_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
            await member.add_roles(muteRole)
            await member.remove_roles(MemberRole)
            await channel.send(embed=mute_embed)
            await asyncio.sleep(600)
            await member.remove_roles(muteRole)
            await member.add_roles(MemberRole)
            unmute_message = f"{member.mention} You have been unmuted."
            unmute_embed = discord.Embed(title="Unmute", description=unmute_message, color=0x313338)
            unmute_embed.set_footer(text=f'{time_str1} {time_meridian_part}')
            await channel.send(embed=unmute_embed)
    
    except sqlite3.Error as e:
        print(f"Error while adding warning to database: {e}")
    finally:
        db.close()

#####################################################################################
#                                  Remove Warning Command                           #
#####################################################################################

@bot.command(name='remove_warning', description='This is a command to remove a warning by ID')
@app_commands.default_permissions(administrator=True)
async def removewarn(interaction: discord.Interaction, warn_id: int):
    channel = interaction.channel
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM warns WHERE rowid = ?", (warn_id,))
    data = cursor.fetchone()
    if data:
        cursor.execute("DELETE FROM warns WHERE rowid = ?", (warn_id,))
        embed = discord.Embed(title="Warning Removed", color=0x313338)
        embed.add_field(name="Warning ID:", value=warn_id)
        await channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Invalid Warning ID", color=0x313338)
        await channel.send(embed=embed)

    db.commit()

#####################################################################################
#                                  Remove Warnings Command                          #
#####################################################################################

@bot.command(name='remove_warnings', description='This is a command to remove all warnings from a user')
@app_commands.default_permissions(administrator=True)
async def removeallwarns(interaction: discord.Interaction, member: discord.Member):
    user = member
    
    channel = interaction.channel
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM warns WHERE user = ? AND guild = ?", (member.id, interaction.guild.id))
    data = cursor.fetchall()
    if data:
        cursor.execute("DELETE FROM warns WHERE user = ? AND guild = ?", (member.id, interaction.guild.id))
        embed = discord.Embed(title="Warnings Removed", color=0x313338)
        embed.set_author(name=user.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)
    else:
        embed = discord.Embed(title="No Warnings Found", color=0x313338)
        embed.set_author(name=user.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)

    db.commit()

#####################################################################################
#                                  Warnings Command                                 #
#####################################################################################
    
@bot.command(name='warnings', description='This command displays the number of warnings that a member of the community has.')
async def warnings(interaction: discord.Interaction, member: discord.Member):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM warns WHERE user = ? AND guild = ?", (member.id, interaction.guild.id))
        rows = cursor.fetchall()
        num_warnings = len(rows)

        embed = discord.Embed(title="Warning Information", color=0x313338)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Member:", value=member.mention)
        embed.add_field(name="Number of Warnings:", value=num_warnings)

        if num_warnings == 0:
            embed.add_field(name="", value="")
        else:
            for row in rows:
                warning_id = row[0]
                reason = row[2]
                timestamp = datetime.now().strftime("%I:%M %p")
                embed.add_field(name=f"Warning ID: {warning_id}             Reason: {reason}", value=f"", inline=False)
            embed.set_footer(text=f"Time: {timestamp}")

        await interaction.response.send_message(embed=embed, ephemeral=True)
    except sqlite3.Error as e:
        print(f"Error while fetching warnings from database: {e}")
    finally:
        cursor.close()
        db.close()

#####################################################################################
#                                  Info Command                                     #
#####################################################################################

bot.start_time = datetime.now()

@bot.command(name="info", description="Shows info about the bot")
async def info_command(interaction: discord.Interaction):
    uptime = datetime.now() - bot.start_time  # Calculate the bot's uptime
    uptime_str = str(uptime).split(".")[0]  # Remove milliseconds from the string

    embed = discord.Embed(
        title=f"**Bot Info**",
        color=0x313338,
        description=f'''
        **Version:** ``1.0.1``
        **Discord:** https://discord.gg/rMukhzE7hY
        **Creators:** __<@1065809062119358494>__ and __<@481065698127380500>__
        **Ping Latency:** ``{round(client.latency * 1000)}ms``
        **Uptime:** ``{uptime_str}``
        '''
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(token)