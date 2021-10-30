import string
import asyncio
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

logger = bf.Logger("Auditing (Cog)", 1)

# --------------------------------------------------------------------------
# COG:          A cog responsible for logging server events and activities.
# --------------------------------------------------------------------------
class Auditing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        logger.message("Initializing cog: Auditing")

    # ----------------------------------------------------------------------
    # EVENT:        Called when a member joins the server.
    #
    # INPUT:        member          -> The user that joined.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            logger.message(f"Member joined: {member.name}")
       
        except Exception as e:
            logger.error(f"{e}")

    # ----------------------------------------------------------------------
    # EVENT:        Called when a member leaves the server.
    #
    # INPUT:        member          -> The user that joined.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            logger.message(f"Member left: {member.name}")
        
        except Exception as e:
            logger.error(f"{e}")

    """
    # ----------------------------------------------------------------------
    # EVENT:        Called when a member updates their profile.
    #
    # INPUT:        before          -> The member's old info.
    #               after           -> The member's updated info.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            # TODO: rewrite this fucking mess.
            if before.nick == after.nick:
                logger.message(f"User updated: {after.nick}")
            else:
                logger.message(
                    f"User updated: {before.nick} => {after.nick}")

            # f"                a"

            # Find any new roles and output them.
            for role in after.roles:
                if role not in before.roles:
                    logger.message(f"    Added role: {role.name}")

            # Find any removed roles and output them.
            for role in before.roles:
                if role not in after.roles:
                    logger.message(f"    Removed role: {role.name}")

        except Exception as e:
            logger.error(f"{e}")

    # ----------------------------------------------------------------------
    # EVENT:        Called when a user updates their profile.
    #
    # INPUT:        before          -> The user object with the details
    #                                  before the change.
    #               after           -> The user object with the details
    #                                  after the change.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        try:
            # TODO: rewrite this fucking mess.
            if before.name == after.name:
                logger.message(f"User updated: {after.name}")
            else:
                logger.message(
                    f"User updated: {before.name} => {after.name}")

            # f"              a"

        except Exception as e:
            logger.error(f"{e}")
    """

    # ----------------------------------------------------------------------
    # EVENT:        Called when a member sends a message.
    #
    # INPUT:        message         -> The message object.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.is_system():
                return

            if message.author.bot:
                return

            channel_name = \
                ''.join(filter(lambda x: x in string.printable, 
                                              message.channel.name))

            # Remove any dashes at the end of the name.
            if channel_name.endswith('-'):
                channel_name = channel_name[:len(channel_name) - 1]

            logger.message(f"IN {channel_name} FROM " + 
                f"{message.author.name}: \"{message.clean_content}\"")
        
        except Exception as e:
            logger.error(f"{e}")

    # ----------------------------------------------------------------------
    # EVENT:        Called when a member is banned.
    #
    # INPUT:        guild           -> The guild the user was banned from.
    #               user            -> The user that was banned.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            logger.message(f"User banned: {user.name}")

        except Exception as e:
            logger.error(f"{e}")

    # ----------------------------------------------------------------------
    # EVENT:        Called when a member is unbanned.
    #
    # INPUT:        guild           -> The guild the user was unbanned from.
    #               user            -> The user that was unbanned.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        try:
            logger.message(f"User unbanned: {user.name}")

        except Exception as e:
            logger.error(f"{e}")

    # ----------------------------------------------------------------------
    # EVENT:        Called when an invite is created.
    #
    # INPUT:        invite          -> The created invite.
    # ----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        try:
            logger.message(f"Invite created by {invite.inviter.name}")

        except Exception as e:
            logger.error(f"{e}")