import discord
from discord.ext import commands
import logging

# --- Bot Setup ---
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True  # Required for message events
intents.members = True         # Required for on_member_join

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Constants ---
SECRET_ROLE = "Gamer"  # UPPERCASE for constants
TOKEN = "token"  # Paste your token directly here

# --- Events ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_member_join(member):
    try:
        await member.send(f"Welcome to the server, {member.name}!")
    except discord.Forbidden:
        print(f"Could not DM {member.name} (DMs closed)")

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Ignore self
        return

    if "shit" in message.content.lower():  # Bad word filter
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} - Please avoid using that word!",
            delete_after=5.0  # Auto-deletes after 5 sec
        )

    await bot.process_commands(message)  # Required for commands to work

# --- Commands ---
@bot.command()
async def hello(ctx):
    """Says hello to the user"""
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    """Assigns the secret role to the user"""
    role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now a {SECRET_ROLE}!")
    else:
        await ctx.send(f"Role '{SECRET_ROLE}' not found.")

@bot.command()
async def remove(ctx):
    """Removes the secret role from the user"""
    role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{SECRET_ROLE} role removed from {ctx.author.mention}.")
    else:
        await ctx.send(f"Role '{SECRET_ROLE}' not found.")

@bot.command()
async def dm(ctx, *, msg: str):
    """Sends your message back to you via DM"""
    await ctx.author.send(f"You said: {msg}")
    await ctx.message.delete()  # Deletes the command message

@bot.command()
async def reply(ctx):
    """Replies to your message"""
    await ctx.reply("This is a reply!")

@bot.command()
async def poll(ctx, *, question: str):
    """Creates a simple yes/no poll"""
    embed = discord.Embed(
        title="📊 Poll",
        description=question,
        color=discord.Color.blue()
    )
    poll_msg = await ctx.send(embed=embed)
    await poll_msg.add_reaction("👍")
    await poll_msg.add_reaction("👎")

@bot.command()
@commands.has_role(SECRET_ROLE)
async def secret(ctx):
    """Secret command for special role"""
    await ctx.send("🔐 Welcome to the secret club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("🚫 You don't have permission for this command!")

# --- Run the Bot ---
if __name__ == "__main__":
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("Please replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token")
    
    try:
        bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
    except discord.LoginFailure:
        print("Invalid Discord token. Please check your token.")

