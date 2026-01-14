# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
import os
import re
import json
import time
import shutil
import asyncio
import logging
import uuid
import pytz
from datetime import datetime
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatAction, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor  # Added missing import
from plugins.antinsfw import check_anti_nsfw
from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import rexbots
from plugins.start import *
from config import Config
from functools import wraps
from os import makedirs
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
Semaphore = asyncio.Semaphore(3)  # Fixed: Should be asyncio.Semaphore
chat_data_cache = {}
ADMIN_URL = Config.ADMIN_URL
FSUB_PIC = Config.FSUB_PIC
BOT_USERNAME = Config.BOT_USERNAME
OWNER_ID = Config.OWNER_ID
FSUB_LINK_EXPIRY = 10
thread_pool = ThreadPoolExecutor(max_workers=4)
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
# ========== Decorators ==========

def check_ban(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        user = await rexbots.col.find_one({"_id": user_id})
        if user and user.get("ban_status", {}).get("is_banned", False):
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ...!!", url=ADMIN_URL)]]
            )
            return await message.reply_text(
                "Wᴛғ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ʙʏ ᴏᴜʀ ᴀᴅᴍɪɴ/ᴏᴡɴᴇʀ . Iғ ʏᴏᴜ ᴛʜɪɴᴋs ɪᴛ's ᴍɪsᴛᴀᴋᴇ ᴄʟɪᴄᴋ ᴏɴ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ...!!",
                reply_markup=keyboard
            )
        return await func(client, message, *args, **kwargs)
    return wrapper

# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
async def check_user_premium(user_id):
    """Check if user has premium access - handles missing method gracefully"""
    try:
        # First check if the method exists
        if hasattr(rexbots, 'has_premium_access'):
            return await rexbots.has_premium_access(user_id)
        else:
            # Fallback: Check database directly
            user_data = await rexbots.col.find_one({"_id": user_id})
            if not user_data:
                return False
            
            # Check for premium in user data
            premium_data = user_data.get("premium", {})
            
            # Check if premium is active and not expired
            is_premium = premium_data.get("is_premium", False)
            expiry_date = premium_data.get("expiry_date")
            
            if is_premium and expiry_date:
                if isinstance(expiry_date, datetime):
                    return expiry_date > datetime.utcnow()
                else:
                    return True
            
            return is_premium
    except Exception as e:
        logger.error(f"Error checking premium status: {e}")
        return False
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def check_verification(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        logger.debug(f"check_verification decorator called for user {user_id}")
        
        try:
            text = message.text or message.caption
            if text and len(text) > 7:
                try:
                    param = text.split(" ", 1)[1]
                    if param.startswith("verify_"):
                        token = param[7:]
                        await handle_verification_callback(client, message, token)
                        return
                        
                except Exception as e:
                    logger.error(f"Error processing start parameter: {e}")
                    await message.reply_text(f"Error: {e}")
    
            # Step 1: Check if user has premium access - premium users bypass verification
            try:
                if await check_user_premium(user_id):
                    logger.debug(f"User {user_id} has premium, bypassing verification")
                    return await func(client, message, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error checking premium status in decorator: {e}")
                # Continue with verification check even if premium check fails
            
            # Step 2: Get verification settings to check if verification is enabled
            settings = await rexbots.get_verification_settings()
            verify_status_1 = settings.get("verify_status_1", False)
            verify_status_2 = settings.get("verify_status_2", False)
            
            # If both verification systems are disabled, allow access
            if not verify_status_1 and not verify_status_2:
                logger.debug(f"Verification disabled, allowing user {user_id}")
                return await func(client, message, *args, **kwargs)
            
            # Step 3: Check if user is already verified (EXACTLY like /verify command)
            try:
                if await is_user_verified(user_id):
                    try:
                        user_data = await rexbots.col.find_one({"_id": user_id}) or {}
                        verification_data = user_data.get("verification", {})
                        
                        verified_time_1 = verification_data.get("verified_time_1")
                        verified_time_2 = verification_data.get("verified_time_2")
                        
                        current_time = datetime.utcnow()
                        
                        # Check if fully verified (shortener 1 within 24 hours)
                        if verified_time_1:
                            try:
                                if isinstance(verified_time_1, datetime) and current_time < verified_time_1 + timedelta(hours=24):
                                    time_left = timedelta(hours=24) - (current_time - verified_time_1)
                                    hours_left = time_left.seconds // 3600
                                    minutes_left = (time_left.seconds % 3600) // 60
                                    return await func(client, message, *args, **kwargs)
                            except Exception as e:
                                logger.error(f"Error checking verified_time_1: {e}")

                        # Check if fully verified (shortener 2 within 24 hours)
                        if verified_time_2:
                            try:
                                if isinstance(verified_time_2, datetime) and current_time < verified_time_2 + timedelta(hours=24):
                                    time_left = timedelta(hours=24) - (current_time - verified_time_2)
                                    hours_left = time_left.seconds // 3600
                                    minutes_left = (time_left.seconds % 3600) // 60
                                    return await func(client, message, *args, **kwargs)
                            except Exception as e:
                                logger.error(f"Error checking verified_time_2: {e}")
                                
                    except Exception as e:
                        logger.error(f"Error checking verification status: {e}")
            except Exception as e:
                logger.error(f"Error in is_user_verified check: {e}")

            
            # Step 4: User is NOT verified - send verification message
            logger.debug(f"User {user_id} is not verified, sending verification prompt")

            try:
                await send_verification_message(client, message)
            except Exception as e:
                logger.error(f"Error sending verification message in decorator: {e}")
                await message.reply_text(
                    f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @seishiro_obito</i></b>\n"
                    f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {str(e)}</blockquote>"
                )
            return
            
        except Exception as e:
            logger.error(f"FATAL ERROR in check_verification decorator: {e}")
            await message.reply_text(
                f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @seishiro_obito</i></b>\n"
                f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {str(e)}</blockquote>"
            )
            return
    
    return wrapper
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def check_fsub(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        print(f"DEBUG: check_fsub decorator called for user {user_id}")

        async def is_sub(client, user_id, channel_id):
            try:
                member = await client.get_chat_member(channel_id, user_id)
                status = member.status
                return status in {
                    ChatMemberStatus.OWNER,
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.MEMBER
                }
            except UserNotParticipant:
                mode = await rexbots.get_channel_mode(channel_id)
                if mode == "on":
                    exists = await rexbots.req_user_exist(channel_id, user_id)
                    return exists
                return False
            except Exception as e:
                print(f"[!] Error in is_sub(): {e}")
                return False

        async def is_subscribed(client, user_id):
            channel_ids = await rexbots.show_channels()
            if not channel_ids:
                return True
            if user_id == OWNER_ID:
                return True
            for cid in channel_ids:
                if not await is_sub(client, user_id, cid):
                    mode = await rexbots.get_channel_mode(cid)
                    if mode == "on":
                        await asyncio.sleep(2)
                        if await is_sub(client, user_id, cid):
                            continue
                    return False
            return True
        
        try:
            is_sub_status = await is_subscribed(client, user_id)
            print(f"DEBUG: User {user_id} subscribed status: {is_sub_status}")
            
            if not is_sub_status:
                print(f"DEBUG: User {user_id} is not subscribed, calling not_joined.")
                return await not_joined(client, message)
            
            print(f"DEBUG: User {user_id} is subscribed, proceeding with function call.")
            return await func(client, message, *args, **kwargs)
        
        except Exception as e:
            print(f"FATAL ERROR in check_fsub: {e}")
            await message.reply_text(f"An unexpected error occurred: `{e}`. Please contact the developer.")
            return

    return wrapper
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
async def check_admin(filter, client, update):
    try:
        user_id = update.from_user.id
        return any([user_id == OWNER_ID, await rexbots.admin_exist(user_id)])
    except Exception as e:
        print(f"! Exception in check_admin: {e}")
        return False

async def not_joined(client: Client, message: Message):
    print(f"DEBUG: not_joined function called for user {message.from_user.id}")
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>")

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await rexbots.show_channels()
        for chat_id in all_channels:
            mode = await rexbots.get_channel_mode(chat_id)

            await message.reply_chat_action(ChatAction.TYPING)

            # Re-check is_sub status for this logic
            try:
                member = await client.get_chat_member(chat_id, user_id)
                is_member = member.status in {
                    ChatMemberStatus.OWNER,
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.MEMBER
                }
            except UserNotParticipant:
                is_member = False
            except Exception as e:
                is_member = False
                print(f"[!] Error checking member in not_joined: {e}")

            if not is_member:
                try:
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title

                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                        )
                        link = invite.invite_link
                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Error with chat {chat_id}: {e}")
                    return await temp.edit(
                        f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @seishiro_obito</i></b>\n"
                        f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
                    )

        try:
            buttons.append([
                InlineKeyboardButton(
                    text='• Jᴏɪɴᴇᴅ •',
                    url=f"https://t.me/{Config.BOT_USERNAME}?start=true"
                )
            ])
        except IndexError:
            pass

        text = "<b>Yᴏᴜ Bᴀᴋᴋᴀᴀ...!! \n\n<blockquote>Jᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍʏ ᴏᴛʜᴇʀᴡɪsᴇ Yᴏᴜ ᴀʀᴇ ɪɴ ʙɪɢ sʜɪᴛ...!!</blockquote></b>"
        await temp.delete()
        
        print(f"DEBUG: Sending final reply photo to user {user_id}")
        await message.reply_photo(
            photo=FSUB_PIC,
            caption=text,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except Exception as e:
        print(f"Final Error: {e}")
        await temp.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @seishiro_obito</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )
        
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

active_sequences = {}
message_ids = {}
renaming_operations = {}
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def detect_quality(file_name):
    quality_order = {"360p": 0, "480p": 1, "720p": 2, "1080p": 3, "1440p": 4, "2160p": 5, "4k": 6}
    match = re.search(r"(360p|480p|720p|1080p|1440p|2160p|4k)\b", file_name, re.IGNORECASE)
    return quality_order.get(match.group(1).lower(), 7) if match else 7

# --- Duration Detection Function (from the first bot) ---
async def detect_duration(file_path):
    """Detect the duration of a video or audio file using ffprobe."""
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        logger.error("ffprobe not found in PATH")
        raise RuntimeError("ffprobe not found in PATH")

    cmd = [
        ffprobe,
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        file_path
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    try:
        info = json.loads(stdout)
        format_info = info.get('format', {})
        duration = float(format_info.get('duration', 0))
        return duration
    except Exception as e:
        logger.error(f"Duration detection error: {e}")
        return 0

# --- REVISED extract_episode_number ---
def extract_episode_number(filename):
    if not filename:
        return None

    print(f"DEBUG: Extracting episode from: '{filename}')")

    quality_and_year_indicators = [
        r'\d{2,4}[pP]',
        r'\dK',
        r'HD(?:RIP)?',
        r'WEB(?:-)?DL',
        r'BLURAY',
        r'X264',
        r'X265',
        r'HEVC',
        r'FHD',
        r'UHD',
        r'HDR',
        r'H\.264', r'H\.265',
        r'(?:19|20)\d{2}',
        r'Multi(?:audio)?',
        r'Dual(?:audio)?',
    ]
    quality_pattern_for_exclusion = r'(?:' + '|'.join([f'(?:[\s._-]*{ind})' for ind in quality_and_year_indicators]) + r')'

    patterns = [
        re.compile(r'S\d+[.-_]?E(\d+)', re.IGNORECASE),
        re.compile(r'(?:Episode|EP)[\s._-]*(\d+)', re.IGNORECASE),
        re.compile(r'\bE(\d+)\b', re.IGNORECASE),
        re.compile(r'[\[\(]E(\d+)[\]\)]', re.IGNORECASE),
        re.compile(r'\b(\d+)\s*of\s*\d+\b', re.IGNORECASE),

        re.compile(
            r'(?:^|[^0-9A-Z])'
            r'(\d{1,4})'
            r'(?:[^0-9A-Z]|$)'
            r'(?!' + quality_pattern_for_exclusion + r')'
            , re.IGNORECASE
        ),
    ]

    for i, pattern in enumerate(patterns):
        matches = pattern.findall(filename)
        if matches:
            for match in matches:
                try:
                    if isinstance(match, tuple):
                        episode_str = match[0]
                    else:
                        episode_str = match

                    episode_num = int(episode_str)

                    if 1 <= episode_num <= 9999:
                        if episode_num in [360, 480, 720, 1080, 1440, 2160, 2020, 2021, 2022, 2023, 2024, 2025]:
                            if re.search(r'\b' + str(episode_num) + r'(?:p|K|HD|WEB|BLURAY|X264|X265|HEVC|Multi|Dual)\b', filename, re.IGNORECASE) or \
                                re.search(r'\b(?:19|20)\d{2}\b', filename, re.IGNORECASE) and len(str(episode_num)) == 4:
                                print(f"DEBUG: Skipping {episode_num} as it is a common quality/year number.")
                                continue

                        print(f"DEBUG: Episode Pattern {i+1} found episode: {episode_num}")
                        return episode_num
                except ValueError:
                    continue

    print(f"DEBUG: No episode number found in: '{filename}'")
    return None
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
# --- MODIFIED: extract_season_number (added negative lookahead) ---
def extract_season_number(filename):
    if not filename:
        return None

    print(f"DEBUG: Extracting season from: '{filename}')")

    quality_and_year_indicators = [
        r'\d{2,4}[pP]',
        r'\dK',
        r'HD(?:RIP)?',
        r'WEB(?:-)?DL',
        r'BLURAY',
        r'X264',
        r'X265',
        r'HEVC',
        r'FHD',
        r'UHD',
        r'HDR',
        r'H\.264', r'H\.265',
        r'(?:19|20)\d{2}',
        r'Multi(?:audio)?',
        r'Dual(?:audio)?',
    ]
    quality_pattern_for_exclusion = r'(?:' + '|'.join([f'(?:[\s._-]*{ind})' for ind in quality_and_year_indicators]) + r')'


    patterns = [
        re.compile(r'S(\d+)[._-]?E\d+', re.IGNORECASE),

        re.compile(r'(?:Season|SEASON|season)[\s._-]*(\d+)', re.IGNORECASE),

        re.compile(r'\bS(\d+)\b(?!E\d|' + quality_pattern_for_exclusion + r')', re.IGNORECASE),

        re.compile(r'[\[\(]S(\d+)[\]\)]', re.IGNORECASE),

        re.compile(r'[._-]S(\d+)(?:[._-]|$)', re.IGNORECASE),

        re.compile(r'(?:season|SEASON|Season)[\s._-]*(\d+)', re.IGNORECASE),

        re.compile(r'(?:^|[\s._-])(?:season|SEASON|Season)[\s._-]*(\d+)(?:[\s._-]|$)', re.IGNORECASE),

        re.compile(r'[\[\(](?:season|SEASON|Season)[\s._-]*(\d+)[\]\)]', re.IGNORECASE),

        re.compile(r'(?:season|SEASON|Season)[._\s-]+(\d+)', re.IGNORECASE),

        re.compile(r'(?:^season|season$)[\s._-]*(\d+)', re.IGNORECASE),
    ]

    for i, pattern in enumerate(patterns):
        match = pattern.search(filename)
        if match:
            try:
                season_num = int(match.group(1))
                if 1 <= season_num <= 99:
                    print(f"DEBUG: Season Pattern {i+1} found season: {season_num}")
                    return season_num
            except ValueError:
                continue

    print(f"DEBUG: No season number found in: '{filename}'")
    return None
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def extract_audio_info(filename):
    """Extract audio information from filename, including languages and 'dual'/'multi'."""
    audio_keywords = {
        'Hindi': re.compile(r'Hindi', re.IGNORECASE),
        'English': re.compile(r'English', re.IGNORECASE),
        'Multi': re.compile(r'Multi(?:audio)?', re.IGNORECASE),
        'Telugu': re.compile(r'Telugu', re.IGNORECASE),
        'Eng': re.compile(r'Eng', re.IGNORECASE),
        'Sub': re.compile(r'Sub', re.IGNORECASE),
        'Eng sub': re.compile(r'Eng sub', re.IGNORECASE),
        'Dub': re.compile(r'Dub', re.IGNORECASE),
        'Eng dub': re.compile(r'Eng dub', re.IGNORECASE),
        'Tamil': re.compile(r'Tamil', re.IGNORECASE),
        'Jap': re.compile(r'Jap', re.IGNORECASE),
        'Dual': re.compile(r'Dual(?:audio)?', re.IGNORECASE),
        'Dual_Enhanced': re.compile(r'(?:DUAL(?:[\s._-]?AUDIO)?|\[DUAL\])', re.IGNORECASE),
        'AAC': re.compile(r'AAC', re.IGNORECASE),
        'AC3': re.compile(r'AC3', re.IGNORECASE),
        'DTS': re.compile(r'DTS', re.IGNORECASE),
        'MP3': re.compile(r'MP3', re.IGNORECASE),
        '5.1': re.compile(r'5\.1', re.IGNORECASE),
        '2.0': re.compile(r'2\.0', re.IGNORECASE),
    }

    detected_audio = []

    if re.search(r'\bMulti(?:audio)?\b', filename, re.IGNORECASE):
        detected_audio.append("Multi")
    if re.search(r'\bDual(?:audio)?\b', filename, re.IGNORECASE):
        detected_audio.append("Dual")


    priority_keywords = ['Hindi', 'English', 'Telugu', 'Tamil', 'Eng', 'Sub', 'Eng sub', 'Dub', 'Eng dub', 'Jap']
    for keyword in priority_keywords:
        if audio_keywords[keyword].search(filename):
            if keyword not in detected_audio:
                detected_audio.append(keyword)

    for keyword in ['AAC', 'AC3', 'DTS', 'MP3', '5.1', '2.0']:
        if audio_keywords[keyword].search(filename):
            if keyword not in detected_audio:
                detected_audio.append(keyword)

    detected_audio = list(dict.fromkeys(detected_audio))

    if detected_audio:
        return ' '.join(detected_audio)

    return None
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
def extract_quality(filename):
    """Extract video quality from filename."""
    patterns = [
        re.compile(r'\b(4K|2K|2160p|1440p|1080p|720p|480p|360p)\b', re.IGNORECASE),
        re.compile(r'\b(HD(?:RIP)?|WEB(?:-)?DL|BLURAY)\b', re.IGNORECASE),
        re.compile(r'\b(X264|X265|HEVC)\b', re.IGNORECASE),
    ]

    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            found_quality = match.group(1)
            if found_quality.lower() in ["4k", "2k", "hdrip", "web-dl", "bluray"]:
                return found_quality.upper() if found_quality.upper() in ["4K", "2K"] else found_quality.capitalize()
            return found_quality

    return None

@Client.on_message(filters.command("start_sequence") & filters.private)
@check_ban
@check_fsub
async def start_sequence(client, message: Message):
    user_id = message.from_user.id
    if user_id in active_sequences:
        await message.reply_text("Hᴇʏ ᴅᴜᴅᴇ...!! A sᴇǫᴜᴇɴᴄᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴇ! Usᴇ /end_sequence ᴛᴏ ᴇɴᴅ ɪᴛ.")
    else:
        active_sequences[user_id] = []
        message_ids[user_id] = []
        msg = await message.reply_text("Sᴇǫᴜᴇɴᴄᴇ sᴛᴀʀᴛᴇᴅ! Sᴇɴᴅ ʏᴏᴜʀ ғɪʟᴇs ɴᴏᴡ ʙʀᴏ....Fᴀsᴛ")
        message_ids[user_id].append(msg.id)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
@check_ban
@check_verification
@check_fsub
async def auto_rename_files(client, message):
    """Main handler for auto-renaming files"""
    async with Semaphore:
        # Initialize variables at the start to avoid UnboundLocalError
        msg = None 
        download_path = None
        metadata_path = None
        output_path = None
        input_path = None
        
        try:
            user_id = message.from_user.id
            user = message.from_user
            format_template = await rexbots.get_format_template(user_id)
            media_preference = await rexbots.get_media_preference(user_id)
        
            if not format_template:
                await message.reply_text("Pʟᴇᴀsᴇ Sᴇᴛ Aɴ Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ Fɪʀsᴛ Usɪɴɢ /autorename")
                return
        
            # Correctly identify file properties and initial media type
            if message.document:
                file_id = message.document.file_id
                file_name = message.document.file_name
                file_size = message.document.file_size
                media_type = "document"
            elif message.video:
                file_id = message.video.file_id
                file_name = message.video.file_name or "video"
                file_size = message.video.file_size
                media_type = "video"
            elif message.audio:
                file_id = message.audio.file_id
                file_name = message.audio.file_name or "audio"
                file_size = message.audio.file_size
                media_type = "audio"
            else:
                return await message.reply_text("Unsupported file type")
                
            if not file_name:
                await message.reply_text("Could not determine file name.")
                return

            if file_id in renaming_operations:
                if (datetime.now() - renaming_operations[file_id]).seconds < 10:
                    return
            renaming_operations[file_id] = datetime.now()
                    
            file_info = {
                "file_id": file_id,
                "file_name": file_name,
                "message": message,
                "episode_num": extract_episode_number(file_name)
            }

            if user_id in active_sequences:
                active_sequences[user_id].append(file_info)
                reply_msg = await message.reply_text("Wᴇᴡ...ғɪʟᴇs ʀᴇᴄᴇɪᴠᴇᴅ ɴᴏᴡ ᴜsᴇ /end_sequence ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs...!!")
                message_ids[user_id].append(reply_msg.id)
                return

            if media_preference:
                media_type = media_preference
            else:
                # Fallback to intelligent guessing if no preference is set
                if file_name.endswith((".mp4", ".mkv", ".avi", ".webm")):
                    media_type = "document"
                elif file_name.endswith((".mp3", ".flac", ".wav", ".ogg")):
                    media_type = "audio"
                else:
                    media_type = "video"

            if await check_anti_nsfw(file_name, message):
                await message.reply_text("NSFW ᴄᴏɴᴛᴇɴᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ. Fɪʟᴇ ᴜᴘʟᴏᴀᴅ ʀᴇᴊᴇᴄᴛᴇᴅ.")
                return

            episode_number = extract_episode_number(file_name)
            season_number = extract_season_number(file_name)
            audio_info_extracted = extract_audio_info(file_name)
            quality_extracted = extract_quality(file_name)

            print(f"DEBUG: Final extracted values - Season: {season_number}, Episode: {episode_number}, Quality: {quality_extracted}, Audio: {audio_info_extracted}")

            season_value_formatted = str(season_number).zfill(2) if season_number is not None else "01"
            episode_value_formatted = str(episode_number).zfill(2) if episode_number is not None else "01"

            template = re.sub(r'S(?:Season|season|SEASON)(\d+)', f'S{season_value_formatted}', format_template, flags=re.IGNORECASE)

            season_replacements = [
                (re.compile(r'\{season\}', re.IGNORECASE), season_value_formatted),
                (re.compile(r'\{Season\}', re.IGNORECASE), season_value_formatted),
                (re.compile(r'\{SEASON\}', re.IGNORECASE), season_value_formatted),
                (re.compile(r'\bseason\b', re.IGNORECASE), season_value_formatted),
                (re.compile(r'\bSeason\b', re.IGNORECASE), season_value_formatted),
                (re.compile(r'\bSEASON\b', re.IGNORECASE), season_value_formatted),
                (re.compile(r'Season[\s._-]*\d*', re.IGNORECASE), season_value_formatted),
                (re.compile(r'season[\s._-]*\d*', re.IGNORECASE), season_value_formatted),
                (re.compile(r'SEASON[\s._-]*\d*', re.IGNORECASE), season_value_formatted),
            ]

            for pattern, replacement in season_replacements:
                template = pattern.sub(replacement, template)
                    
            template = re.sub(r'EP(?:Episode|episode|EPISODE)', f'EP{episode_value_formatted}', template, flags=re.IGNORECASE)

            episode_patterns = [
                re.compile(r'\{episode\}', re.IGNORECASE),
                re.compile(r'\bEpisode\b', re.IGNORECASE),
                re.compile(r'\bEP\b', re.IGNORECASE)
            ]

            for pattern in episode_patterns:
                template = pattern.sub(episode_value_formatted, template)

            audio_replacement = audio_info_extracted if audio_info_extracted else ""
            audio_patterns = [
                re.compile(r'\{audio\}', re.IGNORECASE),
                re.compile(r'\bAudio\b', re.IGNORECASE),
            ]

            for pattern in audio_patterns:
                template = pattern.sub(audio_replacement, template)

            quality_replacement = quality_extracted if quality_extracted else ""
            quality_patterns = [
                re.compile(r'\{quality\}', re.IGNORECASE),
                re.compile(r'\bQuality\b', re.IGNORECASE),
            ]

            for pattern in quality_patterns:
                template = pattern.sub(quality_replacement, template)

            template = re.sub(r'\[\s*\]', '', template)
            template = re.sub(r'\(\s*\)', '', template)
            template = re.sub(r'\{\s*\}', '', template)

            _, file_extension = os.path.splitext(file_name)

            # Force MP4 files to be converted to MKV to ensure subtitle compatibility
            if file_extension.lower() in ['.mp4', '.m4v']:
                final_extension = ".mkv"
            else:
                final_extension = file_extension

            if not final_extension.startswith('.'):
                final_extension = '.' + final_extension if file_extension else ''
    
            new_file_name = f"{template}{final_extension}"
            user_folder = str(user_id)
            download_path = os.path.join("downloads", user_folder, new_file_name)
            metadata_path = os.path.join("metadata", user_folder, new_file_name)
            output_path = os.path.join("processed", user_folder, new_file_name)

            # Create user-specific directories
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            msg = await message.reply_text("Wᴇᴡ... Iᴀm ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ғɪʟᴇ...!!")
            await message.reply_chat_action(ChatAction.PLAYING)

            try:
                file_path = await client.download_media(
                    message,
                    file_name=download_path,
                    progress=progress_for_pyrogram,
                    progress_args=("Dᴏᴡɴʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ ᴅᴜᴅᴇ...!!", msg, time.time())
                )
            except Exception as e:
                await msg.edit(f"Dᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ: {e}")
                raise

            if file_extension.lower() in ['.mp4', '.m4v']:
                await msg.edit("MP4! Dᴇᴛᴇᴄᴛᴇᴅ. Cᴏɴᴠᴇʀᴛɪɴɢ ᴛᴏ MKV...")
                await message.reply_chat_action(ChatAction.PLAYING)
                try:
                    await convert_to_mkv(file_path, metadata_path, user_id)
                    file_path = metadata_path
                except Exception as e:
                    await msg.edit(f"❌ Eʀʀᴏʀ Dᴜʀɪɴɢ ᴄᴏɴᴠᴇʀᴛɪɴɢ ᴛᴏ ᴍᴋᴠ... {str(e)}")
                    return

            # Detect duration for video or audio files
            duration = 0
            if media_type in ["video", "audio"] or file_name.endswith((".mp4", ".mkv", ".avi", ".webm", ".mp3", ".flac", ".wav", ".ogg")):
                try:
                    duration = await detect_duration(file_path)
                except Exception as e:
                    logger.error(f"Failed to detect duration: {e}")
                    duration = 0
            human_readable_duration = convert(duration) if duration > 0 else "N/A"
            
            # Only add metadata if not already converted (to avoid double processing)
            if not file_extension.lower() in ['.mp4', '.m4v']:
                await msg.edit("Nᴏᴡ ᴀᴅᴅɪɴɢ ᴍᴇᴛᴀᴅᴀᴛᴀ ᴅᴜᴅᴇ...!!")
                await message.reply_chat_action(ChatAction.PLAYING)
                try:
                    await add_metadata(file_path, metadata_path, user_id)
                    file_path = metadata_path
                except Exception as e:
                    logger.error(f"Failed to add metadata: {e}")

            await msg.edit("Wᴇᴡ... Iᴀm Uᴘʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ғɪʟᴇ...!!")
            await message.reply_chat_action(ChatAction.PLAYING)
            
            try:
                await rexbots.col.update_one(
                    {"_id": user_id},
                    {
                        "$inc": {"rename_count": 1},
                        "$set": {
                            "first_name": message.from_user.first_name,
                            "username": message.from_user.username,
                            "last_activity_timestamp": datetime.now()
                        }
                    }
                )
            except Exception as e:
                logger.error(f"Failed to update database: {e}")

            c_caption = await rexbots.get_caption(message.chat.id)
            
            if c_caption:
                caption = c_caption.format(
                    filename=new_file_name,
                    filesize=humanbytes(file_size),
                    duration=human_readable_duration
                )
            else:
                caption = f"**{new_file_name}**"
                
            c_thumb = await rexbots.get_thumbnail(message.chat.id)

            ph_path = None
            if c_thumb:
                ph_path = await client.download_media(c_thumb)
            elif media_type == "video" and message.video and message.video.thumbs:
                try:
                    ph_path = await client.download_media(message.video.thumbs[0].file_id)
                except IndexError:
                    ph_path = None

            if ph_path:
                try:
                    img = Image.open(ph_path).convert("RGB")
                    img.save(ph_path, "JPEG")
                except Exception as e:
                    logger.error(f"Failed to process video thumbnail: {e}")
                    ph_path = None

            # Define common upload parameters
            common_upload_params = {
                'chat_id': message.chat.id,
                'caption': caption,
                'thumb': ph_path,
                'progress': progress_for_pyrogram,
                'progress_args': ("Uᴘʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ ᴅᴜᴅᴇ...!!", msg, time.time())
            }

            sent_message = None
            if media_type == "document":
                sent_message = await client.send_document(document=file_path, **common_upload_params)
            elif media_type == "video":
                if duration > 0:
                    common_upload_params['duration'] = int(duration)
                sent_message = await client.send_video(video=file_path, **common_upload_params)
            elif media_type == "audio":
                if duration > 0:
                    common_upload_params['duration'] = int(duration)
                sent_message = await client.send_audio(audio=file_path, **common_upload_params)

            if Config.DUMP:
                try:
                    ist = pytz.timezone('Asia/Kolkata')
                    current_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")
                    
                    first_name = message.from_user.first_name
                    full_name = first_name
                    if message.from_user.last_name:
                        full_name += f" {user.last_name}"
                    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
                    has_premium_accesss = await check_user_premium(user_id)
                    premium_status = '🗸' if has_premium_accesss else '✘'
                    
                    dump_caption = (
                        f"» Usᴇʀ Dᴇᴛᴀɪʟs «\n"
                        f"ID: {user_id}\n"
                        f"Nᴀᴍᴇ: {first_name}\n"
                        f"Usᴇʀɴᴀᴍᴇ: {username}\n"
                        f"Pʀᴇᴍɪᴜᴍ: {premium_status}\n"
                        f"Tɪᴍᴇ: {current_time}\n"
                        f"Oʀɪɢɪɴᴀʟ Fɪʟᴇɴᴀᴍᴇ: {file_name}\n"
                        f"Rᴇɴᴀᴍᴇᴅ Fɪʟᴇɴᴀᴍᴇ: {new_file_name}"
                    )
                    
                    dump_channel = Config.DUMP_CHANNEL
                    if media_type == "document" and sent_message.document:
                        await client.send_document(
                            chat_id=dump_channel,
                            document=sent_message.document.file_id,
                            thumb=ph_path,
                            caption=dump_caption
                        )
                    elif media_type == "video" and sent_message.video:
                        await client.send_video(
                            chat_id=dump_channel,
                            video=sent_message.video.file_id,
                            thumb=ph_path,
                            caption=dump_caption
                        )
                    elif media_type == "audio" and sent_message.audio:
                        await client.send_audio(
                            chat_id=dump_channel,
                            audio=sent_message.audio.file_id,
                            thumb=ph_path,
                            caption=dump_caption
                        )
                except Exception as e:
                    logger.error(f"Error sending to dump channel: {e}")
                    await msg.edit(f"❌ Eʀʀᴏʀ: {str(e)}")
                    
            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Eʀʀᴏʀ ᴅᴜʀɪɴɢ ʀᴇɴᴀᴍɪɴɢ: {str(e)}")
            raise
        finally:
            # Clean up files
            for path in [download_path, metadata_path]:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception as e:
                        print(f"Error removing file {path}: {e}")
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.command("showformat") & filters.private)
@check_ban
@check_fsub
async def show_format_cmd(client, message: Message):
    """Shows the user their currently set auto-rename format."""
    user_id = message.from_user.id
    
    # 1. Fetch the format template from the database
    # This calls the same function used in your auto_rename_files handler
    try:
        format_template = await rexbots.get_format_template(user_id)
    except Exception as e:
        # Handle potential database errors (optional but recommended)
        await message.reply_text(f"❌ Eʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ғᴏʀᴍᴀᴛ: {e}")
        return

    # 2. Check if a format was found
    if format_template:
        response_text = (
            f"✨ Yᴏᴜʀ ᴄᴜʀʀᴇɴᴛ Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ ɪs:\n\n"
            f"/autorename `{format_template}`\n\n"
            "Uꜱᴇ /autorename ᴛᴏ ᴄʜᴀɴɢᴇ ɪᴛ."
        )
    else:
        response_text = (
            "⚠️ Yᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ꜱᴇᴛ ᴀɴ Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ ʏᴇᴛ.\n"
            "Pʟᴇᴀꜱᴇ ꜱᴇᴛ ᴏɴᴇ ᴜꜱɪɴɢ /autorename."
        )

    # 3. Send the response
    await message.reply_text(response_text)
# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
@Client.on_message(filters.command("end_sequence") & filters.private)
@check_ban
@check_fsub
async def end_sequence(client, message: Message):
    user_id = message.from_user.id
    if user_id not in active_sequences:
        await message.reply_text("Wʜᴀᴛ ᴀʀᴇ ʏᴏᴜ ᴅᴏɪɴɢ ɴᴏ ᴀᴄᴛɪᴠᴇ sᴇǫᴜᴇɴᴄᴇ ғᴏᴜɴᴅ...!!")
    else:
        file_list = active_sequences.pop(user_id, [])
        delete_messages = message_ids.pop(user_id, [])
        count = len(file_list)

        if not file_list:
            await message.reply_text("Nᴏ ғɪʟᴇs ᴡᴇʀᴇ sᴇɴᴛ ɪɴ ᴛʜɪs sᴇǫᴜᴇɴᴄᴇ....ʙʀᴏ...!!")
        else:
            file_list.sort(key=lambda x: x["episode_num"] if x["episode_num"] is not None else float('inf'))
            await message.reply_text(f"Sᴇǫᴜᴇɴᴄᴇ ᴇɴᴅᴇᴅ. Nᴏᴡ sᴇɴᴅɪɴɢ ʏᴏᴜʀ {count} ғɪʟe(s) ʙᴀᴄᴋ ɪɴ sᴇǫᴜᴇɴᴄᴇ...!!")

            for index, file_info in enumerate(file_list, 1):
                try:
                    await asyncio.sleep(0.5)

                    original_message = file_info["message"]

                    if original_message.document:
                        await client.send_document(
                            message.chat.id,
                            original_message.document.file_id,
                            caption=f"{file_info['file_name']}"
                        )
                    elif original_message.video:
                        await client.send_video(
                            message.chat.id,
                            original_message.video.file_id,
                            caption=f"{file_info['file_name']}"
                        )
                    elif original_message.audio:
                        await client.send_audio(
                            message.chat.id,
                            original_message.audio.file_id,
                            caption=f"{file_info['file_name']}"
                        )
                except Exception as e:
                    await message.reply_text(f"Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ғɪʟᴇ: {file_info.get('file_name', '')}\n{e}")

            await message.reply_text(f"✅ Aʟʟ {count} ғɪʟes sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ɪɴ sᴇǫᴜᴇɴᴄᴇ!")

        try:
            await client.delete_messages(chat_id=message.chat.id, message_ids=delete_messages)
        except Exception as e:
            print(f"Error deleting messages: {e}")

async def add_metadata(input_path, output_path, user_id):
    ffmpeg_cmd = shutil.which('ffmpeg')
    if not ffmpeg_cmd:
        raise RuntimeError("FFmpeg not found in PATH")

    metadata_command = [
        ffmpeg_cmd,
        '-i', input_path,
        '-metadata', f'title={await rexbots.get_title(user_id)}',
        '-metadata', f'artist={await rexbots.get_artist(user_id)}',
        '-metadata', f'author={await rexbots.get_author(user_id)}',
        '-metadata:s:v', f'title={await rexbots.get_video(user_id)}',
        '-metadata:s:a', f'title={await rexbots.get_audio(user_id)}',
        '-metadata:s:s', f'title={await rexbots.get_subtitle(user_id)}',
        '-metadata', f'encoded_by={await rexbots.get_encoded_by(user_id)}',
        '-metadata', f'custom_tag={await rexbots.get_custom_tag(user_id)}',
        '-map', '0',
        '-c', 'copy',
        '-loglevel', 'error',
        '-y',
        output_path
    ]

    process = await asyncio.create_subprocess_exec(
        *metadata_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {stderr.decode()}")

async def convert_to_mkv(input_path, output_path, user_id):
    """Convert video file to MKV format"""
    ffmpeg_cmd = shutil.which('ffmpeg')
    if not ffmpeg_cmd:
        raise RuntimeError("FFmpeg not found in PATH")

    metadata_add_cmd = [
        ffmpeg_cmd,
        '-hide_banner',
        '-i', input_path,
        '-metadata', f'title={await rexbots.get_title(user_id)}',
        '-metadata', f'artist={await rexbots.get_artist(user_id)}',
        '-metadata', f'author={await rexbots.get_author(user_id)}',
        '-metadata:s:v', f'title={await rexbots.get_video(user_id)}',
        '-metadata:s:a', f'title={await rexbots.get_audio(user_id)}',
        '-metadata:s:s', f'title={await rexbots.get_subtitle(user_id)}',
        '-metadata', f'encoded_by={await rexbots.get_encoded_by(user_id)}',
        '-metadata', f'custom_tag={await rexbots.get_custom_tag(user_id)}',
        '-map', '0',
        '-c', 'copy',
        '-f', 'matroska',
        '-y',
        output_path
    ]

    process = await asyncio.create_subprocess_exec(
        *metadata_add_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await process.communicate()

    if process.returncode != 0:
        error_msg = stderr.decode().strip()
        raise RuntimeError(f"MKV conversion failed: {error_msg}")


# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 MovieGalaxyX
# 𝐓𝐆 𝐈𝐃 : @MovieGalaxyX
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------
