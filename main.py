import telebot
import constants
import functions
import random
import os
import variables as var
import threading



bot = telebot.TeleBot(constants.token)
print("--------------------")
print("       START")
print("--------------------")


functions.everyday_update()




the_date = "02.09.2019" ####################################################

def keyboard(msg_id):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("para", "meme", "smart mode")
    user_markup.row("subjects", "doc")
    user_markup.row("schedule")
   # user_markup.row("refresh sch")
    bot.send_message(msg_id, "...", reply_markup=user_markup)

@bot.message_handler(commands=["start"])
def handle_text(message):
    bot.send_message(message.chat.id, var.discript)
    keyboard(message.chat.id)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    # message.text = message.text.strip().lower()
    # message.text = message.text.replace(" ", "")
    # message.text = message.text.strip().lower().replace(" ", "")

    if message.text == "stop smart mode":
        var.smartmode = False
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Smart mode session is finished", reply_markup=hide_markup)
        keyboard(message.chat.id)


    elif (var.smartmode):
        try:
            var.smartmode = True
            bot.send_chat_action(message.chat.id, "typing")
            triple = functions.smart_mode(message.text)
            output = str(triple[0])
            pics_list = triple[1]
            pics_title = triple[2]
            bot.send_message(message.chat.id, "Result: ")
            bot.send_message(message.chat.id, output)
        except Exception:
            bot.send_message(message.chat.id, "Invalid request or code's problems")
            var.inv_req = "Invalid request"
            pics_list = []
            pics_title = []
        i = -1
        for pic_url in pics_list:
            i+=1
            try:
                bot.send_chat_action(message.chat.id, "upload_photo")
                bot.send_message(message.chat.id, str(pics_title[i])+":")
                bot.send_photo(message.chat.id, str(pic_url))
            except Exception:
                bot.send_message(message.chat.id, "I cannot send this picture:\n {}".format(pic_url))



    elif message.text == "start" or message.text == "go":
        keyboard(message.chat.id)


    elif var.sendfile != -1 :
        hide_markup = telebot.types.ReplyKeyboardRemove()
        if  os.path.exists("materials/study/{}/{}".format(var.last_msg, message.text)):
            src = "materials/study/{}/{}".format(var.last_msg, message.text)
            docum = open(src, "rb")
            bot.send_chat_action(message.chat.id, "upload_document")
            bot.send_document(message.chat.id, docum, reply_markup=hide_markup)
        else:
            bot.send_message(message.chat.id, "Invalid request", reply_markup=hide_markup)

        var.sendfile = -1
        var.last_msg = ""
        keyboard(message.chat.id)


    elif message.text == "check":
        current_date = "02.09.2019"
        group = "БПАД181"
        # lessons = functions.sch(current_date, group)
        # for lesson in lessons:
        #   strout = functions.listToStr(lesson)
        #   if var.last_msg != strout:
        #     bot.send_message(message.chat.id, strout)
        #   var.last_msg = strout
        pass


    elif message.text == "subjects":
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Choose the subject", reply_markup=hide_markup)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        for subject in var.subjects:
            user_markup.row(str(subject))
        bot.send_message(message.chat.id, "...", reply_markup=user_markup)


    elif message.text == "test":
        pass
        # docum = open("02-Basics.pdf", "rb")
        # bot.send_document(message.chat.id, docum)


    elif message.text == "refresh sch":
        bot.send_chat_action(message.chat.id, "typing")
        current_date = "02.09.2019"

        group = "БПАД181"
        functions.refreshSch(current_date, group)

        bot.send_chat_action(message.chat.id, "typing")
        group = "БПАД182"
        #functions.refreshSch(current_date, group)

        bot.send_message(message.chat.id, "Done")



    elif message.text == "back":
        keyboard(message.chat.id)


    elif message.text == "meme refresh":
        bot.send_chat_action(message.chat.id, "upload_document")
        functions.refreshMemesLinks()
        bot.send_message(message.chat.id, "Done")


    elif message.text == "smart mode":
        var.smartmode = True
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("stop smart mode")
        bot.send_message(message.chat.id, "...", reply_markup=user_markup)


    elif message.text == "schedule":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("БПАД181", "БПАД182")
        user_markup.row("back")
        bot.send_message(message.chat.id, "...", reply_markup=user_markup)


    elif "БПАД" in message.text:
        bot.send_chat_action(message.chat.id, "typing")
        current_date = the_date
        group = message.text
        lessons = functions.sch(current_date, group)
        for lesson in lessons:
            strout = functions.listToStr(lesson)
            if var.last_msg != strout:
                lessonTime = lesson[2]
                if functions.isNearestLesson(lessonTime) and not var.flag:
                    var.flag = True
                    bot.send_message(message.chat.id,
                                     parse_mode="HTML",
                                     text="<strong>Actual lesson:</strong>")
                    bot.send_message(message.chat.id,
                                     parse_mode="HTML",
                                     text="<strong>{}</strong>".format(strout))
                    venue = lesson[6][0].lower()
                    map_gif = open("materials/working/map/{}.gif".format(venue), "rb")
                    #bot.send_chat_action(message.chat.id, "upload_photo")
                    bot.send_document(message.chat.id, map_gif)

                else:
                    bot.send_message(message.chat.id,
                    parse_mode= "HTML",
                    text="<code>{}</code>".format(strout))
            var.last_msg = strout
        var.flag = False


    elif message.text == "doc":
        docum = open("materials/working/documentation.txt")
        bot.send_chat_action(message.chat.id, "upload_document")
        bot.send_document(message.chat.id, docum)


    elif message.text in var.subjects:
        dir = "materials/study/{}".format(str(message.text))
        files_in_dir = os.listdir(dir)
        str_out = "Choose file: \n"
        cont = 0
        for file in files_in_dir:
            cont+=1
            str_out += "{}. {}\n".format(str(cont), str(file))

        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, str_out, reply_markup=hide_markup)

        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        for file in files_in_dir:
            user_markup.row(str(file))
        bot.send_message(message.chat.id, "...", reply_markup=user_markup)

        var.last_msg = message.text
        var.sendfile = 0



    elif message.text == "para":
        bot.send_message(message.chat.id, functions.paraNow())


    elif message.text == "meme":
        bot.send_chat_action(message.chat.id, "upload_photo")
        file = open("materials/working/memes.txt", "r")
        s = file.read()
        s = s.split()
        pic_url = s[(random.randint(0, len(s)-1))% len(s)]
        file.close()
        bot.send_photo(message.chat.id, str(pic_url))


    else:
        bot.send_message(message.chat.id, "Invalid request")
        var.inv_req = "Invalid request"


    functions.log(message.text, var.inv_req,
                  message.from_user.first_name,
                  message.from_user.last_name)
    var.inv_req = ""


bot.polling(none_stop=True, interval=0)


