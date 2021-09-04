mport requests
from bs4 import BeautifulSoup
import random as ran
from PIL import Image
import io
from langdetect import detect
import pymysql

host = ur host
user = ur user name
pw = ur database pw
db = ur database name
port = ur port


def parser(x, y):
    url = 'https://chemequations.com/ru/?s=' + x + '+%2B+' + y + '&ref=input'

    def get_html(url, params=None):
        r = requests.get(url, params=params)
        return r

    def get_content(html):
        global c
        s = BeautifulSoup(html, 'html.parser')
        pog = s.find('h1', class_='equation main-equation well').get_text()
        return pog

    def parse():
        html = get_html(url)
        if html.status_code == 200:
            return get_content(html.text)
        else:
            print('Error')

    return parse()


def gradient(color1, color2, color3=False):
    if not color3:
        ni = Image.new('RGB', (512, 200), (0, 0, 0))
    else:
        ni = Image.new('RGB', (1024, 400), (0, 0, 0))
    w, h, = ni.size
    pix = ni.load()
    r = color1[0]
    g = color1[1]
    b = color1[2]
    r1 = color2[0]
    g1 = color2[1]
    b1 = color2[2]
    if color3:
        r2 = color3[0]
        g2 = color3[1]
        b2 = color3[2]
    for i in range(512):
        if i % 2 == 0:
            if r < r1:
                r += 1
            elif r > r1:
                r -= 1
            if g < g1:
                g += 1
            elif g > g1:
                g -= 1
            if b < b1:
                b += 1
            elif b > b1:
                b -= 1
        for j in range(h):
            f = (r, g, b)
            pix[i, j] = f
    if color3:
        for i in range(512):
            if i % 2 == 0:
                if r < r2:
                    r += 1
                elif r > r2:
                    r -= 1
                if g < g2:
                    g += 1
                elif g > g2:
                    g -= 1
                if b < b2:
                    b += 1
                elif b > b2:
                    b -= 1
            for j in range(h):
                f = (r, g, b)
                pix[i + 512, j] = f
    return (ni)




def anagliph(image):
    response = requests.get(image)
    im = Image.open(io.BytesIO(response.content))
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            if i > 20 and j > 20:
                pixels[i - 20, j - 20] = (pixels[i, j][0], pixels[i - 20,
                                                                        j - 20][1], pixels[i - 20, j - 20][2])
    return(im)


def reverse(image):
    response = requests.get(image)
    im = Image.open(io.BytesIO(response.content))
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            pixels[i, j] = (256 - pixels[i, j][0], 256 - pixels[i, j][1], 256 - pixels[i, j][2])
    return(im)


def checklang(s):
    lang = detect(s)
    return lang


def updatesql(server, joinchannel=False, joinrole=False, joinvoice=False, voicecat=False, logs=False, links=2):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=pw,
            database=db,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as c:
                x = c.execute(
                    "SELECT id, COUNT(*) FROM bot WHERE id = %s GROUP BY id",
                    (server)
                )
                if not x:
                    insert_query = f"INSERT INTO `bot` (id) VALUES ({server});"
                    c.execute(insert_query)
                    connection.commit()

                if joinvoice:
                    update_query = f"UPDATE `bot` SET joinvoice = {joinvoice}, voicecat = {voicecat}  WHERE id = {server};"
                    c.execute(update_query)
                    connection.commit()
                if joinrole:
                    update_query = f"UPDATE `bot` SET joinrole = {joinrole}  WHERE id = {server};"
                    c.execute(update_query)
                    connection.commit()
                if joinchannel:
                    update_query = f"UPDATE `bot` SET joinchannel = {joinchannel}  WHERE id = {server};"
                    c.execute(update_query)
                    connection.commit()
                if logs:
                    update_query = f"UPDATE `bot` SET logs = {logs}  WHERE id = {server};"
                    c.execute(update_query)
                    connection.commit()
                if links != 2:
                    update_query = f"UPDATE `bot` SET linksfilter = {links}  WHERE id = {server};"
                    c.execute(update_query)
                    connection.commit()
        finally:
            connection.close()

    except Exception as e:
        print(e)


def getsqldata(server, joinchannel=False, joinrole=False, joinvoice=False, logs=False, links=False):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=pw,
            database=db,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as c:
                select_all_rows = f"SELECT * FROM `bot` WHERE id = {server};"
                c.execute(select_all_rows)
                rows = c.fetchall()
                for row in rows:
                    if joinvoice:
                        return (row['joinvoice'], row['voicecat'])
                    elif joinrole:
                        return row['joinrole']
                    elif joinchannel:
                        return row['joinchannel']
                    elif logs:
                        return row['logs']
                    elif links:
                        return row['linksfilter']
        finally:
            connection.close()
    except Exception as e:
        print(e)


def checker(guild):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=pw,
            database=db,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as c:
                return c.execute(f"SELECT * FROM `bot` WHERE id = {guild};")
        finally:
            connection.close()
    except Exception as e:
        print(e)


def checklink(message):
    url = message[message.find('http'):]
    url = url.split('/')[2]
    url = 'https://www.urlvoid.com/scan/' + url

    def get_html(url, params=None):
        r = requests.get(url, params=params)
        return r

    def get_content(html):
        global c
        s = BeautifulSoup(html, 'html.parser')
        pog = s.find('span', class_='label label-success')
        if not pog:
            pog = s.find('span', class_='label label-danger')
        return int(pog.get_text().split('/')[0])

    def parse():
        html = get_html(url)
        if html.status_code == 200:
            return get_content(html.text)
        else:
            print('Error')

    return parse()
