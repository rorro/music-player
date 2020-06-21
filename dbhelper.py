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

def has_voted(token, link):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute(''' select * from user_votes where token = ? and link = ?''', (token, link))
    res = c.fetchall()

    if res:
        return True
    else:
        return False

    db.close()

def get_vote_type(token, link):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute(''' select vote from user_votes where token = ? and link = ?''', (token, link))
    res = c.fetchall()

    if res:
        return res[0][0]
    else:
        return None

    db.close()


def upvote(token, link):
    vote_type = get_vote_type(token, link)
    votes = get_votes(link)
    voted = has_voted(token, link)

    db = sqlite3.connect(DATABASE)
    c = db.cursor()


    if votes:
        if not voted:
            c.execute(''' update songs set upvotes = ? where link = ? ''', (votes[0]+1, link))

            c.execute(''' insert into user_votes (token, link, vote)
                          values (?, ?, ?) ''', (token, link, 1))
        else:
            if vote_type == 1:
                c.execute(''' delete from user_votes where token = ? and link = ? ''', (token, link))
                c.execute(''' update songs set upvotes = ? where link = ? ''', (votes[0]-1, link))
            else:
                c.execute(''' update user_votes set vote = ? where token = ? and link = ? ''', (1, token, link))
                c.execute(''' update songs set upvotes = ?, downvotes = ?
                              where link = ? ''', (votes[0]+1, votes[1]-1, link))
    else:
        c.execute(''' insert into songs values (?, ?, ?) ''', (link, 1, 0))

        c.execute(''' insert into user_votes (token, link, vote)
                      values (?, ?, ?) ''', (token, link, 1))

    db.commit()
    db.close()

def downvote(token, link):
    vote_type = get_vote_type(token, link)
    votes = get_votes(link)
    voted = has_voted(token, link)

    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    if votes:
        if not voted:
            c.execute(''' update songs set downvotes = ? where link = ? ''', (votes[1]+1, link))

            c.execute(''' insert into user_votes (token, link, vote)
                          values (?, ?, ?) ''', (token, link, 0))
        else:
            if vote_type == 0:
                c.execute(''' delete from user_votes where token = ? and link = ? ''', (token, link))
                c.execute(''' update songs set downvotes = ? where link = ? ''', (votes[1]-1, link))
            else:
                c.execute(''' update user_votes set vote = ? where token = ? and link = ? ''', (0, token, link))
                c.execute(''' update songs set upvotes = ?, downvotes = ?
                              where link = ? ''', (votes[0]-1, votes[1]+1, link))
    else:
        c.execute(''' insert into songs values (?, ?, ?) ''', (link, 0, 1))

        c.execute(''' insert into user_votes (token, link, vote)
                      values (?, ?, ?) ''', (token, link, 0))

    db.commit()
    db.close()

def highlight_votes(upvotes, downvotes):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    upvoted, downvoted = [], []

    if upvotes == "true":
        c.execute(''' select link from songs where upvotes > 0 and downvotes = 0 ''')
        upvoted = [link[0] for link in c.fetchall()]
    if downvotes == "true":
        c.execute(''' select link from songs where upvotes = 0 and downvotes > 0 ''')
        downvoted = [link[0] for link in c.fetchall()]

    res = {"upvoted": upvoted, "downvoted": downvoted}
    return res

    db.close()
