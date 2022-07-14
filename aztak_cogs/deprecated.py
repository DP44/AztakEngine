import bot_functions as bf
from discord.ext import commands

# --------------------------------------------------------------------------
# COG:          Features on life support.
# --------------------------------------------------------------------------
class Deprecated(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------
    # COMMAND:      Get info on a certain drug. (Why?)
    #
    # INPUT:        drug            -> The drug to look up.
    # ----------------------------------------------------------------------
    @commands.command(name='info', brief='Get info on a certain drug.')
    async def info(self, ctx, drug):
        try:
            rsp = bf.info(drug.lower().replace(' ', '-'))

            if len(rsp) > 2000:
                link = bf.content_upload(rsp)
                upload_box = bf.box(f"{drug} info", 
                                    f"Size limit reached.\nInfo at: {link}")
                await ctx.send(f'```{upload_box}```')
            else:
                await ctx.send(f'```{rsp}```')
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'info'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")

    # ----------------------------------------------------------------------
    # COMMAND:      Get records for a certain address.
    #
    # INPUT:        addr            -> The address to check.
    #               record          -> The record type to search for.
    # ----------------------------------------------------------------------
    @commands.command(name='getrec', 
                      brief='Prints any records for an address.')
    async def getrec(self, ctx, addr, record='txt'):
        try:
            response = bf.box(f"{record} RECORDS FOR {addr}", 
                              bf.get_records(addr, record))

            if len(response) < 2000:
                await ctx.send(f"```{response}```")
            else:
                content_address = bf.content_upload(response)
                rsp = bf.box(f"{record} RECORDS FOR {addr}", 
                             f"Record Size Limit Reached\n" + 
                             f"Records Stored At: {content_address}")
                await ctx.send(f"```{rsp}```")
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'getrec'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")
