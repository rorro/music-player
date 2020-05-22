from flask import g
import sqlite3

DATABASE = "database.db"

def get_votes(link):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute('''select upvotes, downvotes from songs where link = ? ''', (link,))

    res = c.fetchall()
    if res:
        return res[0]
    return None

    db.close()

def upvote(token, link):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    votes = get_votes(link)
    if votes:
        c.execute(''' update songs set upvotes = ? where link = ? ''', (votes[0]+1, link))
    else:
        c.execute(''' insert into songs values (?, ?, ?) ''', (link, 1, 0))

    c.execute(''' insert into user_votes (token, link, vote)
                  values (?, ?, ?)
                  on conflict (token, link)
                  do update set vote = ?''', (token, link, 1, 1))

    db.commit()
    db.close()

def downvote(token, link):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    votes = get_votes(link)
    if votes:
        c.execute(''' update songs set downvotes = ? where link = ? ''', (votes[1]+1, link))
    else:
        c.execute(''' insert into songs values (?, ?, ?) ''', (link, 0, 1))

    c.execute(''' insert into user_votes (token, link, vote)
                  values (?, ?, ?)
                  on conflict (token, link)
                  do update set vote = ?''', (token, link, 0, 0))

    db.commit()
    db.close()
