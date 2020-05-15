import threading
import mysql.connector
from hashlib import sha256
semLock = threading.Lock()
glob_found = False
pattern = '00'

def mining(data: tuple) :
    # akan melakukan mining dari data tuple
    global pattern
    pat = str(pattern)

    # tuple dirubah menjadi dictionanry
    data_dict = {'id': data[0],
                 'prevHash': data[1],
                 'filename': data[2],
                 'partNumber': data[3],
                 'data': data[4],
                 'time': data[5],
                 'hash' : data[-1]}

    nonce = 0
    found_nonce = False
    global glob_found
    # brute force mencari nonce
    while not found_nonce :
        temp =  dict(data_dict)
        temp['nonce'] = nonce
        hashed_nonce = str(sha256(str(temp).encode('utf-8')).hexdigest())

        nonce += 1
        if hashed_nonce[:len(pat)] == pat:
            found_nonce = True

        if glob_found == True :
            found_nonce = True


    # nonce ditemukan
    data_dict['nonce'] = nonce

    # critical section
    semLock.acquire()

    # raise flag
    # nonce _found
    glob_found = True

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()

    sql = """SELECT count(*) as tot FROM blockchain where id = %s"""
    val = (data_dict['id'], )
    cursor.execute(sql, val)
    cnt = cursor.fetchone()[0]

    # jika blockchain tidak ada pada table
    if cnt == 0 :
        sql2 = 'INSERT INTO `blockchain`(`id`, `prevHash`, `filename`, `partNumber`, `data`, `time`, `hash`, `nonce`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)'
        val2 = (data_dict['id'], data_dict['prevHash'], data_dict['filename'],
               data_dict['partNumber'], data_dict['data'], data_dict['time'],
               data_dict['hash'], data_dict['nonce'], )
        cursor.execute(sql2, val2)
        mydb.commit()

        sql3 = 'DELETE FROM `data_pool` WHERE `id`= %s'
        val3 = (data_dict['id'], )
        cursor.execute(sql3, val3)
        mydb.commit()

    mydb.close


    semLock.release()

def main () :
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()

    thread_list = []
    thread_num = 3

    sql = 'SELECT * FROM `data_pool` ORDER BY `id` '
    cursor.execute(sql)
    data = cursor.fetchall()
    mydb.close()
    global glob_found
    for dt in data :
        print('Mining on ID : %s' % str(dt[0]))
        glob_found = False
        for i in range(thread_num) :
            thread_list.append(threading.Thread(target=mining, args=(dt,)))

        for t in thread_list :
            t.start()

        for t in thread_list :
            t.join()

        thread_list = []

if __name__ == '__main__' :
    main()




