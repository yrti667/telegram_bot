from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# بيانات المنتجات
products = [
    {
        "name": "ساعة بدون طباعة صور",
        "price": "7,000 دينار",
        "desc": "لون ذهبي وأسود، لون ذهبي وفضي وأسود. البكج يجي معاه سبحة كرستال 📿 ومحبس مطابق للون مالت الساعة"
    },
    {
        "name": "ساعة بدون طباعة صور (أسود فقط)",
        "price": "7,000 دينار",
        "desc": "لون أسود فقط"
    },
    {
        "name": "ساعة رقمية (شكل عسكري)",
        "price": "12,000 دينار",
        "desc": "لون أسود فقط"
    },
    {
        "name": "ساعة مع طباعة + سبحة + محبس + قلم",
        "price": "17,000 دينار",
        "desc": "لون ذهبي وأسود، لون ذهبي وفضي وأسود. البكج يجي معاه سبحة كرستال 📿، محبس، وقلم ذهبي أو فضي مطابق للساعة"
    }
]

# رقم الـ Chat ID مالك (بدّله بالرقم اللي طلعلك من get_id.py)
OWNER_CHAT_ID = 761234567

# عرض القائمة الرئيسية
async def show_menu(chat_id, context):
    keyboard = [
        [InlineKeyboardButton(p["name"], callback_data=str(i))] for i, p in enumerate(products)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="أهلاً بك! اختر منتجًا لعرض التفاصيل:", reply_markup=reply_markup)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_menu(update.message.chat_id, context)

# عرض تفاصيل المنتج
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = products[int(query.data)]
    text = f"📦 *{product['name']}*\n💵 السعر: {product['price']}\n📋 المواصفات: {product['desc']}"
    keyboard = [
        [InlineKeyboardButton("📩 طلب المنتج", callback_data=f"order_{query.data}")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel"), InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=query.message.chat_id, text=text, parse_mode="Markdown", reply_markup=reply_markup)

# إرسال الطلب
async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data.split("_")[1])
    product = products[index]
    user = query.from_user
    order_text = (
        f"🛒 طلب جديد!\n\n"
        f"👤 المستخدم: @{user.username if user.username else user.first_name}\n"
        f"📦 المنتج: {product['name']}\n"
        f"💵 السعر: {product['price']}\n"
        f"📋 المواصفات: {product['desc']}"
    )
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=order_text)
    await context.bot.send_message(chat_id=query.message.chat_id, text="✅ تم إرسال طلبك بنجاح! راح نتواصل وياك قريبًا.")

# زر الرجوع
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_menu(query.message.chat_id, context)

# زر الإلغاء
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(chat_id=query.message.chat_id, text="❌ تم إلغاء الطلب. تقدر ترجع وتختار منتج ثاني.")

# تشغيل البوت
print("✅ البوت اشتغل وينتظر أوامر...")
app = ApplicationBuilder().token("7613981022:AAFBhfs5tRKOIo9EepJmtewIGjrk_DUcx7I").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_order, pattern="^order_"))
app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"))
app.add_handler(CallbackQueryHandler(cancel, pattern="^cancel$"))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()