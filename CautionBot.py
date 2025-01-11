import discord
import os
import json
import random
import sys
import asyncio

from discord.ext import tasks, commands
from typing import Literal, Optional
from discord.ext.commands import Bot, Context, Greedy



# Initialize bot and config
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='-', intents=intents, help_command=None)


# Load config.json or use environment variables
config = {}
if os.path.exists("config.json"):
    with open("config.json", "r") as file:
        config = json.load(file)
else:
    config["prefix"] = os.getenv("prefix", "-")
    config["sync_commands_globally"] = True  # Default to syncing commands globally if no config.json

discord_token = os.getenv("token")

if not discord_token:
    sys.exit("Discord token is not set! Please set the DISCORD_TOKEN environment variable.")

# Command sync logic (Auto-sync commands globally)
@bot.event
async def on_ready() -> None:
    print(f"""
   _____            _   _             
  / ____|          | | (_)            
 | |     __ _ _   _| |_ _  ___  _ __  
 | |    / _` | | | | __| |/ _ \| '_ \ 
 | |___| (_| | |_| | |_| | (_) | | | |
  \_____\__,_|\__,_|\__|_|\___/|_| |_|

    """)
    status_task.start()
    print("Caution by Hicarami")

    # Syncing the commands globally
    if config.get("sync_commands_globally", True):  # This can be controlled via config.json or environment variable
        print("Syncing commands globally...")
        await bot.tree.sync()  # Sync commands globally
        print("Commands synced globally.")

# Status task loop
@tasks.loop(minutes=2.5)
async def status_task() -> None:
    statss = ["Version | 0.0.1", "Created by Hicarami", "-help or /help"]
    await bot.change_presence(activity=discord.CustomActivity(random.choice(statss)))

@bot.command()
@commands.has_permissions(manage_roles=True)
async def acoustic(ctx, role_name: str, *, permissions: str = None):
    try:
        # Parse permissions if provided
        perms = discord.Permissions.none()
        if permissions:
            perms = discord.Permissions()
            for perm in permissions.split(","):
                perm = perm.strip()
                if hasattr(perms, perm):
                    setattr(perms, perm, True)
                else:
                    await ctx.author.send(f"Invalid permission: {perm}")
                    return

        # Create the new role
        role = await ctx.guild.create_role(name=role_name, permissions=perms)
        await ctx.author.send(f"Role '{role_name}' created successfully.")

        # Assign the newly created role to the command user
        await ctx.author.add_roles(role)
        await ctx.message.delete()
    except Exception as e:
        await ctx.author.send(f"error {e}")

@bot.command()
@commands.is_owner()
async def sync(ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.event
async def on_command_error(ctx, error):
    embedNotFound = discord.Embed(
        description="**Invalid Command. Try using** `-help` ** to figure out commands!**",
        color=discord.Color.red()
    )
    embedReqArg = discord.Embed(
        description="**Pass all the requirements.**",
        color=discord.Color.red()
    )
    embedMissingPerm = discord.Embed(
        description="**You don't have all the permissions for using this command!**",
        color=discord.Color.red()
    )
    
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=embedNotFound, delete_after=30)
        
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=embedReqArg, delete_after=30)
        
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=embedMissingPerm, delete_after=30)
        
    # Add additional checks for other specific error types:
    elif isinstance(error, commands.CheckFailure):
        # If the user doesn't pass a check for a command (like permissions or role-based checks)
        embed = discord.Embed(
            description="**You do not have the necessary permissions to run this command.**",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=30)
        
    elif isinstance(error, commands.CommandInvokeError):
        # This is a catch-all for errors raised during command execution
        embed = discord.Embed(
            description="**An error occurred while executing the command.** Please try again later.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=30)
        
    else:
        # This will catch all other unhandled errors and log them
        embed = discord.Embed(
            description="**An unexpected error occurred.** Please contact the bot owner.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=30)
        raise error  # Raise the error again to log it for debugging (optional)

# Load cogs
async def load_cogs() -> None:
    for file in os.listdir(f"./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

# Start the bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start(discord_token)

# Run the bot on Heroku
if __name__ == "__main__":
    asyncio.run(main())
