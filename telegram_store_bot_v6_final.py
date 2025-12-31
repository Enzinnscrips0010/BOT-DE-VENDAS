import logging
import json
import os
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração de Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURAÇÕES ---
TOKEN = "8210914362:AAGVFLVlF3f6Dqqe9_IaLe8xK8SbRJh9zqM"
PIX_KEY = "admnzpix@gmail.com"
IMAGE_URL = "https://i.imgur.com/v8p7X6H.png"
DB_FILE = "users_db.json"
GIFT_FILE = "gifts_db.json"
ESTOQUE_FILE = "estoque_db.json"
ADMIN_IDS = [7971433228]
SUPORTE_USER = "@Nz_chef"

# --- BANCO DE DADOS ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f: return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, 'w') as f: json.dump(data, f, indent=4)

def get_user_data(user_id):
    db = load_json(DB_FILE)
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"balance": 0.0, "points": 0.0}
        save_json(DB_FILE, db)
    return db[uid]

# --- FUNÇÕES DO BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_user_data(user.id)
    welcome_text = (
        "<b>BEM VINDOS A 7STORE!!</b>\n"
        "A MELHOR STORE DE INFO CC DO TELEGRAM!!\n"
        "CHECKER DEBITANDO GARANTINDO SUA APROVAÇÃO!\n\n"
        "👑 | Entre agora no grupo de ref:\n"
        f"❤️ | Suporte: {SUPORTE_USER}\n"
        "💬 | Dono: @Nz_chef\n\n"
        "💰 <b>Carteira:</b>\n"
        f"┣ ID: <code>{user.id}</code>\n"
        f"┣ Saldo: R$ {user_data['balance']:.2f}\n"
        f"┗ Pontos: {user_data['points']:.2f} (~R${user_data['points']/2:.2f})\n\n"
        "<i>\"ENQUANTO TIVER VIVO VAI VOAR.\"</i>"
    )
    keyboard = [
        [InlineKeyboardButton("💳 Comprar CC", callback_query_data="menu_compra_full")],
        [InlineKeyboardButton("👤 Minha conta", callback_query_data="my_account"), InlineKeyboardButton("💰 Adicionar saldo", callback_query_data="add_balance_menu")],
        [InlineKeyboardButton("🔄 Trocas", callback_query_data="trades"), InlineKeyboardButton("👑 Dono", url="https://t.me/Nz_chef")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_photo(photo=IMAGE_URL, caption=welcome_text, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update.callback_query.message.edit_caption(caption=welcome_text, reply_markup=reply_markup, parse_mode="HTML")

async def menu_compra_full(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu de Compra Full com Regras e Filtros."""
    query = update.callback_query
    user = query.from_user
    user_data = get_user_data(user.id)
    await query.answer()
    
    text = (
        "💳 <b>Comprar Full (Com dados do titular)</b>\n\n"
        "⚠️ <i>Compre apenas se você estiver de acordo com as regras:</i>\n\n"
        "GARANTIMOS SOMENTE LIVE!\n"
        "NÃO GARANTIMOS A APROVAÇÃO\n\n"
        f"CONTATO PARA TROCAS: {SUPORTE_USER}\n"
        "COMO PEDIR TROCA:\n"
        "GRAVE UM VIDEO TENTANDO VINCULAR A INFO NO SITE TRAMONTINA\n"
        "LIMITE DE TEMPO PRA TROCAS: 10 MINUTOS\n\n"
        "<b>BONUS DE 100% EM DEPOSITOS ACIMA DE 50 R$</b>\n\n"
        "- <i>Escolha abaixo o produto que deseja comprar.</i>\n\n"
        "💰 <b>Carteira:</b>\n"
        f"┣ ID: <code>{user.id}</code>\n"
        f"┣ Saldo: R$ {user_data['balance']:.2f}\n"
        f"┗ Pontos: {user_data['points']:.2f} (~R${user_data['points']/2:.2f})"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Unitária", callback_query_data="buy_unitaria")],
        [
            InlineKeyboardButton("🏦 Pesquisar banco", callback_query_data="search_bank"),
            InlineKeyboardButton("🔐 Pesquisar bin", callback_query_data="search_bin")
        ],
        [
            InlineKeyboardButton("🏳️ Pesquisa bandeira", callback_query_data="search_brand"),
            InlineKeyboardButton("🔰 Pesquisar level", callback_query_data="search_level")
        ],
        [InlineKeyboardButton("🌎 Pesquisar país", callback_query_data="search_country")],
        [InlineKeyboardButton("⬅️ Voltar", callback_query_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_caption(caption=text, reply_markup=reply_markup, parse_mode="HTML")

async def add_balance_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "💰 <b>Adicionar saldo</b>\n- Escolha abaixo como você deseja adicionar o saldo."
    keyboard = [
        [InlineKeyboardButton("🔹 Pix Automático", callback_query_data="pix_auto"), InlineKeyboardButton("💰 Pix Manual", callback_query_data="pix_manual")],
        [InlineKeyboardButton("⬅️ Voltar", callback_query_data="start")]
    ]
    await query.message.edit_caption(caption=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def pix_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "<b>💰 PIX MANUAL</b>\n\n"
        "1. Faça o Pix para a chave abaixo:\n"
        f"<code>{PIX_KEY}</code>\n\n"
        "2. Envie o comprovante para o suporte:\n"
        f"👉 {SUPORTE_USER}\n\n"
        "<b>BÔNUS:</b> Depósitos acima de R$ 50,00 ganham 100% de bônus!"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Voltar", callback_query_data="add_balance_menu")]]
    await query.message.edit_caption(caption=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

if __name__ == '__main__':
    if TOKEN == "SEU_TOKEN_AQUI":
        print("ERRO: Configure o TOKEN!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CallbackQueryHandler(start, pattern="^start$"))
        application.add_handler(CallbackQueryHandler(menu_compra_full, pattern="^menu_compra_full$"))
        application.add_handler(CallbackQueryHandler(add_balance_menu, pattern="^add_balance_menu$"))
        application.add_handler(CallbackQueryHandler(pix_manual, pattern="^pix_manual$"))
        
        print("Bot Savitar Store v6 Final iniciado...")
        application.run_polling()
