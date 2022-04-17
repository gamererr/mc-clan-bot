import discord
import asyncio
from dotenv import dotenv_values
import extra

intents = discord.Intents.all()
client = discord.Bot()

config = extra.config({
	**dict(dotenv_values('example.env')),
	**dict(dotenv_values('.env'))
})

clan_group = client.create_group("clan","Do things involving clans",guild_ids=[config.GUILD])
edit_group = clan_group.create_subgroup("edit","Modify your clan in certain ways",)

guild:discord.Guild = None
inClan:discord.Role = None
leader:discord.Role = None
clans:discord.CategoryChannel = None
clanBorder:discord.Role = None

@client.event
async def on_ready():
	print(f"logged in as {client.user}")
	global inClan, leader, clans, clanBorder, guild
	guild = await client.fetch_guild(config.GUILD)
	inClan = guild.get_role(config.INCLAN)
	leader = guild.get_role(config.LEADER)
	clanBorder = guild.get_role(config.CLANBORDER)
	clans = await guild.fetch_channel(config.CLANS)
	print(f"ready!")

async def can_run_clan_command(ctx:discord.ApplicationContext):
	if inClan not in ctx.author.roles:
		raise extra.CheckFailedError
	elif leader not in ctx.author.roles:
		raise extra.CheckFailedError

class InviteView(discord.ui.View):
	def __init__(self,invitedTo,invitee):
		self.invitedTo = invitedTo
		self.invitee = invitee
		super().__init__()

	@discord.ui.button(label="Accept",style=discord.ButtonStyle.primary,emoji="✅")
	async def accept_callback(self,button,interaction):
		# await ctx.author.send(f"{self.invitee.display_name} accepted the invite")
		await self.invitee.send(f"you joined {self.invitedTo.name}!")
		await self.invitee.add_roles(self.invitedTo)
		await self.invitee.add_roles(inClan)

edit_group.checks.append(can_run_clan_command)

# VVVVVV commands VVVVVV'

@clan_group.command(description="make a clan")
async def make(ctx:discord.ApplicationContext, name:discord.Option(str,"Name of the clan"), color:discord.Option(str,"color code in hex format") = None):
	rgb_color = discord.Colour(int(color,16)) if color else discord.Colour.default()
	if inClan in ctx.author.roles:
		await ctx.respond("you are already in a clan, leave to make a clan",ephemeral=True)
		return
	await ctx.author.add_roles(inClan)
	role = await guild.create_role(name=name, colour=rgb_color)
	await ctx.author.add_roles(role)
	await ctx.author.add_roles(leader)

	channel = await clans.create_text_channel(name=name, overwrites={guild.default_role:discord.PermissionOverwrite(view_channel=False),role:discord.PermissionOverwrite(view_channel=True)})

	await ctx.respond(f"made clan {role.mention}")

@clan_group.command(description="leave a clan, obviously")
async def leave(ctx):
	for x in guild.roles:
		if x in ctx.author.roles and x.position <= clanBorder.position and x.position != 0:
			leaving = x

	if leader in ctx.author.roles and len(leaving.members) != 1:
		await ctx.respond("you own your clan, transfer it to leave",ephemeral=True)
		return
	elif inClan in ctx.author.roles:
		await ctx.respond(f"you left clan {leaving.name}",ephemeral=True)
	elif inClan not in ctx.author.roles:
		await ctx.respond("you are not in a clan",ephemeral=True)
		return

	
	await ctx.author.remove_roles(leaving)
	await ctx.author.remove_roles(inClan)
	await ctx.author.remove_roles(leader)

@clan_group.command(description="admin only, delete a clan")
async def remove(ctx, role):

	role:discord.Role = ctx.message.role_mentions[0]

	if ctx.channel.permissions_for(ctx.author).manage_guild:
		for x in guild.roles:
			if x == role and x.position <= clanBorder.position and x.position != 0:
				# await ctx.respond(f"removing clan {x}...")
				role = x
				break

		for x in role.members:
			await x.remove_roles(inClan)
			await x.remove_roles(leader)
		await ctx.respond(f"done! clan had {len(role.members)} members")
		await role.delete()

@clan_group.command(description="transfer ownership of a clan")
async def transfer(ctx:discord.ApplicationContext, new_owner:discord.Member):
	if not leader in ctx.author.roles:
		await ctx.respond("you do not own your clan",ephemeral=True)
		return

	for x in guild.roles:
		if x in ctx.author.roles and x in new_owner.roles and x.position <= clanBorder.position and x.position != 0:
			clan = x
			break
		else:
			clan = None
			break
		
	if clan == None:
		await ctx.respond(f"you and {new_owner.display_name} arent in the same clan",ephemeral=True)
		return
	else:
		await ctx.author.remove_roles(leader)
		await new_owner.add_roles(leader)
		await ctx.respond(f"transfered ownership of {clan.name} to {new_owner.display_name}",ephemeral=True)

@clan_group.command(description="kick a member from a clan")
async def kick(ctx, kicked:discord.Member):
	if ctx.author == kicked or not leader in ctx.author.roles:
		await ctx.respond("you don't own your clan",ephemeral=True)
		return

	for x in guild.roles:
		if x in ctx.author.roles and x in kicked.roles and x.position <= clanBorder.position and x.position != 0:
			clan = x
			break
		else:
			clan = None
		
	if clan == None:
		await ctx.respond(f"you and {kicked.display_name} arent in the same clan",ephemeral=True)
		return
	else:
		await kicked.remove_roles(clan)
		await kicked.remove_roles(inClan)
		await ctx.respond(f"kicked {kicked.display_name} from {clan.name}")

@clan_group.command(description="invite a user to your clan")
async def invite(ctx, invitee:discord.Member):
	if inClan in invitee.roles:
		await ctx.respond(f"{invitee.display_name} is already in a clan",ephemeral=True)
		return
	if not leader in ctx.author.roles:
		await ctx.respond("you do not own your clan",ephemeral=True)
		return

	for x in guild.roles:
		if x in ctx.author.roles and x.position <= clanBorder.position and x.position != 0:
			invitedTo = x
	
	await ctx.respond(f"invited {invitee.display_name} to {invitedTo.name}!",ephemeral=True)
	await invitee.send(f"{ctx.author.mention} invited you to thier guild, {invitedTo.name} do you accept?",view=InviteView(invitedTo,invitee))

	# try:
	# 	reaction, user = await client.wait_for('reaction_add', timeout=3600, check=check)
	# except asyncio.TimeoutError:
	# 	await ctx.author.send(f"{invitee.display_name} didnt accept the invite in time")
	# 	await invitee.send("invite timed out")
	# 	return
	# print("2")
	# await ctx.author.send(f"{invitee.display_name} accepted the invite")
	# print("3")
	# await invitee.send(f"you joined {invitedTo.name}!")
	# await invitee.add_roles(invitedTo)
	# await invitee.add_roles(inClan)

@edit_group.command(description="change the name of your clan")
async def name(ctx:discord.ApplicationContext, name:str):
	for x in guild.roles:
		if x in ctx.author.roles and x.position <= clanBorder.position and x.position != 0:
			clan = x
			break
		else: return
	
	await clan.edit(name=name)
	await ctx.respond(f"edited your clan {clan.name} to its new name")

@edit_group.command(description="change the color of your clan")
async def color(ctx:discord.ApplicationContext,color:discord.Option(str,"color code in hex format")):
	for x in guild.roles:
		if x in ctx.author.roles and x.position <= clanBorder.position and x.position != 0:
			clan = x
			break
		else: return
	
	rgb_color = discord.Colour(int(color,16))
	
	await clan.edit(colour=rgb_color)
	await ctx.respond(f"edited clan {clan.name} to its new color")

@clan_group.command()
async def list(ctx:discord.ApplicationContext):
	embed = discord.Embed(title="List of clans")
	embed.description = "\n".join( [i.mention for i in guild.roles if i.position < clanBorder.position and i != guild.default_role and len(i.members) > 0 ] )
	await ctx.respond(embed=embed,allowed_mentions=discord.AllowedMentions.none(),ephemeral=True)

client.run(config.TOKEN)