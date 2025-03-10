import discord
from discord.ext import commands
import random
import asyncio

# Initialize the bot with intents and remove the default help command
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  

# List of words for the game
word_list= [
    "ability", "absence", "accept", "accident", "account", "acquire", "activity", "addition", "address", "advance",
    "advice", "affect", "airline", "alcohol", "animal", "anxiety", "attempt", "balance", "battery", "biology",
    "breathe", "candle", "capture", "category", "chicken", "climate", "college", "computer", "container", "courage",
    "creature", "culture", "danger", "debate", "degree", "disaster", "distance", "economy", "elephant", "empathy",
    "energy", "enough", "example", "famous", "finance", "formula", "fortune", "freedom", "gather", "happen",
    "healing", "honesty", "hotel", "imagine", "impact", "income", "insight", "journey", "journey", "jungle",
    "justice", "kingdom", "language", "laptop", "laughter", "library", "market", "mission", "minute", "moment",
    "network", "noble", "nature", "object", "option", "oracle", "outcome", "palace", "parents", "positive",
    "power", "plasma", "planet", "question", "quickly", "reality", "refuge", "remote", "respect", "return",
    "reunion", "serenity", "season", "system", "service", "silent", "shadow", "shelter", "solution", "statement",
    "summer", "tackle", "tiger", "target", "treatment", "universe", "unique", "unity", "victory", "value",
    "vaccine", "vital", "venture", "violence", "wander", "wonder", "whisper", "world", "young", "yellow",
    "zebra", "zombie", "absence", "ability", "brilliant", "acquire", "academic", "charity", "remarkable", 
    "advance", "enigma", "companion", "initiative", "increase", "determination", "abundant", "universe", 
    "jurisdiction", "evidence", "consensus", "irregular", "accomplish", "community", "calculation", "achieve",
    "reception", "tranquility", "tolerant", "ambition", "radiation", "dilemma", "empower", "imperfect", 
    "vacuum", "momentum", "trajectory", "puzzle", "comet", "substance", "together", "theory", "consequence",
    "climate", "target", "television", "arena", "migration", "clarity", "complication", "conclusion", 
    "combination", "earthquake", "intelligence", "maximum", "concern", "adapt", "momentary", "aroma", "witness",
    "solar", "patrol", "statistic", "creative", "question", "realize", "corruption", "prophecy", "advice",
    "uncover", "excellent", "routine", "search", "virtual", "daylight", "impressive", "curiosity", "genetics",
    "action", "clarify", "select", "element", "enhance", "lucky", "define", "novel", "inspire", "doubt",
    "direction", "benefit", "negative", "account", "secrets", "debate", "spectrum", "drastic", "reality",
    "clarity", "expect", "painful", "object", "influence", "nominee", "problem", "imperfect", "convention",
    "timepiece", "balance", "lifestyle", "rumor", "tension", "treatment", "internal", "occasion", "puzzle",
    "reunion", "attempt", "general", "perfection", "warrior", "exercise", "effect", "purpose", "prodigy", "intact",
    "truth", "attack", "symbol", "solution", "radical", "domain", "phenomenon", "magnet", "reception", "concentration",
    "pursuit", "process", "magnificent", "central", "territory", "principal", "equation", "dominion", "distract",
    "intensity", "accept", "match", "approach", "strategy", "essence", "desire", "approach", "final", "comet",
    "gathering", "prison", "approach", "session", "victory", "rejuvenate", "physical", "emerge", "special",
    "subject", "importance", "glory", "success", "solution", "calculation", "chase", "moment", "finale", "demonstrate",
    "analysis", "innovate", "universe", "sudden", "deeply", "emphasis", "gather", "spectrum", "careful", "strive",
    "research", "orderly", "passage", "reason", "noble", "prevention", "capital", "admission", "breakthrough", "quality",
    "attempt", "permanent", "investigate", "number", "formula", "combination", "alcohol", "diverse", "manage",
    "agency", "universal", "transparency", "horizon", "responsibility", "justice", "equality", "leadership", "comprehend",
    "selection", "researcher", "discussion", "memoir", "insight", "benefit", "structure", "definite", "goodwill", "fitness",
    "progress", "strategy", "notable", "contrast", "outcome", "determine", "concept", "finalize", "report", "concise",
    "plasma", "shadow", "consequence", "random", "feedback", "travel", "difficulty", "area", "sequence", "purpose"
]

# Hangman ASCII art stages (0 incorrect guesses to 6 = game over)
HANGMAN_PICS = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """
]

active_games = {}

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')

# Command to start a Hangman game
@bot.command()
async def hangman(ctx):
    """Start a new Hangman game in the current channel."""
    channel_id = ctx.channel.id

    # Check if a game is already active in this channel
    if channel_id in active_games:
        await ctx.send("A game is already in progress in this channel! Finish it or use `!stop` to end it.")
        return

    # Initialize game state
    word = random.choice(word_list).upper()
    guessed_letters = set()
    incorrect_guesses = 0   
    max_guesses = 6
    total_letters = len(word)  # Get the total number of letters in the word
    word_display = '-' * total_letters  # Create a string with dashes for each letter

    active_games[channel_id] = {
    "word": word,
    "guessed_letters": guessed_letters,
    "incorrect_guesses": incorrect_guesses,
    "max_guesses": max_guesses,
    "total_letters": total_letters,  # Store the total number of letters
    "word_display": word_display  # Store the current display of dashes
}


    # Send initial game state
    await send_game_state(ctx)

    # Game loop
    while channel_id in active_games:
        game = active_games[channel_id]

        # Check if the game is over
        if game["incorrect_guesses"] >= game["max_guesses"]:
            await ctx.send(f"Game Over! The word was **{game['word']}**.\n{HANGMAN_PICS[game['incorrect_guesses']]}")
            del active_games[channel_id]
            break

        if all(letter in game["guessed_letters"] for letter in game["word"]):
            await ctx.send(f"Congratulations! You guessed the word: **{game['word']}**!")
            del active_games[channel_id]
            break

        # Wait for a guess
        def check_guess(msg):
            return msg.channel == ctx.channel and len(msg.content) == 1 and msg.content.isalpha()

        try:
            guess_msg = await bot.wait_for("message", check=check_guess, timeout=30.0)
            guess = guess_msg.content.upper()

            # Process the guess
            if guess in game["guessed_letters"]:
                await ctx.send(f"You already guessed '{guess}'! Try again.")
            else:
                game["guessed_letters"].add(guess)
                if guess in game["word"]:
                    await ctx.send(f"Good guess! '{guess}' is in the word.")
                else:
                    game["incorrect_guesses"] += 1
                    await ctx.send(f"'{guess}' is not in the word. {game['max_guesses'] - game['incorrect_guesses']} attempts left.")

                # Update game state
                await send_game_state(ctx)

        except asyncio.TimeoutError:
            await ctx.send("No guesses in 30 seconds! Game over.")
            del active_games[channel_id]
            break

# Command to stop an active game
@bot.command()
async def stop(ctx):
    """Stop the current Hangman game in this channel."""
    channel_id = ctx.channel.id
    if channel_id in active_games:
        del active_games[channel_id]
        await ctx.send("Hangman game stopped!")
    else:
        await ctx.send("No active Hangman game in this channel!")

@bot.command()
async def help(ctx):
    """Show available commands."""
    help_text = (
        "**Hangman Bot Commands**\n"
        "`!hangman` - Start a new Hangman game.\n"
        "`!stop` - Stop the current Hangman game.\n"
        "`!help` - Display this help message.\n"
        "Guess by typing a single letter (e.g., 'a') after starting the game."
    )
    await ctx.send(help_text)

async def send_game_state(ctx):
    """Send the current state of the Hangman game."""
    channel_id = ctx.channel.id
    if channel_id not in active_games:
        return

    game = active_games[channel_id]
    word_display = "".join(letter if letter in game["guessed_letters"] else "_" for letter in game["word"])
    guessed = ", ".join(sorted(game["guessed_letters"]))
    state_message = (
        f"**Hangman Game**\n"
        f"Word: {word_display}\n"
        f"Guessed Letters: {guessed if guessed else 'None'}\n"
        f"Attempts Left: {game['max_guesses'] - game['incorrect_guesses']}\n"
        f"{HANGMAN_PICS[game['incorrect_guesses']]}"
    )
    await ctx.send(state_message)

# Run the bot (replace with your token)
bot.run("your own token")