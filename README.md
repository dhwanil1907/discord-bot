# Hangman Discord Bot

This is a simple Hangman game bot for Discord, built using the `discord.py` library. The bot allows users to play the classic word-guessing game directly in a Discord channel.

## Features

- Start a Hangman game with the `!hangman` command.
- Guess letters to reveal the word.
- The bot tracks guesses and provides feedback.
- Stop an active game using the `!stop` command.
- Displays Hangman ASCII art as the game progresses.
- Timeout functionality (game ends if no guesses are made within 30 seconds).
- Help command to list available commands.

## Prerequisites

- Python 3.7+
- `discord.py` library (can be installed via pip)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/hangman-discord-bot.git
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a bot on [Discord Developer Portal](https://discord.com/developers/applications) and get your bot token.

4. Replace `your own token` in the `bot.run("your own token")` line with your actual bot token.

5. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `!hangman`: Starts a new Hangman game in the current channel.
- `!stop`: Stops the current Hangman game in the current channel.
- `!help`: Displays the list of available commands.

## Example Usage

1. Start a new Hangman game:
   ```
   !hangman
   ```

2. Guess a letter:
   ```
   a
   ```

3. Stop the current game:
   ```
   !stop
   ```

4. Display the help message:
   ```
   !help
   ```

## Screenshots

**Hangman Game Example:**

```
**Hangman Game**
Word: _ _ _ _ _
Guessed Letters: a, b, c
Attempts Left: 4

   +---+
   |   |
       |
       |
       |
       |
=========
```

## Contributing

If you want to contribute to this project, feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
