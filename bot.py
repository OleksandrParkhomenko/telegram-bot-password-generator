from telebot import TeleBot, types
import messages
import config
from password_generator import PasswordGenerator


bot = TeleBot(config.config['token'])
defaultGenerator = PasswordGenerator()
generator = PasswordGenerator()


@bot.message_handler(commands=['start'])
def start(message):
    markup_inline = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text="Yes", callback_data="start_generating")
    button_no = types.InlineKeyboardButton(text="Later", callback_data="generate_later")
    markup_inline.add(button_yes, button_no)
    bot.send_message(message.chat.id, messages.welcome_message, reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: call.data == "restart")
def restart(call):
    start_generating(call)


@bot.callback_query_handler(lambda call: call.data == "generate_later")
def generate_later(call):
    markup_inline = types.InlineKeyboardMarkup()
    button_restart = types.InlineKeyboardButton(text="Start", callback_data="restart")
    markup_inline.add(button_restart)
    bot.send_message(call.message.chat.id, messages.waiting_message, reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: call.data == "start_generating")
def start_generating(call):
    markup_inline = types.InlineKeyboardMarkup()
    button_standard = types.InlineKeyboardButton(text="Standard", callback_data="generate_default")
    button_custom = types.InlineKeyboardButton(text="Custom", callback_data="customize_generator")
    markup_inline.add(button_standard, button_custom)
    bot.send_message(call.message.chat.id, messages.general_question, reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: call.data == "generate_default")
def generate_default(call):
    password = defaultGenerator.generate()
    markup_inline = types.InlineKeyboardMarkup()
    button_restart = types.InlineKeyboardButton(text="Generate new password", callback_data="restart")
    markup_inline.add(button_restart)
    bot.send_message(call.message.chat.id, messages.generated_password_message.format(password),
                     reply_markup=markup_inline, parse_mode="Markdown")


@bot.callback_query_handler(lambda call: call.data == "generate")
def generate(call):
    global generator
    password = generator.generate()
    markup_inline = types.InlineKeyboardMarkup()
    button_restart = types.InlineKeyboardButton(text="Generate new password", callback_data="restart")
    markup_inline.add(button_restart)
    bot.send_message(call.message.chat.id, messages.generated_password_message.format(password),
                     reply_markup=markup_inline, parse_mode="Markdown")


@bot.callback_query_handler(lambda call: call.data == "customize_generator")
def customize_generator(call):
    markup_inline = types.InlineKeyboardMarkup()
    numbers_text = "Numbers " + (messages.emoji_check_mark if generator.numbers else messages.emoji_x)
    uppercase_text = "Uppercase letters " + (messages.emoji_check_mark if generator.uppercase else messages.emoji_x)
    special_symbols_text = "Special characters " + (
        messages.emoji_check_mark if generator.special_symbols else messages.emoji_x)
    length_text = "Password length - " + str(generator.length)
    button_uppercase = types.InlineKeyboardButton(text=uppercase_text, callback_data="uppercase")
    button_numbers = types.InlineKeyboardButton(text=numbers_text, callback_data="numbers")
    button_special_symbols = types.InlineKeyboardButton(text=special_symbols_text, callback_data="special_symbols")
    button_length = types.InlineKeyboardButton(text=length_text, callback_data="length")
    button_generate = types.InlineKeyboardButton(text="Generate", callback_data="generate")
    markup_inline.row(button_numbers, button_special_symbols)
    markup_inline.row(button_uppercase)
    markup_inline.row(button_length)
    markup_inline.row(button_generate)
    bot.send_message(call.message.chat.id, messages.customize_question, reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: call.data == "uppercase")
def uppercase(call):
    markup_inline = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text="Yes", callback_data="uppercase_include")
    button_no = types.InlineKeyboardButton(text="No", callback_data="uppercase_exclude")
    markup_inline.add(button_yes, button_no)
    bot.send_message(call.message.chat.id, messages.uppercase_question,
                     reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: call.data == "uppercase_include")
def uppercase_include(call):
    generator.uppercase = True
    customize_generator(call)


@bot.callback_query_handler(lambda call: call.data == "uppercase_exclude")
def uppercase_exclude(call):
    generator.uppercase = False
    customize_generator(call)


@bot.callback_query_handler(lambda call: call.data == "numbers")
def numbers(call):
    markup_inline = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text="Yes", callback_data="numbers_include")
    button_no = types.InlineKeyboardButton(text="No", callback_data="numbers_exclude")
    markup_inline.add(button_yes, button_no)
    bot.send_message(call.message.chat.id, messages.numbers_question,
                     reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: call.data == "numbers_include")
def numbers_include(call):
    generator.numbers = True
    customize_generator(call)


@bot.callback_query_handler(lambda call: call.data == "numbers_exclude")
def numbers_exclude(call):
    generator.numbers = False
    customize_generator(call)


@bot.callback_query_handler(lambda call: call.data == "special_symbols")
def numbers(call):
    markup_inline = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text="Yes", callback_data="special_symbols_include")
    button_no = types.InlineKeyboardButton(text="No", callback_data="special_symbols_exclude")
    markup_inline.add(button_yes, button_no)
    bot.send_message(call.message.chat.id, messages.special_symbols_question,
                     reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: call.data == "special_symbols_include")
def special_symbols_include(call):
    generator.special_symbols = True
    customize_generator(call)


@bot.callback_query_handler(lambda call: call.data == "special_symbols_exclude")
def special_symbols_exclude(call):
    generator.special_symbols = False
    customize_generator(call)


@bot.callback_query_handler(lambda call: call.data == "length")
def length(call):
    bot.send_message(call.message.chat.id, messages.length_message)
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, password_length)


def password_length(message):
    try:
        new_length = int(message.text)
        markup_inline = types.InlineKeyboardMarkup()
        button_yes = types.InlineKeyboardButton(text="Yes",
                                                callback_data="password_length_approve?{}".format(new_length))
        button_no = types.InlineKeyboardButton(text="No", callback_data="customize_generator")
        markup_inline.add(button_yes, button_no)
        bot.send_message(message.chat.id, messages.length_approval_question.format(new_length),
                         reply_markup=markup_inline)
    except Exception as e:
        print("ERROR: " + str(e))
        bot.send_message(message.chat.id, messages.invalid_length_message)
        bot.register_next_step_handler_by_chat_id(message.chat.id, password_length)


@bot.callback_query_handler(lambda call: call.data[:23] == "password_length_approve")
def special_symbols_exclude(call):
    length = int(call.data[24:])
    if length < 6 or length > 50:
        bot.send_message(call.message.chat.id, messages.length_value_message)
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, password_length)
    else:
        generator.length = length
        customize_generator(call)


bot.polling(none_stop=True, interval=0)
