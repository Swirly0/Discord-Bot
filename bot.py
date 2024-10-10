import discord
import os # default module
from dotenv import load_dotenv
import challonge
import challenge

load_dotenv() # load all the variables from the env file
bot = discord.Bot()
challonge.set_credentials("Swirly_", os.getenv('APIKEY'))

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

@bot.slash_command(name="param-test", description="test")
# pycord will figure out the types for you
async def param_test(ctx: discord.ApplicationContext, bracket_name: discord.Option(str), 
                     url: discord.Option(str), 
                     tournament_type: discord.Option(str),
                     game_name: discord.Option(str)):
  # you can use them as they were actual integers
  await ctx.respond(f"Bracket name: {bracket_name}\nurl: {url}\ntournament_type: {tournament_type}\ngame_name: {game_name}")

#BUTTON
class MyView(discord.ui.View):
    def __init__(self, bracket_id):
        super().__init__()
        self.bracket_id = bracket_id  # Store the bracket ID for use in the button callback

    @discord.ui.button(label="CLICK TO BE ADDED TO THE BRACKET", style=discord.ButtonStyle.primary, emoji="😎")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        user = interaction.user.display_name  # Get the display name of the user who clicked the button
        print(user)

        challenge.add_participant(self.bracket_id, user)  # Use the bracket ID when adding the participant
        await interaction.response.send_message(content=f"Added {user} to the bracket!", ephemeral=True)

#CREATE TOURNEY
@bot.slash_command(name="create-bracket", description="Creates a challonge bracket")
async def create_bracket(ctx: discord.ApplicationContext, 
                         title: discord.Option(str, description="Title for the bracket"), 
                         id: discord.Option(str, description="the unique ending of the line. ex: https://challonge.com/ID"), 
                         tourney_type: discord.Option(str, choices=["single elimination", "double elimination"]),
                         have_button: discord.Option(bool, default=False, required=False, choices=[False, True]),
                         have_embed: discord.Option(bool, default=True, required=False, choices=[False, True])):
    
    tourney = challenge.create_tourney(title, id, tourney_type)

    if not tourney:
        await ctx.respond("URL is taken or invalid!")
    else:
        embed = discord.Embed(
            title=title,
            description=f"Bracket Link: {tourney}",
            color=discord.Color.dark_purple()
        )
        embed.set_author(name="Swirly's Bot")
        embed.set_image(url="https://i.ytimg.com/vi/58a9_OtYS5w/maxresdefault.jpg")
        embed.set_footer(text=challenge.entrant_num(id))
        if have_button and have_embed:
            await ctx.respond(embed=embed, view=MyView(bracket_id=id))
        elif have_button:
            await ctx.respond(tourney, view=MyView(bracket_id=id))
        elif have_embed:
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(tourney)

#ADD A PLAYER
@bot.slash_command(name="add-player", description="adds someone")
async def create_bracket(ctx: discord.ApplicationContext, url: discord.Option(str), name: discord.Option(str)):
    player = challenge.add_participant(url, name)
    await ctx.respond(player)

#ADD MULTIPLE PLAYERS
@bot.slash_command(name="bulk-add-player", description="adds people")
async def create_bracket(ctx: discord.ApplicationContext, 
                         url: discord.Option(str), 
                         names: discord.Option(str, description="Separate by a space. Ex: swirly ace poket kemono")):
    name_list = names.split()
    # print(name_list)
    player = challenge.bulk_add(url, name_list)
    
    await ctx.respond(player)

#REMOVE A PLAYER
@bot.slash_command(name="remove-player", description="remove someone")
async def create_bracket(ctx: discord.ApplicationContext, url: discord.Option(str), name: discord.Option(str)):

    player = challenge.remove_participant(url, name)
    
    await ctx.respond(player)

@bot.slash_command(name="random-seeding", description="Randomizes the seeding of a bracket.")
async def create_bracket(ctx: discord.ApplicationContext, 
                         url: discord.Option(str, description="id for the tourney to randomize.")):

    seed = challenge.random_seeding(url)
    
    await ctx.respond(seed)

@bot.slash_command(name="delete-tourney", description="DANGEROUS")
async def create_bracket(ctx: discord.ApplicationContext, 
                         url: discord.Option(str, description="id for the tourney to delete.")):
    print(ctx.author.id)
    if ctx.author.id == 264934913751384064:
        delete = challenge.delete_bracket(url)
        await ctx.respond(delete)
    else:
        await ctx.respond("ONLY SWIRLY CAN DELETE")

@bot.slash_command(name="view-tourney", description="creates an embed")
async def create_bracket(ctx: discord.ApplicationContext, 
                         url: discord.Option(str, description="id for the tourney to delete.")):
    
    tourney = challenge.view_tourney(url)
    # print(tourney["name"])
    # print(tourney["live_image_url"])
    embed = discord.Embed(
            title=tourney["name"],
            description=f"Bracket Link: {tourney["full_challonge_url"]}",
            color=discord.Color.dark_purple()
        )
    # print(challenge.get_completed(url))
    # print(challenge.entrant_num(url))

    embed.add_field(name="Winner:", value=challenge.display_winner(url))
    embed.set_author(name="Challonge")
    embed.set_image(url="https://i.ytimg.com/vi/58a9_OtYS5w/maxresdefault.jpg")
    embed.set_footer(text=f"{challenge.entrant_num(url)} entrants ")

    print(challenge.display_winner(url))

    await ctx.respond(embed=embed)

bot.run(os.getenv('TOKEN')) # run the bot with the token