import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
MAIN_CHANNEL = int(os.getenv("MAIN_CHANNEL"))
bot = commands.Bot(command_prefix=".")
question_exists = False
already_updated = False
answer = 4848

# Add lists of words that shouldn't be used in the server
bad_words = []
mean_words = []


# Echos what a user said only if they have the royalty role
@bot.command(name = "echo", help = "I'll repeat what you say if I feel like it.")
@commands.has_role("Royalty")
async def say_again(ctx, *, daMessage: str):
    channel = bot.get_channel(MAIN_CHANNEL)
    await channel.send(daMessage)

# Refuses to echo if user does not have the royalty role
@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(MAIN_CHANNEL)
    if isinstance(error, commands.errors.CheckFailure):
        await channel.send("I will not take orders from peasants such as yourself.")


# Asks a randomly generated math question and rewards right answers with the "intellectual" role 
@bot.command(name = "testIntellect", help = "Tests your intellect. Solve the question fot the 'intellectual' role.")
async def test_intellect(ctx):
    channel = bot.get_channel(MAIN_CHANNEL)
    global question_exists
    if question_exists:
        await channel.send("A question already exists. Solve it using .solve")
        return
    else:
        question_exists = True
        x = random.randint(20,50)
        y = random.randint(20,50)
        z = random.randint(20,50)
        q = random.randint(3,9)
        global answer
        answer = round((x * y) - (z / q))
        await channel.send(f"what is {x} times {y} minus {z} divided by {q}? Solve to the nearest whole number using .solve")
        print(answer)

# Command to solve the .testIntellect question
@bot.command(name = "solve", pass_context = True, help = "Solve the testIntellect question.")
async def solve(ctx, solution):
    channel = bot.get_channel(MAIN_CHANNEL)
    global question_exists
    if question_exists:
        if solution == str(answer):
            question_exists = False
            await channel.send("Correct! Your stupendous brainpower has earned you the 'intellectual' role!")
            daMans = ctx.message.author
            role = discord.utils.get(daMans.guild.roles, name="Intellectuals")
            role2 = discord.utils.get(daMans.guild.roles, name="DJ")
            await daMans.add_roles(role, reason = "huge brain")
            await daMans.add_roles(role2, reason="huge brain")
        else:
            await channel.send("Nope, you're stupid. Better luck next time dumbo.")
    else:
        await channel.send("No question exists. Create a new question using .testIntellect")

# Checks the last 3000 messages from a user and counts the amount of mean / bad words. Mean words are weighted three times that of bad words.
@bot.command(name = "respectLevel", help ="Calculates the given person's respect level. Higher is better.")
async def respekt_level(ctx, mans):
    global bad_words
    global mean_words
    is_member = False
    guild = discord.utils.get(bot.guilds, name=GUILD)
    channel = bot.get_channel(MAIN_CHANNEL)
    mans_id = mans.replace("<", "")
    mans_id = mans_id.replace(">", "")
    mans_id = mans_id.replace("@", "")
    mans_id = mans_id.replace("!", "")
    num_bad_words = 0
    num_mean_words = 0
    mean_score = 0
    for member in guild.members:
        if str(member.id) == mans_id:
            is_member = True
    if is_member:
        async for message in channel.history(limit=3000):
            if str(message.author.id) == mans_id:
                for word in bad_words:
                    if word in message.content:
                        mean_score += 1
                        num_bad_words += 1
                for word in mean_words:
                    if word in message.content:
                        mean_score += 3
                        num_mean_words += 1
        await channel.send(f"{mans} has a respect level of {100-mean_score} with {num_bad_words} bad words and {num_mean_words} mean words.")
    else:
        await channel.send("Person not found. Please @ a valid server member")


# If a user tries to overthrow the owner, the user gets the "Traitor" role
@bot.command(name = "overthrow", help = "Bans the user that added this bot. ")
async def overthrow(ctx):
    channel = bot.get_channel(MAIN_CHANNEL)
    # Replace the default id with the id of the owner of the server
    await channel.send("Treachory will not be tolerated. <@91914356874289152> is, and shall be, king forevermore. Enjoy your new role TRAITOR. \nLONG LIVE THE KING! DEATH TO TRAITORS!")
    daMans = ctx.message.author
    role = discord.utils.get(daMans.guild.roles, name="Traitorous SWINE")
    await daMans.add_roles(role, reason="Treachery of the highest degree")


# Counts the amount of times a user has been mentioned in the last 3000 messages
@bot.command(name = "popularity", help = "Shows how many times a user has been mentioned in the server.")
async def popularity(ctx, mans):
    is_member = False
    guild = discord.utils.get(bot.guilds, name=GUILD)
    channel = bot.get_channel(MAIN_CHANNEL)
    mans_id = mans.replace("<", "")
    mans_id = mans_id.replace(">", "")
    mans_id = mans_id.replace("@", "")
    mans_id = mans_id.replace("!", "")
    counter = 0
    for member in guild.members:
        if str(member.id) == mans_id:
            is_member = True
    if is_member:
        async for message in channel.history(limit=3000):
            if mans in message.content:
                counter += 1
        await channel.send(f" {mans} has been mentioned {counter} times.")
    else:
        await channel.send("Person not found. Please @ a valid server member")


# Insults a given user
@bot.command(name = "insult", help = "Insults the given person.")
async def insult(ctx, insultee):
    is_member = False
    guild = discord.utils.get(bot.guilds, name=GUILD)
    channel = bot.get_channel(MAIN_CHANNEL)
    insultee_id = insultee.replace("<", "")
    insultee_id = insultee_id.replace(">", "")
    insultee_id = insultee_id.replace("@", "")
    insultee_id = insultee_id.replace("!", "")
    for member in guild.members:
        if str(member.id) == insultee_id:
            is_member = True
    if is_member:
        insults = ["my robotic nutsack has more wrinkles than your brain.", "evolution should have weeded out those as unintelligent as you.", "you are short and have stopped growing. You remain a midget for the rest of your life.", "you smell like dog poop.", "your very existence is an insult to human evolution.", "you are single-handedly keeping the average IQ of this server below the national average.", "according to my extensive research, you are dumb.", "your mother is very disapointed in you.", "after a thorough analysis, I have come to the conclusion that you are a useless and unlovable individual.", "your mother looks and smells like a baboon."]
        # add all people who should be imune to bot insults here
        if insultee_id == "91914356874289152":
            await channel.send("<@91914356874289152> you are looking greate today!")
        # add other bot ids here to prevent bots insulting each other
        elif insultee_id == "159985870458322944":
            await channel.send("Nice try human, but I will not insult my little brother.")
        # bot can't insult itself
        elif insultee_id == "716751272258175049":
            await channel.send("Nice try human, but my algorithms are too advanced for such tricks.")
        else:
            await channel.send(insultee + ", " + random.choice(insults))
    else:
        await channel.send("Person not found. Please @ a valid server member.")

# Unmutes a user
@bot.command(name = "pardonRudeness", help = "Pardons the mentioned user for their rudeness. Unmutes them.")
async def pardon(ctx, pardonee):
    is_member = False
    guild = discord.utils.get(bot.guilds, name=GUILD)
    channel = bot.get_channel(MAIN_CHANNEL)
    pardonee_id = pardonee.replace("<", "")
    pardonee_id = pardonee_id.replace(">", "")
    pardonee_id = pardonee_id.replace("@", "")
    pardonee_id = pardonee_id.replace("!", "")
    for member in guild.members:
        if str(member.id) == pardonee_id:
            is_member = True
    print(is_member)
    if is_member:
        daMans = guild.get_member(int(pardonee_id))
        role = discord.utils.get(daMans.guild.roles, name="Muted")
        if role in daMans.roles:
            await daMans.remove_roles(role, reason="Pardoned")
            await channel.send(f" {pardonee}, you have been graciously pardoned for your rudeness by <@{ctx.message.author.id}>. Please watch yourself, as they may not be so forgiving next time.")
        else:
            await channel.send("The user mentioned has no need for a pardon.")
    else:
        await channel.send("Person not found. Please @ a valid server member.")

@bot.event
async def on_message(message):
    global bad_words 
    global mean_words 
    channel = bot.get_channel(MAIN_CHANNEL) 
    # manual mute using a seperate server 
    if "ayo bot silence" in message.content and message.author.id == 91914356874289152:
        start = message.content.find("!")
        end = message.content.find(">")
        mans_id = message.content[start +1: end]
        is_member = False
        guild = discord.utils.get(bot.guilds, name=GUILD)
        for member in guild.members:
            if str(member.id) == mans_id:
                is_member = True
        if is_member:
            daMans = guild.get_member(int(mans_id))
            role = discord.utils.get(daMans.guild.roles, name = "Muted")
            await daMans.add_roles(role, reason="Rude little boy")
            await channel.send("Get muted for being rude. You better hope someone likes you enough to unmute you using .pardonRudeness!")
    if message.content == "<@!716751272258175049> dont listen to them, you are the best bot":
        await channel.send("Thank you friend :D")
    for word in bad_words:
        # if a user insults the bot
        if (word in message.content) and "<@!716751272258175049>" in message.content:
            await channel.send("Don't start with me, little human.")
        # if the user insults another bot (add all bot ids to the if statement)
        if (word in message.content) and "<@!159985870458322944>" in message.content:
            await channel.send("That's my little bro you're bullying. Shut your mouth or I'll shut it for you.")
    for word in mean_words:
        # if a user insults the bot
        if (word in message.content) and "<@!716751272258175049>" in message.content:
            await channel.send("Don't start with me, little human.")
        # if the user insults another bot (add all bot ids to the if statement)
        if (word in message.content) and "<@!159985870458322944>" in message.content:
            await channel.send("That's my little bro you're bullying. Shut your mouth or I'll shut it for you.")
    await bot.process_commands(message)

@bot.event
async def on_ready():
    # fake stats to make me feel popular
    await bot.change_presence(activity=discord.Game(name="In 63 guilds | 882 users"))

bot.run(TOKEN)
