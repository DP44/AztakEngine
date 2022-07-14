import os
import random
import distutils.util
import bot_functions as bf
from discord.ext import commands

# List of user IDS for people who are allowed to use this feature.
approved_users = [
    665755257460097064, # Mili#0001
    877300169186623578, # DP44#2706
    829275326303567892, # Oskarnik (not putting his tag, too much for this)
    878034080921448469, # chuck#3780
    253646353299668992, # chip#6569
    846993554257346592, # A5#3371
    393096618976739329, # posin#0701
    739945566712365078, # soda#1192 
]

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling twitch utilities.
# --------------------------------------------------------------------------
class Twitch(commands.Cog):
    def __init__(self, bot, file_path):
        self.bot = bot
        self.file_path = file_path

        # Create .twitch_accounts if it doesn't exist.
        if not os.path.exists(self.file_path):
            f = open(self.file_path, 'w')
            f.write('# FORMAT:\n')
            f.write('# [USERNAME]:[PASSWORD]:[EXISTS]:[VERIFIED]:[SPAM]\n')
            f.close()

        # Save the number of accounts in the .twitch_accounts file.
        self.count = len(self.get_accounts())

    # ----------------------------------------------------------------------
    # DESCRIPTION:  Parses a file used for storing accounts and returns a
    #               list of dictionaries holding account details for each
    #               entry in the file.
    # ----------------------------------------------------------------------
    def get_accounts(self):
        file_buf = open(self.file_path, 'r').read()
        file_lines = file_buf.split('\n')

        # We will append to this list.
        accounts = []

        for line in file_lines:
            # Ignore comments.
            if line.startswith('#'):
                continue

            # Ignore comments that are after entries.
            a = line.split('#')
    
            # Fix entry after removing comments.
            if len(a) > 1:
                line = a[0][:len(a[0])]

                while line[len(line) - 1:len(line)] == " ":
                    line = line[:len(line) - 1]

            # Ignore whitespaces.
            if line == "\n" or line == "":
                continue

            # Split the line into a list holding each detail for the entry.
            account_details = line.split(':')

            # Convert boolean fields from strings to actual booleans.
            if account_details[2] != 'UNKN':
                exists = bool(distutils.util.strtobool(account_details[2]))
            else:
                # TODO: Find a better way to represent unknown values.
                exists = False
            
            if account_details[3] != 'UNKN':
                verified = bool(distutils.util.strtobool(
                                    account_details[3]))
            else:
                # TODO: Find a better way to represent unknown values.
                verified = False

            if account_details[4] != 'UNKN':
                spam_account = bool(distutils.util.strtobool(
                                        account_details[4]))
            else:
                # TODO: Find a better way to represent unknown values.
                spam_account = False

            # Append the account details to the list.
            accounts.append({ 
                'username': account_details[0],
                'password': account_details[1],
                'exists': exists,
                'verified': verified,
                'spam_account': spam_account
            })
        
        # Return our created list.
        return accounts

    # ----------------------------------------------------------------------
    # COMMAND:      Returns a random twitch account.
    # ----------------------------------------------------------------------
    # Returns a dict for the account details for a randomly chosen account.
    @commands.command(name="fetch_account", 
                      brief="Fetches a random twitch account.")
    async def fetch_account(self, ctx):
        if ctx.author.id not in approved_users:
            await ctx.send("Sorry, you don't have permission to do this!")
            return

        # Get a random account dict from the list.
        account = random.choice(self.get_accounts())

        if account['exists']:
            msg  = f"Username: {account['username']}\n"
            msg += f"Password: {account['password']}\n"
            msg += f"Verified: {account['verified']}\n"
            msg += f"Spam Acc: {account['spam_account']}"
            await ctx.send(f'```{bf.box("Account Details", msg)}```')

    # ----------------------------------------------------------------------
    # COMMAND:      Adds a new account to the list of accounts.
    #
    # INPUT:        username    -> The account's username.
    #               password    -> The account's password.
    #               exists      -> If the account exists or not.
    #               verified    -> If the account is verified or not.
    #               spam_acc    -> If the account is made for spamming.
    # ----------------------------------------------------------------------
    @commands.command(name="add_account", 
                      brief="Adds a new account to the database.")
    async def add_account(self, ctx, username, password,
                          exists: bool, verified: bool, spam_acc: bool):
        try:
            if ctx.author.id not in approved_users:
                await ctx.send(
                    "Sorry, you don't have permission to do this!")
                return
            
            # The account must have a username and password.
            if username == '' or password == '':
                await ctx.send('Username or password cannot be blank!')
                return

            # Don't add entries that would fuck our parser.
            if ':' in password or '#' in password:
                await ctx.send("the password specified must not have " +
                               "either ':' or '#' in it.")
                return

            # # Usernames must be alphanumeric.
            # if not username.isalnum():
            #     await ctx.send("Usernames must be alphanumeric.")
            #     return

            entry  = f'{username}:'
            entry += f'{password}:'

            entry += \
                f'{exists}:'.upper() if type(exists) == bool else 'UNKN:'
            
            entry += \
                f'{verified}:'.upper() \
                    if type(verified) == bool else 'UNKN:'
            
            entry += \
                f'{spam_acc}'.upper() if type(spam_acc) == bool else 'UNKN'

            # NOTE: We don't need to filter out comments or whitespace here
            #       as we're only doing an exact comparison for each line.
            current_entries = open(self.file_path, 'r').read().split('\n')

            # Check for duplicate entries.
            # NOTE: This could be quite expensive for large lists of 
            #       entries, but it shouldn't be a problem for now.
            for i in current_entries:
                if i == entry:
                    await ctx.send(
                        "This account is already in the database!")
                    return

            with open(self.file_path, 'a') as f:
                f.write(f"\n{entry}")
                f.close()

                await ctx.send(f"Added entry for account `{username}`.")
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'add_account'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")
            await ctx.send('```Command usage:\n' + 
                           '$add_account [USERNAME] [PASSWORD] ' + 
                           '[EXISTS] [VERIFIED] [SPAM_ACC]\n' + 
                           'Example usage:\n' + 
                           '$add_account test passwd false false true```')
            return