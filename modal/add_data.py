import mysql.connector
from datetime import datetime
import tkinter
from tkinter.filedialog import askopenfilename
from hashlib import sha256

# success
def test_blob() :
    filename = '20200124140438_1.jpg'
    sql = 'SELECT `partNumber`, `data` FROM `data_entry` WHERE `filename` = %s ORDER by partNumber'
    val = (filename, )
    print(sql)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()
    cursor.execute(sql, val)
    data = cursor.fetchall()

    with open(filename, mode='wb') as f :
        for dt in data :
            f.write(dt[-1])

    mydb.close()



# real def

def getLatestId() :
    # untuk mendapatkan id terakhir dari
    # data yang ada pada database
    # return id : int
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()
    sql = """SELECT count(*) as tot FROM data_pool"""
    cursor.execute(sql)
    cntData = cursor.fetchone()[0]
    id = -1
    if cntData == 0 :
        sql2 = 'SELECT `id` FROM `blockchain` ORDER BY ID DESC LIMIT 1'
        cursor.execute(sql2)
        id = cursor.fetchone()[0]
    else :
        sql2 = 'SELECT `id` FROM `data_pool` ORDER BY ID DESC LIMIT 1'
        cursor.execute(sql2)
        id = cursor.fetchone()[0]
    mydb.close()
    return id


def getLatestHash() :
    # mengambil hash terakhir dari data
    # mengembalikan hash
    # return hash : str 256
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()
    sql = """SELECT count(*) as tot FROM data_pool"""
    cursor.execute(sql)
    cntData = cursor.fetchone()[0]
    hash = ''
    if cntData == 0 :
        sql2 = 'SELECT `hash` FROM `blockchain` ORDER BY ID DESC LIMIT 1'
        cursor.execute(sql2)
        hash = cursor.fetchone()[0]
    else :
        sql2 = 'SELECT `hash` FROM `data_pool` ORDER BY ID DESC LIMIT 1'
        cursor.execute(sql2)
        hash = cursor.fetchone()[0]
    mydb.close()
    return hash

def addDataPool() :
    # will add data to data_pool from table data_entry
    # ini memasukkan data dari table data entry ke table data pool
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()
    sql = 'SELECT `id`, `filename`, `partNumber`, `data`, `time` FROM `data_entry` ORDER BY id'
    cursor.execute(sql)
    data = cursor.fetchall()

    for dt in data :
        # get latest id
        id = getLatestId()
        prevHash = getLatestHash()

        data_entryId = dt[0]
        data_dict = {'id'         : id+1,
                     'prevHash'   : prevHash,
                     'filename'   : dt[1],
                     'partNumber' : dt[2],
                     'data'       : dt[3],
                     'time'       : dt[4]}
        hash = str(sha256(str(data_dict).encode('utf-8')).hexdigest())
        data_dict['hash'] = hash
        sql = 'INSERT INTO `data_pool`(`id`, `prevHash`, `filename`, `partNumber`, `data`, `time`, `hash`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        val = tuple([v for k, v in data_dict.items()])
        cursor.execute(sql,val)
        mydb.commit()

        sql2 = 'DELETE FROM `data_entry` WHERE `id` = %s'
        val = (data_entryId, )
        cursor.execute(sql2, val)
        mydb.commit()

    mydb.close()

def dataEntry(path:str, time:datetime) :
    # parameter path -> path data
    #           time -> datetime
    # memasukkan data ke dalam table data entry
    slash_char = '/'
    temp = []
    with open(file=path, mode='rb') as f :
         stop = False
         while not stop :
             # split to 64k blob
             data = f.read(64*1024-1)
             if data != b'' :
                temp.append(data)
             else :
                stop = True

    filename = path.split(slash_char)[-1]
    tName = filename.split('.')
    fName = []
    fName.append(tName[0])
    fName.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d_%H-%M-%S'))
    fName.append(tName[-1])
    fName = '%s_%s.%s' % (fName[0], fName[1], fName[-1])

    sql = """INSERT INTO `data_entry`(`filename`, `partNumber`, `data`, `time`) VALUES (%s, %s, %s, %s)"""
    for i in range(0,len(temp)) :
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database='imgblockchain'
        )
        cursor = mydb.cursor()
        val = (fName, i, temp[i], time)
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()




def main () :
    # main loop untuk modul add_data
    root = tkinter.Tk()
    path = ''
    while path == '' :
        path = askopenfilename()
    now = datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    root.withdraw()
    root.destroy()

    dataEntry(path, now)
    addDataPool()

if __name__ == '__main__' :
    #test_blob()
    main ()
