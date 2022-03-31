from telebot import types


# Main menu
main_menu = types.InlineKeyboardMarkup(row_width=3)
main_menu.add(
    types.InlineKeyboardButton(text='🛍 Каталог', callback_data='catalog'),
    types.InlineKeyboardButton(text='👤 Профиль', callback_data='profile'),
    types.InlineKeyboardButton(text='ℹ️ Информация', callback_data='info'),
    types.InlineKeyboardButton(text='🛒 Мои покупки', callback_data='purchases'),
    types.InlineKeyboardButton(text='💸 Пополнить баланс', callback_data='replenishment'),
)
main_menu.add(
    types.InlineKeyboardButton(text='👥 Реферальная сеть', callback_data='referral_web'),
)

i_buy_cr = types.InlineKeyboardMarkup(row_width=1)
i_buy_cr.add(
    types.InlineKeyboardButton(text='Я приобрел', callback_data='crypto'),
    types.InlineKeyboardButton(text='Назад', callback_data='replenishment2'),
)
# f'Bitcoin|BTC\n'
#                                        f'Monero|XMR\n'
#                                        f'Binance coin|BNB\n'
#                                        f'Binance USD|BUSD\n'
#                                        f'USD Coin|USDC\n'
#                                        f'Tether|USDT\n'
#                                        f'Dash|DASH\n'
crypto = types.InlineKeyboardMarkup(row_width=1)
crypto.add(
    types.InlineKeyboardButton(text='Bitcoin|BTC', callback_data='BTC'),
    types.InlineKeyboardButton(text='Monero|XMR', callback_data='XMR'),
    types.InlineKeyboardButton(text='Binance coin|BNB', callback_data='BNB'),
    types.InlineKeyboardButton(text='USD Coin|USDC', callback_data='USDC'),
    types.InlineKeyboardButton(text='Tether|USDT', callback_data='USDT'),
    types.InlineKeyboardButton(text='Dash|DASH', callback_data='DASH'),
    types.InlineKeyboardButton(text='Назад', callback_data='replenishment2'),
)

replenishments = types.InlineKeyboardMarkup(row_width=1)
replenishments.add(
    types.InlineKeyboardButton(text='У меня есть криптовалюта', callback_data='crypto'),
    types.InlineKeyboardButton(text='У меня нет криптовалюты', callback_data='no_crypto'),
    types.InlineKeyboardButton(text='Назад', callback_data='main'),
)

no_crypto_back = types.InlineKeyboardMarkup(row_width=1)
no_crypto_back.add(
    types.InlineKeyboardButton(text='Я приобрел, выбрать кошелек', callback_data='crypto'),
    types.InlineKeyboardButton(text='Назад', callback_data='replenishment'),
)

btc = types.InlineKeyboardMarkup(row_width=1)
btc.add(
    types.InlineKeyboardButton(text='Я оплатил', callback_data='i_pay'),
    types.InlineKeyboardButton(text='Назад', callback_data='crypto'),
)


# Admin menu
admin_menu = types.InlineKeyboardMarkup(row_width=2)
admin_menu.add(types.InlineKeyboardButton(text='Управление каталогом', callback_data='catalog_control'))
admin_menu.add(types.InlineKeyboardButton(text='Управление товаром', callback_data='section_control'))
admin_menu.add(types.InlineKeyboardButton(text='Изменить баланс', callback_data='give_balance'))
admin_menu.add(types.InlineKeyboardButton(text='Рассылка', callback_data='admin_sending_messages'))
admin_menu.add(types.InlineKeyboardButton(text='Топ рефералов(доходы)', callback_data='admin_top_ref'))
admin_menu.add(
    types.InlineKeyboardButton(text='Информаци', callback_data='admin_info'),
    types.InlineKeyboardButton(text='Выйти', callback_data='exit_admin_menu')
)

# Admin control
admin_menu_control_catalog = types.InlineKeyboardMarkup(row_width=1)
admin_menu_control_catalog.add(
    types.InlineKeyboardButton(text='Добавить раздел в каталог', callback_data='add_section_to_catalog'),
    types.InlineKeyboardButton(text='Удалить раздел в каталог', callback_data='del_section_to_catalog'),
    types.InlineKeyboardButton(text='Назад', callback_data='back_to_admin_menu')
)

# Admin control section
admin_menu_control_section = types.InlineKeyboardMarkup(row_width=1)
admin_menu_control_section.add(
    types.InlineKeyboardButton(text='Добавить товар в раздел', callback_data='add_product_to_section'),
    types.InlineKeyboardButton(text='Удалить товар из раздела', callback_data='del_product_to_section'),
    types.InlineKeyboardButton(text='Загрузить товар', callback_data='download_product'),
    types.InlineKeyboardButton(text='Назад', callback_data='back_to_admin_menu')
)


# Back to admin menu
back_to_admin_menu = types.InlineKeyboardMarkup(row_width=1)
back_to_admin_menu.add(
    types.InlineKeyboardButton(text='Вернуться в админ меню', callback_data='back_to_admin_menu')
)

btn_purchase = types.InlineKeyboardMarkup(row_width=2)
btn_purchase.add(
    types.InlineKeyboardButton(text='Купить', callback_data='buy'),
    types.InlineKeyboardButton(text='Выйти', callback_data='exit_to_menu')
)

btn_ok = types.InlineKeyboardMarkup(row_width=3)
btn_ok.add(
    types.InlineKeyboardButton(text='Понял', callback_data='btn_ok')
)

replenish_balance = types.InlineKeyboardMarkup(row_width=3)
replenish_balance.add(
    types.InlineKeyboardButton(text='🔄 Проверить', callback_data='check_payment'),
    types.InlineKeyboardButton(text='❌ Отменить', callback_data='cancel_payment')
)

to_close = types.InlineKeyboardMarkup(row_width=3)
to_close.add(
    types.InlineKeyboardButton(text='❌', callback_data='to_close')
)




