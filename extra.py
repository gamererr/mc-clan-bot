# modified from https://github.com/jackbotgames/jackbot/

# import discord
# from discord.ext import	commands
from enum import Enum,auto

import discord

class config:
	# __slots__ = ["TOKEN","INCLAN","LEADER","CLANS","CLANBORDER","GUILD"]
	def __init__(self,from_dict):
		self.TOKEN:str = from_dict['TOKEN']
		self.INCLAN = int(from_dict['INCLAN'])
		self.LEADER = int(from_dict['LEADER'])
		self.CLANS = int(from_dict['CLANS'])
		self.CLANBORDER = int(from_dict['CLANBORDER'])
		self.IGNORE = int(from_dict['IGNORE'])
		self.GUILD = int(from_dict['GUILD'])


class EditTypes(Enum):
	EDIT = auto()
	COLOR = auto()

class CheckFailedError(discord.ApplicationCommandError): pass