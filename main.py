from flask import Flask, render_template, request, redirect
from base62Util import decode, encode
app = Flask(__name__)

def getSqliteConnection():
    import sqlite3
    conn = sqlite3.connect('test.db')
    return conn

def getMaxID():
    conn = getSqliteConnection()
    c = conn.cursor()
    cursor = c.execute("SELECT MAX(ID) from URLTable")
    id  = cursor.fetchone()[0]
    print("id = %d" % id)
    return id if id else -1

@app.route('/')
def index():
    conn = getSqliteConnection()
    c = conn.cursor()
    # cursor = c.execute("DELETE from URLTable")
    cursor = c.execute("SELECT * from URLTable")
    for row in cursor:
        print(row)

    # conn.commit()
    conn.close()
    return render_template("mainPage.html")

def saveURLtoDB(url):
    conn = getSqliteConnection()
    c = conn.cursor()
    script = "INSERT INTO URLTable (targetURL) VALUES ('%s')" % url
    c.execute(script)
    conn.commit()
    conn.close()

def getIDFromURL(url):
    conn = getSqliteConnection()
    c = conn.cursor()
    script = "SELECT ID from URLTable Where targetURL = '%s'" % url
    c.execute(script)
    bResult = c.rowcount >= 1
    if bResult:
        id = c.fetchone()[0]
    else:
        id = -1
    conn.close()
    return id

def isURLinDB(url):
    conn = getSqliteConnection()
    c = conn.cursor()
    script = "SELECT ID from URLTable Where targetURL = '%s'" % url
    c.execute(script)
    bResult = c.rowcount >= 1
    conn.close()
    return bResult

@app.route('/makeItShorter', methods=['POST'])
def makeItShorter(targetURL=''):
    import re
    if len(targetURL) == 0:
        targetURL = request.form.get('targetURL', 'ALL')
    print("targetURL = ", targetURL)
    if re.match(r'^https?:/{2}\w.+$', targetURL):
        pass
    else:
        return "請輸入合法網址!!"

    if targetURL:
        if isURLinDB(targetURL):
            id = getIDFromURL(targetURL)
            if id > 0:
                encodedStr = encode(id)
                if len(encodedStr) < 5:
                    while len(encodedStr) < 5:
                        encodedStr = "0" + encodedStr
            else:
                return "ERROR!! Try another url"
        else:
            id = getMaxID() + 1
            encodedStr = encode(id)
            if len(encodedStr) < 5:
                while len(encodedStr) < 5:
                    encodedStr = "0" + encodedStr
            saveURLtoDB(targetURL)
        return "目標網址 = %s 短網址 = %s" % (targetURL, encodedStr)
    else:
        return redirect("/")

@app.route('/previewURL', methods=['POST'])
def querySource():
    previewURL = request.form.get('previewURL', 'ALL')
    if previewURL:
        print("previewURL %s" % previewURL)
        url = getURLfromShortURL(previewURL)
        if not url:
            return "找不到這個短網址的目標網址"
        return "目標網址 => %s " % url
    else:
        return redirect("/")

def getURLfromShortURL(previewURL):
    conn = getSqliteConnection()
    c = conn.cursor()
    decodedID = decode(previewURL)
    print("decodeID = %d "% decodedID)
    script = "SELECT targetURL from URLTable Where ID = %d" % decodedID
    cursor = c.execute(script)
    data = cursor.fetchone()
    url = ''
    if data:
        url = data[0]
    return url


@app.route('/<url_key>')
def redirectTo(url_key):
    if url_key in ["previewURL", "makeItShorter", "/", "favicon.ico"]:
        return '', 204
    url = getURLfromShortURL(url_key)
    return redirect(url)

if __name__ == "__main__":
    app.run()