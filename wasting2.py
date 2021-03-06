from skills.YandexOlympicsAlice.db_working import to_db, from_db, change_db
import pymorphy2
from skills.YandexOlympicsAlice import w2n
morph = pymorphy2.MorphAnalyzer()


def wasting(s, user_name, info):
    old = info
    req = s.split()
    for i in range(len(req)):
        try:
            parse_it = morph.parse(req[i])
            maybe_num = parse_it[0].normal_form
            req[i] = str(w2n.word_to_num(maybe_num))
        except Exception:
            pass
    s = ' '.join(req)
    flag = True
    list = [('развлечения', ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг', "аттракционы"]),
            ('продукты', ['продукты', 'еда', "покушать", "еду", 'пятёрочка', 'пятерочке']),
            ('налоги', ['налоги', 'жкх', 'ЖКХ', 'кредит', 'ипотека', 'ипотеку']),
            ('магазины', ['магазины', 'одежду', 'одежда', 'канцелярию', 'канцелярия', "одежда"])]
    list2 = ['развлечения', 'кафе', 'ресторан', 'ресторане', 'шоппинг', "аттракционы",
             'продукты', 'еда', "покушать", "еду", 'пятёрочка', 'пятерочке',
             'налоги', 'жкх', 'ЖКХ', 'кредит', 'ипотека', 'ипотеку',
             'магазины', 'одежду', 'одежда', 'канцелярию', 'канцелярия', "одежда"]
    user_id1 = [i.id for i in from_db("users", "Users", {"username": user_name})]
    user_id = user_id1[0]
    n = []
    N = []
    x = []
    t = []
    names = [i.accounts for i in from_db("accounts", "Accounts", {"user_id": user_id})]
    if info == {}:
        a = s.split(' и ')
        for i in range(len(a)):
            a1 = a[i].split()
            for j in range(len(a1)):
                if ord('0') <= ord(a1[j][0]) <= ord('9') and len(x) < (i + 1):
                    x.append(a1[j])
            for j in names:
                kosh = ' ' + j + ' '
                vvod = ' ' + a[i] + ' '
                if kosh in vvod and len(N) < (1 + i):
                    N.append(j)
            for j in list2:
                if j in a[i]:
                    n.append(j)
            for j in n:
                for k in list:
                    if j in k[1] and len(t) < (i + 1):
                        t.append(k[0])
            if len(x) < (i + 1):
                x.append(None)
            if len(N) < (i + 1):
                N.append(None)
            if len(t) < (i + 1):
                t.append('другое')
                n.append('другое')
        info = {}
        s = ''
        s_error = ''
        info['summ'] = []
        info['name'] = []
        info['cate'] = []
        for o in range(min(len(N), len(x), len(t))):
            if x[o] == None or N[o] == None:
                if x[o] == None and N[o] == None:
                    s_error += 'Извините, не совсем Вас понял.'
                elif x[o] != None and N[o] == None:
                    s_error += 'Повторите пожалуйста, с какого счёта списать ' + str(x[o]) + '?'
                elif x[o] == None and N[o] != None:
                    s_error += 'Извините, сколько вы потратили со счёта ' + N[o] + '?'
                x1 = info['summ']
                N1 = info['name']
                t1 = info['cate']
                t1.append(t[o])
                N1.append(N[o])
                x1.append(x[o])
                info['summ'] = x1
                info['name'] = N1
                info['cate'] = t1
                s_error += '    '
            else:
                id1 = [i.id for i in from_db("accounts", "Accounts", {"accounts": N[o], "user_id": user_id})]
                id = id1[0]
                summ1 = [j.bank for j in from_db("accounts", "Accounts", {"accounts": N[o], "user_id": user_id})]
                summ = summ1[0]
                summ -= int(x[o])
                change_db("accounts", "Accounts", {"bank": summ}, {"accounts": N[o], "user_id": user_id})
                newcount1 = [k.count for k in from_db("waste", "Waste", {"account_id": id, "category": t[o]})]
                if len(newcount1) != 0:
                    newcount = newcount1[0]
                    newcount += int(x[o])
                    change_db("waste", "Waste", {"count": newcount}, {"account_id": id, "category": t[o]})
                else:
                    to_db("waste", "Waste", ("account_id", "category", "count"), (id, t[o], int(x[o])))
                cur1 = [i.currency for i in from_db('accounts', 'Accounts', {'user_id': user_id, 'accounts': N[o]})]
                cur = cur1[0]
                st = 'Успешно списано ' + str(x[o]) + ' ' + cur[0:3] + '.' + ' с кошелька ' + str(N[o]) + ' за ' + t[o] + '.'
                s += st
                s += '  '
        s += s_error
    else:
        a = s.split(' и ')
        for i in range(len(a)):
            a1 = a[i].split()
            if info['summ'][i] is None:
                for j in range(len(a1)):
                    if ord('0') <= ord(a1[j][0]) <= ord('9') and info['summ'][i] == None:
                        info['summ'][i] = a1[j]
            if info['name'][i] == None:
                for j in names:
                    if (' ' + j + ' ') in (' ' + a[i] + ' ') and info['name'][i] == None:
                        info['name'][i] = j
        x = info['summ']
        N = info['name']
        t = info['cate']
        info = {}
        s = ''
        s_error = ''
        info['summ'] = []
        info['name'] = []
        info['cate'] = []
        for o in range(min(len(N), len(x), len(t))):
            if x[o] == None or N[o] == None or t[o] == None:
                if x[o] == None and N[o] == None:
                    s_error += 'Извините, не совсем Вас понял.'
                elif x[o] != None and N[o] == None:
                    s_error += 'Повторите пожалуйста, с какого счёта списать ' + str(x[o]) + '?'
                elif x[o] == None and N[o] != None:
                    s_error += 'Извините, сколько вы потратили со счёта ' + N[o] + '?'
                x1 = info['summ']
                N1 = info['name']
                t1 = info['cate']
                t1.append(t[o])
                N1.append(N[o])
                x1.append(x[o])
                info['summ'] = x1
                info['name'] = N1
                info['cate'] = t1
                s_error += '    '
            else:
                id1 = [i.id for i in from_db("accounts", "Accounts", {"accounts": N[o], "user_id": user_id})]
                id = id1[0]
                summ1 = [j.bank for j in from_db("accounts", "Accounts", {"accounts": N[o], "user_id": user_id})]
                summ = summ1[0]
                summ -= int(x[o])
                change_db("accounts", "Accounts", {"bank": summ}, {"accounts": N[o], "user_id": user_id})
                newcount1 = [k.count for k in from_db("waste", "Waste", {"account_id": id, "category": t[o]})]
                if len(newcount1) != 0:
                    newcount = newcount1[0]
                    newcount += int(x[o])
                    change_db("waste", "Waste", {"count": newcount}, {"account_id": id, "category": t[o]})
                else:
                    to_db("waste", "Waste", ("account_id", "category", "count"), (id, t[o], int(x[o])))
                cur1 = [i.currency for i in from_db('accounts', 'Accounts', {'user_id': user_id, 'accounts': N[o]})]
                cur = cur1[0]
                st = 'Успешно списано ' + str(x[o]) + ' ' + cur[0:3] + '.' + ' с кошелька ' + str(N[o]) + ' за ' + t[o] + '.'
                s += st
                s += '  '
        s += s_error
    if info['summ'] == [] and info['name'] == [] and info['cate'] == []:
        info = {}
    if old != {} and info == old:
        s = 'Извините, я вас не понял. Проверьте правильность называемых кошельков, категорий и сумм.'
        info = {}
    return s, info

