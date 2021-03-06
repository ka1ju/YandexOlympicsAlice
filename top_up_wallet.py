from skills.YandexOlympicsAlice.db_working import *
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()


def top_up_wallet(st, user_name, k):
    if k == {}:
        b = st.split(' и ')
        user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
        user_id = user_id1[0]
        bd = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
        q1 = []
        currency = ['рубль', 'рубля', 'рублей', 'евро', 'доллар', 'доллара', 'долларов', 'фунт', 'фунта', 'фунтов',
                    'йена', 'йены', 'йен', 'франк', 'франка', 'франков', 'тенге']
        cur = []
        for j in range(len(b)):
            y = 0
            for i in bd:
                if i in ''.join(b[j]):
                    y = 1
                    q1.append(i)
            if y == 0:
                q1.append(' ')
        for j in range(len(b)):
            y = 0
            for i in range(len(b[j].split(' '))):
                if b[j].split(' ')[i] in currency:
                    y = 1
                    m = morph.parse(b[j].split(' ')[i])[0].normal_form
                    cur.append(m)
            if y == 0:
                cur.append(' ')
        words = ["кошел", "счёт", "счета", "кошелёк", 'кошелек', "кошельки", "с", "на", "названием", "название",
                 "названиями", "который", "которые", "назваются", "назвается", "привет", "пожалуйста", "пока",
                 "спасибо", "а", "ещё", 'пополни', 'добавь', 'положи', 'счет']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        q = []
        for i in range(len(q1)):
            if q1[i] == ' ':
                li = b[i].split(' ')
                q2 = []
                for j in range(len(li)):
                    if li[j] not in words and li[j] not in currency and list(li[j])[0] not in numbers:
                        q2.append(li[j])
                if not q2:
                    q.append(None)
                else:
                    q.append(' '.join(q2))
            else:
                q.append(q1[i])
        for i in range(len(q)):
            if q[i] not in bd and q[i] is not None:
                var = ['Что-то пошло не так. ', 'Ой произошла ошибка. ', 'Я не смог выполнить операцию. ']
                ok = random.choice(var)
                ret = ok
                ret += 'У вас нет кошелька с названием: ' + str(q[i])
                return ret, {}
        x = []
        if len(b) > 1:
            for i in range(len(b)):
                x.append(b[i].split(' '))
        else:
            x = st.split(' ')
        c = []
        for i in range(len(x)):
            if len(b) > 1:
                c1 = []
                for j in range(len(x[i])):
                    m = morph.parse(x[i][j])[0].normal_form
                    c1.append(m)
                c.append(c1)
            else:
                m = morph.parse(x[i])[0].normal_form
                c.append(m)
        summa = []
        if len(b) > 1:
            for i in range(len(c)):
                y = 0
                for j in range(len(c[i])):
                    w = list(c[i][j])
                    if w[0] in numbers:
                        y = 1
                        summa.append(int(c[i][j]))
                if y == 0:
                    summa.append(None)
        else:
            y = 0
            for i in range(len(c)):
                w = list(c[i])
                if w[0] in numbers:
                    y = 1
                    summa.append(int(c[i]))
            if y == 0:
                summa.append(None)
        for i in range(len(q)):
            if q[i] is None and summa[i] is None:
                ret = 'Какой кошелёк вы хотите пополнить?', {'username': q, 'summa': summa, 'currency': cur}
                return ret
            elif q[i] is None:
                ret = 'Какой кошелёк вы хотите пополнить на ' + str(summa[i]) + '?', {'username': q, 'summa': summa,
                                                                                      'currency': cur}
                return ret
            elif summa[i] is None:
                ret = 'На какую сумму вы хотите пополнить кошелёк ' + q[i] + '?', {'username': q, 'summa': summa,
                                                                                   'currency': cur}
                return ret
        ret = ''
        for j in range(len(q)):
            if q[j] in bd:
                currencyN = from_db("accounts", "Accounts", {"user_id": user_id, "accounts": q[j]})[0]
                if cur[j] != currencyN.currency and cur[j] != ' ':
                    var = ['Что-то пошло не так. ', 'Ой произошла ошибка. ', 'Я не смог выполнить операцию. ']
                    ok = random.choice(var)
                    ret += ok
                    ret += 'Валюта не соответствует валюте кошелька: ' + q[j] + '\n'
                    continue
                v = [i.bank for i in from_db('accounts', 'Accounts', {'accounts': q[j], 'user_id': user_id})]
                v1 = v[0]
                change_db('accounts', 'Accounts', {'bank': int(v1) + summa[j]}, {'accounts': q[j], 'user_id': user_id})
                var = ['Получилось! ', 'Я смог! ', 'У меня получилось! ']
                ok = random.choice(var)
                ret += ok
                ret += 'Баланс кошелька ' + q[j] + ' пополнен' + '\n'
                acc_id = [i.id for i in from_db('accounts', 'Accounts', {'accounts': q[j], 'user_id': user_id})][0]
                inwaste = [i.count for i in from_db('waste', 'Waste', {'category': 'пополнение', 'account_id': acc_id})]
                if inwaste == []:
                    to_db('waste', 'Waste', ('account_id', 'category', 'count'), (acc_id, 'пополнение', summa[j]))
                else:
                    summ = inwaste[0]
                    summ += summa[j]
                    change_db('waste', 'Waste', {'count': summ}, {'account_id': acc_id, 'category': 'пополнение'})
            elif q[j] not in words:
                var = ['Что-то пошло не так. ', 'Ой произошла ошибка. ', 'Я не смог выполнить операцию. ']
                ok = random.choice(var)
                ret += ok
                ret += 'У вас нет кошелька с названием ' + q[j] + '\n'
        return ret[:-1], {}
    else:
        b = st.split(' и ')
        user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
        user_id = user_id1[0]
        bd = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
        q1 = []
        currency = ['рубль', 'рубля', 'рублей', 'евро', 'доллар', 'доллара', 'долларов', 'фунт', 'фунта', 'фунтов',
                    'йена', 'йены', 'йен', 'франк', 'франка', 'франков', 'тенге']
        for j in range(len(b)):
            y = 0
            for e in bd:
                if e in ''.join(b[j]):
                    y = 1
                    q1.append(e)
            if y == 0:
                q1.append(' ')
        words = ["кошел", "счёт", "счета", "кошелёк", 'кошелек', "кошельки", "с", "на", "названием", "название",
                 "названиями", "который", "которые", "назваются", "назвается", "привет", "пожалуйста", "пока",
                 "спасибо", "а", "ещё", 'пополни', 'добавь', 'положи', "счет"]
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        q = []
        for i in range(len(q1)):
            if q1[i] == ' ':
                li = b[i].split(' ')
                q2 = []
                for j in range(len(li)):
                    if li[j] not in words and li[j] not in currency and list(li[j])[0] not in numbers:
                        q2.append(li[j])
                if not q2:
                    q.append(None)
                else:
                    q.append(' '.join(q2))
            else:
                q.append(q1[i])
        for i in range(len(q)):
            if q[i] not in bd:
                var = ['Что-то пошло не так. ', 'Ой произошла ошибка. ', 'Я не смог выполнить операцию. ']
                ok = random.choice(var)
                ret = ok
                ret += 'Я вас не понял)'
                return ret, {}
        x = []
        if len(b) > 1:
            for i in range(len(b)):
                x.append(b[i].split(' '))
        else:
            x = st.split(' ')
        c = []
        for i in range(len(x)):
            if len(b) > 1:
                c1 = []
                for j in range(len(x[i])):
                    m = morph.parse(x[i][j])[0].normal_form
                    c1.append(m)
                c.append(c1)
            else:
                m = morph.parse(x[i])[0].normal_form
                c.append(m)
        summa = []
        if len(b) > 1:
            for i in range(len(c)):
                y = 0
                for j in range(len(c[i])):
                    w = list(c[i][j])
                    if w[0] in numbers:
                        y = 1
                        summa.append(int(c[i][j]))
                if y == 0:
                    summa.append(None)
        else:
            y = 0
            for i in range(len(c)):
                w = list(c[i])
                if w[0] in numbers:
                    y = 1
                    summa.append(int(c[i]))
            if y == 0:
                summa.append(None)
        username = k['username']
        summaO = k['summa']
        for i in range(len(username)):
            if username[i] is None:
                username[i] = q[0]
                q.pop(0)
                break
            elif summaO[i] is None:
                summaO[i] = summa[0]
                summa.pop(0)
                for j in range(len(b)):
                    y = 0
                    for e in range(len(b[j].split(' '))):
                        if b[j].split(' ')[e] in currency:
                            y = 1
                            m = morph.parse(b[j].split(' ')[e])[0].normal_form
                            k['currency'][i] = m
                    if y == 0:
                        k['currency'][i] = ' '
                break
        q.clear()
        summa.clear()
        q = username.copy()
        summa = summaO.copy()
        for i in range(len(q)):
            if q[i] is None and summa[i] is None:
                ret = 'Какой кошелёк вы хотите пополнить?', {'username': q, 'summa': summa, 'currency': k['currency']}
                return ret
            elif q[i] is None:
                ret = 'Какой кошелёк вы хотите пополнить на ' + str(summa[i]) + '?', {'username': q, 'summa': summa,
                                                                                      'currency': k['currency']}
                return ret
            elif summa[i] is None:
                ret = 'На какую сумму вы хотите пополнить кошелёк ' + q[i] + '?', {'username': q, 'summa': summa,
                                                                                   'currency': k['currency']}
                return ret
        cur = k['currency']
        ret = ''
        for j in range(len(q)):
            if q[j] in bd:
                currencyN = from_db("accounts", "Accounts", {"user_id": user_id, "accounts": q[j]})[0]
                if cur[j] != currencyN.currency and cur[j] != ' ':
                    var = ['Что-то пошло не так. ', 'Ой произошла ошибка. ', 'Я не смог выполнить операцию. ']
                    ok = random.choice(var)
                    ret += ok
                    ret += 'Валюта не соответствует валюте кошелька: ' + q[j] + '\n'
                    continue
                v = [i.bank for i in from_db('accounts', 'Accounts', {'accounts': q[j], 'user_id': user_id})]
                v1 = v[0]
                change_db('accounts', 'Accounts', {'bank': int(v1) + summa[j]}, {'accounts': q[j], 'user_id': user_id})
                var = ['Получилось! ', 'Я смог! ', 'У меня получилось! ']
                ok = random.choice(var)
                ret += ok
                ret += 'Баланс кошелька ' + q[j] + ' пополнен' + '\n'
                acc_id = [i.id for i in from_db('accounts', 'Accounts', {'accounts': q[j], 'user_id': user_id})][0]
                inwaste = [i.count for i in from_db('waste', 'Waste', {'category': 'пополнение', 'account_id': acc_id})]
                if inwaste == []:
                    to_db('waste', 'Waste', ('account_id', 'category', 'count'), (acc_id, 'пополнение', summa[j]))
                else:
                    summ = inwaste[0]
                    summ += summa[j]
                    change_db('waste', 'Waste', {'count': summ}, {'account_id': acc_id, 'category': 'пополнение'})
            elif q[j] not in words:
                var = ['Что-то пошло не так. ', 'Ой произошла ошибка. ', 'Я не смог выполнить операцию. ']
                ok = random.choice(var)
                ret += ok
                ret += 'У вас нет кошелька с названием ' + q[j] + '\n'
        return ret[:-1], {}
