import asyncio
import requests
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling IMVU related commands.
# --------------------------------------------------------------------------
class IMVU(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------
    # COMMAND:      Finds the location of a user in a public world.
    # 
    # INPUT:        player_cid     -> The CID to look up.
    # ----------------------------------------------------------------------
    @commands.command(name="find_locations", 
                      brief="Attempts to find a user based off their CID.")
    async def find_locations(self, ctx, player_cid):
        # TODO: Implement bulk searching as the web API supports it.
        try:
            # Store the path to the API call.
            url = 'http://client-dynamic.imvu.com/api/find_locations.php'

            # Do a GET request to the api with our given parameters.
            query = requests.get(f"{url}?cid=0&cids={player_cid}").json()

            # Check if our search was valid.
            if query['result'] == []:
                await ctx.send("Failed to find user! " + 
                               "The user may be in a private room.")
                return
            
            # Fetch the fields to our result.
            fields = query['result'][player_cid]

            # Construct our output string.
            output = "Found user in " + f"{len(fields)} " + \
                     ("room" if len(fields) == 1 else "rooms") + ".\n"

            for i in range(len(fields)):
                output += f" \nROOM {i + 1}\n"
                output += f"name: {fields[i]['name']}\n"
                output += \
                    f"room_instance_id: {fields[i]['room_instance_id']}\n"

            await ctx.send(f"```{bf.box('Query Results', output)}```")

        except Exception as e:
            msg = bf.box("Exception Handler", 
                        f"Exception caught in command 'find_locations'!\n" + 
                        f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")

        # await ctx.send("`This command is not yet implemented!`")

    # ----------------------------------------------------------------------
    # COMMAND:      Fetches a player's CID, used for API calls.
    # 
    # INPUT:        player_name    -> The name of the player to look for.
    # ----------------------------------------------------------------------
    @commands.command(name="get_player_cid", 
                      brief="Fetches a player's CID, used in API calls.")
    async def get_player_cid(self, ctx, player_name):
        try:
            await ctx.send("This command is not yet implemented!")
        except Exception as e:
            msg = bf.box("Exception Handler", 
                        f"Exception caught in command 'get_player_cid'!\n" + 
                        f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")