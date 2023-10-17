import time
from datetime import datetime, timedelta
import json
import shutil
import os

from aiogram import Bot, Dispatcher, types, executor

import config


bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


if not os.path.exists(f"files"):
    os.makedirs(f"files")
if not os.path.exists(f"files/ТО Запад"):
    os.makedirs(f"files/ТО Запад")
if not os.path.exists(f"files/ТО Север"):
    os.makedirs(f"files/ТО Север")


# Тестовая функция для проверки даты
@dp.message_handler(commands=['del'])
async def echo_mess(message: types.Message):
    # Получим ид пользователя и сравним со списком разрешенных в файле конфига
    user_id = message.from_user.id
    print(f"user_id {user_id}")
    t_o = ""
    if user_id in config.users:
        # Определим ТО по ид юзера в телеграм
        if user_id == 976374565:
            t_o = "ТО Запад"
        elif user_id == 652928171:
            t_o = "ТО Север"
        command = message.get_full_command()[1]  # [1].split('.')
        print(command)
        if len(command) == 10:
            await bot.send_message(message.chat.id, f"Хотим удалить папку /{t_o}/{command}")
            try:
                shutil.rmtree(f"files/{t_o}/{command}")
                print(f"/{t_o}/{command} удален")
                await bot.send_message(message.chat.id, f"Папка /{t_o}/{command} удалена")
            except OSError as error:
                print("Возникла ошибка.")
                await bot.send_message(message.chat.id, f"Папка /{t_o}/{command} не найдена!!!")
        else:
            await bot.send_message(message.chat.id, f"Дата не указана или указана не верно")

    else:
        await bot.send_message(message.chat.id, "Вы не авторизованны")
    # else:
    #     await bot.send_message(message.chat.id, f"Дата введена некорректно")
    #
    # await bot.send_message(message.chat.id, f"test")


@dp.message_handler()
async def echo_mess(message: types.Message):
    # Получим ид пользователя и сравним со списком разрешенных в файле конфига
    user_id = message.from_user.id
    print(f"user_id {user_id}")
    t_o = ""
    if user_id in config.users:
        # Определим ТО по ид юзера в телеграм
        if user_id == 976374565:
            t_o = "ТО Запад"
        elif user_id == 652928171:
            t_o = "ТО Север"

        # answer = []
        date_now = datetime.now()
        date_ago = date_now - timedelta(1)  # здесь мы выставляем минус день
        print(date_ago)
        date_now_year = date_ago.strftime("%d.%m.%Y")
        date_now_no_year = date_ago.strftime("%d.%m")

        if message.text == "1" or message.text == "отчет" or message.text == "отчёт":
            await bot.send_message(message.chat.id, f"Готовим отчет")
            if os.path.exists(f"files/{t_o}/{date_now_year}"):
                files = os.listdir(f"files/{t_o}/{date_now_year}")
                await bot.send_message(message.chat.id, f"Найдено {len(files)} файл(ов)")
                rep_a, num_rep = report(files, date_now_year, t_o)
                await bot.send_message(message.chat.id, f"Посчитано {num_rep[0]} файл(ов)")
                rep_masters = ""
                for i in range(1, len(num_rep)):
                    rep_masters += f'{num_rep[i]} \n'
                await bot.send_message(message.chat.id, rep_masters)
                print(files)
                at_int = rep_a["at_int"]
                at_int_pri = rep_a["at_int_pri"]
                at_serv = rep_a["at_serv"]

                ti_int = rep_a["ti_int"]
                ti_int_pri = rep_a["ti_int_pri"]
                ti_serv = rep_a["ti_serv"]

                et_int = rep_a["et_int"]
                et_int_pri = rep_a["et_int_pri"]
                et_tv = rep_a["et_tv"]
                et_tv_pri = rep_a["et_tv_pri"]
                et_dom = rep_a["et_dom"]
                et_dom_pri = rep_a["et_dom_pri"]
                et_serv = rep_a["et_serv"]
                et_serv_tv = rep_a["et_serv_tv"]

                answer = (f"{t_o} {date_now_no_year} \n\n"
                          f"ЭХ: интернет {at_int}({at_int_pri} прив), сервис {at_serv} \n"
                          f"Тиера: интернет {ti_int}({ti_int_pri} прив), сервис {ti_serv} \n"
                          f"ЕТ: интернет {et_int}({et_int_pri} прив), "
                          f"ТВ {et_tv}({et_tv_pri} прив), \n"
                          f"домофон {et_dom}({et_dom_pri} прив), "
                          f"сервис интернет {et_serv}, "
                          f"сервис ТВ {et_serv_tv} \n\n"
                          f"Итого: интернет {at_int + ti_int + et_int}({(at_int_pri + ti_int_pri + et_int_pri)}), "
                          f"ТВ {et_tv}({et_tv_pri}), "
                          f"домофон {et_dom}({et_dom_pri}), "
                          f"сервис {at_serv + ti_serv + et_serv}, "
                          f"сервис ТВ {et_serv_tv}")
                await bot.send_message(message.chat.id, answer)
            else:
                await bot.send_message(message.chat.id, f"Папка /{t_o}/{date_now_year} не найдена!!!")

        elif message.text[0].lower() == "у" or message.text[0].lower() == "y":  # Английская y
            search_date = message.text.split(" ")
            if len(search_date) > 1:
                await bot.send_message(message.chat.id, f"Хотим удалить папку /{t_o}/{search_date[1]}")
                try:
                    shutil.rmtree(f"files/{t_o}/{search_date[1]}")
                    print(f"/{t_o}/{search_date[1]} удален")
                    await bot.send_message(message.chat.id, f"Папка /{t_o}/{search_date[1]} удалена")
                except OSError as error:
                    print("Возникла ошибка.")
                    await bot.send_message(message.chat.id, f"Папка /{t_o}/{search_date[1]} не найдена!!!")
            else:
                await bot.send_message(message.chat.id, f"Дата не указана или указана не верно")

        else:
            # Создадим папку за текущий день если не существует
            if not os.path.exists(f"files/{t_o}/{date_now_year}"):
                os.makedirs(f"files/{t_o}/{date_now_year}")

            at_int = 0
            at_int_pri = 0
            at_serv = 0

            ti_int = 0
            ti_int_pri = 0
            ti_serv = 0

            et_int = 0
            et_int_pri = 0
            et_tv = 0
            et_tv_pri = 0
            et_dom = 0
            et_dom_pri = 0
            et_serv = 0
            et_serv_tv = 0

            # Разбиваем по ":", так мы определим провайдер
            txt = message.text.split(":")

            # Строчка ЭтХоум
            print(f"тут1 {txt[1]}")
            # Заменим скобки и перенос строки пробелами и разобьем на список
            new_txt_at = (txt[1].replace("(", " ").
                          replace(")", " ").
                          replace("\n", " ").
                          replace(",", " ").
                          replace(".", " "))
            new_txt_at_list = new_txt_at.split(" ")
            print(new_txt_at_list)

            # Сделаем перебор нового списка, где значения будем искать после ключевых слов
            for num, val in enumerate(new_txt_at_list):
                # print(f"111 {num, val}")
                if val.lower() == "интернет":
                    try:
                        at_int = int(new_txt_at_list[num + 1])  # Следующее значение после "интернет"
                    except ValueError:
                        at_int = 0
                elif val.lower() == "прив" or val.lower() == "привл":
                    try:
                        at_int_pri = int(new_txt_at_list[num - 1])  # Перед "прив"
                    except ValueError:
                        at_int_pri = 0
                elif val.lower() == "сервис":
                    try:
                        at_serv = int(new_txt_at_list[num + 1])  # После "сервис"
                    except ValueError:
                        at_serv = 0

            # Строчка Тиера
            new_txt_ti = (txt[2].replace("(", " ").
                          replace(")", " ").
                          replace("\n", " ").
                          replace(",", " ").
                          replace(".", " "))
            new_txt_ti_list = new_txt_ti.split(" ")
            print(new_txt_ti_list)

            # Сделаем перебор нового списка, где значения будем искать после ключевых слов
            for num, val in enumerate(new_txt_ti_list):
                # print(f"111 {num, val}")
                if val.lower() == "интернет":
                    try:
                        ti_int = int(new_txt_ti_list[num + 1])  # Следующее значение после "интернет"
                    except ValueError:
                        ti_int = 0
                elif val.lower() == "прив" or val.lower() == "привл":
                    try:
                        ti_int_pri = int(new_txt_ti_list[num - 1])  # Перед "прив"
                    except ValueError:
                        ti_int_pri = 0
                elif val.lower() == "сервис":
                    try:
                        ti_serv = int(new_txt_ti_list[num + 1])  # После "сервис"
                    except ValueError:
                        ti_serv = 0

            # Строчка Е-телеком
            new_txt_et = (txt[3].replace("(", " ").
                          replace(")", " ").
                          replace("\n", " ").
                          replace(",", " ").
                          replace(".", " "))
            new_txt_et_list = new_txt_et.split(" ")
            print(new_txt_et_list)

            # Сделаем перебор нового списка, где значения будем искать после ключевых слов
            # Сделаем несколько флагов, для разделения сервисов и привлеченных
            flag_priv_int = 0
            flag_priv_tv = 0
            flag_priv_dom = 0
            # flag_tv = 0
            # flag_serv_int = 0
            # flag_serv_tv = 0

            for num, val in enumerate(new_txt_et_list):
                print(f"111 {num, val}")
                if val.lower() == "интернет" and new_txt_et_list[num - 1].lower() != "сервис":
                    print(f"тут интернет {new_txt_et_list[num + 1]}")
                    try:
                        et_int = int(new_txt_et_list[num + 1])  # Следующее значение после "интернет"
                    except ValueError:
                        et_int = 0
                elif val.lower() == "прив" or val.lower() == "привл":
                    if flag_priv_int == 0:  # Флаг привлеченного интернета
                        print(f"тут прив интернет {new_txt_et_list[num - 1]}")
                        flag_priv_int += 1
                        try:
                            et_int_pri = int(new_txt_et_list[num - 1])  # Перед "прив"
                        except ValueError:
                            et_int_pri = 0
                    elif flag_priv_tv == 0:  # Флаг привлеченного тв
                        print(f"тут прив тв {new_txt_et_list[num - 1]}")
                        flag_priv_tv += 1
                        try:
                            et_tv_pri = int(new_txt_et_list[num - 1])  # Перед "прив"
                        except ValueError:
                            et_tv_pri = 0
                    elif flag_priv_dom == 0:  # Флаг привлеченного домофона
                        print(f"тут прив домофон {new_txt_et_list[num - 1]}")
                        flag_priv_dom += 1
                        try:
                            et_dom_pri = int(new_txt_et_list[num - 1])  # Перед "прив"
                        except ValueError:
                            et_dom_pri = 0
                # Сочетание тв
                elif val.lower() == "тв":
                    if new_txt_et_list[num - 1].lower() == "сервис":
                        print("тут сервис тв")
                        try:
                            et_serv_tv = int(new_txt_et_list[num + 1])  # После "тв"
                        except ValueError:
                            et_serv_tv = 0
                        except IndexError:  # После сервисов тв часто не ставят значение, а это конец сообщения
                            et_serv_tv = 0
                    else:
                        print("тут подключение тв")
                        print(new_txt_et_list[num + 1])
                        try:
                            et_tv = int(new_txt_et_list[num + 1])  # После "тв"
                        except ValueError:
                            et_tv = 0
                        except IndexError:  # После сервисов тв часто не ставят значение, а это конец сообщения
                            et_tv = 0
                elif val.lower() == "домофон":
                    try:
                        et_dom = int(new_txt_et_list[num + 1])  # После "тв"
                    except ValueError:
                        et_dom = 0
                elif val.lower() == "сервис" and new_txt_et_list[num + 1].lower() == "интернет":
                    try:
                        et_serv = int(new_txt_et_list[num + 2])  # + 2
                    except ValueError:
                        et_serv = 0

            to_save = {
                "at_int": at_int,
                "at_int_pri": at_int_pri,
                "at_serv": at_serv,

                "ti_int": ti_int,
                "ti_int_pri": ti_int_pri,
                "ti_serv": ti_serv,

                "et_int": et_int,
                "et_int_pri": et_int_pri,
                "et_tv": et_tv,
                "et_tv_pri": et_tv_pri,
                "et_dom": et_dom,
                "et_dom_pri": et_dom_pri,
                "et_serv": et_serv,
                "et_serv_tv": et_serv_tv,
                'master': "не указан"
            }

            print(message)

            if message.forward_from is not None:
                if message.forward_from.last_name:
                    to_save["master"] = message.forward_from.last_name
                elif message.forward_from.first_name:
                    to_save["master"] = message.forward_from.first_name
            elif message.forward_sender_name is not None:
                to_save["master"] = message.forward_sender_name
            else:
                to_save["master"] = "не указан"

            # Сохраним в файл
            with open(f'files/{t_o}/{date_now_year}/{date_now}.json', 'w') as outfile:
                json.dump(to_save, outfile)

            answe1 = (f"{t_o} {date_now_no_year}. Мастер {to_save['master']} \n\n"
                      f"ЭХ: интернет {at_int}({at_int_pri} прив), сервис {at_serv} \n" 
                      f"Тиера: интернет {ti_int}({ti_int_pri} прив), сервис {ti_serv} \n" 
                      f"ЕТ: интернет {et_int}({et_int_pri} прив), "
                      f"ТВ {et_tv}({et_tv_pri} прив), \n"
                      f"домофон {et_dom}({et_dom_pri} прив), "
                      f"сервис интернет {et_serv}, "
                      f"сервис ТВ {et_serv_tv} \n\n"
                      f"Итого: интернет {at_int + ti_int + et_int}({(at_int_pri + ti_int_pri + et_int_pri)}), "
                      f"ТВ {et_tv}({et_tv_pri}), "
                      f"домофон {et_dom}({et_dom_pri}), "
                      f"сервис {at_serv + ti_serv + et_serv}, "
                      f"сервис ТВ {et_serv_tv}")

            print(answe1)

            await bot.send_message(message.chat.id, f"{answe1}")

    else:
        await bot.send_message(message.chat.id, "Вы не авторизованны")


def report(files, date, t_o):
    to_save = {
        "at_int": 0,
        "at_int_pri": 0,
        "at_serv": 0,

        "ti_int": 0,
        "ti_int_pri": 0,
        "ti_serv": 0,

        "et_int": 0,
        "et_int_pri": 0,
        "et_tv": 0,
        "et_tv_pri": 0,
        "et_dom": 0,
        "et_dom_pri": 0,
        "et_serv": 0,
        "et_serv_tv": 0
    }
    # Возвращаем количество отчетов для сверки. Первый индекс количество, остальные фамилии мастеров
    rep = [0]
    # masters = []
    for file in files:
        with open(f'files/{t_o}/{date}/{file}', 'r') as outfile:
            data = json.load(outfile)
            print(data)
            to_save["at_int"] += data["at_int"]
            to_save["at_int_pri"] += data["at_int_pri"]
            to_save["at_serv"] += data["at_serv"]

            to_save["ti_int"] += data["ti_int"]
            to_save["ti_int_pri"] += data["ti_int_pri"]
            to_save["ti_serv"] += data["ti_serv"]

            to_save["et_int"] += data["et_int"]
            to_save["et_int_pri"] += data["et_int_pri"]
            to_save["et_tv"] += data["et_tv"]
            to_save["et_tv_pri"] += data["et_tv_pri"]
            to_save["et_dom"] += data["et_dom"]
            to_save["et_dom_pri"] += data["et_dom_pri"]
            to_save["et_serv"] += data["et_serv"]
            to_save["et_serv_tv"] += data["et_serv_tv"]
            rep[0] += 1  # Добавим счетчик количества посчитанных
            rep.append(data["master"])  # Добавим фамилию мастера

    # Сохраним в файл
    # Хотя необходимости нет
    with open(f'files/{t_o}/{date}.json', 'w') as outfile:
        json.dump(to_save, outfile)

    return to_save, rep


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
