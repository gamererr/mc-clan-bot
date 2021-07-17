import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix='clan ', intents=intents)

@client.event
async def on_ready():
	print(f"hello world")

with open("tokenfile", "r") as tokenfile: token=tokenfile.read()

# VVVVVV commands VVVVVV'

@client.command()
async def make(ctx, name, *color):
	if color == []: color = discord.Colour.default()
	else:
		colortemp = []
		for x in color:
			colortemp.append(int(x))
		color = discord.Colour.from_rgb(int(color[0]), int(color[1]), int(color[2]))

	inClan:discord.Role = ctx.guild.get_role(865713278860656661)
	leader:discord.Role = ctx.guild.get_role(865992562364252163)

	if inClan in ctx.author.roles:
		await ctx.send("you are already in a clan, leave to make a clan")
		return
	else:
		await ctx.send(f"making clan {name}")
		await ctx.author.add_roles(inClan)

	role:discord.Role = await ctx.guild.create_role(name=name, colour=color)
	await ctx.author.add_roles(role)
	await ctx.author.add_roles(leader)

	clans:discord.CategoryChannel = ctx.guild.get_channel(865650519434461206)

	channel:discord.TextChannel = await clans.create_text_channel(name=name, overwrites={ctx.guild.default_role:discord.PermissionOverwrite(view_channel=False),role:discord.PermissionOverwrite(view_channel=True)})

	await ctx.send(f"made clan {role.mention}")

@client.command()
async def leave(ctx):
	
	inClan:discord.Role = ctx.guild.get_role(865713278860656661)
	clanBorder:discord.Role = ctx.guild.get_role(865819163087994911)
	leader:discord.Role = ctx.guild.get_role(865992562364252163)

	for x in ctx.guild.roles:
		if x in ctx.author.roles and x.position <= clanBorder.position and x.position != 0:
			leaving = x

	if leader in ctx.author.roles and len(leaving.members) != 1:
		await ctx.send("you own your clan, transfer it to leave")
		return
	elif inClan in ctx.author.roles:
		await ctx.send(f"you left clan {leaving.name}")
	elif inClan not in ctx.author.roles:
		await ctx.send("you are not in a clan")
		return

	
	await ctx.author.remove_roles(leaving)
	await ctx.author.remove_roles(inClan)
	await ctx.author.remove_roles(leader)

@client.command()
async def remove(ctx, role):

	role:discord.Role = ctx.message.role_mentions[0]
	inClan:discord.Role = ctx.guild.get_role(865713278860656661)
	clanBorder:discord.Role = ctx.guild.get_role(865819163087994911)
	leader:discord.Role = ctx.guild.get_role(865992562364252163)

	if ctx.channel.permissions_for(ctx.author).manage_guild:
		for x in ctx.guild.roles:
			if x == role and x.position <= clanBorder.position and x.position != 0:
				await ctx.send(f"removing clan {x}...")
				role = x
				break

		for x in role.members:
			await x.remove_roles(inClan)
			await x.remove_roles(leader)
		await ctx.send(f"done! clan had {len(role.members)} members")
		await role.delete()

@client.command()
async def transfer(ctx, newOwner):

	newOwner = ctx.mentions[0]

	leader:discord.Role = ctx.guild.get_role(865992562364252163)
	clanBorder:discord.Role = ctx.guild.get_role(865819163087994911)

	if not leader in ctx.author.roles:
		return

	for x in ctx.guild.roles:
		if x in ctx.author.roles and x in newOwner.roles and x.position <= clanBorder.position and x.position != -1:
			clan = x
			break
		else:
			clan = None
			break
		
	if clan == None:
		await ctx.send(f"you and {newOwner.display_name} arent in the same clan")
		return
	else:
		await ctx.author.remove_roles(leader)
		await newOwner.add_roles(leader)
		await ctx.send(f"transfered ownership of {clan.name} to {newOwner.display_name}")

@client.command()
async def kick(ctx, kicked):

	kicked = ctx.message.mentions[0]

	leader:discord.Role = ctx.guild.get_role(865992562364252163)
	inClan:discord.Role = ctx.guild.get_role(865713278860656661)
	clanBorder:discord.Role = ctx.guild.get_role(865819163087994911)

	if ctx.author == kicked or not leader in ctx.author.roles:
		return

	for x in ctx.guild.roles:
		if x in ctx.author.roles and x in kicked.roles and x.position == clanBorder.position:
			clan = x
			break
		else:
			clan = None
		
	if clan == None:
		await ctx.send(f"you and {kicked.display_name} arent in the same clan")
		return
	else:
		await kicked.remove_roles(clan)
		await kicked.remove_roles(inClan)
		await ctx.send(f"kicked {kicked.display_name} from {clan.name}")


client.run(token)