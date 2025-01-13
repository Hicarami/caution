import discord
from discord.ext import commands
from discord.ui import Button, View

class Paginator(View):
    def __init__(self, embeds, user):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current_page = 0
        self.user = user  # Store the user who invoked the command
        self.update_buttons()

    def update_buttons(self):
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == len(self.embeds) - 1

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't interact with this!", ephemeral=True)
            return

        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't interact with this!", ephemeral=True)
            return

        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embeds = []
        self.update_command_pages()

    def update_command_pages(self):
        self.embeds.clear()

        EXCLUDED_COMMANDS = ["clearbotmessages", "command2", "command3"]  # Exclude specific commands

        # Group commands by their cog (category)
        categories = {}
        for command in self.bot.commands:
            if command.name in ["help"] or command.cog_name is None or command.name in EXCLUDED_COMMANDS:
                continue

            category = command.cog_name or "No Category"
            if category not in categories:
                categories[category] = []
            categories[category].append(command)

        for category, commands_list in categories.items():
            command_descriptions = [
                f"**/{command.name}**: {command.description or 'No description provided'}"
                for command in commands_list
            ]

            embed = discord.Embed(
                title=f"**{category.upper()} COMMANDS**",
                description="\n".join(command_descriptions),
                color=discord.Color.blue()
            )
            self.embeds.append(embed)

        cover_page = discord.Embed(
            title="** BOT COMMANDS :dividers: **",
            description="Press the button to view a list of commands categorized for *CautionBot*",
            color=discord.Color.green()
        ).set_image(
            url="https://media.discordapp.net/attachments/1048271893444177930/1276102466894827583/commands.png?ex=66c84e88&is=66c6fd08&hm=4ebda42459a81547a97c43b1d83b4786445c2f0de6cd2bf853eb75507301ccd9&=&format=webp&quality=lossless"
        )
        self.embeds.insert(0, cover_page)

    @commands.hybrid_command(name="help", description="Displays the list of bot commands categorized by type")
    async def help(self, ctx):
        # Update the embeds to include the user's avatar
        for embed in self.embeds:
            embed.set_footer(text="CautionBot by Hicarami", icon_url=ctx.author.avatar.url)

        view = Paginator(self.embeds, ctx.author)  # Pass the invoking user to Paginator
        await ctx.reply(embed=self.embeds[0], view=view, ephemeral=True)  # Make the response ephemeral

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_command_pages()

    @commands.Cog.listener()
    async def on_command_add(self, command):
        self.update_command_pages()

async def setup(bot):
    await bot.add_cog(Help(bot))
