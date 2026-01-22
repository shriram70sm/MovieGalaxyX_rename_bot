# ----------------------------------------
# MADE BY MovieGalaxyX
# TG ID : @MovieGalaxyX
# ----------------------------------------

import motor.motor_asyncio
import logging
from config import Config
from datetime import timedelta, datetime, date, timezone
from helper.utils import send_log

# ----------------------------------------

class Seishiro:
    def __init__(self, uri, database_name):
        try:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            self._client.server_info()
            logging.info("Successfully connected to MongoDB")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise e

        self.database = self._client[database_name]

        self.col = self.database.users
        self.channel_data = self.database['channels']
        self.admins_data = self.database['admins']
        self.autho_user_data = self.database['autho_user']
        self.fsub_data = self.database['fsub']
        self.rqst_fsub_data = self.database['request_forcesub']
        self.rqst_fsub_Channel_data = self.database['request_forcesub_channel']
        self.counts = self.database['counts']
        self.verification_data = self.database['verification']
        self.verification_settings = self.database['verification_settings']
        self.premium_users = self.database['premium_users']
        self.banned_users = self.database['banned_users']

        self.timezone = timezone.utc

    # ---------------- USERS ----------------

    def new_user(self, id, username=None):
        return {
            "_id": int(id),
            "username": username.lower() if username else None,
            "join_date": date.today().isoformat(),
            "file_id": None,
            "caption": None,
            "format_template": None,
            "rename_count": 0,
            "metadata": True,
            "metadata_code": "Telegram : @MovieGalaxyX",
            "ban_status": {
                "is_banned": False,
                "ban_reason": "",
                "banned_on": None
            }
        }

    async def is_user_exist(self, user_id):
        return bool(await self.col.find_one({"_id": int(user_id)}))

    async def ensure_user_exists(self, user_id, username=None):
        if not await self.is_user_exist(user_id):
            await self.col.insert_one(self.new_user(user_id, username))

    async def add_user(self, bot, message):
        u = message.from_user
        if not await self.is_user_exist(u.id):
            await self.col.insert_one(self.new_user(u.id, u.username))
            await send_log(bot, u)

    async def get_user(self, user_id):
        return await self.col.find_one({"_id": int(user_id)})

    async def update_user(self, user_data):
        await self.col.update_one(
            {"_id": user_data["_id"]},
            {"$set": user_data},
            upsert=True
        )

    async def total_users_count(self):
        return await self.col.count_documents({})

    # ---------------- ADMINS ----------------

    async def admin_exist(self, admin_id):
        return bool(await self.admins_data.find_one({"_id": admin_id}))

    async def add_admin(self, admin_id):
        if not await self.admin_exist(admin_id):
            await self.admins_data.insert_one({"_id": admin_id})

    async def del_admin(self, admin_id):
        await self.admins_data.delete_one({"_id": admin_id})

    async def get_all_admins(self):
        docs = await self.admins_data.find().to_list(None)
        return [d["_id"] for d in docs]

    # ---------------- FORCE SUB ----------------

    async def add_channel(self, channel_id):
        await self.fsub_data.update_one(
            {"_id": channel_id},
            {"$set": {"_id": channel_id}},
            upsert=True
        )

    async def rem_channel(self, channel_id):
        await self.fsub_data.delete_one({"_id": channel_id})

    async def show_channels(self):
        docs = await self.fsub_data.find().to_list(None)
        return [d["_id"] for d in docs]

    # ---------------- PREMIUM ----------------

    async def add_premium(self, user_id, days=30):
        expiry = datetime.now(self.timezone) + timedelta(days=days)
        await self.col.update_one(
            {"_id": user_id},
            {"$set": {"expiry_time": expiry, "is_premium": True}},
            upsert=True
        )

    async def has_premium_access(self, user_id):
        user = await self.get_user(user_id)
        if not user:
            return False

        expiry = user.get("expiry_time")
        if not expiry:
            return False

        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=self.timezone)

        return datetime.now(self.timezone) <= expiry

    async def remove_premium_access(self, user_id):
        await self.col.update_one(
            {"_id": user_id},
            {"$set": {"expiry_time": None, "is_premium": False}}
        )

    # ---------------- MEDIA SETTINGS ----------------

    async def set_thumbnail(self, user_id, file_id):
        await self.col.update_one({"_id": user_id}, {"$set": {"file_id": file_id}})

    async def get_thumbnail(self, user_id):
        user = await self.get_user(user_id)
        return user.get("file_id") if user else None

    async def set_caption(self, user_id, caption):
        await self.col.update_one({"_id": user_id}, {"$set": {"caption": caption}})

    async def get_caption(self, user_id):
        user = await self.get_user(user_id)
        return user.get("caption") if user else None

    # ---------------- BAN SYSTEM ----------------

    async def ban_user(self, user_id, reason="Reason"):
        await self.banned_users.update_one(
            {"_id": user_id},
            {"$set": {
                "ban_status.is_banned": True,
                "ban_status.ban_reason": reason,
                "ban_status.banned_on": date.today().isoformat()
            }},
            upsert=True
        )

    async def unban_user(self, user_id):
        await self.banned_users.update_one(
            {"_id": user_id},
            {"$set": {
                "ban_status.is_banned": False,
                "ban_status.ban_reason": "",
                "ban_status.banned_on": None
            }}
        )

    async def is_banned(self, user_id):
        return await self.banned_users.find_one({"_id": user_id})


# ----------------------------------------
# DATABASE INSTANCE (IMPORTANT)
# ----------------------------------------

db = Seishiro(Config.DB_URL, Config.DB_NAME)

# Backward compatibility (OLD CODE SAFE)
MovieGalaxyX = db
rexbots = Seishiro()
