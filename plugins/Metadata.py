# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
from helper.database import MovieGalaxyX as db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import *
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.command("metadata"))
async def metadata(client, message):
    user_id = message.from_user.id

    # Fetch user metadata from the database
    current = await db.get_metadata(user_id)
    title = await db.get_title(user_id)
    author = await db.get_author(user_id)
    artist = await db.get_artist(user_id)
    video = await db.get_video(user_id)
    audio = await db.get_audio(user_id)
    subtitle = await db.get_subtitle(user_id)
    encoded_by = await db.get_encoded_by(user_id)
    custom_tag = await db.get_custom_tag(user_id)

    # Display the current metadata
    text = f"""
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ: {current}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪꜱᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴅᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Eɴᴄᴏᴅᴇᴅ Bʏ ▹** `{encoded_by if encoded_by else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`
**◈ Cᴜsᴛᴏᴍ Tᴀɢ ▹** `{custom_tag if custom_tag else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`
    """

    # Inline buttons to toggle metadata
    buttons = [
        [
            InlineKeyboardButton(f"Oɴ{' ✅' if current == 'On' else ''}", callback_data='on_metadata'),
            InlineKeyboardButton(f"Oғғ{' ✅' if current == 'Off' else ''}", callback_data='off_metadata')
        ],
        [
            InlineKeyboardButton("Hᴏᴡ ᴛᴏ Sᴇᴛ Mᴇᴛᴀᴅᴀᴛᴀ...!!", callback_data="metainfo")
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await message.reply_text(text=text, reply_markup=keyboard, disable_web_page_preview=True)

# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
async def metadata_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data

    if data == "on_metadata":
        await db.set_metadata(user_id, "On")
    elif data == "off_metadata":
        await db.set_metadata(user_id, "Off")
    elif data == "metainfo":
        await query.message.edit_text("<b><u>ᴍᴀɴᴀɢɪɴɢ ᴍᴇᴛᴀᴅᴀᴛᴀ ғᴏʀ ʏᴏᴜʀ ᴠɪᴅᴇᴏs ᴀɴᴅ ғɪʟᴇs</u></b> \n\n<b><u>ᴠᴀʀɪᴏᴜꜱ ᴍᴇᴛᴀᴅᴀᴛᴀ:</u></b> \n\n- <b>ᴛɪᴛʟᴇ</b>: Descriptive title of the media. \n- <b>ᴀᴜᴛʜᴏʀ</b>: The creator or owner of the media. \n- <b>ᴀʀᴛɪꜱᴛ</b>: The artist associated with the media. \n- <b>ᴀᴜᴅɪᴏ</b>: Title or description of audio content. \n- <b>ꜱᴜʙᴛɪᴛʟᴇ</b>: Title of subtitle content. \n- <b>ᴠɪᴅᴇᴏ</b>: Title or description of video content. \n\n<b><u>ᴄᴏᴍᴍᴀɴᴅꜱ ᴛᴏ ᴛᴜʀɴ ᴏɴ ᴏғғ ᴍᴇᴛᴀᴅᴀᴛᴀ:</u></b> \n➜ /metadata: Turn on or off metadata. \n\n<b><u>ᴄᴏᴍᴍᴀɴᴅꜱ ᴛᴏ ꜱᴇᴛ ᴍᴇᴛᴀᴅᴀᴛᴀ:</u></b> \n\n➜ /settitle: Set a custom title of media. \n➜ /setauthor: Set the author. \n➜ /setartist: Set the artist. \n➜ /setaudio: Set audio title. \n➜ /setsubtitle: Set subtitle title. \n➜ /setvideo: Set video title. \n➜ /setencoded_by: Set encoded by title. \n➜ /setcustom_tag: Set custom tag title. \n\n<b><u>ᴇxᴀᴍᴘʟᴇ:</u></b> /settitle Your Title Here \n\n<b>ᴜꜱᴇ ᴛʜᴇꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴛᴏ ᴇɴʀɪᴄʜ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ᴡɪᴛʜ ᴀᴅᴅɪᴛɪᴏɴᴀʟ ᴍᴇᴛᴀᴅᴀᴛᴀ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ!</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Hᴏᴍᴇ", callback_data="start"),
                    InlineKeyboardButton("Bᴀᴄᴋ", callback_data="commands")
                ]
            ])
        )
        return
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
    # Fetch updated metadata after toggling
    current = await db.get_metadata(user_id)
    title = await db.get_title(user_id)
    author = await db.get_author(user_id)
    artist = await db.get_artist(user_id)
    video = await db.get_video(user_id)
    audio = await db.get_audio(user_id)
    subtitle = await db.get_subtitle(user_id)
    encoded_by = await db.get_encoded_by(user_id)
    custom_tag = await db.get_custom_tag(user_id)

    # Updated metadata message after toggle
    text = f"""
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ: {current}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪꜱᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴅᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Eɴᴄᴏᴅᴇᴅ Bʏ ▹** `{encoded_by if encoded_by else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`
**◈ Cᴜsᴛᴏᴍ Tᴀɢ ▹** `{custom_tag if custom_tag else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`
    """

    # Update inline buttons
    buttons = [
        [
            InlineKeyboardButton(f"Oɴ{' ✅' if current == 'On' else ''}", callback_data='on_metadata'),
            InlineKeyboardButton(f"Oғғ{' ✅' if current == 'Off' else ''}", callback_data='off_metadata')
        ],
        [
            InlineKeyboardButton("Hᴏᴡ ᴛᴏ Sᴇᴛ Mᴇᴛᴀᴅᴀᴛᴀ...!!", callback_data="metainfo")
        ]
    ]
    await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command('settitle'))
async def title(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /settitle Encoded By @RexBots_Official**")
    title = message.text.split(" ", 1)[1]
    await db.set_title(message.from_user.id, title=title)
    await message.reply_text("**✅ Tɪᴛʟᴇ Sᴀᴠᴇᴅ**")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.private & filters.command('setauthor'))
async def author(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Aᴜᴛʜᴏʀ\n\nExᴀᴍᴩʟᴇ:- /setauthor @RexBots_Official**")
    author = message.text.split(" ", 1)[1]
    await db.set_author(message.from_user.id, author=author)
    await message.reply_text("**✅ Aᴜᴛʜᴏʀ Sᴀᴠᴇᴅ**")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.private & filters.command('setartist'))
async def artist(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Aʀᴛɪꜱᴛ\n\nExᴀᴍᴩʟᴇ:- /setartist RexBots_Official**")
    artist = message.text.split(" ", 1)[1]
    await db.set_artist(message.from_user.id, artist=artist)
    await message.reply_text("**✅ Aʀᴛɪꜱᴛ Sᴀᴠᴇᴅ**")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.private & filters.command('setaudio'))
async def audio(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Aᴜᴅɪᴏ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setaudio @RexBots_Official**")
    audio = message.text.split(" ", 1)[1]
    await db.set_audio(message.from_user.id, audio=audio)
    await message.reply_text("**✅ Aᴜᴅɪᴏ Sᴀᴠᴇᴅ**")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.private & filters.command('setsubtitle'))
async def subtitle(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Sᴜʙᴛɪᴛʟᴇ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setsubtitle @RexBots_Official**")
    subtitle = message.text.split(" ", 1)[1]
    await db.set_subtitle(message.from_user.id, subtitle=subtitle)
    await message.reply_text("**✅ Sᴜʙᴛɪᴛʟᴇ Sᴀᴠᴇᴅ**")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.private & filters.command('setvideo'))
async def video(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Vɪᴅᴇᴏ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setvideo Encoded by @RexBots_Official**")
    video = message.text.split(" ", 1)[1]
    await db.set_video(message.from_user.id, video=video)
    await message.reply_text("**✅ Vɪᴅᴇᴏ Sᴀᴠᴇᴅ**")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.private & filters.command('setencoded_by'))
async def encoded_by(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Eɴᴄᴏᴅᴇᴅ Bʏ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setencoded_by @RexBots_Official**")
    encoded_by = message.text.split(" ", 1)[1]
    await db.set_encoded_by(message.from_user.id, encoded_by=encoded_by)
    await message.reply_text("**✅ Eɴᴄᴏᴅᴇᴅ Bʏ Sᴀᴠᴇᴅ**")
 # ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------   
@Client.on_message(filters.private & filters.command('setcustom_tag'))
async def custom_tag(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Cᴜsᴛᴏᴍ Tᴀɢ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setcustom_tag @RexBots_Official**")
    custom_tag = message.text.split(" ", 1)[1]
    await db.set_custom_tag(message.from_user.id, custom_tag=custom_tag)
    await message.reply_text("**✅ Eɴᴄᴏᴅᴇᴅ Bʏ Sᴀᴠᴇᴅ**")
