from db_working import to_db, from_db, change_db, remove_from_db


def wasting(a):
    id1 = [i.id for i in from_db("accounts", "Accounts", {"account": N})]
    id = id1[0]
    summ1 = [j.bank for j in from_db("accounts", "Accounts", {"account": N})]
    summ = summ1[0]
    summ -= x
    newcount1 = [k.count for k in from_db("waste", "Waste", {"account_id": id, "category": t})]
    newcount = newcount1[0]
    newcount += x
    change_db("accouns", "Accounts", {"bank": summ}, {"acccount": N})
    change_db("waste", "Waste", {"count": newcount}, {"account_id": id, "category": t})
# N - название счёта, x - сумма, t - категория
# это пока без распознавания. но я уже прописал, что программа делает, после распознавания