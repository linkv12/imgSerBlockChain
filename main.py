from modal import add_data
from modal import mining
from modal import unload

def main() :
    sto = True
    while sto :
        print('Option :')
        print('1. Add data')
        print('2. Mine data')
        print('3. Unload data')
        print('4. Exit')
        user_input = str(input('Input (1,2,3,4): '))
        if user_input == '1' :
            add_data.main()
        elif user_input == '2' :
            print('Will takes ~ 30 min')
            mining.main()
        elif user_input == '3' :
            unload.main()
        elif user_input == '4' :
            sto = False
        else :
            print('Invalid input')



if __name__ == '__main__' :
    print("Nama file akan ditambah dengan waktu saat ini")
    main ()