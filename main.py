import numpy as np
import pandas as pd
from tkinter import *
import tkinter.ttk

from IPython.core.display import display

import KDDataProcess as KDP
import arenav4
from tkinter import messagebox


def errorMessage(errorString):
    messagebox.showinfo(errorString, errorString)  # 메시지 박스를 띄운다.


def validateInputs():
    if myPoint.get() > 5000:
        errorMessage("myPoint error")

    if enPoint.get() > 5000:
        errorMessage("enPoint error")

    if enPower.get() < 300000:
        errorMessage("enPower error")

    if enPaper.get() > 13:
        errorMessage("enPaper error")


def predict():
    validateInputs()
    # print(str(eval(tMyPoint.get())))
    # print(myPoint.get())

    # 데이터 만들기
    X_test = pd.read_csv('arenaTestV4.CSV')
    # print(X_test)

    X_test['me'] = deckList.get()
    X_test['mypoint'] = myPoint.get()
    X_test['mypower'] = KDP.myPower[deckList.current()]
    X_test['enpoint'] = enPoint.get()
    X_test['enpower'] = enPower.get()
    X_test['paper'] = enPaper.get()

    inputDataFromGUIC = [deck1, deck2, deck3, deck4, deck5]
    columnsC = ['c1', 'c2', 'c3', 'c4', 'c5']
    inputDataFromGUIL = [star1, star2, star3, star4, star5]
    columnsL = ['l1', 'l2', 'l3', 'l4', 'l5']

    for (col, value) in zip(columnsC, inputDataFromGUIC):
        if value.get() == '':
            X_test[col] = np.nan
        else:
            X_test[col] = value.get()

    for (col, value) in zip(columnsL, inputDataFromGUIL):
        if value.get() == '' or value.get() == 0:
            X_test[col] = np.nan
        else:
            X_test[col] = int(value.get())

    global v3ResultOnMain  # = pd.read_csv('arenaTest.CSV')
    global v4ResultOnMain  # = pd.read_csv('arenaTestV4.CSV')
    global resultString

    v3ResultOnMain, v4ResultOnMain, resultString = arenav4.runV4(X_test) # , deckList.current())
    predictVar.set(resultString)

    bUpdateWin.configure(state='active')
    bUpdateLoose.configure(state='active')
    # print(X_test)


def updateResultWin():
    print("update result win")
    print(v3ResultOnMain)
    print(v4ResultOnMain)
    # display(v4ResultOnMain)
    KDP.addTestDataIntoTrainData(v4ResultOnMain, 'arenaDataV4.CSV', str(deckList.current()), 1, 4)
    KDP.addTestDataIntoTrainData(v3ResultOnMain, 'arenaDataV3.CSV', str(deckList.current()), 1, 3)
    bUpdateWin.configure(state='disabled')
    bUpdateLoose.configure(state='disabled')


def updateResultLoose():
    print("update result loose")
    print(v3ResultOnMain)
    print(v4ResultOnMain)
    KDP.addTestDataIntoTrainData(v4ResultOnMain, 'arenaDataV4.CSV', str(deckList.current()), 0, 4)
    KDP.addTestDataIntoTrainData(v3ResultOnMain, 'arenaDataV3.CSV', str(deckList.current()), 0, 3)
    bUpdateWin.configure(state='disabled')
    bUpdateLoose.configure(state='disabled')


# def updateArenaResult(winOrLoose):
#     print("update result " + str(winOrLoose))
#     # print(v4ResultOnMain)
#     KDP.addTestDataIntoTrainData(v4ResultOnMain, 'arenaDataV4.CSV', str(deckList.current()), winOrLoose, 4)
#     KDP.addTestDataIntoTrainData(v3ResultOnMain, 'arenaDataV3.CSV', str(deckList.current()), winOrLoose, 3)
#     bUpdateWin.configure(state='disabled')
#     bUpdateLoose.configure(state='disabled')


# def listSelected(event):
#     selectedDeck=deckList.current()
#     # print(selectedDeck[0])


def onArrowKey(event, limit, amount):
    newValue = 0

    if root.focus_get().get() == '':
        root.focus_get().delete(0, "end")
        root.focus_get().insert(0, str(newValue))

    if event.keysym == 'Up':
        newValue = int(root.focus_get().get()) + amount
        if int(root.focus_get().get()) >= limit:
            newValue = limit
    elif event.keysym == 'Down':
        newValue = int(root.focus_get().get()) - amount
        if int(root.focus_get().get()) <= limit:
            newValue = limit

    root.focus_get().delete(0, "end")
    root.focus_get().insert(0, str(newValue))


def setDefaultValue():
    lastData = pd.read_csv('arenaDataV4.CSV')
    lastRow = lastData.iloc[-1].fillna('')

    deckList.current(KDP.myDeck.index(lastRow['me']))
    deck1.set(lastRow['c1'])
    deck2.set(lastRow['c2'])
    deck3.set(lastRow['c3'])
    deck4.set(lastRow['c4'])
    deck5.set(lastRow['c5'])
    star1.set(2) #  int(lastRow['l1']))
    star2.set(2)
    star3.set(2)
    star4.set(2)
    star5.set(2)
    myPoint.set(lastRow['mypoint'])
    enPaper.set(lastRow['paper'])
    enPower.set(lastRow['enpower'])
    enPoint.set(lastRow['enpoint'])
    bUpdateWin.configure(state='disabled')
    bUpdateLoose.configure(state='disabled')


def on_focus_out_remove_next_value(event, levelWidget):
    if event.widget.get() == '':
        levelWidget.delete(0, 'end')


root = Tk()
root.title('Kingdom Arena')
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# 변수 정의
myPoint = IntVar()
selectedDeck = 0
# selectedDeck = StringVar()
enPoint = IntVar()
enPower = IntVar()
enPaper = IntVar()
deck1 = StringVar()
deck2 = StringVar()
deck3 = StringVar()
deck4 = StringVar()
deck5 = StringVar()
star1 = StringVar()
star2 = StringVar()
star3 = StringVar()
star4 = StringVar()
star5 = StringVar()
predictVar = StringVar()

# 내 데이터
lMyPoint = Label(root, text="내 트로피", width=10)
tMyPoint = Entry(root, width=4, textvariable=myPoint)


deckList = tkinter.ttk.Combobox(root, values=KDP.myDeck)
deckList.current(1)

# for i in KDP.myDeck:
#     deckList.insert(END, i)

# deckList.bind('<<ListboxSelect>>', listSelected)
# 상대 데이터
lEnPoint = Label(root, text="상대 트로피", width=8)
tEnPoint = Entry(root, width=6, textvariable=enPoint)
lEnPower = Label(root, text="상대 전투력")
tEnPower = Entry(root, width=6, textvariable=enPower)
lEnPaper = Label(root, text="상대 무공비")
tEnPaper = Entry(root, width=6, textvariable=enPaper)

# 상대 덱
lEn1 = Label(root, text="deck 1")
tEn1 = tkinter.ttk.Combobox(root, width=2, textvariable=deck1, values=KDP.enDeck)
tEn1.current(0)
lEn2 = Label(root, text="deck 2")
tEn2 = tkinter.ttk.Combobox(root, width=2, textvariable=deck2, values=KDP.enDeck)
tEn2.current(1)
lEn3 = Label(root, text="deck 3")
tEn3 = tkinter.ttk.Combobox(root, width=2, textvariable=deck3, values=KDP.enDeck)
tEn3.current(2)
lEn4 = Label(root, text="deck 4")
tEn4 = tkinter.ttk.Combobox(root, width=2, textvariable=deck4, values=KDP.enDeck)
tEn4.current(3)
lEn5 = Label(root, text="deck 5")
tEn5 = tkinter.ttk.Combobox(root, width=2, textvariable=deck5, values=KDP.enDeck)
tEn5.current(4)

# 상대 레벨
lEnStar1 = Label(root, text="Star 1")
tEnStar1 = Entry(root, width=2, textvariable=star1)
lEnStar2 = Label(root, text="Star 2")
tEnStar2 = Entry(root, width=2, textvariable=star2)
lEnStar3 = Label(root, text="Star 3")
tEnStar3 = Entry(root, width=2, textvariable=star3)
lEnStar4 = Label(root, text="Star 4")
tEnStar4 = Entry(root, width=2, textvariable=star4)
lEnStar5 = Label(root, text="Star 5")
tEnStar5 = Entry(root, width=2, textvariable=star5)

# 버튼
bRun = Button(root, text="예측", command=predict, width=5)
bUpdateWin = Button(root, text="승", command=updateResultWin, width=5)
bUpdateLoose = Button(root, text="패", command=updateResultLoose, width=5)

predictResult = Label(root, textvariable=predictVar, anchor='center')

# 구분선
sep1 = tkinter.ttk.Separator(root, orient="vertical")
sep2 = tkinter.ttk.Separator(root, orient="vertical")

# 배치
enCol1 = 3
enCol2 = 4
enCol3 = 5
enCol4 = 6

lMyPoint.grid(row=0, column=0, pady=12)
tMyPoint.grid(row=0, column=1)
deckList.grid(row=1, column=0, rowspan=7, columnspan=2, padx=12)
bRun.grid(row=8, column=0, padx=12, pady=12, columnspan=2)

sep1.grid(row=0, column=2, sticky='ns', rowspan=9, padx=12, pady=12)
sep2.grid(row=0, column=7, sticky='ns', rowspan=9, padx=12, pady=12)

lEnPoint.grid(row=0, column=enCol1, columnspan=2)
tEnPoint.grid(row=0, column=enCol3, columnspan=2)
lEnPower.grid(row=1, column=enCol1, columnspan=2)
tEnPower.grid(row=1, column=enCol3, columnspan=2)
lEnPaper.grid(row=2, column=enCol1, columnspan=2)
tEnPaper.grid(row=2, column=enCol3, columnspan=2)

lEn1.grid(row=3, column=enCol1)
lEn2.grid(row=4, column=enCol1)
lEn3.grid(row=5, column=enCol1)
lEn4.grid(row=6, column=enCol1)
lEn5.grid(row=7, column=enCol1)

lEnStar1.grid(row=3, column=enCol3)
lEnStar2.grid(row=4, column=enCol3)
lEnStar3.grid(row=5, column=enCol3)
lEnStar4.grid(row=6, column=enCol3)
lEnStar5.grid(row=7, column=enCol3)

tEn1.grid(row=3, column=enCol2)
tEnStar1.grid(row=3, column=enCol4)
tEn2.grid(row=4, column=enCol2)
tEnStar2.grid(row=4, column=enCol4)
tEn3.grid(row=5, column=enCol2)
tEnStar3.grid(row=5, column=enCol4)
tEn4.grid(row=6, column=enCol2)
tEnStar4.grid(row=6, column=enCol4)
tEn5.grid(row=7, column=enCol2)
tEnStar5.grid(row=7, column=enCol4, padx=12)

predictResult.grid(row=0, column=8, rowspan=9, padx=12)

# 키 바인드
tMyPoint.bind('<Up>', lambda event: onArrowKey(event, 3000, 1))
tMyPoint.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tMyPoint.bind('<Shift-Up>', lambda event: onArrowKey(event, 3000, 10))
tMyPoint.bind('<Shift-Down>', lambda event: onArrowKey(event, 0, 10))

tEnPoint.bind('<Up>', lambda event: onArrowKey(event, 3000, 1))
tEnPoint.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tEnPoint.bind('<Shift-Up>', lambda event: onArrowKey(event, 3000, 10))
tEnPoint.bind('<Shift-Down>', lambda event: onArrowKey(event, 0, 10))

tEnPower.bind('<Up>', lambda event: onArrowKey(event, 800000, 1))
tEnPower.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tEnPower.bind('<Shift-Up>', lambda event: onArrowKey(event, 800000, 100))
tEnPower.bind('<Shift-Down>', lambda event: onArrowKey(event, 0, 100))
tEnPower.bind('<Control-Shift-Up>', lambda event: onArrowKey(event, 800000, 1000))
tEnPower.bind('<Control-Shift-Down>', lambda event: onArrowKey(event, 0, 1000))

tEnPaper.bind('<Up>', lambda event: onArrowKey(event, 12, 1))
tEnPaper.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tEnStar1.bind('<Up>', lambda event: onArrowKey(event, 5, 1))
tEnStar1.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tEnStar2.bind('<Up>', lambda event: onArrowKey(event, 5, 1))
tEnStar2.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tEnStar3.bind('<Up>', lambda event: onArrowKey(event, 5, 1))
tEnStar3.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tEnStar4.bind('<Up>', lambda event: onArrowKey(event, 5, 1))
tEnStar4.bind('<Down>', lambda event: onArrowKey(event, 0, 1))
tEnStar5.bind('<Up>', lambda event: onArrowKey(event, 5, 1))
tEnStar5.bind('<Down>', lambda event: onArrowKey(event, 0, 1))

tEn1.bind("<FocusOut>", lambda event: on_focus_out_remove_next_value(event, tEnStar1))
tEn2.bind("<FocusOut>", lambda event: on_focus_out_remove_next_value(event, tEnStar2))
tEn3.bind("<FocusOut>", lambda event: on_focus_out_remove_next_value(event, tEnStar3))
tEn4.bind("<FocusOut>", lambda event: on_focus_out_remove_next_value(event, tEnStar4))
tEn5.bind("<FocusOut>", lambda event: on_focus_out_remove_next_value(event, tEnStar5))

bUpdateWin.grid(row=8, column=enCol1, columnspan=2)
bUpdateLoose.grid(row=8, column=enCol3, columnspan=2)

new_order = (tEn1, tEnStar1, tEn2, tEnStar2, tEn3, tEnStar3, tEn4, tEnStar4, tEn5, tEnStar5, bRun, bUpdateWin, bUpdateLoose)
for widget in new_order:
    widget.lift()

setDefaultValue()

tMyPoint.focus_set()
root.mainloop()
