import time
import mysql.connector as c
import pwinput

mydb=c.connect(host='localhost',user='root',database='project',password='')
cu=mydb.cursor()

def accno():                           #Function to automatically assign account number
    l=[]
    cu.execute('select * from usr_dat')
    dat=cu.fetchall()
    for i in dat:
        l.append(i[0])
    accno=max(l)+1
    return(accno)

def register():                        #Register function
    acc=accno()
    usr=input('Enter your username: ')
    pas=pwinput.pwinput('Enter your password: ')
    cpass=pwinput.pwinput('Confirm your password: ')
    tab=399
    if cpass==pas:
        q="insert into usr_dat(acc_no,username,tab,password) values({},'{}',{},'{}')".format(acc,usr,tab,pas)
        cu.execute(q)
        mydb.commit()
        print('Successfully registered')
    else:
        print('Passwords do not match')
        register()
    main_menu()

def a_main_menu(i):                    #Admin Menu
    print()
    print('Loading...')
    print()
    time.sleep(1)
    print('''Welcome admin What would you like to do

    [1]EDIT CAFE MENU
    [2]EDIT BOOK DATABASE
    [3]EDIT GAME DATABASE
    [4]MANAGE GAMING STATION DETAILS
    [5]MANAGE MOVIE HALL DETAILS
    [6]LOGOUT
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        print('EDITING CAFE MENU')
        cafe_e(i)
    elif n==2:
        print('EDITING BOOK DATABASE')
        book_e(i)
    elif n==3:
        print('EDITING GAME DATABASE')
        gam_e(i)
    elif n==4:
        print('MANAGING GAMING STATION BOOKINGS')
        gst_e(i)
    elif n==5:
        print('MANAGING MOVIE HALL BOOKINGS')
        mov_e(i)
    elif n==6:
        print('Logging out...')
        time.sleep(1)
        main_menu()
    else:
        print('Enter a valid choice')

def cafe_menu(x):                      #Cafe Menu
    print('''
    CAFE MENU

    [1] COFFEE
    [2] LATTE
    [3] PASTRIES
    [4] SANDWICH
    [5] JUICE
    [6] DESSERTS
    [7] MILKSHAKES
    [8] BACK
    ''')
    n=int(input('Enter your option: '))
    if n==1:
        print()
        print('COFFEE')
        y='coffee'
    elif n==2:
        print()
        print('LATTE')
        y='latte'
    elif n==3:
        print()
        print('PASTRIES')
        y='pastries'
    elif n==4:
        print()
        print('SANDWICH')
        y='sandwich'
    elif n==5:
        print()
        print('JUICE')
        y='juice'
    elif n==6:
        print()
        print('DESSERTS')
        y='desserts'
    elif n==7:
        print()
        print('MILKSHAKES')
        y='milkshakes'
    elif n==8:
        print()
        u_main_menu(x)
    else:
        print('Enter a valid choice')
    cafe(y,x)
def cafe(y,x):                         #Function for ordering
    Q=("select * from cafe_menu where i_type=%s")
    cu.execute(Q,(y,))
    dat=cu.fetchall()
    l=[]
    for i in dat:
        l.append(i[2].lower())
    print()
    print(y.title())
    print()
    for i in dat:
        r=str(i[2])+'- - - - - ₹ '+str(i[3])
        print(r)
    print()
    n=input('Enter your choice of '+str(y)+': ')
    Q1=("select * from cafe_menu where i_name=%s")
    cu.execute(Q1,(n,))
    d=cu.fetchall()
    if n.lower()=='cancel':
        cafe_menu(x)
    elif n.lower() not in l:
        print()
        print("Please select a valid choice")
        cafe_menu(x)
    else:
        for i in d:
            p=i[3]
            Q2=("update usr_dat set tab=tab+%s where username=%s")
            cu.execute(Q2,(p,x))
            print('Enjoy your',n.title())
            mydb.commit()
    cafe_menu(x)

def u_main_menu(i):                    #Main menu for non-admins
    print()
    print('Loading...')
    print()
    time.sleep(1)
    print('Welcome',i,'''What would you like to do

    [1]CAFE MENU
    [2]ISSUE/RETURN BOOK
    [3]RENT/RETURN GAME
    [4]BOOK MOVIE HALL (PREMIUM FEATURE)
    [5]BOOK GAMING STATION (PREMIUM FEATURE)
    [6]PLANS
    [7]ABOUT ME
    [8]LOGOUT
    ''')
    Q=('select plan from usr_dat where username=%s')
    cu.execute(Q,(i,))
    d=cu.fetchone()
    pla=d[0]
    n=int(input('Enter your choice: '))
    if n==1:
        print()
        cafe_menu(i)
    elif n==2:
        print()
        bk_menu(i)
    elif n==3:
        print()
        gam_menu(i)
    elif n==4:
        print()
        if pla.lower()=='premium':
            mov_menu(i)
        else:
            print('Upgrade to premium to access movie halls') 
            u_main_menu(i)
    elif n==5:
        print()
        if pla.lower()=='premium':
            gst_menu(i)
        else:
            print('Upgrade to premium to access gaming station')
            u_main_menu(i)
    elif n==6:
        print()
        plans(i)
    elif n==7:
        print()
        print('ABOUT YOU')
        print()
        det(i)
    elif n==8:
        Q=('select tab from usr_dat where username=%s')
        cu.execute(Q,(i,))
        d=cu.fetchone()
        p=d[0]
        if p==0:
            print('Logging out...')
            time.sleep(1)
            main_menu()
        else:
            pay(i)
    else:
        print('Enter a valid choice')

def check_aoru(x,y):                   #Function to check if user is admin or not
    if x=='admin':
        a_main_menu(y)
    elif x=='user':
        u_main_menu(y)
    else:
        print('?')

def gam_menu(x):                       #Game menu
    print('''
    RENT/RETURN GAMES

    [1] View games
    [2] Rent a game
    [3] Return a game
    [4] BACK
    ''')
    n=int(input('Enter your option: '))
    if n==1:
        print()
        print('LIST OF GAMES')
        gam_disp(x)
    elif n==2:
        print()
        gam_rent(x)
    elif n==3:
        Q=('select rnt_gam from usr_dat where username=%s')
        cu.execute(Q,(x,))
        d=cu.fetchone()
        if d[0]=='None':
            print()
            print("Rent a game first")
            gam_menu(x)
        else:
            print()
            print('RETURN CURRENTLY ISSUED GAME')
            print()
            ck=input('Are you sure you want to return the game (yes/no): ')
            if ck.lower()=='yes':
                Q0=('select * from usr_dat where username=%s')
                cu.execute(Q0,(x,))
                dd=cu.fetchone()
                g=dd[6]
                Q1=("update usr_dat set rnt_gam=0 where username=%s")
                cu.execute(Q1,(x,))
                Q2=("update gam_rec set avail='Yes' where s_no=%s")
                cu.execute(Q2,(g,))
                mydb.commit()
                print()
                print('Thank you for returning the game!')
            elif ck.lower()=='no':
                print('Enjoy your game!')
            else:
                print("Answer in yes or no")
            time.sleep(1)
            gam_menu(x)
    elif n==4:
        u_main_menu(x)
    else:
        print('Enter a valid choice')
        time.sleep(1)
        gam_menu(x)
def gam_disp(x):                       #Function to display list of games
    cu.execute('select * from gam_rec')
    dat=cu.fetchall()
    gam_list(dat)
    filter(x)
def filter(x):                         #Function to filter list of games
    print('''
    Filter/Sort by
    [1]Default
    [2]Name
    [3]Genre
    [4]Available
    [5]Price(Low to High)
    [6]Price(High to Low)
    [7]A -> Z
    [8]Z -> A
    [9]BACK
    ''')
    n=int(input('Enter filter number: '))
    if n==1:
        cu.execute('select * from gam_rec')
        dat=cu.fetchall()
        gam_list(dat)
    elif n==2:
        f=input('Enter the name of the game: ')+'%'
        Q=("select * from gam_rec where g_name like %s")
        cu.execute(Q,(f,))
        d=cu.fetchall()
        gam_list(d)
    elif n==3:
        f=input('Enter the genre of the game: ')+'%'
        Q=("select * from gam_rec where genre like %s")
        cu.execute(Q,(f,))
        d=cu.fetchall()
        gam_list(d)
    elif n==4:
        cu.execute("select * from gam_rec where avail='Yes'")
        d=cu.fetchall()
        gam_list(d)
    elif n==5:
        cu.execute("select * from gam_rec order by price ASC")
        d=cu.fetchall()
        gam_list(d)
    elif n==6:
        cu.execute("select * from gam_rec order by price DESC")
        d=cu.fetchall()
        gam_list(d)
    elif n==7:
        cu.execute("select * from gam_rec order by g_name ASC")
        d=cu.fetchall()
        gam_list(d)
    elif n==8:
        cu.execute("select * from gam_rec order by g_name DESC")
        d=cu.fetchall()
        gam_list(d)
    elif n==9:
        gam_menu(x)
    else:
        print("Enter a valid option")
        gam_disp(x)
    filter(x)
def gam_list(dat):                     #List of games
    gap=' '*3
    head=f"{'Serial No':10s}{gap}{'Name':30s}{gap}{'Developer':20s}{gap}{'Genre':15s}{gap}{'Price(weekly)(₹)':16s}{gap}{'Availablity':3s}"
    print('='*118)
    print(head)
    print('-'*118)
    for i in dat:
        r=f"{i[0]:10d}{gap}{i[1]:30s}{gap}{i[2]:20s}{gap}{i[3]:15s}{gap}{i[4]:16d}{gap}{i[5]:3s}"
        print(r)
    print('-'*118)
def gam_rent(x):                       #Function to rent games
    Q='select * from usr_dat where username=%s'
    cu.execute(Q,(x,))
    da=cu.fetchone()
    if da[6]!=0:
        print()
        print('Please return your currently rented game before renting another')
        time.sleep(1)
        gam_menu(x)
    else:
        print('AVAILABLE GAMES TO RENT')
        cu.execute("select * from gam_rec where avail='Yes'")
        dat=cu.fetchall()
        gam_list(dat)
        print()
        l=[]
        n=input('Know which game you want to rent?(yes/no): ')
        if n.lower()=='yes':
            print()
            cu.execute("select * from gam_rec where avail='Yes'")
            de=cu.fetchall()
            for i in de:
                l.append(i[0])
            sg=int(input('Alright! Enter the Serial No of the game you want to rent: '))
            if sg in l:
                Q1=("update gam_rec set avail='No' where s_no=%s")
                cu.execute(Q1,(sg,))
                Q2=("update usr_dat set rnt_gam=%s where username=%s")
                cu.execute(Q2,(sg,x))
                Q2_5=('select * from gam_rec where s_no=%s')
                cu.execute(Q2_5,(sg,))
                dd=cu.fetchone()
                p=dd[4]
                Q3=("update usr_dat set tab=tab+%s where username=%s")
                cu.execute(Q3,(p,x))
                mydb.commit()
                print('''
                Enjoy your game!
                Don't forget to return it once your done!''')
                time.sleep(1)
                gam_menu(x)
            else:
                print('Enter a valid available game')
                time.sleep(1)
                gam_rent(x)
        elif n.lower()=='no':
            print()
            print('Check our list of games to get a better idea!')
            time.sleep(1)
            print()
            gam_disp(x)
        else:
            print()
            print('Please answer in yes or no')
            print()
            time.sleep(1)
            gam_rent(x)

def bk_menu(x):                        #Book menu
    print('''
    ISSUE/RETURN BOOKS

    [1] View books
    [2] Issue a book
    [3] Return a book
    [4] BACK
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        print()
        print('LIST OF BOOKS')
        bk_disp(x)
    elif n==2:
        print()
        bk_iss(x)
    elif n==3:
        Q=('select iss_bk from usr_dat where username=%s')
        cu.execute(Q,(x,))
        d=cu.fetchone()
        if d[0]=='None':
            print()
            print("Issue a book before returning")
            bk_menu(x)
        else:
            print()
            print('RETURN CURRENTLY ISSUED BOOK')
            print()
            ck=input('Are you sure you want to return the book (yes/no): ')
            if ck.lower()=='yes':
                Q0=('select * from usr_dat where username=%s')
                cu.execute(Q0,(x,))
                dd=cu.fetchone()
                g=dd[5]
                Q1=("update usr_dat set iss_bk=0 where username=%s")
                cu.execute(Q1,(x,))
                Q2=("update bk_rec set b_avail='Yes' where b_no=%s")
                cu.execute(Q2,(g,))
                mydb.commit()
                print()
                print('Thank you for returning the book!')
            elif ck.lower()=='no':
                print('Enjoy your book!')
            else:
                print("Answer in yes or no")
            time.sleep(1)
            bk_menu(x)
    elif n==4:
        u_main_menu(x)
    else:
        print('Enter a valid choice')
        time.sleep(1)
        bk_menu(x)
def bk_disp(x):                        #Function to display list of books
    cu.execute('select * from bk_rec')
    dat=cu.fetchall()
    bk_list(dat)
    bk_filter(x)
def bk_list(dat):                      #List of books
    gap=' '*3
    head=f"{'Serial No':10s}{gap}{'Name':50s}{gap}{'Author':20s}{gap}{'Genre':15s}{gap}{'Availablity':3s}"
    print('='*118)
    print(head)
    print('-'*118)
    for i in dat:
        r=f"{i[0]:10d}{gap}{i[1]:50s}{gap}{i[2]:20s}{gap}{i[3]:15s}{gap}{gap}{i[4]:3s}"
        print(r)
    print('-'*118)
def bk_filter(x):                      #Function to filter list of books
    print('''
    Filter/Sort by
    [1]Default
    [2]Name
    [3]Genre
    [4]Available
    [6]A -> Z
    [7]Z -> A
    [8]BACK
    ''')
    n=int(input('Enter filter number: '))
    if n==1:
        cu.execute('select * from bk_rec')
        dat=cu.fetchall()
        bk_list(dat)
    elif n==2:
        f=input('Enter the name of the book: ')+'%'
        Q=("select * from bk_rec where b_name like %s")
        cu.execute(Q,(f,))
        d=cu.fetchall()
        bk_list(d)
    elif n==3:
        f=input('Enter the genre of the book: ')+'%'
        Q=("select * from bk_rec where genre like %s")
        cu.execute(Q,(f,))
        d=cu.fetchall()
        bk_list(d)
    elif n==4:
        cu.execute("select * from bk_rec where b_avail='Yes'")
        d=cu.fetchall()
        bk_list(d)
    elif n==6:
        cu.execute("select * from bk_rec order by b_name ASC")
        d=cu.fetchall()
        bk_list(d)
    elif n==7:
        cu.execute("select * from bk_rec order by b_name DESC")
        d=cu.fetchall()
        bk_list(d)
    elif n==8:
        bk_menu(x)
    else:
        print("Enter a valid option")
        bk_disp(x)
    bk_filter(x)
def bk_iss(x):                         #Function to issue book
    Q='select * from usr_dat where username=%s'
    cu.execute(Q,(x,))
    da=cu.fetchone()
    if da[5]!=0:
        print()
        print('Please return your currently issued book before renting another')
        time.sleep(1)
        bk_menu(x)
    else:
        print('AVAILABLE BOOKS TO ISSUE')
        cu.execute("select * from bk_rec where b_avail='Yes'")
        dat=cu.fetchall()
        bk_list(dat)
        print()
        l=[]
        n=input('Know which book you want to issue?(yes/no): ')
        if n.lower()=='yes':
            print()
            cu.execute("select * from bk_rec where b_avail='Yes'")
            de=cu.fetchall()
            sg=int(input('Alright! Enter Serial No the book you want to issue: '))
            for i in de:
                l.append(i[0])
            if sg in l:
                Q1=("update bk_rec set b_avail='No' where b_no=%s")
                cu.execute(Q1,(sg,))
                Q2=("update usr_dat set iss_bk=%s where username=%s")
                cu.execute(Q2,(sg,x))
                mydb.commit()
                print('''
                Enjoy your book!
                Don't forget to return it once your done!''')
                time.sleep(1)
                bk_menu(x)
            else:
                print('Enter a valid available book')
                time.sleep(1)
                bk_iss(x)
        elif n.lower()=='no':
            print()
            print('Check our list of books to get a better idea!')
            time.sleep(1)
            print()
            bk_disp(x)
        else:
            print()
            print('Please answer in yes or no')
            print()
            time.sleep(1)
            bk_iss(x)

def mov_menu(x):                       #Movie hall menu
    print('''
    MOVIE HALL BOOKINGS

    [1]View the list of movie halls
    [2]Book a movie hall
    [3]End booking
    [4]Cancel booking
    [5]Back
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        print()
        print('LIST OF HALLS')
        mov_view(x)
    elif n==2:
        print()
        mov_book(x)
    elif n==3:
        Q=('select h_booked from usr_dat where username=%s')
        cu.execute(Q,(x,))
        d=cu.fetchone()
        if d[0]==0:
            print()
            print("You have no bookings")
            mov_menu(x)
        else:
            print()
            print('ENDING BOOKING')
            print()
            ck=input('Are you sure you want to end the booking (yes/no): ')
            if ck.lower()=='yes':
                Q0=('select * from usr_dat where username=%s')
                cu.execute(Q0,(x,))
                dd=cu.fetchone()
                g=dd[7]
                Q1=("update usr_dat set h_booked=0 where username=%s")
                cu.execute(Q1,(x,))
                Q2=("update mov_hall set h_avail='Yes' where h_no=%s")
                cu.execute(Q2,(g,))
                mydb.commit()
                print()
                print('Thank you for booking with us!')
            elif ck.lower()=='no':
                print('Enjoy your hall!')
            else:
                print("Answer in yes or no")
            time.sleep(1)
            mov_menu(x)
    elif n==4:
        Q=('select h_booked from usr_dat where username=%s')
        cu.execute(Q,(x,))
        d=cu.fetchone()
        if d[0]==0:
            print()
            print("You have no bookings")
            mov_menu(x)
        else:
            print()
            print('CANCELLING BOOKING')
            print()
            ck=input('Are you sure you want to cancel the booking (yes/no): ')
            if ck.lower()=='yes':
                Q0=('select * from usr_dat where username=%s')
                cu.execute(Q0,(x,))
                dd=cu.fetchone()
                g=dd[7]
                Q1=("update usr_dat set h_booked=0 where username=%s")
                cu.execute(Q1,(x,))
                Q2_5=('select * from mov_hall where h_no=%s')
                cu.execute(Q2_5,(g,))
                dd=cu.fetchone()
                p=dd[2]
                Q1_5=("update usr_dat set tab=tab-%s where username=%s")
                cu.execute(Q1_5,(p,x))
                Q2=("update mov_hall set h_avail='Yes' where h_no=%s")
                cu.execute(Q2,(g,))
                mydb.commit()
                print()
                print('Thank you for booking with us!')
            elif ck.lower()=='no':
                print('Enjoy your hall!')
            else:
                print("Answer in yes or no")
            time.sleep(1)
            mov_menu(x)
    elif n==5:
        u_main_menu(x)
def mov_view(x):                       #Function to display list of halls
    cu.execute('select * from mov_hall')
    dat=cu.fetchall()
    mov_list(dat)
    hall_filter(x)
def mov_list(dat):                     #List of halls
    gap=' '*3
    head=f"{'Hall Number':11s}{gap}{'Hall Type':9s}{gap}{'Pricing(Hourly)(₹)':18s}{gap}{'Availablity':12s}"
    print('='*59)
    print(head)
    print('-'*59)
    for i in dat:
        r=f"{i[0]:11d}{gap}{i[1]:9s}{gap}{i[2]:18d}{gap}{i[3]:12s}"
        print(r)
    print('-'*59)
def mov_book(x):                       #Function to book hall
    print('HALL BOOKINGS')
    Q='select * from usr_dat where username=%s'
    cu.execute(Q,(x,))
    da=cu.fetchone()
    if (da[7])!=0:
        print()
        print('You can only book one hall at a time')
        time.sleep(1)
        mov_menu(x)
    else:
        cu.execute("select * from mov_hall where h_avail='Yes'")
        dat=cu.fetchall()
        mov_list(dat)
        print()
        n=input('Know which hall you want to book?(yes/no): ')
        if n.lower()=='yes':
            print()
            hn=int(input('Alright! Enter the hall number want to book: '))
            Q1=("update mov_hall set h_avail='No' where h_no=%s")
            cu.execute(Q1,(hn,))
            Q2=("update usr_dat set h_booked=%s where username=%s")
            cu.execute(Q2,(hn,x))
            Q2_5=('select * from mov_hall where h_no=%s')
            cu.execute(Q2_5,(hn,))
            dd=cu.fetchone()
            p=dd[2]
            Q3=("update usr_dat set tab=tab+%s where username=%s")
            cu.execute(Q3,(p,x))
            mydb.commit()
            print('''
            Enjoy your time in the hall!''')
            time.sleep(1)
            mov_menu(x)
        elif n.lower()=='no':
            print()
            print('Check our list of halls to get a better idea!')
            time.sleep(1)
            print()
            mov_view(x)
        else:
            print()
            print('Please answer in yes or no')
            print()
            time.sleep(1)
            mov_book(x)
def hall_filter(x):                    #Function to filter list of halls
    print('''
    Filter/Sort by
    [1]Default
    [2]Type
    [3]Available
    [4]Price(Low to High)
    [5]Price(High to Low)
    [6]Back
    ''')
    n=int(input('Enter filer number: '))
    if n==1:
        mov_view(x)
    elif n==2:
        f=input('Enter the hall format: ')+'%'
        Q=("select * from mov_hall where h_type like %s")
        cu.execute(Q,(f,))
        d=cu.fetchall()
        mov_list(d)
    elif n==3:
        cu.execute("select * from mov_hall where h_avail='Yes'")
        d=cu.fetchall()
        mov_list(d)
    elif n==4:
        cu.execute("select * from mov_hall order by h_price ASC")
        d=cu.fetchall()
        mov_list(d)
    elif n==5:
        cu.execute("select * from mov_hall order by h_price DESC")
        d=cu.fetchall()
        mov_list(d)
    elif n==6:
        mov_menu(x)
    hall_filter(x)

def gst_menu(x):                       #Gaming station menu
    print('''
    GAMING STATION BOOKINGS

    [1]View the list of gaming stations
    [2]Book a gaming station
    [3]Cancel booking
    [4]End booking
    [5]Back
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        print()
        print('LIST OF STATIONS')
        gst_view(x)
    elif n==2:
        print()
        gst_book(x)
    elif n==3:
        Q=('select g_booked from usr_dat where username=%s')
        cu.execute(Q,(x,))
        d=cu.fetchone()
        if d[0]=='0':
            print()
            print("You have no bookings")
            gst_menu(x)
        else:
            print()
            print('CANCELLING BOOKING')
            print()
            ck=input('Are you sure you want to end the booking (yes/no): ')
            if ck.lower()=='yes':
                Q0=('select * from usr_dat where username=%s')
                cu.execute(Q0,(x,))
                dd=cu.fetchone()
                g=dd[8]
                Q1=("update usr_dat set g_booked=0 where username=%s")
                cu.execute(Q1,(x,))
                Q2_5=('select * from gam_st where g_no=%s')
                cu.execute(Q2_5,(g,))
                dd=cu.fetchone()
                p=dd[2]
                Q1_5=("update usr_dat set tab=tab-%s where username=%s")
                cu.execute(Q1_5,(p,x))
                Q2=("update gam_st set g_avail='Yes' where g_no=%s")
                cu.execute(Q2,(g,))
                mydb.commit()
                print()
                print('Thank you for booking with us!')
            elif ck.lower()=='no':
                print('Enjoy your station!')
            else:
                print("Answer in yes or no")
            time.sleep(1)
            gst_menu(x)
    elif n==4:
        Q=('select g_booked from usr_dat where username=%s')
        cu.execute(Q,(x,))
        d=cu.fetchone()
        if d[0]==0:
            print()
            print("You have no bookings")
            mov_menu(x)
        else:
            print()
            print('ENDING BOOKING')
            print()
            ck=input('Are you sure you want to end the booking (yes/no): ')
            if ck.lower()=='yes':
                Q0=('select * from usr_dat where username=%s')
                cu.execute(Q0,(x,))
                dd=cu.fetchone()
                g=dd[8]
                Q1=("update usr_dat set g_booked=0 where username=%s")
                cu.execute(Q1,(x,))
                Q2=("update mov_hall set g_avail='Yes' where g_no=%s")
                cu.execute(Q2,(g,))
                mydb.commit()
                print()
                print('Thank you for booking with us!')
            elif ck.lower()=='no':
                print('Enjoy your gaming session!')
            else:
                print("Answer in yes or no")
            time.sleep(1)
            gst_menu(x)
    elif n==5:
        u_main_menu(x)
def gst_view(x):                       #Function to list gaming stations
    cu.execute('select * from gam_st')
    dat=cu.fetchall()
    gst_list(dat)
    st_filter(x)
def gst_list(dat):                     #List of gaming stations
    gap=' '*3
    head=f"{'Station Number':14s}{gap}{'Station Type':12s}{gap}{'Pricing(Hourly)(₹)':18s}{gap}{'Availablity':12s}"
    print('='*65)
    print(head)
    print('-'*65)
    for i in dat:
        r=f"{i[0]:14d}{gap}{i[1]:12s}{gap}{i[2]:18d}{gap}{i[3]:12s}"
        print(r)
    print('-'*65)
def gst_book(x):                       #Function to book gaming station
    print('STATION BOOKINGS')
    Q='select * from usr_dat where username=%s'
    cu.execute(Q,(x,))
    da=cu.fetchone()
    if (da[7])!=0:
        print()
        print('You can only book one station at a time')
        time.sleep(1)
        gst_menu(x)
    else:
        cu.execute("select * from gam_st where g_avail='Yes'")
        dat=cu.fetchall()
        gst_list(dat)
        print()
        n=input('Know which station you want to book?(yes/no): ')
        if n.lower()=='yes':
            print()
            hn=int(input('Alright! Enter the station number want to book: '))
            Q1=("update gam_st set g_avail='No' where g_no=%s")
            cu.execute(Q1,(hn,))
            Q2=("update usr_dat set g_booked=%s where username=%s")
            cu.execute(Q2,(hn,x))
            Q2_5=('select * from gam_st where g_no=%s')
            cu.execute(Q2_5,(hn,))
            dd=cu.fetchone()
            p=dd[2]
            Q3=("update usr_dat set tab=tab+%s where username=%s")
            cu.execute(Q3,(p,x))
            mydb.commit()
            print('''
            Enjoy your gaming station!''')
            time.sleep(1)
            gst_menu(x)
        elif n.lower()=='no':
            print()
            print('Check our list of stations to get a better idea!')
            time.sleep(1)
            print()
            gst_view(x)
        else:
            print()
            print('Please answer in yes or no')
            print()
            time.sleep(1)
            gst_book(x)
def st_filter(x):                      #Function to filter list of halls
    print('''
    Filter/Sort by
    [1]Default
    [2]Type
    [3]Available
    [4]Price(Low to High)
    [5]Price(High to Low)
    [6]Back
    ''')
    n=int(input('Enter filer number: '))
    if n==1:
        gst_view(x)
    elif n==2:
        f=input('Enter the hall format: ')+'%'
        Q=("select * from gam_st where g_type like %s")
        cu.execute(Q,(f,))
        d=cu.fetchall()
        gst_list(d)
    elif n==3:
        cu.execute("select * from gam_st where g_avail='Yes'")
        d=cu.fetchall()
        gst_list(d)
    elif n==4:
        cu.execute("select * from gam_st order by g_price ASC")
        d=cu.fetchall()
        gst_list(d)
    elif n==5:
        cu.execute("select * from gam_st order by g_price DESC")
        d=cu.fetchall()
        gst_list(d)
    elif n==6:
        gst_menu(x)
    st_filter(x)

def det(x):                            #Function to display details about user
    Q=('select * from usr_dat where username=%s')
    cu.execute(Q,(x,))
    d=cu.fetchall()
    gap='|'
    head=f"{'Acc No':6s}{gap}{'Username':15s}{gap}{'Pending Tab':11s}{gap}{'Issued Book':25s}{gap}{'Rented Game':25s}{gap}{'Booked station':25s}{gap}{'Booked hall':11s}{gap}"
    print('='*125)
    print(head)
    print('-'*125)
    for i in d:
        r=f"{i[0]:6d}{gap}{i[1]:15s}{gap}{i[4]:11d}{gap}{i[5]:25d}{gap}{i[6]:25d}{gap}{i[7]:25d}{gap}{i[8]:11d}{gap}"
        print(r)
    print('-'*125)
    u_main_menu(x)

def cafe_view():                       #Viewing the cafe menu
    cu.execute("select * from cafe_menu")
    dat=cu.fetchall()
    gap=' '*3
    head=f"{'Item type':15s}{gap}{'Item name':30s}{gap}{'Price':4s}"
    print('='*57)
    print(head)
    print('-'*57)
    for i in dat:
        r=f"{i[1]:15s}{gap}{i[2]:30s}{gap}{i[3]:4d}"
        print(r)
    print('-'*57)
def cafe_e(x):                         #Function to edit cafe menu
    print('''
    [1] ADD ITEMS
    [2] DELETE ITEMS
    [3] MODIFY ITEMS
    [4] VIEW CAFE MENU
    [5] BACK
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        l=[]
        cu.execute('select * from cafe_menu')
        dat=cu.fetchall()
        for i in dat:
            l.append(i[0])
        sno=max(l)+1
        print('ADDING ITEMS')
        print()
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter type of item: ')
        if a.lower()=='cancel':
            cafe_e(x)
        else:
            b=input('Enter name of item: ')
            c=int(input('Enter price of item: '))
            Q1="insert into cafe_menu values(%s,%s,%s,%s)"
            cu.execute(Q1,(sno,a,b,c))
            print('Item added successfully')
    elif n==2:
        print('DELETING ITEMS')
        print()
        cafe_view()
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of item you want to delete: ')
        if a.lower()=='cancel':
            cafe_e(x)
        else:
            con=input('Are you sure you want to delete this item? (yes/no): ')
            if con.lower()=='yes':
                Q1="delete from cafe_menu where i_name=%s"
                cu.execute(Q1,(a,))
                print('Deleted item successfully')
            elif con.lower()=='no':
                print('Alright!')
            else:
                print('Answer in yes or no')
    elif n==3:
        print('MODIFYING ITEMS')
        print()
        cafe_view()
        l=[]
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of item you want to modify: ')
        if a.lower()=='cancel':
            cafe_e(x)
        else:
            cu.execute('select i_name from cafe_menu')
            d=cu.fetchall()
            for i in d:
                l.append(i[0].lower())
            if a in l:
                x=input('Enter new item type: ')
                y=input('Enter new item name: ')
                z=int(input('Enter new item price: '))
                Q2=('update cafe_menu set i_type=%s,i_name=%s,price=%s where i_name=%s')
                cu.execute(Q2,(x,y,z,a))
            else:
                print('Enter an existing item to edit')
    elif n==4:
        cafe_view()
    elif n==5:
        a_main_menu(x)
    else:
        print('Enter a valid choice')
        cafe_e(x)
    mydb.commit()
    cafe_e(x)

def book_e(x):                         #Function to edit book list
    print('''
    [1] ADD BOOKS
    [2] DELETE BOOKS
    [3] MODIFY BOOKS
    [4] VIEW LIST OF BOOKS
    [5] BACK
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        l=[]
        cu.execute('select * from bk_rec')
        dat=cu.fetchall()
        for i in dat:
            l.append(i[0])
        sno=max(l)+1
        print('ADDING BOOKS')
        print()
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of book: ')
        if a.lower()=='cancel':
            book_e(x)
        else:
            b=input('Enter name of author: ')
            c=input('Enter genre of book: ')
            Q1="insert into bk_rec values(%s,%s,%s,%s,'Yes')"
            cu.execute(Q1,(sno,a,b,c))
            print('Book added successfully')
    elif n==2:
        print('DELETING BOOKS')
        print()
        cu.execute('select * from bk_rec')
        d=cu.fetchall()
        bk_list(d)
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of book you want to delete: ')
        if a.lower()=='cancel':
            book_e(x)
        else:
            k=[]
            cu.execute('select b_name from bk_rec')
            d=cu.fetchall()
            for i in d:
                k.append(i[1].lower())
            if a in k:
                con=input('Are you sure you want to delete this book? (yes/no): ')
                if con.lower()=='yes':
                    Q1="delete from bk_rec where b_name=%s"
                    cu.execute(Q1,(a,))
                    print('Deleted book successfully')
                elif con.lower()=='no':
                    print('Alright!')
                else:
                    print('Answer in yes or no')
            else:
                print()
                print('Enter a valid book name')
    elif n==3:
        print('MODIFYING BOOKS')
        print()
        cu.execute('select * from bk_rec')
        d=cu.fetchall()
        bk_list(d)
        l=[]
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of book you want to modify: ')
        if a.lower()=='cancel':
            book_e(x)
        else:
            cu.execute('select b_name from bk_rec')
            d=cu.fetchall()
            for i in d:
                l.append(i[0].lower())
            if a in l:
                x=input('Enter new book name: ')
                y=input('Enter new author name: ')
                z=input('Enter new book genre: ')
                Q2=('update bk_rec set b_name=%s,a_name=%s,genre=%s where b_name=%s')
                cu.execute(Q2,(x,y,z,a))
                print("Updated details successfully!")
            else:
                print('Enter an existing book to edit')
    elif n==4:
        cu.execute('select * from bk_rec')
        d=cu.fetchall()
        bk_list(d)
    elif n==5:
        a_main_menu(x)
    else:
        print('Enter a valid choice')
        book_e(x)
    mydb.commit()
    book_e(x)

def gam_e(x):                          #Function to edit game list
    print('''
    [1] ADD GAMES
    [2] DELETE GAMES
    [3] MODIFY GAMES
    [4] VIEW LIST OF GAMES
    [5] BACK
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        l=[]
        cu.execute('select * from gam_rec')
        dat=cu.fetchall()
        for i in dat:
            l.append(i[0])
        sno=max(l)+1
        print('ADDING GAMES')
        print()
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of game: ')
        if a.lower()=='cancel':
            gam_e(x)
        else:
            b=input('Enter name of developer: ')
            c=input('Enter genre of game: ')
            d=(input('Enter price of game: '))
            Q1="insert into gam_rec values(%s,%s,%s,%s,%s,'Yes')"
            cu.execute(Q1,(sno,a,b,c,d))
            print('Game added successfully')
    elif n==2:
        print('DELETING GAMES')
        print()
        cu.execute('select * from gam_rec')
        d=cu.fetchall()
        gam_list(d)
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of game you want to delete: ')
        if a.lower()=='cancel':
            gam_e(x)
        else:
            k=[]
            cu.execute('select g_name from gam_rec')
            d=cu.fetchall()
            for i in d:
                k.append(i[1].lower())
            if a in k:
                con=input('Are you sure you want to delete this game? (yes/no): ')
                if con.lower()=='yes':
                    Q1="delete from gam_rec where g_name=%s"
                    cu.execute(Q1,(a,))
                    print('Deleted game successfully')
                elif con.lower()=='no':
                    print('Alright!')
                else:
                    print('Answer in yes or no')
            else:
                print()
                print('Enter a valid game')
    elif n==3:
        print('MODIFYING GAMES')
        print()
        cu.execute('select * from gam_rec')
        d=cu.fetchall()
        gam_list(d)
        l=[]
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter name of game you want to modify: ')
        if a.lower()=='cancel':
            gam_e(x)
        else:
            cu.execute('select g_name from gam_rec')
            d=cu.fetchall()
            for i in d:
                l.append(i[0].lower())
            if a in l:
                x=input('Enter new game name: ')
                y=input('Enter new developer name: ')
                z=input('Enter new game genre: ')
                xx=int(input('Enter new game price: '))
                Q2=('update gam_rec set g_name=%s,dev_name=%s,genre=%s,price=%s where g_name=%s')
                cu.execute(Q2,(x,y,z,xx,a))
                print("Updated details successfully!")
            else:
                print('Enter an existing game to edit')
    elif n==4:
        cu.execute('select * from gam_rec')
        d=cu.fetchall()
        gam_list(d)
    elif n==5:
        a_main_menu(x)
    else:
        print('Enter a valid choice')
        gam_e(x)
    mydb.commit()
    gam_e(x)

def gst_e(x):                          #Function to edit gaming station list
    print('''
    [1] ADD GAME STATIONS
    [2] DELETE GAME STATIONS
    [3] MODIFY GAME STATIONS
    [4] VIEW LIST OF GAME STATIONS
    [5] BACK
    ''')
    n=int(input('Enter your choice: '))
    l=[]
    cu.execute('select * from gam_st')
    dat=cu.fetchall()
    for i in dat:
        l.append(i[0])
    if n==1:
        sno=max(l)+1
        print('ADDING GAME STATIONS')
        print()
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter type of game station: ')
        if a.lower()=='cancel':
            gst_e(x)
        else:
            b=int(input('Enter price of game station: '))
            Q1="insert into gam_st values(%s,%s,%s,'Yes')"
            cu.execute(Q1,(sno,a,b))
            print('Game station added successfully')
    elif n==2:
        print('DELETING GAME STATIONS')
        print()
        cu.execute('select * from gam_st')
        d=cu.fetchall()
        gst_list(d)
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter station number of game station you want to delete: ')
        if a.lower()=='cancel':
            gst_e(x)
        else:
            aa=int(a)
            if aa in l:
                con=input('Are you sure you want to delete this game station? (yes/no): ')
                if con.lower()=='yes':
                    Q1="delete from gam_st where g_no=%s"
                    cu.execute(Q1,(aa,))
                    print('Deleted game station successfully')
                elif con.lower()=='no':
                    print('Alright!')
                else:
                    print('Answer in yes or no')
            else:
                print()
                print('Enter a valid station number')
    elif n==3:
        print('MODIFYING GAME STATIONS')
        print()
        cu.execute('select * from gam_st')
        d=cu.fetchall()
        gst_list(d)
        l=[]
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter station number of game station you want to modify: ')
        if a.lower()=='cancel':
            gst_e(x)
        else:
            aa=int(a)
            cu.execute('select g_no from gam_st')
            d=cu.fetchall()
            for i in d:
                l.append(i[0])
            if aa in l:
                x=input('Enter new game station type: ')
                y=int(input('Enter new game station price: '))
                Q2=('update gam_st set g_type=%s,g_price=%s where g_no=%s')
                cu.execute(Q2,(x,y,aa))
                print("Updated details successfully!")
            else:
                print('Enter an existing game station to edit')
    elif n==4:
        cu.execute('select * from gam_st')
        d=cu.fetchall()
        gst_list(d)
    elif n==5:
        a_main_menu(x)
    else:
        print('Enter a valid choice')
        gst_e(x)
    mydb.commit()
    gst_e(x)

def mov_e(x):                          #Function to edit movie hall list
    print('''
    [1] ADD MOVIE HALL
    [2] DELETE MOVIE HALL
    [3] MODIFY MOVIE HALL
    [4] VIEW LIST OF MOVIE HALL
    [5] BACK
    ''')
    n=int(input('Enter your choice: '))
    l=[]
    cu.execute('select * from mov_hall')
    dat=cu.fetchall()
    for i in dat:
        l.append(i[0])
    if n==1:
        sno=max(l)+1
        print('ADDING MOVIE HALLS')
        print()
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter type of movie hall: ')
        if a.lower()=='cancel':
            mov_e(x)
        else:
            b=int(input('Enter price of mov hall: '))
            Q1="insert into mov_hall values(%s,%s,%s,'Yes')"
            cu.execute(Q1,(sno,a,b))
            print()
            print('Movie hall added successfully')
    elif n==2:
        print('DELETING MOVIE HALLS')
        print()
        cu.execute('select * from mov_hall')
        d=cu.fetchall()
        mov_list(d)
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter hall number of movie hall you want to delete: ')
        if a.lower()=='cancel':
            mov_e(x)
        else:
            aa=int(a)
            if aa in l:
                con=input('Are you sure you want to delete this movie hall? (yes/no): ')
                if con.lower()=='yes':
                    Q1="delete from mov_hall where h_no=%s"
                    cu.execute(Q1,(aa,))
                    print()
                    print('Deleted movie hall successfully')
                elif con.lower()=='no':
                    print('Alright!')
                else:
                    print('Answer in yes or no')
            else:
                print()
                print('Enter a valid hall number: ')
    elif n==3:
        print('MODIFYING MOVIE HALLS')
        print()
        cu.execute('select * from mov_hall')
        d=cu.fetchall()
        mov_list(d)
        l=[]
        print('Enter cancel if you wish to cancel')
        print()
        a=input('Enter hall number of movie hall you want to modify: ')
        if a.lower()=='cancel':
            mov_e(x)
        else:
            aa=int(a)
            cu.execute('select h_no from mov_hall')
            d=cu.fetchall()
            for i in d:
                l.append(i[0])
            if aa in l:
                x=input('Enter new movie hall type: ')
                y=int(input('Enter new movie hall price: '))
                Q2=('update mov_hall set h_type=%s,h_price=%s where h_no=%s')
                cu.execute(Q2,(x,y,aa))
                print("Updated details successfully!")
            else:
                print('Enter an existing movie hall to edit')
    elif n==4:
        cu.execute('select * from mov_hall')
        d=cu.fetchall()
        mov_list(d)
    elif n==5:
        a_main_menu(x)
    else:
        print('Enter a valid choice')
        mov_e(x)
    mydb.commit()
    mov_e(x)

def plans(x):                          #Function to pay pending tab
    print('''
    PLANS

    [1] DETAILS OF PLANS
    [2] BASIC - - - - ₹399 per month
    [3] PREMIUM - - - ₹699 per month
    [4] BACK
    ''')
    Q=('select plan from usr_dat where username=%s')
    cu.execute(Q,(x,))
    d=cu.fetchone()
    p=d[0]
    print('Your currently have the',p,'plan')
    print()
    n=int(input('Enter your choice of plan: '))
    if n==1:
        print('-'*46)
        gap='|'
        head=f"{gap}{'':22s}{gap}{'  Basic':9s}{gap}{'  Premium':11s}{gap}"
        print(head)
        print(f"{gap}{'-'*22}{gap}{'-'*9}{gap}{'-'*11}{gap}")
        c=f"{gap}{'Cafe access':22s}{gap}{'    ✓':9s}{gap}{'     ✓':11s}{gap}"
        b=f"{gap}{'Library access':22s}{gap}{'    ✓':9s}{gap}{'     ✓':11s}{gap}"
        g=f"{gap}{'Games access':22s}{gap}{'    ✓':9s}{gap}{'     ✓':11s}{gap}"
        m=f"{gap}{'Movie Hall access':22s}{gap}{'    X':9s}{gap}{'     ✓':11s}{gap}"
        gst=f"{gap}{'Gaming Station access':22s}{gap}{'    X':9s}{gap}{'     ✓':11s}{gap}"
        print(c)
        print(b)
        print(g)
        print(m)
        print(gst)
        print('-'*46)
    elif n==2:
        i=input('Are you sure you want to select the basic plan (yes/no)?: ')
        if i.lower()=='yes':
            Q=("update usr_dat set plan='Basic' where username=%s")
            cu.execute(Q,(x,))
            print('Selected Basic plan successfully')
        elif n.lower()=='no':
            plans(x)
        else:
            print('Please enter a valid choice')
    elif n==3:
        i=input('Are you sure you want to select the premium plan (yes/no)?: ')
        if i.lower()=='yes':
            Q=("update usr_dat set plan='Premium' where username=%s")
            cu.execute(Q,(x,))
            print('Selected Premium plan successfully')
        elif n.lower()=='no':
            plans(x)
        else:
            print('Please enter a valid choice')
    elif n==4:
        u_main_menu(x)
    else:
        print('Please enter a valid choice')
    mydb.commit()
    plans(x)

def pay(x):                            #Function for payment
    print('''
    Please pay before you leave

    [1] PAY
    [2] GO BACK TO MENU
    ''')
    Q=('select tab from usr_dat where username=%s')
    cu.execute(Q,(x,))
    d=cu.fetchone()
    p=d[0]
    print('Current pending amount to pay: ')
    print('\t'+str(p))
    print()
    n=int(input('Enter your choice: '))
    if n==1:
        print('PAYING...')
        time.sleep(1)
        Q1=('update usr_dat set tab=0 where username=%s')
        cu.execute(Q1,(x,))
        print('Payment successful')
        mydb.commit()
        u_main_menu(x)
    elif n==2:
        u_main_menu(x)
    else:
        print('Enter a valid choice: ')
        pay(x)

def login():                           #Login function
    l=[]
    u=input('Enter your username: ')
    cu.execute('select * from usr_dat')
    dat=cu.fetchall()
    for i in dat:
        l.append(i[1])
    for i in dat:
        if u==i[1]:
            p=pwinput.pwinput('Enter your password: ')
            if p==i[2]:
                check_aoru(i[3],i[1])
            else:
                print('Wrong password. Try again')
                login()
            
        if u not in l:
            print('User not found. Enter a valid username')
            login()

def main_menu():                       #Main Menu for entire application
    print('''
    -=+=-=+=-MAIN MENU-=+=-=+=-
    |                         |
    |       [1]REGISTER       |
    |       [2]LOGIN          |
    |       [3]QUIT           |
    |                         |
    -=+=-=+=--=+=-=+=--=+=-=+=-
    ''')
    n=int(input('Enter your choice: '))
    if n==1:
        print('-=+=-=+=-REGISTER-=+=-=+=-')
        print()
        register()
    elif n==2:
        print('-=+=-=+=-LOGIN-=+=-=+=-')
        print()
        login()
    elif n==3:
        print()
        print('Goodbye, hope to see you soon :)')
        print()
        quit()
    else:
        print('Please enter a valid choice')
        main_menu()

main_menu()
