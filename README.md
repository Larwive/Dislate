# Dislate

A multi-purpose Discord bot.

The required Python packages are listed in [requirements.txt](https://github.com/Larwive/Dislate/blob/main/requirements.txt).

Files explanations :
- [game_data.py](https://github.com/Larwive/Dislate/blob/main/game_data.py) creates the structures the built-in game needs.
- [data_.py](https://github.com/Larwive/Dislate/blob/main/data_.py) contains data for the quote and translation commands.
- [gifs.py](https://github.com/Larwive/Dislate/blob/main/gifs.py) contains the code of the commands for the gif commands.
- [game_cogs.py](https://github.com/Larwive/Dislate/blob/main/game_cogs.py) contains the built-in game commands.
- [game_func.py](https://github.com/Larwive/Dislate/blob/main/game_func.py) contains functions to create and interact with data.bd and also some other useful functions for the game commands.
- [main.py](https://github.com/Larwive/Dislate/blob/main/main.py) contains the bot starter code and also some commands. This is the file to run to start the bot. 


You need to set the following environment variables :
- DEEPL as your deepl API key for the translation commands (optional).
- TENOR as your tenor API key for the gifs commands (optional).
- TOKEN as your Discord token from your Discord application for your bot.
