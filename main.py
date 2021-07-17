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
	print(str(channel))


client.run(token)