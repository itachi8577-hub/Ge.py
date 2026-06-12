import os
import sys
import json
import logging
import asyncio
import random
import time
import math
from datetime import datetime
from collections import defaultdict
from aiohttp import web

from telethon import TelegramClient, events, Button
from telethon.tl.types import MessageEntityMentionName, User
from telethon.errors import FloodWaitError, ChatWriteForbiddenError

# ==================== CONFIG ====================
API_ID = 31525307
API_HASH = '6448492ce1d5d36611612f1ab8864109'
BOT_TOKEN = '8722470348:AAHhuYflf4Tt8JVHv_RT78TEulKNGLEOzsY'
OWNER_ID = 8722144519  # ← YAHI CHANGE KARO BAS!
BOT_USERNAME = '@GETO_x_BOT'  # Change to your bot's actual username
PORT = int(os.environ.get("PORT", 8080))  # ← PORT YAHI ADD KIYA HAI

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ==================== DATA STORAGE ====================
DATA_FILE = 'bot_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

data = load_data()

def get_data(key, default=None):
    return data.get(key, default)

def set_data(key, value):
    data[key] = value
    save_data()

# Initialize data structures
if 'groups' not in data:
    data['groups'] = []
if 'sudo_users' not in data:
    data['sudo_users'] = []
if 'raid_lines' not in data:
    data['raid_lines'] = [
        "TERI MA KI CHUT ME MERA LUND KA JALWA MADARCHOD KE BACHE TERI BEHAN KO CHOD KE WOI PATAK DUNGA SAALE RANDI KE AULAD JITNA ROYEGA UTNA PELUNGA TERI MA KA BHOSA FAAD DUNGA BSDK TERI PURI KHAANDAN KO EK SATH LINE ME KHADA KARKE CHODUNGA!!! 😈",
        "MADARCHOD TERA BAAP HU ME TERI MA KI CHUT ME HATHI KA LUND DAAL DUNGA TERI BEHAN KI CHUT ME DIWALI KE PATAKHE PHODUNGA BSDK TU KYA RAID KAREGA TERI MA KI CHUT ME MERA PURA SHEHAR KA LUND JAYEGA RANDI KE BACHE!!! 🔥",
        "TERI MA KI CHUT ME 500 KILO KA LOHA DAAL DUNGA TERI BEHAN KE CHUT ME MERA LUND AISE JAYEGA JAISE METRO JAATI HAI MADARCHOD KE BACHE TERI MA KI CHADAR PHAD KE USE KAFAN BANA DUNGA BSDK TERI MA KI CHUT ME MERA POORA HAATH!!! 💀",
        "BSDK TERI MA KI CHUT ME JALTA HUA KOYLA DAAL DUNGA TERI BEHAN KO BAZAAR ME BECH DUNGA RANDI KE BACHE TERE KHANDAN KI LADKIYON KO APNE LUND PE NACHAYUNGA MADARCHOD TERI MA KI KASAM TERE KO AISE CHODUNGA KI PANI MANGTE PHIREGA!!! 😡",
        "TERI MA KI CHUT ME TITANIC DOOBA DUNGA BSDK TERI BEHAN KI CHUT ME MERA LUND KA NACH DEKH TERA BAAP HU ME TERI MA KI CHUT ME MERA GARAM PESHAB DALUNGA RANDI KE BACHE TERI BEHAN KO CHOD KE USKA LAL QILA BANA DUNGA!!! 🚩" "TERI MA KI CHUT ME MERA LUND KA JALWA MADARCHOD KE BACHE TERI BEHAN KO CHOD KE WOI PATAK DUNGA SAALE RANDI KE AULAD JITNA ROYEGA UTNA PELUNGA TERI MA KA BHOSA FAAD DUNGA BSDK TERI PURI KHAANDAN KO EK SATH LINE ME KHADA KARKE CHODUNGA!!! 😈",
        "MADARCHOD TERA BAAP HU ME TERI MA KI CHUT ME HATHI KA LUND DAAL DUNGA TERI BEHAN KI CHUT ME DIWALI KE PATAKHE PHODUNGA BSDK TU KYA RAID KAREGA TERI MA KI CHUT ME MERA PURA SHEHAR KA LUND JAYEGA RANDI KE BACHE!!! 🔥",
        "TERI MA KI CHUT ME 500 KILO KA LOHA DAAL DUNGA TERI BEHAN KE CHUT ME MERA LUND AISE JAYEGA JAISE METRO JAATI HAI MADARCHOD KE BACHE TERI MA KI CHADAR PHAD KE USE KAFAN BANA DUNGA BSDK TERI MA KI CHUT ME MERA POORA HAATH!!! 💀",
        "BSDK TERI MA KI CHUT ME JALTA HUA KOYLA DAAL DUNGA TERI BEHAN KO BAZAAR ME BECH DUNGA RANDI KE BACHE TERE KHANDAN KI LADKIYON KO APNE LUND PE NACHAYUNGA MADARCHOD TERI MA KI KASAM TERE KO AISE CHODUNGA KI PANI MANGTE PHIREGA!!! 😡",
        "TERI MA KI CHUT ME TITANIC DOOBA DUNGA BSDK TERI BEHAN KI CHUT ME MERA LUND KA NACH DEKH TERA BAAP HU ME TERI MA KI CHUT ME MERA GARAM PESHAB DALUNGA RANDI KE BACHE TERI BEHAN KO CHOD KE USKA LAL QILA BANA DUNGA!!! 🚩""MADARCHOD SALE KITNA ROYEGA?", "TERI MA KI CHUT 🥵", "BHOSDIWALE", "LAUDE LAG GAYE?", "RANDI KE BACHCHE",  "TERI MAKI CHUT MADARCHODO HIZDA HAI HAI TUM MADARCHODO BOL DE YUTA TERA BAAP HAI WARNA TERI KI CHUT KOI RAMDI KI AULAD NHI BACHA PAYEGA AAJ SAMJH LE MADRCHOD",
    "AIR JORDEN KE JUTE SE TERI KI CHUT PR MAAR MAAR KE LAAL KR DUNGA KALI SE LAAL 😋🥵 RANDI MADARCHODO",
    "MADARCHODO BAAP SE LADEGA APNE TERI MA KI CHUT KHA JAUNGA RAMDI",
    "TERI MAA KI CHHUT KA KHAA JAUNGAA MADARCHODO RANDI KI AULAD SPAM KARTA HAI MADARCOD KE CHAKKE KI AULAD TERE BAAP KO GADHE KE LAND SEE CHODUNGA",
    "TERI MAKI CHUT MADARCHOD SUR KE LAND SE MA CHODUNGA GANDI CHUT KI KALI AULAD FATI KALI CHUT KI AULD CHAMR TERI MAIYA KI CHUT KO CHOR BAZR ME BECHUNGA MADRACHOD",
    "TERI MAIYA KE KI CHUT ME APNE LAND KA PYTHON BOT BANA KR RUN KRUNGA TERI SASTI SPAM USER BOT KA BHOSDA MADARCHODO",
    "TERI MAIYA KA BHOSDA MADARCHODO SASTI GB RAOD KI RANDI KI AULAD",
    "FATI KALI CHUT KI AULD CHAMR TERI MAIYA KI CHUT KO CHOR BAZR ME BECHUNGA MADRACHOD",
    "TERI MAKICHUT KO KUTTO KO KHILA DUNGA RANDI KI SASTSTI AULAD MADARCHODO",
    "TERI MUMMY KI CHUT BSDK 🖕",
    "SUN BHSDIKE, TU APNI MA KI CHUT ME PANI BHAR KE AA RHA HAI KYA? TERI MAKI CHUT KA ANGUTHI KE BARABAR BHI KOI VALUE NAHI HAI, MADARCHOD KAHIN KA. TERI BEHEN KI CHUT KA CHAKKAR MEIN TERA BAAP BHI KUCH NAHI KAR PAYEGA. TERI GAAND ME 4 GOLIYAN MAR KE TUMHE BHAGWA CHOLA PEHNA DUNGA.",
    "MADARCHOD! TERI MAIYA NE TO MUJHE BATAYA KI TU ABHI TAK BACHON WALI NIKKAR PEHENTA HAI. TERI BEHEN TO MERI RANDI HAI AUR TERI MAA MERI RAKHAIL.",
    "BAHEN KE LODE! TUJHE LAGTA HAI TU BOHOT BADA AAYA HAI? TERI MAIYA TO MERI CHODI HUI MALKIN HAI.",
    "TERI MAIYA KI CHUT ME MERA LUND ITNA ZOR SE GHOOSTA HAI JAISE STADIUM KE FLOOD LIGHTS CHAL RAHI HO.",
    "RANDI KI AULAD! TERI MAIYA TO MERI AAFAT HAI AUR TU MERA FAN. TERI MAA KI CHUT ME TO BOHOT ZYADA TRAFFIC HAI.",
    "CHUTIYA TU MAA CHUDANE AAYA HAI? TERI MAIYA TO MERI RANDI LIST ME HIGHEST RATED HAI.",
    "TERI MAA KI CHUT ME MERA LUND BSDK 🍆💦",
    "TERI GAAND PHAT GAYI KYA BHAG KYA RHA HAI 🏃💨",
    "TERI MAA NE MUJHE BOLYA KO GHAS MAT KHILA 💀",
    "TERI MAA KI CHUT KA KERA HAI TU 🤡",
    "TERI BEHEN KO DEKH KE MERA LUND KHARA HO GYA 😏",
    "TU APNI MAA KA DUDH PEENA BAND KAR DE 🍼",
    "TERI BEHEN KI CHUT ME 5 BIHARI EK SAATH 🥵",
    "TERI SHAKAL DEKH KE MERA LUND MURJHA GYA 🥀",
    "TERI BEHEN TO MERI EX HAI AB TERI MAA MERI CURRENT HAI 😎",
    "TERA BAAP BHI RANDI KI AULAD HAI SALE 🚮",
    "TERI MAA KI CHUT ME PARKING LOT 🅿️",
    "TERI BEHEN KI CHUT ME WIFI CHALTA HAI 📶",
    "TERI BEHEN TO MERI FAVORITE RANDI HAI 💋",
    "TERI MAA KI CHUT ME CLOUD STORAGE ☁️",
    "TERI BEHEN KI CHUT ME BLUETOOTH CONNECT 📱",
    "TERI MAA KI CHUT KA SUBSCRIBER HU MAI 🔔",
    "TERI MAA KO CHOD KE THAK GYA HU 💦",
    "TERI BEHEN KA ONLYFANS TOP DONATION MAI HU 👑",
    "TERI BEHEN KO CHODTA HU TO AWAZ AATI HAI OYE HAYE 🎵",
    "TERI BEHEN KI CHUT KA RENT 500 HAI 💵",
    "TERI BEHEN KO DEKH KE MERA LUND BOLTA HAI AAJA 🗣️",
    "TERI BEHEN KA VIRGINITY MAINE LI THI 🏆",
    "TERI BEHEN KE MUH ME MERA LUND 💯",
    "TERI BEHEN KO RANDI BANA KE CHODTA HU 🎯",
    "TERI BEHEN TO MERI SUGARMAMMY HAI 🍭",
    "TERI BEHEN KE MUH KA SWAD CHANG HAI 👅",
    "TERI BEHEN KO RANDI BANANE KA MASTER HU MAI 🧠",
    "TERI BEHEN KI CHUT KA TOLL FREE NUMBER 📞",
    "TERI BEHEN KI CHUT KA PIN 7860 📌",
    "TERI BEHEN KI CHUT KA RATE LIST 💲",
    "TERI BEHEN KI CHUT KA CATALOG 📚",
    "TERI BEHEN KI CHUT KA LOCATION 📍",
    "TERI BEHEN KI CHUT KA COLOR BLACK 🖤",
    "TERI BEHEN KI CHUT KA STOCK AVAILABLE 📦",
    "TERI BEHEN KI CHUT KA OFFER ZONE 🏷️",
    "TERI BEHEN KI CHUT KI QUALITY AAA ✅",
    "TERI BEHEN KI CHUT KA TRACK RECORD 🏅",
    "Teri maa ki chut teri behen ka bhosda 🖕",
    "Madarchod teri aukaat nahi hai bhaag yahan se 🤬",
    "Bhadwe teri maa ki chut itna attitude kahan se laata hai 🖕",
    "Itni shakal buri ki aaina bhi tod de 🔥",
    "Teri photo dekh ke darwaza chod de itna ugly hai tu 🤣",
    "Main aag hoon jo jalati hai aur raakh mein bhi chamakti hai 🔥",
    "Meri aukaat nahi meri shaan hai 👑",
    "Teri shaadi kab hai? Maa ne kaha ghar par rakh legi 😂",
    "Tu itna smart hai ki duniya ko laga tera baap ka paisa hai 🤣","TERI MAKI CHUT MADARCHODO HIZDA HAI HAI TUM MADARCHODO BOL DE YUTA TERA BAAP HAI WARNA TERI KI CHUT KOI RAMDI KI AULAD NHI BACHA PAYEGA AAJ SAMJH LE MADRCHOD",
    "AIR JORDEN KE JUTE SE TERI KI CHUT PR MAAR MAAR KE LAAL KR DUNGA KALI SE LAAL 😋🥵 RANDI MADARCHODO",
    "MADARCHODO BAAP SE LADEGA APNE TERI MA KI CHUT KHA JAUNGA RAMDI",
    "TERI MAA KI CHHUT KA KHAA JAUNGAA MADARCHODO RANDI KI AULAD SPAM KARTA HAI MADARCOD KE CHAKKE KI AULAD TERE BAAP KO GADHE KE LAND SEE CHODUNGA",
    "TERI MAKI CHUT MADARCHOD SUR KE LAND SE MA CHODUNGA GANDI CHUT KI KALI AULAD FATI KALI CHUT KI AULD CHAMR TERI MAIYA KI CHUT KO CHOR BAZR ME BECHUNGA MADRACHOD",
    "TERI MAIYA KE KI CHUT ME APNE LAND KA PYTHON BOT BANA KR RUN KRUNGA TERI SASTI SPAM USER BOT KA BHOSDA MADARCHODO",
    "TERI MAIYA KA BHOSDA MADARCHODO SASTI GB RAOD KI RANDI KI AULAD",
    "FATI KALI CHUT KI AULD CHAMR TERI MAIYA KI CHUT KO CHOR BAZR ME BECHUNGA MADRACHOD",
    "TERI MAKICHUT KO KUTTO KO KHILA DUNGA RANDI KI SASTSTI AULAD MADARCHODO",
    "TERI MUMMY KI CHUT BSDK 🖕",
    "SUN BHSDIKE, TU APNI MA KI CHUT ME PANI BHAR KE AA RHA HAI KYA? TERI MAKI CHUT KA ANGUTHI KE BARABAR BHI KOI VALUE NAHI HAI, MADARCHOD KAHIN KA. TERI BEHEN KI CHUT KA CHAKKAR MEIN TERA BAAP BHI KUCH NAHI KAR PAYEGA. TERI GAAND ME 4 GOLIYAN MAR KE TUMHE BHAGWA CHOLA PEHNA DUNGA.",
    "MADARCHOD! TERI MAIYA NE TO MUJHE BATAYA KI TU ABHI TAK BACHON WALI NIKKAR PEHENTA HAI. TERI BEHEN TO MERI RANDI HAI AUR TERI MAA MERI RAKHAIL.",
    "BAHEN KE LODE! TUJHE LAGTA HAI TU BOHOT BADA AAYA HAI? TERI MAIYA TO MERI CHODI HUI MALKIN HAI.",
    "TERI MAIYA KI CHUT ME MERA LUND ITNA ZOR SE GHOOSTA HAI JAISE STADIUM KE FLOOD LIGHTS CHAL RAHI HO.",
    "RANDI KI AULAD! TERI MAIYA TO MERI AAFAT HAI AUR TU MERA FAN. TERI MAA KI CHUT ME TO BOHOT ZYADA TRAFFIC HAI.",
    "CHUTIYA TU MAA CHUDANE AAYA HAI? TERI MAIYA TO MERI RANDI LIST ME HIGHEST RATED HAI.",
    "TERI MAA KI CHUT ME MERA LUND BSDK 🍆💦",
    "TERI GAAND PHAT GAYI KYA BHAG KYA RHA HAI 🏃💨",
    "TERI MAA NE MUJHE BOLYA KO GHAS MAT KHILA 💀",
    "TERI MAA KI CHUT KA KERA HAI TU 🤡",
    "TERI BEHEN KO DEKH KE MERA LUND KHARA HO GYA 😏",
    "TU APNI MAA KA DUDH PEENA BAND KAR DE 🍼",
    "TERI BEHEN KI CHUT ME 5 BIHARI EK SAATH 🥵",
    "TERI SHAKAL DEKH KE MERA LUND MURJHA GYA 🥀",
    "TERI BEHEN TO MERI EX HAI AB TERI MAA MERI CURRENT HAI 😎",
    "TERA BAAP BHI RANDI KI AULAD HAI SALE 🚮",
    "TERI MAA KI CHUT ME PARKING LOT 🅿️",
    "TERI BEHEN KI CHUT ME WIFI CHALTA HAI 📶",
    "TERI BEHEN TO MERI FAVORITE RANDI HAI 💋",
    "TERI MAA KI CHUT ME CLOUD STORAGE ☁️",
    "TERI BEHEN KI CHUT ME BLUETOOTH CONNECT 📱",
    "TERI MAA KI CHUT KA SUBSCRIBER HU MAI 🔔",
    "TERI MAA KO CHOD KE THAK GYA HU 💦",
    "TERI BEHEN KA ONLYFANS TOP DONATION MAI HU 👑",
    "TERI BEHEN KO CHODTA HU TO AWAZ AATI HAI OYE HAYE 🎵",
    "TERI BEHEN KI CHUT KA RENT 500 HAI 💵",
    "TERI BEHEN KO DEKH KE MERA LUND BOLTA HAI AAJA 🗣️",
    "TERI BEHEN KA VIRGINITY MAINE LI THI 🏆",
    "TERI BEHEN KE MUH ME MERA LUND 💯",
    "TERI BEHEN KO RANDI BANA KE CHODTA HU 🎯",
    "TERI BEHEN TO MERI SUGARMAMMY HAI 🍭",
    "TERI BEHEN KE MUH KA SWAD CHANG HAI 👅",
    "TERI BEHEN KO RANDI BANANE KA MASTER HU MAI 🧠",
    "TERI BEHEN KI CHUT KA TOLL FREE NUMBER 📞",
    "TERI BEHEN KI CHUT KA PIN 7860 📌",
    "TERI BEHEN KI CHUT KA RATE LIST 💲",
    "TERI BEHEN KI CHUT KA CATALOG 📚",
    "TERI BEHEN KI CHUT KA LOCATION 📍",
    "TERI BEHEN KI CHUT KA COLOR BLACK 🖤",
    "TERI BEHEN KI CHUT KA STOCK AVAILABLE 📦",
    "TERI BEHEN KI CHUT KA OFFER ZONE 🏷️",
    "TERI BEHEN KI CHUT KI QUALITY AAA ✅",
    "TERI BEHEN KI CHUT KA TRACK RECORD 🏅",
    "Teri maa ki chut teri behen ka bhosda 🖕",
    "Madarchod teri aukaat nahi hai bhaag yahan se 🤬",
    "Bhadwe teri maa ki chut itna attitude kahan se laata hai 🖕",
    "Itni shakal buri ki aaina bhi tod de 🔥",
    "Teri photo dekh ke darwaza chod de itna ugly hai tu 🤣",
    "Main aag hoon jo jalati hai aur raakh mein bhi chamakti hai 🔥",
    "Meri aukaat nahi meri shaan hai 👑",
    "Teri shaadi kab hai? Maa ne kaha ghar par rakh legi 😂",
    "Tu itna smart hai ki duniya ko laga tera baap ka paisa hai 🤣","TERI MAKI CHUT MADARCHODO BOL DE YUTA TERA BAAP HAI VARNA TERI KI CHUT KOI RAMDI KI AULAD NHI BACHA PAYEGA AAJ SAMJH LE MADRCHOD MADARCHOD BAAP SE LADEGA APNE TERI MA KI CHUT KHA JAUNGA","RANDI TERI MA KI CHUT KO NICKE AIR JORDAN SE MAR MAR KE KALI SE LAL KAR DUNGA TERI MA KI CHUT KO GADHE KE LAND SE FADUNGA RAMDI MADARCHOD RANDI ITACHI PAPA BOL KE THODI AUKAT BANA LE HIZDE","MUJHSE NHI CHUDWAYA JA RHA TO ITACHI PAPA KE BOT SE CHUDWA LE MADRACHOD"," TERI MA KO ULTA TANG DUNGA PHIR USKI CHUT MARUNGA","ABE RANDI MADARCHOD TERI MA MERI SETTING HAI PAPA BOL ITACHI PAPA","RANDI KE BACCHE TERA KHANDAN HI RANDIYO KA H","TERI MUMMI KO DEEPTHROAT DEDUGA MADARCHOD K BACHE","TERA PAPA BHI RANDI KI AULAD H BSDK","TERI MUMMI KO YOGA SIKHADUGA AUR USKO DIFFERENT","STYLES ME CHODUGA TERA PAPA HU MAI TERI MUMMY KA BF","TERI BEHEN KI CHUT ME SSD BOOT KAR DUNGA","TERI BEHEN KA LUND OLX PE BECH DUNGA","TERI BEHEN KI GAAND ME QR CODE CHIPKA DUNGA TERI BEHEN KA BHOSDA NFT ME MINT KAR DUNGA","TERI BEHEN MERI PROPERTY","TERI MA OR BAHEN DONO MERI FAVOURITE RANDIYA HAI",
    ]
if 'shayari' not in data:
    data['shayari'] = {}
if 'sticker_ids' not in data:
    data['sticker_ids'] = []
save_data()

# ==================== RAID STATE ====================
raid_active = defaultdict(bool)
raid_target = {}
bot_alive = True
broadcast_groups = []
bot_start_time = time.time()

# For speed optimization - concurrent semaphore
raid_semaphore = asyncio.Semaphore(5)

# ==================== HELPERS ====================
def is_owner(user_id):
    return user_id == OWNER_ID

def is_sudo(user_id):
    return user_id == OWNER_ID or user_id in data.get('sudo_users', [])

def is_authorized(user_id):
    return is_sudo(user_id)

def get_prefix(text):
    for p in ['.', '/', '!']:
        if text.startswith(p):
            return p
    return None

def extract_args(text, prefix):
    parts = text[len(prefix):].strip().split(maxsplit=1)
    cmd = parts[0].lower() if parts else ''
    args = parts[1] if len(parts) > 1 else ''
    return cmd, args

def get_display_name(user):
    if hasattr(user, 'first_name') and user.first_name:
        return user.first_name
    if hasattr(user, 'title') and user.title:
        return user.title
    return "User"

# ==================== REAL MENTION SYSTEM ====================
async def real_mention(event, user_id, text=None):
    """Send a real mention using tg://user?id= that works without username"""
    try:
        entity = await bot.get_entity(user_id)
        if text:
            await event.reply(text, parse_mode='html')
        else:
            mention_text = f"<a href='tg://user?id={user_id}'>{get_display_name(entity)}</a>"
            await event.reply(mention_text, parse_mode='html')
        return True
    except Exception as e:
        try:
            if text:
                await event.reply(text)
            else:
                await event.reply(f"<a href='tg://user?id={user_id}'>User</a>", parse_mode='html')
            return True
        except:
            return False

# ==================== GROUP TRACKING ====================
@bot.on(events.ChatAction)
async def track_groups(event):
    """Auto-track groups when bot is added"""
    if event.user_added or event.user_join:
        me = await bot.get_me()
        if event.user_added and event.users:
            if me.id in event.users:
                chat_id = event.chat_id
                groups = data.get('groups', [])
                if chat_id not in groups:
                    groups.append(chat_id)
                    data['groups'] = groups
                    save_data()

# ==================== COMMANDS ====================

# --- START & MENU ---
@bot.on(events.NewMessage(pattern='^/start$'))
async def start_cmd(event):
    text = (
        f"👋 **Welcome to Raid Bot!**\n\n"
        f"Your ID: `{event.sender_id}`\n"
        f"Owner ID: `{OWNER_ID}`\n\n"
        f"Use /menu to see all commands."
    )
    await event.reply(text, parse_mode='markdown')

@bot.on(events.NewMessage(pattern='^[.!/]menu$'))
@bot.on(events.NewMessage(pattern='^/menu$'))
async def menu_cmd(event):
    # Track group when menu is used in a group
    chat_id = event.chat_id
    if chat_id < 0:  # It's a group
        groups = data.get('groups', [])
        if chat_id not in groups:
            groups.append(chat_id)
            data['groups'] = groups
            save_data()
    
    buttons = [
        [Button.inline("👤 MY OWNER", b"my_owner")],
        [Button.inline("📋 COMMAND LIST", b"cmd_list")],
        [Button.inline("➕ ADD GROUP", b"add_group")],
        [Button.inline("💬 CHAT BOX", b"chat_box")]
    ]
    await event.reply("**🤖 MAIN MENU**\n\nSelect an option:", buttons=buttons, parse_mode='markdown')

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data_cb = event.data.decode()
    
    if data_cb == "my_owner":
        await event.edit(f"👤 **OWNER:** [{OWNER_ID}](tg://user?id={OWNER_ID})", parse_mode='markdown')
    
    elif data_cb == "cmd_list":
        text = (
            "**📋 COMMAND LIST**\n\n"
            "**🟢 Bot Control:**\n"
            "`.alive` - Check bot status\n"
            "`.off` - Turn bot offline\n\n"
            "**⚔️ Raid:**\n"
            "`.r @user` - Start raid on user\n"
            "`.rrr @user` - Ultra fast raid (5x speed)\n"
            "`.s` - Stop raid\n"
            "`.addline <text>` - Add raid line\n"
            "`.lines` - Show all raid lines\n\n"
            "**🔇 Mute:**\n"
            "`.mute @user [reason]` - Mute user\n"
            "`.unmute @user` - Unmute user\n\n"
            "**🎭 Shayari & Sticker:**\n"
            "`.shayari <type> <line>` - Add shayari\n"
            "`.shayari <type> @user [count]` - Send shayari\n"
            "`.addsticker` - Reply to sticker to add\n"
            "`.sticker @user [count]` - Send stickers\n\n"
            "**📢 Broadcast:**\n"
            "`.broadcast <msg>` - Text broadcast\n"
            "`.tagbroadcast <msg>` - Tag all broadcast\n"
            "`.chatbox <msg>` - Send to chat box\n\n"
            "**👑 Sudo:**\n"
            "`.sudo @user` - Add sudo\n"
            "`.remsudo @user` - Remove sudo\n"
            "`.sudolist` - List sudo users\n\n"
            "**🛠 Other:**\n"
            "`.id` - Get ID\n"
            "`.info @user` - User info\n"
            "`.hack @user` - Hack animation\n"
            "`.spam @user <count>` - Spam user\n"
            "`.quote` - Random quote\n"
            "`.calc <expr>` - Calculate\n"
            "`.joke` - Random joke\n"
            "`.truth` - Truth question\n"
            "`.dare` - Dare challenge\n"
            "`.gc` - Group count\n"
            "`.restart` - Restart bot\n"
            "`.botstats` - Bot statistics\n"
            "`.forward @user <count>` - Forward message\n"
            "`.ping` - Check response time"
        )
        await event.edit(text, parse_mode='markdown')
    
    elif data_cb == "add_group":
        await event.edit("➕ **Add me to any group!**\n\nUse /menu in the target group to register it.")
    
    elif data_cb == "chat_box":
        await event.edit("💬 **Chat Box Active!**\n\nSend message with .chatbox <msg>")

# --- ALIVE / OFF / PING ---
@bot.on(events.NewMessage(pattern=r'^[.!/]alive$'))
async def alive_cmd(event):
    if not is_authorized(event.sender_id):
        return
    global bot_alive
    bot_alive = True
    uptime_sec = int(time.time() - bot_start_time)
    uptime_str = f"{uptime_sec//3600}h {(uptime_sec%3600)//60}m {uptime_sec%60}s"
    await event.reply(f"✅ **Bot is ALIVE!**\n⏱ Uptime: {uptime_str}\n👥 Groups: {len(data.get('groups', []))}", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]off$'))
async def off_cmd(event):
    if not is_authorized(event.sender_id):
        return
    global bot_alive, raid_active
    bot_alive = False
    raid_active.clear()
    await event.reply("🔴 **Bot is now OFFLINE.** All raids stopped.", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]ping$'))
async def ping_cmd(event):
    if not is_authorized(event.sender_id):
        return
    start = time.time()
    msg = await event.reply("Pong! 🏓")
    end = time.time()
    await msg.edit(f"**PONG!** 🏓\n⏱ Response: `{round((end-start)*1000)}ms`", parse_mode='markdown')

# --- RAID SYSTEM ---
async def raid_worker(event, target_id, target_name):
    """Worker for sending raid messages"""
    global raid_active
    lines = data.get('raid_lines', ["MADARCHOD"])
    
    while raid_active.get(event.chat_id, False) and raid_active.get('target') == target_id:
        try:
            async with raid_semaphore:
                line = random.choice(lines)
                mention = f"<a href='tg://user?id={target_id}'>{target_name}</a>\n\n{line}"
                await bot.send_message(event.chat_id, mention, parse_mode='html')
                await asyncio.sleep(0.05)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
        except ChatWriteForbiddenError:
            raid_active[event.chat_id] = False
            break
        except Exception:
            await asyncio.sleep(0.1)

@bot.on(events.NewMessage(pattern=r'^[.!/]r\s+@?'))
async def raid_cmd(event):
    global raid_active
    if not bot_alive:
        return
    if not is_authorized(event.sender_id):
        return
    
    try:
        target_username = event.message.text.split()[1].lstrip('@')
        if event.message.entities:
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            else:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
        
        target_name = get_display_name(entity)
    except:
        await event.reply("❌ User not found!")
        return
    
    raid_active[event.chat_id] = True
    raid_active['target'] = target_id
    
    await event.reply(f"⚔️ **Raid started on** {target_name}!\nUse .s to stop.", parse_mode='markdown')
    
    # Run 3 concurrent workers for speed
    workers = [raid_worker(event, target_id, target_name) for _ in range(3)]
    await asyncio.gather(*workers)

@bot.on(events.NewMessage(pattern=r'^[.!/]rrr\s+@?'))
async def ultra_raid_cmd(event):
    """Ultra fast raid - runs 5 concurrent workers"""
    global raid_active
    if not bot_alive:
        return
    if not is_authorized(event.sender_id):
        return
    
    try:
        target_username = event.message.text.split()[1].lstrip('@')
        if event.message.entities:
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            else:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
        
        target_name = get_display_name(entity)
    except:
        await event.reply("❌ User not found!")
        return
    
    raid_active[event.chat_id] = True
    raid_active['target'] = target_id
    
    await event.reply(f"⚔️🔥 **ULTRA RAID started on** {target_name}!\nUse .s to stop.", parse_mode='markdown')
    
    # 5 concurrent workers for max speed
    workers = [raid_worker(event, target_id, target_name) for _ in range(5)]
    await asyncio.gather(*workers)

@bot.on(events.NewMessage(pattern=r'^[.!/]s$'))
async def stop_raid_cmd(event):
    global raid_active
    if not is_authorized(event.sender_id):
        return
    raid_active[event.chat_id] = False
    raid_active['target'] = None
    await event.reply("🛑 **Raid stopped!**", parse_mode='markdown')

# --- RAID LINES ---
@bot.on(events.NewMessage(pattern=r'^[.!/]addline\s+'))
async def addline_cmd(event):
    if not is_authorized(event.sender_id):
        return
    prefix = get_prefix(event.message.text)
    _, args = extract_args(event.message.text, prefix)
    if not args:
        await event.reply("❌ Usage: .addline <text>")
        return
    
    lines = data.get('raid_lines', [])
    lines.append(args)
    data['raid_lines'] = lines
    save_data()
    await event.reply(f"✅ **Line added!**\nTotal lines: {len(lines)}", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]lines$'))
async def lines_cmd(event):
    if not is_authorized(event.sender_id):
        return
    lines = data.get('raid_lines', [])
    text = "**📝 RAID LINES:**\n\n"
    for i, line in enumerate(lines, 1):
        text += f"{i}. {line}\n"
    text += f"\n**Total:** {len(lines)}"
    await event.reply(text, parse_mode='markdown')

# --- MUTE SYSTEM ---
muted_users = {}

@bot.on(events.NewMessage(pattern=r'^[.!/]mute\s+@?'))
async def mute_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    parts = event.message.text.split()
    target_username = parts[1].lstrip('@')
    reason = ' '.join(parts[2:]) if len(parts) > 2 else 'No reason'
    
    try:
        if event.message.entities:
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            else:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
        target_name = get_display_name(entity)
    except:
        await event.reply("❌ User not found!")
        return
    
    chat_id = event.chat_id
    if chat_id not in muted_users:
        muted_users[chat_id] = {}
    
    muted_users[chat_id][target_id] = reason
    await event.reply(f"🔇 **Muted** {target_name}\nReason: {reason}")

@bot.on(events.NewMessage(pattern=r'^[.!/]unmute\s+@?'))
async def unmute_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    parts = event.message.text.split()
    target_username = parts[1].lstrip('@')
    
    try:
        if event.message.entities:
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            else:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
    except:
        await event.reply("❌ User not found!")
        return
    
    chat_id = event.chat_id
    if chat_id in muted_users and target_id in muted_users[chat_id]:
        del muted_users[chat_id][target_id]
        await event.reply(f"🔊 **Unmuted** User")
    else:
        await event.reply("❌ User is not muted!")

# --- SHAYARI SYSTEM ---
@bot.on(events.NewMessage(pattern=r'^[.!/]shayari\s+'))
async def shayari_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    prefix = get_prefix(event.message.text)
    parts = event.message.text[len(prefix):].strip().split(maxsplit=2)
    
    if len(parts) < 2:
        await event.reply("❌ Usage: .shayari <type> <line>  OR  .shayari <type> @user [count]")
        return
    
    shayari_type = parts[1]
    
    # Check if targeting a user
    if len(parts) > 2 and '@' in parts[2]:
        target_parts = parts[2].split()
        target_username = target_parts[0].lstrip('@')
        count = int(target_parts[1]) if len(target_parts) > 1 and target_parts[1].isdigit() else 5
        
        try:
            if event.message.entities:
                target_id = None
                for ent in event.message.entities:
                    if isinstance(ent, MessageEntityMentionName):
                        target_id = ent.user_id
                        break
                if not target_id:
                    entity = await bot.get_entity(target_username)
                    target_id = entity.id
            else:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
            target_name = get_display_name(entity)
        except:
            await event.reply("❌ User not found!")
            return
        
        all_shayari = data.get('shayari', {})
        type_lines = all_shayari.get(shayari_type, [])
        
        if not type_lines:
            await event.reply(f"❌ No shayari found for type '{shayari_type}'")
            return
        
        for i in range(min(count, 20)):
            line = random.choice(type_lines)
            mention = f"<a href='tg://user?id={target_id}'>{target_name}</a>\n\n{line}"
            await bot.send_message(event.chat_id, mention, parse_mode='html')
            await asyncio.sleep(0.3)
    else:
        # Adding shayari
        line = parts[2] if len(parts) > 2 else ''
        if not line:
            await event.reply("❌ Usage: .shayari <type> <line>")
            return
        
        all_shayari = data.get('shayari', {})
        if shayari_type not in all_shayari:
            all_shayari[shayari_type] = []
        all_shayari[shayari_type].append(line)
        data['shayari'] = all_shayari
        save_data()
        await event.reply(f"✅ **Shayari added!**\nType: {shayari_type}\nTotal: {len(all_shayari[shayari_type])}", parse_mode='markdown')

# --- STICKER SYSTEM ---
@bot.on(events.NewMessage(pattern=r'^[.!/]addsticker$'))
async def addsticker_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    if event.message.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if reply_msg.sticker:
            sticker_id = reply_msg.sticker.id
            sticker_ids = data.get('sticker_ids', [])
            if sticker_id not in sticker_ids:
                sticker_ids.append(sticker_id)
                data['sticker_ids'] = sticker_ids
                save_data()
                await event.reply(f"✅ **Sticker added!** Total: {len(sticker_ids)}")
            else:
                await event.reply("⚠️ Sticker already exists!")
        else:
            await event.reply("❌ Reply to a **sticker**!")
    else:
        await event.reply("❌ Reply to a sticker with .addsticker")

@bot.on(events.NewMessage(pattern=r'^[.!/]sticker\s+@?'))
async def sticker_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    parts = event.message.text.split()
    target_username = parts[1].lstrip('@')
    count = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 5
    
    try:
        if event.message.entities:
            target_id = None
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            if not target_id:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
    except:
        await event.reply("❌ User not found!")
        return
    
    sticker_ids = data.get('sticker_ids', [])
    if not sticker_ids:
        await event.reply("❌ No stickers added! Use .addsticker first.")
        return
    
    for i in range(min(count, 10)):
        try:
            sticker_id = random.choice(sticker_ids)
            mention = f"<a href='tg://user?id={target_id}'>User</a>"
            await bot.send_message(event.chat_id, mention, parse_mode='html')
            await bot.send_file(event.chat_id, sticker_id)
            await asyncio.sleep(0.5)
        except:
            pass

# --- BROADCAST ---
@bot.on(events.NewMessage(pattern=r'^[.!/]broadcast\s+'))
async def broadcast_cmd(event):
    if not is_owner(event.sender_id):
        return
    
    prefix = get_prefix(event.message.text)
    _, msg = extract_args(event.message.text, prefix)
    
    if not msg:
        await event.reply("❌ Usage: .broadcast <message>")
        return
    
    groups = data.get('groups', [])
    sent = 0
    failed = 0
    
    status_msg = await event.reply(f"📢 **Broadcasting to {len(groups)} groups...**")
    
    for chat_id in groups:
        try:
            await bot.send_message(chat_id, f"📢 **BROADCAST**\n\n{msg}", parse_mode='markdown')
            sent += 1
            await asyncio.sleep(0.5)
        except:
            failed += 1
    
    await status_msg.edit(f"✅ **Broadcast complete!**\n✅ Sent: {sent}\n❌ Failed: {failed}", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]tagbroadcast\s+'))
async def tagbroadcast_cmd(event):
    if not is_owner(event.sender_id):
        return
    
    prefix = get_prefix(event.message.text)
    _, msg = extract_args(event.message.text, prefix)
    
    if not msg:
        await event.reply("❌ Usage: .tagbroadcast <message>")
        return
    
    groups = data.get('groups', [])
    sent = 0
    
    status_msg = await event.reply(f"📢 **Tag Broadcast to {len(groups)} groups...**")
    
    for chat_id in groups:
        try:
            await bot.send_message(chat_id, f"📢 **🔔 @all NOTICE**\n\n{msg}", parse_mode='markdown')
            sent += 1
            await asyncio.sleep(0.5)
        except:
            pass
    
    await status_msg.edit(f"✅ **Tag Broadcast complete!**\n✅ Sent: {sent}", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]chatbox\s+'))
async def chatbox_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    prefix = get_prefix(event.message.text)
    _, msg = extract_args(event.message.text, prefix)
    
    if not msg:
        await event.reply("❌ Usage: .chatbox <message>")
        return
    
    try:
        await bot.send_message(OWNER_ID, f"💬 **Chat Box Message**\nFrom: {event.sender_id}\n\n{msg}", parse_mode='markdown')
        await event.reply("✅ **Message sent to owner!**")
    except:
        await event.reply("❌ Failed to send message!")

# --- SUDO SYSTEM ---
@bot.on(events.NewMessage(pattern=r'^[.!/]sudo\s+@?'))
async def sudo_cmd(event):
    if not is_owner(event.sender_id):
        return
    
    parts = event.message.text.split()
    target_username = parts[1].lstrip('@')
    
    try:
        if event.message.entities:
            target_id = None
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            if not target_id:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
    except:
        await event.reply("❌ User not found!")
        return
    
    sudo_users = data.get('sudo_users', [])
    if target_id not in sudo_users:
        sudo_users.append(target_id)
        data['sudo_users'] = sudo_users
        save_data()
        await event.reply(f"✅ **Sudo added!**", parse_mode='markdown')
    else:
        await event.reply("⚠️ User is already sudo!", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]remsudo\s+@?'))
async def remsudo_cmd(event):
    if not is_owner(event.sender_id):
        return
    
    parts = event.message.text.split()
    target_username = parts[1].lstrip('@')
    
    try:
        if event.message.entities:
            target_id = None
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            if not target_id:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
    except:
        await event.reply("❌ User not found!")
        return
    
    sudo_users = data.get('sudo_users', [])
    if target_id in sudo_users:
        sudo_users.remove(target_id)
        data['sudo_users'] = sudo_users
        save_data()
        await event.reply(f"✅ **Sudo removed!**", parse_mode='markdown')
    else:
        await event.reply("❌ User is not sudo!", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]sudolist$'))
async def sudolist_cmd(event):
    if not is_owner(event.sender_id):
        return
    
    sudo_users = data.get('sudo_users', [])
    text = "**👑 SUDO USERS:**\n\n"
    text += f"👤 Owner: [{OWNER_ID}](tg://user?id={OWNER_ID})\n"
    for i, uid in enumerate(sudo_users, 1):
        text += f"{i}. [{uid}](tg://user?id={uid})\n"
    text += f"\n**Total:** {len(sudo_users) + 1}"
    await event.reply(text, parse_mode='markdown')

# --- ID & INFO ---
@bot.on(events.NewMessage(pattern=r'^[.!/]id$'))
async def id_cmd(event):
    text = f"**👤 Your ID:** `{event.sender_id}`\n"
    if event.chat_id < 0:
        text += f"**💬 Group ID:** `{event.chat_id}`"
    await event.reply(text, parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]info\s+@?'))
async def info_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    target_username = event.message.text.split()[1].lstrip('@')
    
    try:
        if event.message.entities:
            target_id = None
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            if not target_id:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
        
        user = entity
        text = (
            f"**📋 USER INFO**\n\n"
            f"**ID:** `{user.id}`\n"
            f"**Name:** {get_display_name(user)}\n"
            f"**Username:** @{user.username if user.username else 'N/A'}\n"
            f"**Bot:** {'Yes' if user.bot else 'No'}\n"
            f"**Profile:** [Link](tg://user?id={user.id})"
        )
        await event.reply(text, parse_mode='markdown')
    except:
        await event.reply("❌ User not found!")

# --- HACK ANIMATION ---
@bot.on(events.NewMessage(pattern=r'^[.!/]hack\s+@?'))
async def hack_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    target_username = event.message.text.split()[1].lstrip('@')
    
    try:
        if event.message.entities:
            target_id = None
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            if not target_id:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
        target_name = get_display_name(entity)
    except:
        await event.reply("❌ User not found!")
        return
    
    hack_lines = [
        f"🔴 **HACKING {target_name}...**",
        f"🟡 [1/5] Fetching IP address... `192.168.1.{random.randint(1,255)}`",
        f"🟡 [2/5] Breaching firewall... ████████░░ 80%",
        f"🟡 [3/5] Extracting personal data... 📂",
        f"🟢 [4/5] Downloading complete! ✅",
        f"💀 **{target_name} has been HACKED!**\n\n📱 Device: {random.choice(['iPhone 15', 'Samsung S24'])}\n📍 Location: {random.choice(['Delhi, India', 'Mumbai, India'])}"
    ]
    
    msg = await event.reply("Initializing hack... 💻")
    for line in hack_lines:
        await asyncio.sleep(1.2)
        await msg.edit(line, parse_mode='markdown')

# --- SPAM ---
@bot.on(events.NewMessage(pattern=r'^[.!/]spam\s+@?\w+\s+\d+'))
async def spam_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    parts = event.message.text.split()
    target_username = parts[1].lstrip('@')
    count = int(parts[2])
    
    try:
        if event.message.entities:
            target_id = None
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            if not target_id:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
    except:
        await event.reply("❌ User not found!")
        return
    
    for i in range(min(count, 50)):
        await bot.send_message(event.chat_id, f"<a href='tg://user?id={target_id}'>User</a> SPAM #{i+1}", parse_mode='html')
        await asyncio.sleep(0.3)

# --- QUOTE ---
@bot.on(events.NewMessage(pattern=r'^[.!/]quote$'))
async def quote_cmd(event):
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "In the middle of difficulty lies opportunity. - Albert Einstein",
        "Success is not final, failure is not fatal. - Winston Churchill",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Be the change you wish to see in the world. - Mahatma Gandhi"
    ]
    await event.reply(f"💭 **Quote:**\n\n{random.choice(quotes)}", parse_mode='markdown')

# --- CALC ---
@bot.on(events.NewMessage(pattern=r'^[.!/]calc\s+'))
async def calc_cmd(event):
    prefix = get_prefix(event.message.text)
    _, expr = extract_args(event.message.text, prefix)
    
    if not expr:
        await event.reply("❌ Usage: .calc <expression>")
        return
    
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith('__')}
        allowed_names.update({'abs': abs, 'round': round, 'min': min, 'max': max})
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        await event.reply(f"🧮 **{expr} =** `{result}`", parse_mode='markdown')
    except Exception as e:
        await event.reply(f"❌ Error: {e}")

# --- JOKE ---
@bot.on(events.NewMessage(pattern=r'^[.!/]joke$'))
async def joke_cmd(event):
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "What do you call a snake that builds websites? A python developer! 🐍",
        "Why did the developer go broke? Because he used up all his cache! 💰",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡"
    ]
    await event.reply(f"😂 **Joke:**\n\n{random.choice(jokes)}", parse_mode='markdown')

# --- TRUTH / DARE ---
@bot.on(events.NewMessage(pattern=r'^[.!/]truth$'))
async def truth_cmd(event):
    truths = [
        "What's the most embarrassing thing you've ever done?",
        "Have you ever cheated on a test?",
        "What's the biggest lie you've ever told?",
        "Who is your secret crush?",
        "What's the worst thing you've done when angry?"
    ]
    await event.reply(f"🤫 **Truth:**\n\n{random.choice(truths)}", parse_mode='markdown')

@bot.on(events.NewMessage(pattern=r'^[.!/]dare$'))
async def dare_cmd(event):
    dares = [
        "Send a random sticker to the last person you texted!",
        "Do 20 pushups right now!",
        "Sing a song in the chat!",
        "Send your last photo to the group!",
        "Talk in rhymes for the next 5 minutes!"
    ]
    await event.reply(f"🎯 **Dare:**\n\n{random.choice(dares)}", parse_mode='markdown')

# --- GC (GROUP COUNT) ---
@bot.on(events.NewMessage(pattern=r'^[.!/]gc$'))
async def gc_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    groups = data.get('groups', [])
    text = f"**👥 GROUPS:**\n\n**Total:** {len(groups)}\n\n"
    for i, gid in enumerate(groups, 1):
        try:
            entity = await bot.get_entity(gid)
            name = entity.title if hasattr(entity, 'title') else str(gid)
            text += f"{i}. {name}\n"
        except:
            text += f"{i}. `{gid}`\n"
    
    await event.reply(text, parse_mode='markdown')

# --- RESTART ---
@bot.on(events.NewMessage(pattern=r'^[.!/]restart$'))
async def restart_cmd(event):
    if not is_owner(event.sender_id):
        return
    
    await event.reply("🔄 **Restarting bot...**")
    save_data()
    os._exit(0)

# --- BOT STATS ---
@bot.on(events.NewMessage(pattern=r'^[.!/]botstats$'))
async def botstats_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    uptime_sec = int(time.time() - bot_start_time)
    uptime_str = f"{uptime_sec//3600}h {(uptime_sec%3600)//60}m {uptime_sec%60}s"
    
    groups = data.get('groups', [])
    sudo_users = data.get('sudo_users', [])
    raid_lines = data.get('raid_lines', [])
    stickers = data.get('sticker_ids', [])
    shayari_count = sum(len(v) for v in data.get('shayari', {}).values())
    
    text = (
        f"**📊 BOT STATISTICS**\n\n"
        f"⏱ **Uptime:** {uptime_str}\n"
        f"👥 **Groups:** {len(groups)}\n"
        f"👑 **Sudo Users:** {len(sudo_users)}\n"
        f"📝 **Raid Lines:** {len(raid_lines)}\n"
        f"🎭 **Shayari Lines:** {shayari_count}\n"
        f"🎨 **Stickers:** {len(stickers)}\n"
        f"✅ **Status:** {'🟢 Alive' if bot_alive else '🔴 Offline'}"
    )
    await event.reply(text, parse_mode='markdown')

# --- FORWARD ---
@bot.on(events.NewMessage(pattern=r'^[.!/]forward\s+@?'))
async def forward_cmd(event):
    if not is_authorized(event.sender_id):
        return
    
    parts = event.message.text.split()
    if len(parts) < 3:
        await event.reply("❌ Usage: .forward @user <count>")
        return
    
    target_username = parts[1].lstrip('@')
    count = int(parts[2])
    
    try:
        if event.message.entities:
            target_id = None
            for ent in event.message.entities:
                if isinstance(ent, MessageEntityMentionName):
                    target_id = ent.user_id
                    break
            if not target_id:
                entity = await bot.get_entity(target_username)
                target_id = entity.id
        else:
            entity = await bot.get_entity(target_username)
            target_id = entity.id
    except:
        await event.reply("❌ User not found!")
        return
    
    if not event.message.reply_to_msg_id:
        await event.reply("❌ Reply to a message to forward!")
        return
    
    reply_msg = await event.get_reply_message()
    
    for i in range(min(count, 10)):
        try:
            await reply_msg.forward_to(event.chat_id)
            await asyncio.sleep(0.5)
        except:
            pass

# ==================== WEBSERVER FOR RENDER ====================
WEBAPP = web.Application()

async def health_check(request):
    return web.Response(text="✅ Bot is running!", content_type='text/html')

async def web_server():
    WEBAPP.router.add_get('/', health_check)
    WEBAPP.router.add_get('/health', health_check)
    runner = web.AppRunner(WEBAPP)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)  # ← PORT YAHI USE KAR RAHA HAI
    await site.start()
    print(f"🌐 Web server started on port {PORT}")
    
    # Keep the server running
    await asyncio.Event().wait()

# ==================== MAIN ====================
async def main():
    print("🤖 Starting bot...")
    print(f"👤 Owner ID: {OWNER_ID}")
    print(f"👥 Groups tracked: {len(data.get('groups', []))}")
    
    me = await bot.get_me()
    print(f"✅ Bot started as @{me.username}")
    
    # Run both bot and web server concurrently
    await asyncio.gather(
        bot.run_until_disconnected(),
        web_server()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("❌ Bot stopped!")
        save_data()
