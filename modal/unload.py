import mysql.connector
import tkinter
from tkinter.filedialog import asksaveasfile, asksaveasfilename

def askFileToUnload() :
    # untuk memilih file dari blockchain
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()
    sql = 'SELECT `filename` FROM `blockchain`'
    cursor.execute(sql)
    dt = cursor.fetchall()
    fileName = []
    for d in dt :
        fileName.append(d[0])

    fileName = list(set(fileName))
    text = 'genenis.genesis'

    idx = 0
    while fileName[idx] != text :
        #print(fileName[idx])
        idx += 1

    fileName = fileName[:idx] + fileName[idx+1:]
    mydb.close()

    sto = True
    user_input = ''
    while sto :
        print('Available File : ')
        idx = 0
        for fName in fileName :
            print('[%d] : %s' % (idx, fName))
            idx += 1
        print('Please Input Number in the Brackets')
        user_input = str(input('Input : '))
        try :
            user_input = int(user_input)
            if user_input < 0 or user_input > len(fileName) -1 :
                print('Invalid Input')
            else :
                sto = False

        except ValueError:
            print('Invalid Input')
    return fileName[user_input]

def getBlobData(fileName) :
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()
    sql = 'SELECT `data` FROM `blockchain` WHERE `filename` = %s ORDER BY partNumber'
    val = (fileName, )
    cursor.execute(sql, val)
    dt = cursor.fetchall()
    t_blob = []
    for d in dt :
        t_blob.append(d[0])

    return t_blob




def main() :
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='imgblockchain'
    )
    cursor = mydb.cursor()

    fileName = askFileToUnload()
    blob_data = getBlobData(fileName)

    root = tkinter.Tk()
    fileExt = str(fileName.split('.')[-1])
    saveFilePath = ''
    while saveFilePath == '' :
        saveFilePath = asksaveasfile(initialfile=fileName, title="Save as", mode='wb',
                                                    filetypes=(("%s files" % fileExt, "*.%s" % fileExt), ("all files", "*.*")))

    with saveFilePath :
        for b in blob_data :
            saveFilePath.write(b)

    saveFilePath.close()
    root.withdraw()
    root.destroy()

if __name__ == '__main__':
    main()