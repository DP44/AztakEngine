import constants
import discord.utils
import bot_functions as bf
from discord.ext import commands

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling Admin commands.
# --------------------------------------------------------------------------
class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------
    # COMMAND:      Force clear the zoo channel.
    # ----------------------------------------------------------------------
    @commands.command(name="cleanzoo", 
                 brief="[DEV] Force clean the zoo channel.")
    @commands.has_permissions(administrator=True)
    async def cleanzoo(self, ctx):
        try:
            if not ctx.author.id in constants.dev_ids:
                await ctx.send(
                    "Sorry, you don't have permission to do this!")
                return

            zoo = self.bot.get_channel(838085979784871936)
            message_count = await bf.get_message_count(zoo)
            
            deleted_messages = await zoo.purge(limit=message_count, 
                                               check=bf.check_message)
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'cleanzoo'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")

    # ----------------------------------------------------------------------
    # COMMAND:      Approve a user to access the server.
    #
    # INPUT:        user            -> The user to approve.
    # ----------------------------------------------------------------------
    @commands.command(name="approve", 
                      brief='[ADMIN] approves a user who is ' + 
                            'restricted to #zoo.')
    @commands.has_permissions(administrator=True)
    async def approve(self, ctx, user: discord.Member):
        try:
            # Role given on member join.
            initial_role = discord.utils.get(user.guild.roles, 
                                             id=826243626560520234)

            # Role given to approved users.
            approved_role = discord.utils.get(user.guild.roles, 
                                              id=668977982496440352)

            # Check if the user has the role.
            if initial_role in user.roles and \
               not approved_role in user.roles:
                # Remove the inital role
                await user.remove_roles(initial_role)

                # Give the user the Novice role.
                await user.add_roles(approved_role)

                # Let the admin know the user was approved.
                await ctx.send(f"Approved {user.name}.")
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'approve'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")

    # ----------------------------------------------------------------------
    # COMMAND:      Clears the chat by a certain amount.
    #
    # INPUT:        number          -> Number of messages to delete.
    # ----------------------------------------------------------------------
    @commands.command(name="purge", 
                      brief='[ADMIN] Deletes a specified amount of ' + 
                            'messages.', 
                      pass_context=True)
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, number: int=5):
        try:
            # Delete messages.
            await ctx.message.channel.purge(limit=number + 1)
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'purge'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")