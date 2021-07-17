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

	if inClan in ctx.author.roles:
		await ctx.send("you are already in a clan, leave to make a clan")
		return
	else:
		await ctx.send(f"making clan {name}")
		await ctx.author.add_roles(inClan)

	role:discord.Role = await ctx.guild.create_role(name=name, colour=color)
	await ctx.author.add_roles(role)

	clans:discord.CategoryChannel = ctx.guild.get_channel(865650519434461206)

	channel:discord.TextChannel = await clans.create_text_channel(name=name, overwrites={ctx.guild.default_role:discord.PermissionOverwrite(view_channel=False),role:discord.PermissionOverwrite(view_channel=True)})

	await ctx.send(f"made clan {role.mention}")

@client.command()
async def leave(ctx):
	
	inClan:discord.Role = ctx.guild.get_role(865713278860656661)
	clanBorder:discord.Role = ctx.guild.get_role(865819163087994911)

	if inClan in ctx.author.roles:
		await ctx.send("leaving clan...")
	else:
		await ctx.send("you are not in a clan")
		return

	for x in ctx.guild.roles:
		if x in ctx.author.roles and x.position <= clanBorder.position and x.position != 0:
			print(x)
			await ctx.author.remove_roles(x)
			await ctx.author.remove_roles(inClan)
			left = x

	await ctx.send(f"you left clan {left.name}")

@client.command()
async def remove(ctx, role):
	role = role.replace("<", "")
	role = role.replace(">", "")
	role = role.replace("&", "")
	role = role.replace("@", "")

	role:discord.Role = ctx.guild.get_role(int(role))
	inClan:discord.Role = ctx.guild.get_role(865713278860656661)
	clanBorder:discord.Role = ctx.guild.get_role(865819163087994911)

	if ctx.channel.permissions_for(ctx.author).administrator:
		for x in ctx.guild.roles:
			if x == role and x.position <= clanBorder.position and x.position != 0:
				await ctx.send(f"removing clan {x}...")
				role = x
				break

		tempCount = 0
		for x in role.members:
			await x.remove_roles(inClan)
			tempCount += 1
		await role.delete()
		await ctx.send(f"done! clan had {tempCount} members")


client.run(token)