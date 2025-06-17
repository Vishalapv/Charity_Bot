
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
import qrcode
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Function to show the inline menu
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the inline keyboard layout
    keyboard = [
        [InlineKeyboardButton("Donate", callback_data='donate')],
        [InlineKeyboardButton("Learn More", callback_data='learn_more')],
        [InlineKeyboardButton("Volunteer", callback_data='volunteer')],
        [InlineKeyboardButton("Events", callback_data='events')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("""Hello! Welcome to Benevolent 
Please choose an option:""", reply_markup=reply_markup)

# Callback query handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'donate':
        await query.edit_message_text(text="You chose to donate!click this /donate")
    elif query.data == 'learn_more':
        await query.edit_message_text(text="Here’s more about our mission and services.../learn_more")
    elif query.data == 'volunteer':
        await query.edit_message_text(text="Here’s how you can help us by volunteering.../volunteer")
    elif query.data == 'events':
        await query.edit_message_text(text="Check out our upcoming events.../events")
# Directory to save QR codes
QR_CODE_DIR = 'qrcodes'
os.makedirs(QR_CODE_DIR, exist_ok=True) 

# UPI ID for receiving donations
UPI_ID = "vishal31apv@oksbi"  

# Conversation states
WAITING_FOR_AMOUNT, WAITING_FOR_CONFIRMATION = range(2)

# Function to generate a QR code for a specified amount
def generate_qr_code(upi_id: str, amount: int, filename: str):
    payment_info = f"upi://pay?pa={upi_id}&am={amount}&cu=INR"
    qr = qrcode.make(payment_info)
    qr.save(filename)

# Command handler for /donate command to start the donation process
async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the amount you wish to donate in INR (e.g., '100' for ₹100).")
    return WAITING_FOR_AMOUNT

# Handler for receiving the donation amount
async def receive_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = int(update.message.text)  
        if amount <= 0:
            await update.message.reply_text("Please enter a valid positive amount.")
            return WAITING_FOR_AMOUNT 

        # Ask for confirmation
        context.user_data['amount'] = amount 
        await update.message.reply_text(f"You entered ₹{amount}. Do you want to proceed with this amount? (yes/no)")
        return WAITING_FOR_CONFIRMATION

    except ValueError:
        await update.message.reply_text("Please enter a valid number for the amount.")
        return WAITING_FOR_AMOUNT  
    
# Handler for confirming the donation amount
async def confirm_donation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text.lower()
    
    if user_response == 'yes':
        amount = context.user_data['amount'] 
        # Generate QR code for the specified amount
        qr_path = os.path.join(QR_CODE_DIR, f'donation_{amount}.png')
        generate_qr_code(UPI_ID, amount, qr_path)

        # Send the QR code image to the user
        with open(qr_path, 'rb') as qr_file:
            await update.message.reply_photo(qr_file, caption=f"Thank you for choosing to donate ₹{amount}! Please proceed with the payment.")

    elif user_response == 'no':
        await update.message.reply_text("Donation process has been canceled. If you wish to donate, you can start again with /donate.")
    else:
        await update.message.reply_text("Please respond with 'yes' or 'no'.")

    return ConversationHandler.END


# Command handler for /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""\
The following commands are available:

/start -> Welcome to the channel
/help -> Know how it works
/learn_more -> Learn more about our team and our works.
/donate -> Help others by donating
/volunteer -> Join our team
/events -> Check out our upcoming events
    """)

# Command handler for /learn_more
async def learn_more_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """\
        Our mission is to provide essential food and shelter to individuals and families facing hardship. 
        Here are some of the services we offer:

        - Food Distribution: Regular food drives to provide nutritious meals.
        - Temporary Housing: Safe and supportive shelter for those in need.
        - Job Training: Skills development workshops to help individuals gain employment.
        - Rescue Services: Immediate support for individuals in crisis.

        Learn more about our work: [link to website or social media]. 
        For any inquiries, you can contact us at: [contact information]. 
        """
    )

# Command handler for /events
async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """\
        Here are some upcoming events you can participate in:

        1. Food Drive 
           Date: [Insert Date]  
           Location: [Insert Location]  
           Join us as we collect and distribute food to families in need!

        2. Community Awareness Workshop
           Date: [Insert Date]  
           Location: [Insert Location]  
           Help us spread awareness about our mission and programs. 

        3. Annual Fundraising Gala
           Date: [Insert Date]  
           Location: [Insert Location]  
           Join us for an evening of fun and fundraising to support our services!

        For more details on any event, feel free to reach out or visit our website: [link to website].
        """
    )

# Command handler for /volunteer
async def volunteer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """\
        Join our compassionate team of volunteers at [Charity Name]! Your support can make a real difference in the lives of those we serve. Here are some ways you can help:

        - Food Distribution: Assist in sorting, packaging, and delivering food to families in need during our food drives.
        - Shelter Support: Help provide a safe and welcoming environment for those seeking shelter. This may include organizing activities or assisting with meal preparation.
        - Community Outreach: Engage with the community to spread awareness about our mission and recruit more supporters.
        - Fundraising Events: Help organize and promote events to raise funds for our programs and services.
        - Administrative Tasks: Support our team with office duties such as answering calls, managing emails, and organizing files.

        To become a volunteer, please fill out our volunteer application form: [link to volunteer form]. 
        If you have any questions or need more information, feel free to contact us at [contact information].

        Your time and dedication can create a positive impact in our community. Thank you for considering volunteering with Benevolent!
        """
    )

# Function to process responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed or 'hi' in processed:
        return 'Hey there! How can I assist you today?'
    elif 'how are you' in processed:
        return 'I’m just a bot, but I’m here to help you! What can I do for you?'
    elif 'information' in processed:
        return (
            'Our mission is to provide essential food and shelter to individuals and families facing hardship. '
            'We offer food distribution, temporary housing, job training, and rescue services. '
            'Learn more about our work: [link to website or social media].'
        )
    elif 'donate' in processed:
        return (
            'Thank you for your interest in donating! Your contributions help us serve those in need. '
            'To make a donation, please click:/donate .'
        )
    elif 'volunteer' in processed:
        return (
            'We’d love to have you as a volunteer! Please fill out our application form here: [link to volunteer form]. '
            'Your time can make a significant difference in our community!'
        )
    elif 'thank you' in processed or 'thanks' in processed:
        return 'You’re welcome! If you have any more questions or need assistance, feel free to ask.'
    elif 'what can i do' in processed:
        return (
            'There are several ways you can help: '
            '1. Volunteer your time to assist with our programs. '
            '2. Make a donation to support our initiatives. '
            '3. Spread the word about our work to your friends and family.'
        )
    elif 'need help' in processed:
        return 'I’m here to help! What do you need assistance with?'
    elif 'contact' in processed:
        return 'You can reach us at avishalofficial.13@gmail.com. We’d be happy to assist you!'

    return "I don't understand. Could you try asking differently?"

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text.lower()

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if 'hi' in text:
        await help_command(update, context) 
    elif message_type == 'group' and BOT_USERNAME in text:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
        response: str = handle_response(new_text)
        await update.message.reply_text(response)
    else:
        response: str = handle_response(text)
        await update.message.reply_text(response)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')

# Main program to run the bot
if __name__ == '__main__':
    # Define the bot token and bot username as constants
    Token: Final = '7603364497:AAH-Y9u5_bO_1vIpKZRlkXSKDnToaUpUsng'
    BOT_USERNAME: Final = '@Benevolent_care_bot'  

    # Create the application
    app = Application.builder().token(Token).build()

    # Set up conversation handler with states
    donation_conversation = ConversationHandler(
        entry_points=[CommandHandler('donate', donate_command)],
        states={
            WAITING_FOR_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_amount)],
            WAITING_FOR_CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_donation)],
        },
        fallbacks=[CommandHandler('start', start_command)],  
    )

    # Add handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('learn_more', learn_more_command))
    app.add_handler(CommandHandler('events', events_command))
    app.add_handler(CommandHandler('volunteer', volunteer_command))
    app.add_handler(donation_conversation)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  

    # Add error handler
    app.add_error_handler(error)

    # Start polling
    print('Polling...')
    app.run_polling(poll_interval=3)
