from skills.YandexOlympicsAlice.db_working import *
import datetime
from datetime import timedelta
import pymorphy2


def all_spends(userName, userMessage):
    if "недел" in userMessage:
        date = datetime.date.today() - timedelta(weeks=1)
        result = ["Ваши траты за последнюю неделю:"]
    elif "год" in userMessage:
        date = datetime.date.today() - timedelta(days=365)
        result = ["Ваши траты за последний год:"]
    else:
        date = datetime.date.today() - timedelta(days=30)
        result = ["Ваши траты за последний месяц:"]
    try:
        userId = [i.id for i in from_db("users", "Users", {"username": userName})][0]
        currencies = {}
        walletsId = [i.id for i in from_db("accounts", "Accounts", {"user_id": userId})]
        for i in from_db("waste", "Waste"):
            d = i.date.split(".")
            if datetime.date(year=int(d[2]), month=int(d[1]), day=int(d[0])) > date:
                walletId = i.account_id
                if walletId in walletsId:
                    if i.category != "пополнение":
                        currency = [i.currency for i in from_db("accounts", "Accounts", {"id": walletId})][0]
                        if currency in currencies:
                            currencies[currency] += int(i.count)
                        else:
                            currencies[currency] = int(i.count)
        for i in currencies:
            if i == "тенге":
                result.append(str(currencies[i]) + " " + i)
            else:
                cur = pymorphy2.MorphAnalyzer().parse(i)[0].make_agree_with_number(currencies[i]).inflect({'gent'}).word
                result.append(str(currencies[i]) + " " + cur)
        if len(result) == 1:
            return "За выбранный период вы не потратили ничего."
        return "\n".join(result)
    except IndexError:
        return "No such a User"


# print(all_spends("AQAAAAAjstOuAAfaP9kRfOsQJ00rlrOmg7BlREQ", ""))
