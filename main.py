from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import uuid
import random
from urllib.parse import parse_qs


# Bot credentials
TOKEN = "token"
BOT_USERNAME = "OurFunFusion_bot"

# Dictionary to store user reference IDs and users per group (by reference ID)
group_data = { }

# async def start(update: Update, context: CallbackContext):
#     await update.message.reply_text("Welcome! to THE Game")

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    # Extract referral ID if present
    args = context.args  # Telegram passes arguments from /start <arg>
    if args:
        ref_id = args[0]
        if ref_id in group_data:
            group_data[ref_id][user_id] = user_name  # Add user to group
            
            await update.message.reply_text(f"You've joined the group with reference ID: {ref_id}")

            # Notify all other members in the group
            for uid in group_data[ref_id]:
                if uid != user_id:
                    await context.bot.send_message(
                        chat_id=uid,
                        text=f"New player {user_name} has joined the game!"
                    )
            print("Group Data:", group_data)
            
        else:
            await update.message.reply_text("Invalid referral link. Please try again.")
    else:
        await update.message.reply_text("Welcome! Use /create_new_group to start a game.")

async def reset(update: Update, context: CallbackContext):
    group_data.clear()
    await update.message.reply_text("Reset successful. All groups have been cleared.")

async def create_new_group(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    ref_id = str(uuid.uuid4())[:8]  # Generate a unique 8-character reference ID
    
    if ref_id not in group_data:
        group_data[ref_id] = {}

    group_data[ref_id][user_id] = user_name  # Store users by ID to message them later
    
    # Generate the referral link
    referral_link = f"https://t.me/{BOT_USERNAME}?start={ref_id}"

    print("Group Data:", group_data)
    
    await update.message.reply_text(f"Welcome! Your reference ID is: {ref_id}\n"
                                    f"Share this link to invite others: {referral_link}")

async def join_group(update: Update, context: CallbackContext):
    # if len(context.args) == 0:
    #     await update.message.reply_text("Please provide a reference ID to join a group.")
    #     return

    # ref_id = context.args[0]
    # user_id = update.effective_user.id
    # user_name = update.effective_user.name

    user_id = update.effective_user.id
    user_name = update.effective_user.name

    # Check if the message contains a referral link with referral ID
    if len(context.args) == 0:
        # Check if the message contains a referral link
        if update.message.text and "referral=" in update.message.text:
            ref_id = parse_qs(update.message.text)["referral"][0]
        else:
            await update.message.reply_text("Please provide a valid referral link.")
            return
    else:
        ref_id = context.args[0]

    if ref_id in group_data:
        group_data[ref_id][user_id] = user_name  # Store users by ID
        print("Group Data:", group_data)
        
        await update.message.reply_text(f"You've joined the group with reference ID: {ref_id}")
        
        # Notify all other users in the group
        for uid in group_data[ref_id]:
            if uid != user_id:
                await context.bot.send_message(chat_id=uid, text=f"New player {user_name} has joined the game!")
    else:
        await update.message.reply_text(f"Invalid reference ID: {ref_id}. Please try again.")

async def play(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /play <reference_id> <number_of_jokers>")
        return

    ref_id = context.args[0]
    try:
        num_jokers = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Please provide a valid number for Jokers.")
        return

    if ref_id not in group_data:
        await update.message.reply_text("Invalid reference ID. Please start a new game first.")
        return

    players = list(group_data[ref_id].keys())  # Get user IDs
    if len(players) < num_jokers + 1:
        await update.message.reply_text("Not enough players. Jokers must be fewer than total players.")
        return

    random.shuffle(players)  # Shuffle players randomly
    jokers = players[:num_jokers]
    civilians = players[num_jokers:]

    # Notify each player of their role
    for joker in jokers:
        joker_names = [group_data[ref_id][jid] for jid in jokers]
        message = f"You are a Joker! Your teammates are: {', '.join(joker_names)}."
        await context.bot.send_message(chat_id=joker, text=message)

    for civilian in civilians:
        await context.bot.send_message(chat_id=civilian, text="You are a Civilian! Watch out for the Jokers!")

    # Broadcast game start to all players
    for uid in players:
        await context.bot.send_message(chat_id=uid, text=f"Game started! {num_jokers} Joker(s) have been chosen. Check your private messages.")

    print(f"Game started in group {ref_id}: {num_jokers} Jokers selected.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("create_new_group", create_new_group))
    application.add_handler(CommandHandler("join_group", join_group))
    application.add_handler(CommandHandler("play", play))

    application.run_polling()

if __name__ == '__main__':
    main()
