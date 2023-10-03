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


@dp.message_handler()
async def echo_mess(message: types.Message):
    # Получим ид пользователя и сравним со списком разрешенных в файле конфига
    user_id = message.from_user.id
    print(f"user_id {user_id}")
    if user_id in config.users:
        # answer = []
        date_now = datetime.now()
        date_ago = date_now - timedelta(1)  # здесь мы выставляем минус день
        print(date_ago)
        date_now_year = date_ago.strftime("%d.%m.%Y")
        date_now_no_year = date_ago.strftime("%d.%m")

        if message.text == "1" or message.text == "отчет" or message.text == "отчёт":
            await bot.send_message(message.chat.id, f"Готовим отчет")
            if os.path.exists(f"files/{date_now_year}"):
                files = os.listdir(f"files/{date_now_year}")
                await bot.send_message(message.chat.id, f"Найдено {len(files)} файл(ов)")
                rep_a, num_rep = report(files, date_now_year)
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

                answer = (f"ТО Запад {date_now_no_year} \n\n"
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
                await bot.send_message(message.chat.id, f"Папка {date_now_year} не найдена!!!")

        elif message.text[0] == "у":
            search_date = message.text.split(" ")
            if len(search_date) > 1:
                await bot.send_message(message.chat.id, f"Хотим удалить папку {search_date[1]}")
                try:
                    shutil.rmtree(f"files/{search_date[1]}")
                    print(f"/{search_date[1]} удален")
                    await bot.send_message(message.chat.id, f"Папка {search_date[1]} удалена")
                except OSError as error:
                    print("Возникла ошибка.")
                    await bot.send_message(message.chat.id, f"Папка {search_date[1]} не найдена!!!")
            else:
                await bot.send_message(message.chat.id, f"Дата не указана или указана не верно")

        else:
            # Создадим папку за текущий день если не существует
            if not os.path.exists(f"files/{date_now_year}"):
                os.makedirs(f"files/{date_now_year}")

            txt = message.text.split(":")
            # Строчка ЭтХоум
            new_txt_at = txt[1].replace("(", ")")
            new_txt_at = new_txt_at.split(")")

            at_int_i = filter(str.isdecimal, new_txt_at[0])
            at_int = ''.join(at_int_i)
            try:
                at_int = int(at_int)
            except ValueError:
                at_int = 0

            at_int_pri_i = filter(str.isdecimal, new_txt_at[1])
            at_int_pri = ''.join(at_int_pri_i)
            try:
                at_int_pri = int(at_int_pri)
            except ValueError:
                at_int_pri = 0

            at_serv_i = filter(str.isdecimal, new_txt_at[2])
            at_serv = ''.join(at_serv_i)
            try:
                at_serv = int(at_serv)
            except ValueError:
                at_serv = 0

            # Строчка Тиера
            new_txt_ti = txt[2].replace("(", ")")
            new_txt_ti = new_txt_ti.split(")")

            ti_int_i = filter(str.isdecimal, new_txt_ti[0])
            ti_int = ''.join(ti_int_i)
            try:
                ti_int = int(ti_int)
            except ValueError:
                ti_int = 0

            ti_int_pri_i = filter(str.isdecimal, new_txt_ti[1])
            ti_int_pri = ''.join(ti_int_pri_i)
            try:
                ti_int_pri = int(ti_int_pri)
            except ValueError:
                ti_int_pri = 0

            ti_serv_i = filter(str.isdecimal, new_txt_ti[2])
            ti_serv = ''.join(ti_serv_i)
            try:
                ti_serv = int(ti_serv)
            except ValueError:
                ti_serv = 0

            # Строчка Е-телеком
            new_txt_et = txt[3].replace("(", ")")
            new_txt_et = new_txt_et.split(")")

            et_int_i = filter(str.isdecimal, new_txt_et[0])
            et_int = ''.join(et_int_i)
            try:
                et_int = int(et_int)
            except ValueError:
                et_int = 0

            et_int_pri_i = filter(str.isdecimal, new_txt_et[1])
            et_int_pri = ''.join(et_int_pri_i)
            try:
                et_int_pri = int(et_int_pri)
            except ValueError:
                et_int_pri = 0

            et_tv_i = filter(str.isdecimal, new_txt_et[2])
            et_tv = ''.join(et_tv_i)
            try:
                et_tv = int(et_tv)
            except ValueError:
                et_tv = 0

            et_tv_pri_i = filter(str.isdecimal, new_txt_et[3])
            et_tv_pri = ''.join(et_tv_pri_i)
            try:
                et_tv_pri = int(et_tv_pri)
            except ValueError:
                et_tv_pri = 0

            et_dom_i = filter(str.isdecimal, new_txt_et[4])
            et_dom = ''.join(et_dom_i)
            try:
                et_dom = int(et_dom)
            except ValueError:
                et_dom = 0

            et_dom_pri_i = filter(str.isdecimal, new_txt_et[5])
            et_dom_pri = ''.join(et_dom_pri_i)
            try:
                et_dom_pri = int(et_dom_pri)
            except ValueError:
                et_dom_pri = 0

            et_serv = filter(str.isdecimal, new_txt_et[6])
            et_serv = ''.join(et_serv)
            try:
                et_serv = int(et_serv)
            except ValueError:
                et_serv = 0

            for_tv = txt[3].split("ТВ")
            for_tv = for_tv[-1].split("(")
            try:
                et_serv_tv = int(for_tv[0])
            except ValueError:
                et_serv_tv = 0

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
            with open(f'files/{date_now_year}/{date_now}.json', 'w') as outfile:
                json.dump(to_save, outfile)

            answe1 = (f"ТО Запад {date_now_no_year}. Мастер {to_save['master']} \n\n"
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


def report(files, date):
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
        with open(f'files/{date}/{file}', 'r') as outfile:
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
    with open(f'files/{date}.json', 'w') as outfile:
        json.dump(to_save, outfile)

    return to_save, rep


# def to_save_json(date, to_save):
#     with open(f'files/{date}.json', 'w') as outfile:
#         json.dump(to_save, outfile)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
