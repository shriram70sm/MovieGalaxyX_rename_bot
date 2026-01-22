# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
import asyncio
import logging
import random
import string 
import requests
from datetime import datetime, timedelta
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from plugins.helper_func import *
from helper.database import Seishiro
from plugins.Metadata import metadata_callback
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
logger = logging.getLogger(__name__)
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def generate_random_alphanumeric():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    try:
        user = await rexbots.col.find_one({"_id": user_id})
        if user and user.get("ban_status", {}).get("is_banned", False):
            return await query.message.edit_text(
                "🚫 You are banned from using this bot.\n\nIf you think this is a mistake, contact the admin.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📩 Contact Admin", url=Config.ADMIN_URL)]]
                )
            )

        if data == "home":
            await query.message.edit_text(
                text=Config.START_TXT.format(
                    first=query.from_user.first_name,
                    last=query.from_user.last_name or "",
                    username=f"@{query.from_user.username}" if query.from_user.username else "None",
                    mention=query.from_user.mention,
                    id=query.from_user.id
                ),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
                    [InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇs', url='https://t.me/RexBots_Official'), InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/+diDK3GRvvvlhZTQ1')],
                    [InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'), InlineKeyboardButton('Dᴇᴠᴇʟᴏᴘᴇʀ •', url='https://t.me/seishiro_obito')]
                ])
            )
        elif data == "caption":
            await query.message.edit_text(
                text=Config.CAPTION_TXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• sᴜᴘᴘᴏʀᴛ", url='https://t.me/+diDK3GRvvvlhZTQ1'), InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
                ])
            )
        elif data == "help":
            await query.message.edit_text(
                text=Config.HELP_TXT.format(query.from_user.mention),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
                    [InlineKeyboardButton('• ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'), InlineKeyboardButton('ᴄᴀᴘᴛɪᴏɴ •', callback_data='caption')],
                    [InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'), InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ •', callback_data='donate')],
                    [InlineKeyboardButton("• Sᴇǫᴜᴇɴᴄᴇ" , callback_data='sequence')],
                    [InlineKeyboardButton('• ʜᴏᴍᴇ •', callback_data='home')]
                ])
            )
        elif data == "sequence":
            await query.message.edit_text(
                "<b>Sᴇɴᴅ ᴍᴇ ғɪʟᴇs ᴀɴᴅ I ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴛʜᴀᴛ ғɪʟᴇs ɪɴ ᴀ ᴘᴇʀғᴇᴄᴛ sᴇǫᴜᴇɴᴄᴇ...!! \n\nʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ғᴏʀ sᴇǫᴜᴇɴᴄᴇ ᴄᴏᴍᴍᴀɴᴅꜱ: \n\nᴀᴡᴇsᴏᴍᴇ Cᴏᴍᴍᴀɴᴅs🫧 \n\n/start_sequence - Tᴏ sᴛᴀʀᴛ sᴇǫᴜᴇɴᴄᴇ. \n/end_sequence - Tᴏ ᴇɴᴅ sᴇǫᴜᴇɴᴄᴇ.</b>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help")
                ]])
            )
        elif data == "meta":
            await query.message.edit_text("<b>--Metadata Settings:--</b> \n\n➜ /metadata: Turn on or off metadata. \n\n<b><u>Description</u></b> <b><i>: Metadata will change MKV video files including all audio, streams, and subtitle titles.</i></b>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• ᴄʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
                ])
            )
        elif data == "donate":
            await query.message.edit_text(
                text=Config.DONATE_TXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("ᴏᴡɴᴇʀ •", url='https://t.me/RexBots_Official')]
                ])
            )
        elif data == "file_names":
            format_template = await rexbots.get_format_template(user_id)
            await query.message.edit_text(
                text=Config.FILE_NAME_TXT.format(format_template=format_template),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• ᴄʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
                ])
            )    
        elif data == "thumbnail":
            await query.message.edit_text(
                text=Config.THUMBNAIL_TXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• ᴄʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
                ])
            )    
        elif data == "about":
            await query.message.edit_text(
                text=Config.ABOUT_TXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="home")
                ]])
            )
        elif data in ["on_metadata", "off_metadata", "metainfo"]:
            await metadata_callback(client, query)

        elif data == "commands":
            await query.message.edit_text(
                "**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ: {current}**".format(current=await rexbots.get_metadata(user_id)),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(f"Oɴ{' ✅' if await rexbots.get_metadata(user_id) == 'On' else ''}", callback_data='on_metadata'),
                        InlineKeyboardButton(f"Oғғ{' ✅' if await rexbots.get_metadata(user_id) == 'Off' else ''}", callback_data='off_metadata')
                    ],
                    [
                        InlineKeyboardButton("Hᴏᴡ ᴛᴏ Sᴇᴛ Mᴇᴛᴀᴅᴀᴛᴀ...!!", callback_data="metainfo")
                    ],
                    [
                        InlineKeyboardButton("Bᴀᴄᴋ", callback_data="start")
                    ]
                ])
            )
        elif data == "close":
            try:
                await query.message.delete()
                if query.message.reply_to_message:
                    await query.message.reply_to_message.delete()
            except Exception:
                await query.message.delete()

        elif data.startswith("rfs_ch_"):
            cid = int(data.split("_")[2])
            try:
                chat = await client.get_chat(cid)
                mode = await rexbots.get_channel_mode(cid)
                status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
                new_mode = "off" if mode == "on" else "on"
                buttons = [
                    [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                    [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
                ]
                await query.message.edit_text(
                    f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            except Exception:
                await query.answer("Failed to fetch channel info", show_alert=True)

        elif data.startswith("rfs_toggle_"):
            cid, action = data.split("_")[2:]
            cid = int(cid)
            mode = "on" if action == "on" else "off"

            await rexbots.set_channel_mode(cid, mode)
            await query.answer(f"Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")

            chat = await client.get_chat(cid)
            status = "🟢 ON" if mode == "on" else "🔴 OFF"
            new_mode = "off" if mode == 'on' else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        elif data == "fsub_back":
            channels = await rexbots.show_channels()
            buttons = []
            for cid in channels:
                try:
                    chat = await client.get_chat(cid)
                    mode = await rexbots.get_channel_mode(cid)
                    status = "🟢" if mode == "on" else "🔴"
                    buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
                except Exception:
                    continue
            if not buttons:
                buttons.append([InlineKeyboardButton("No Channels Found", callback_data="no_channels")])
            await query.message.edit_text(
                "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("ᴠᴇʀɪꜰʏ 𝟷", callback_data="verify_1_cbb"), InlineKeyboardButton("ᴠᴇʀɪꜰʏ 𝟸", callback_data="verify_2_cbb")],
                [InlineKeyboardButton("ᴄᴏᴜɴᴛs", callback_data="verify_count")],
                [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
            ])
            await query.message.edit_text("ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇꜱꜱ:\n\n ➲ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ᴛᴜʀɴ ᴏɴ/ᴏꜰꜰ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇꜱꜱ & Aʟsᴏ ʏᴏᴜ ᴄᴀɴ sᴇᴇ ᴄᴏᴜɴᴛs.", reply_markup=keyboard)

        elif data == "verify_1_cbb":
            settings = await rexbots.get_verification_settings()
            verify_status_1 = settings.get("verify_status_1", False)
            verify_token_1 = settings.get("verify_token_1", "Not set")
            api_link_1 = settings.get("api_link_1", "Not set")
            current_status = "On" if verify_status_1 else "Off"
            
            buttons = [
                [
                    InlineKeyboardButton(f"Oɴ{' ✅' if verify_status_1 else ''}", callback_data='on_vrfy_1'),
                    InlineKeyboardButton(f"Oғғ{' ✅' if not verify_status_1 else ''}", callback_data='off_vrfy_1')
                ],
                [
                    InlineKeyboardButton("Sᴇᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ", callback_data="vrfy_set_1")
                ],
                [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(f"<b>ᴠᴇʀɪꜰʏ 𝟷 ꜱᴇᴛᴛɪɴɢꜱ:\n\nꜱʜᴏʀᴛɴᴇʀ: {api_link_1}\nAPI: {verify_token_1}\n\nꜱᴛᴀᴛᴜꜱ:</b> {current_status}", reply_markup=keyboard)

        elif data == "verify_2_cbb":
            settings = await rexbots.get_verification_settings()
            verify_status_2 = settings.get("verify_status_2", False)
            verify_token_2 = settings.get("verify_token_2", "Not set")
            api_link_2 = settings.get("api_link_2", "Not set")
            current_status = "On" if verify_status_2 else "Off"

            buttons = [
                [
                    InlineKeyboardButton(f"Oɴ{' ✅' if verify_status_2 else ''}", callback_data='on_vrfy_2'),
                    InlineKeyboardButton(f"Oғғ{' ✅' if not verify_status_2 else ''}", callback_data='off_vrfy_2')
                ],
                [
                    InlineKeyboardButton("Sᴇᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ", callback_data="vrfy_set_2")
                ],
                [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(f"<b>ᴠᴇʀɪꜰʏ 𝟸 ꜱᴇᴛᴛɪɴɢꜱ:\n\nꜱʜᴏʀᴛɴᴇʀ: {api_link_2}\nAPI: {verify_token_2}\n\nꜱᴛᴀᴛᴜꜱ:</b> {current_status}", reply_markup=keyboard)

        elif data == "on_vrfy_1":
            try:
                await rexbots.set_verification_mode_1(True)
                await query.answer("Verification 1 turned ON", show_alert=True)
                
                # Refresh the display to show updated tick mark
                settings = await rexbots.get_verification_settings()
                verify_status_1 = settings.get("verify_status_1", False)
                verify_token_1 = settings.get("verify_token_1", "Not set")
                api_link_1 = settings.get("api_link_1", "Not set")
                current_status = "On" if verify_status_1 else "Off"
                
                buttons = [
                    [
                        InlineKeyboardButton(f"Oɴ{' ✅' if verify_status_1 else ''}", callback_data='on_vrfy_1'),
                        InlineKeyboardButton(f"Oғғ{' ✅' if not verify_status_1 else ''}", callback_data='off_vrfy_1')
                    ],
                    [
                        InlineKeyboardButton("Sᴇᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ", callback_data="vrfy_set_1")
                    ],
                    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
                ]
                keyboard = InlineKeyboardMarkup(buttons)
                await query.message.edit_text(f"<b>ᴠᴇʀɪꜰʏ 𝟷 ꜱᴇᴛᴛɪɴɢꜱ:\n\nꜱʜᴏʀᴛɴᴇʀ: {api_link_1}\nAPI: {verify_token_1}\n\nꜱᴛᴀᴛᴜꜱ:</b> {current_status}", reply_markup=keyboard)
            except Exception as e:
                await query.answer(f"An unexpected error occurred: {e}", show_alert=True)

        elif data == "off_vrfy_1":
            try:
                await rexbots.set_verification_mode_1(False)
                await query.answer("Verification 1 turned OFF", show_alert=True)
                
                # Refresh the display to show updated tick mark
                settings = await rexbots.get_verification_settings()
                verify_status_1 = settings.get("verify_status_1", False)
                verify_token_1 = settings.get("verify_token_1", "Not set")
                api_link_1 = settings.get("api_link_1", "Not set")
                current_status = "On" if verify_status_1 else "Off"
                
                buttons = [
                    [
                        InlineKeyboardButton(f"Oɴ{' ✅' if verify_status_1 else ''}", callback_data='on_vrfy_1'),
                        InlineKeyboardButton(f"Oғғ{' ✅' if not verify_status_1 else ''}", callback_data='off_vrfy_1')
                    ],
                    [
                        InlineKeyboardButton("Sᴇᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ", callback_data="vrfy_set_1")
                    ],
                    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
                ]
                keyboard = InlineKeyboardMarkup(buttons)
                await query.message.edit_text(f"<b>ᴠᴇʀɪꜰʏ 𝟷 ꜱᴇᴛᴛɪɴɢꜱ:\n\nꜱʜᴏʀᴛɴᴇʀ: {api_link_1}\nAPI: {verify_token_1}\n\nꜱᴛᴀᴛᴜꜱ:</b> {current_status}", reply_markup=keyboard)
            except Exception as e:
                await query.answer(f"An unexpected error occurred: {e}", show_alert=True)
                
        elif data == "on_vrfy_2":
            try:
                await rexbots.set_verification_mode_2(True)
                await query.answer("Verification 2 turned ON", show_alert=True)
                
                # Refresh the display to show updated tick mark
                settings = await rexbots.get_verification_settings()
                verify_status_2 = settings.get("verify_status_2", False)
                verify_token_2 = settings.get("verify_token_2", "Not set")
                api_link_2 = settings.get("api_link_2", "Not set")
                current_status = "On" if verify_status_2 else "Off"
                
                buttons = [
                    [
                        InlineKeyboardButton(f"Oɴ{' ✅' if verify_status_2 else ''}", callback_data='on_vrfy_2'),
                        InlineKeyboardButton(f"Oғғ{' ✅' if not verify_status_2 else ''}", callback_data='off_vrfy_2')
                    ],
                    [
                        InlineKeyboardButton("Sᴇᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ", callback_data="vrfy_set_2")
                    ],
                    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
                ]
                keyboard = InlineKeyboardMarkup(buttons)
                await query.message.edit_text(f"<b>ᴠᴇʀɪꜰʏ 𝟸 ꜱᴇᴛᴛɪɴɢꜱ:\n\nꜱʜᴏʀᴛɴᴇʀ: {api_link_2}\nAPI: {verify_token_2}\n\nꜱᴛᴀᴛᴜꜱ:</b> {current_status}", reply_markup=keyboard)
            except Exception as e:
                await query.answer(f"An unexpected error occurred: {e}", show_alert=True)

        elif data == "off_vrfy_2":
            try:
                await rexbots.set_verification_mode_2(False)
                await query.answer("Verification 2 turned OFF", show_alert=True)
                
                # Refresh the display to show updated tick mark
                settings = await rexbots.get_verification_settings()
                verify_status_2 = settings.get("verify_status_2", False)
                verify_token_2 = settings.get("verify_token_2", "Not set")
                api_link_2 = settings.get("api_link_2", "Not set")
                current_status = "On" if verify_status_2 else "Off"
                
                buttons = [
                    [
                        InlineKeyboardButton(f"Oɴ{' ✅' if verify_status_2 else ''}", callback_data='on_vrfy_2'),
                        InlineKeyboardButton(f"Oғғ{' ✅' if not verify_status_2 else ''}", callback_data='off_vrfy_2')
                    ],
                    [
                        InlineKeyboardButton("Sᴇᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ", callback_data="vrfy_set_2")
                    ],
                    [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
                ]
                keyboard = InlineKeyboardMarkup(buttons)
                await query.message.edit_text(f"<b>ᴠᴇʀɪꜰʏ 𝟸 ꜱᴇᴛᴛɪɴɢꜱ:\n\nꜱʜᴏʀᴛɴᴇʀ: {api_link_2}\nAPI: {verify_token_2}\n\nꜱᴛᴀᴛᴜꜱ:</b> {current_status}", reply_markup=keyboard)
            except Exception as e:
                await query.answer(f"An unexpected error occurred: {e}", show_alert=True)

        elif data == "vrfy_set_1":
            msg = await query.message.edit_text("<b>ꜱᴇɴᴅ ᴠᴇʀɪꜰʏ 𝟷 ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ:\n\nʟɪᴋᴇ - `gplinks.com`\n\n/cancel ᴛᴏ ᴄᴀɴᴄᴇʟ</b>")
            try:
                api_data_1 = await client.listen(chat_id=query.message.chat.id, filters=filters.text, timeout=300)
                await msg.delete()
                api_link_1_s = api_data_1.text.strip()

                msg = await api_data_1.reply("<b>ꜱᴇɴᴅ ᴠᴇʀɪꜰʏ 𝟷 ꜱʜᴏʀᴛɴᴇʀ ᴀᴘɪ ᴋᴇʏ:\n\nʟɪᴋᴇ - 064438447747gdg4\n\n/cancel ᴛᴏ ᴄᴀɴᴄᴇʟ</b>")
                verify_data_1 = await client.listen(chat_id=query.message.chat.id, filters=filters.text, timeout=300)
                await msg.delete()
                verify_token_1_s = verify_data_1.text.strip()

                await rexbots.set_verify_1(api_link_1_s, verify_token_1_s)
                await query.message.reply_text(
                    "<b>ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ 1 ꜱᴇᴛᴛɪɴɢꜱ ᴜᴘᴅᴀᴛᴇᴅ!</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Hᴏᴍᴇ", callback_data="home"), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
                    ])
                )
            except asyncio.TimeoutError:
                await query.message.reply_text("Tɪᴍᴇᴏᴜᴛ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
            except Exception as e:
                logger.error(f"Error setting verification 1: {e}")
                await query.message.reply_text(f"An error occurred: {e}")

        elif data == "vrfy_set_2":
            msg = await query.message.edit_text("<b>ꜱᴇɴᴅ ᴠᴇʀɪꜰʏ 𝟸 ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ:\n\nʟɪᴋᴇ - `gplinks.com`\n\n/cancel ᴛᴏ ᴄᴀɴᴄᴇʟ</b>")
            try:
                api_data_2 = await client.listen(chat_id=query.message.chat.id, filters=filters.text, timeout=300)
                await msg.delete()
                api_link_2_s = api_data_2.text.strip()
                
                msg = await api_data_2.reply("<b>ꜱᴇɴᴅ ᴠᴇʀɪꜰʏ 𝟸 ꜱʜᴏʀᴛɴᴇʀ ᴀᴘɪ ᴋᴇʏ:\n\nʟɪᴋᴇ - 064438447747gdg4\n\n/cancel ᴛᴏ ᴄᴀɴᴄᴇʟ</b>")
                verify_data_2 = await client.listen(chat_id=query.message.chat.id, filters=filters.text, timeout=300)
                await msg.delete()
                verify_token_2_s = verify_data_2.text.strip()
                
                await rexbots.set_verify_2(api_link_2_s, verify_token_2_s)
                await query.message.reply_text(
                    "<b>ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ 2 ꜱᴇᴛᴛɪɴɢꜱ ᴜᴘᴅᴀᴛᴇᴅ!</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Hᴏᴍᴇ", callback_data="home"), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="verify_settings")]
                    ])
                )
            except asyncio.TimeoutError:
                await query.message.reply_text("Tɪᴍᴇᴏᴜᴛ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
            except Exception as e:
                logger.error(f"Error setting verification 2: {e}")
                await query.message.reply_text(f"An error occurred: {e}")

        elif data == "check_verify":
            user_id = query.from_user.id
            current_time = datetime.utcnow()
            
            user_data = await rexbots.col.find_one({"_id": user_id}) or {}
            verification_data = user_data.get("verification", {})
            
            shortener1_time = verification_data.get("shortener1_time")
            shortener2_time = verification_data.get("shortener2_time")
            
            if shortener1_time and shortener2_time:
                if current_time < shortener1_time + timedelta(hours=24):
                    await query.message.edit_text(
                        "Verification complete! You are verified for 24 hours."
                    )
                else:
                    await rexbots.col.update_one(
                        {"_id": user_id},
                        {"$unset": {"verification": ""}}
                    )
                    await query.message.edit_text(
                        "Verification expired. Please use /verify to start again."
                    )
            elif shortener1_time:
                await rexbots.col.update_one(
                    {"_id": user_id},
                    {"$set": {"verification.shortener2_time": current_time}}
                )
                await query.message.edit_text(
                    "Shortener 2 verified! You are now fully verified for 24 hours."
                )
            else:
                await rexbots.col.update_one(
                    {"_id": user_id},
                    {"$set": {"verification.shortener1_time": current_time}}
                )
                await query.message.edit_text(
                    "Shortener 1 verified! Please verify Shortener 2 after 6 hours using /verify."
                )
            
            await query.answer()

        elif data == "seeplan":
            await query.message.edit_text(
                "<b>👋 ʜᴇʏ Dᴜᴅᴇ, \n\n🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ ʙᴇɴɪꜰɪᴛꜱ:</blockquote>\n\n›› ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ\n❏ Gᴇᴛ ᴅɪʀᴇᴄᴛ ᴀᴜᴛᴏ ʀᴇɴᴀᴍɪɴɢ ғᴇᴀᴛᴜʀᴇ ɴᴏ ɴᴇᴇᴅ ғᴏʀ ᴠᴇʀɪғʏ\n›› ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n❏ Uɴʟɪᴍɪᴛᴇᴅ ᴀᴜᴛᴏ ʀᴇɴᴀᴍɪɴɢ\n\n›› ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan\n\n • ₹80 - 1 ᴡᴇᴇᴋ\n • ₹100 - 1 ᴍᴏɴᴛʜ\n • ₹750 - 1 ʏᴇᴀʀ\n\n Cᴜsᴛᴏᴍ ᴘʟᴀɴ ᴀʟsᴏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴛ :- @RexBots_Official</b>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⇋ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇋', callback_data='home')]]))

        elif data == "refresh_verify_count":
            await query.answer("Rᴇғʀᴇsʜɪɴɢ...!!")
            await query.message.edit_text ("Cᴏᴜɴᴛɪɴɢ ᴀɢᴀɪɴ...!!")
            today = await rexbots.get_vr_count_combined('today')
            yesterday = await rexbots.get_vr_count_combined('yesterday')
            this_week = await rexbots.get_vr_count_combined('this_week')
            this_month = await rexbots.get_vr_count_combined('this_month')
            last_month = await rexbots.get_vr_count_combined('last_month')
            
            count_text = (
                "<b>📊 ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ sᴛᴀᴛɪsᴛɪᴄs:\n\n"
                f"👥 ᴛᴏᴅᴀʏ: {today} ᴜsᴇʀs\n"
                f"📊 ʏᴇsᴛᴇʀᴅᴀʏ: {yesterday} ᴜsᴇʀs\n"
                f"📅 ᴛʜɪs ᴡᴇᴇᴋ: {this_week} ᴜsᴇʀs\n"
                f"📆 ᴛʜɪs ᴍᴏɴᴛʜ: {this_month} ᴜsᴇʀs\n"
                f"📋 ʟᴀsᴛ ᴍᴏɴᴛʜ: {last_month} ᴜsᴇʀs</b>"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="refresh_verify_count")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="verify_settings")]
            ])
            
            await query.message.edit_text(count_text, reply_markup=keyboard)
        
        elif data == "verify_count":
            today = await rexbots.get_vr_count_combined('today')
            yesterday = await rexbots.get_vr_count_combined('yesterday')
            this_week = await rexbots.get_vr_count_combined('this_week')
            this_month = await rexbots.get_vr_count_combined('this_month')
            last_month = await rexbots.get_vr_count_combined('last_month')
            
            count_text = (
                "<b>📊 ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ sᴛᴀᴛɪsᴛɪᴄs:\n\n"
                f"👥 ᴛᴏᴅᴀʏ: {today} ᴜsᴇʀs\n"
                f"📊 ʏᴇsᴛᴇʀᴅᴀʏ: {yesterday} ᴜsᴇʀs\n"
                f"📅 ᴛʜɪs ᴡᴇᴇᴋ: {this_week} ᴜsᴇʀs\n"
                f"📆 ᴛʜɪs ᴍᴏɴᴛʜ: {this_month} ᴜsᴇʀs\n"
                f"📋 ʟᴀsᴛ ᴍᴏɴᴛʜ: {last_month} ᴜsᴇʀs</b>"
            )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="refresh_verify_count")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="verify_settings")]
            ])
            
            await query.message.edit_text(count_text, reply_markup=keyboard)

    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" in str(e) or "message is not modified" in str(e):
            await query.answer("✅ Data is already up to date!", show_alert=True)
        else:
            await query.answer(f"Error: {e}", show_alert=True)




# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
