import os
import re
from PIL import Image
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your bot token
TOKEN = '7833483637:AAFcc6fMlnB8AsSNcWE4q2kuNdBWVhTfIxc'

# Define a global variable for the download directory
DOWNLOAD_DIR = './downloads/'

# Command to start bot interaction
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me image files to rename and get a new thumbnail.')

# Handle file renaming and thumbnail creation
def rename_and_generate_thumbnail(update: Update, context: CallbackContext) -> None:
    # Check if the user sent a document
    if update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        file_size = update.message.document.file_size

        # Get the file object
        file = context.bot.get_file(file_id)
        
        # Download the file to the server
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        downloaded_file_path = os.path.join(DOWNLOAD_DIR, file_name)
        file.download(downloaded_file_path)

        update.message.reply_text(f'File {file_name} received. Renaming and creating thumbnail...')

        # Rename the file (basic example: prepend 'renamed_')
        new_name = f"renamed_{file_name}"
        new_file_path = os.path.join(DOWNLOAD_DIR, new_name)

        # Rename the file
        os.rename(downloaded_file_path, new_file_path)

        # Check if the file is an image (for thumbnail creation)
        if file_name.lower().endswith(('jpg', 'jpeg', 'png', 'gif')):
            create_thumbnail(new_file_path)

        # Send the renamed file back to the user
        with open(new_file_path, 'rb') as renamed_file:
            update.message.reply_document(renamed_file, filename=new_name)

        # Clean up downloaded files after renaming
        os.remove(new_file_path)
    else:
        update.message.reply_text('Please send me a file to rename and generate a thumbnail.')

# Function to create a thumbnail for images
def create_thumbnail(image_path: str) -> None:
    try:
        with Image.open(image_path) as img:
            # Generate a thumbnail with a size of 128x128 (you can change this size)
            img.thumbnail((128, 128))

            # Save the thumbnail to a new file
            thumb_path = image_path.replace(os.path.splitext(image_path)[1], '_thumbnail.jpg')
            img.save(thumb_path)

            print(f"Thumbnail created at {thumb_path}")
            return thumb_path
    except Exception as e:
        print(f"Error creating thumbnail: {e}")

# Handle text messages for bulk renaming with specific patterns
def handle_text(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    if user_message.startswith("/rename_pattern"):
        # Sample pattern for renaming (simple example: change "image" to "photo")
        new_name = user_message.split(" ")[1]  # Extract the new name from the command
        update.message.reply_text(f'Renaming using pattern: {new_name}')
        # Process files for bulk renaming (here we can loop through files)
        # For simplicity, this part is just a placeholder

        # Add your bulk renaming logic here
        # For example, you might loop through a list of files and rename them.

# Set up the main function to run the bot
def main():
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Register file handler
    dispatcher.add_handler(MessageHandler(Filters.document, rename_and_generate_thumbnail))

    # Register text handler (for bulk renaming pattern or commands)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Start the bot
    updater.start_polling()

    # Run the bot until you stop it manually
    updater.idle()

if __name__ == '__main__':
    main()
