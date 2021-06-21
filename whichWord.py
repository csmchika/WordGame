from tkinter import *
from tkinter import messagebox
from random import randint


def pressKey(event):
    if event.keycode == 17:
        wordLabel['text'] = wordComp

    ch = event.char.upper()
    if len(ch) == 0:
        return 0

    codeBtn = ord(ch) - st
    if codeBtn >= 0 and codeBtn <= 32:
        pressLetter(codeBtn)


def updateInfo():
    scoreLabel["text"] = f'Ваши очки: {score}'
    topScoreLabel["text"] = f'Лучший результат: {topScore}'
    userTryLabel["text"] = f"Осталось попыток: {userTry}"


def getWordsFromFile():
    ret = []
    try:
        f = open("words.dat", "r", encoding='utf-8')
        for l in f.readlines():
            l = l.replace('\n', "")
            ret.append(l)
        f.close()
    except:
        messagebox.showinfo('ОШИБКА', 'Возникла проблема со словами')
        quit(0)
    return ret


def saveTopScore():
    global topScore
    topScore = score
    try:
        f = open("money.dat", "w", encoding='utf-8')
        f.write(str(topScore))
        f.close()
    except:
        messagebox.showinfo('ОШИБКА', 'Возникла проблема с сохранением очков')
        quit(0)


def getTopScore():
    try:
        f = open("money.dat", "r", encoding='utf-8')
        m = int(f.readline())
        f.close()
    except:
        m = 0
    return m


def startNewRound():
    global wordStar, wordComp, userTry

    wordComp = dictionary[randint(0, len(dictionary) - 1)]
    wordStar = '*' * len(wordComp)

    wordLabel["text"] = wordStar
    wordLabel.place(x=810 // 2 - wordLabel.winfo_reqwidth() // 2, y=50)

    for i in range(32):
        btn[i]["text"] = chr(st + i)
        btn[i]["state"] = 'normal'

    userTry = 10
    updateInfo()


def compareWord(s1, s2):
    res = 0

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            res += 1

    return res


def getWordStar(ch):
    ret = ''

    for i in range(len(wordComp)):
        if wordComp[i] == ch:
            ret += ch
        else:
            ret += wordStar[i]
    return ret


def pressLetter(n):
    global wordStar, score, userTry

    if btn[n]["text"] == ".":
        return 0

    btn[n]["text"] = "."
    btn[n]["state"] = "disabled"
    oldWordStar = wordStar
    wordStar = getWordStar(chr(st+n))
    count = compareWord(wordStar, oldWordStar)
    wordLabel["text"] = wordStar

    if count > 0:
        score += count * 5
    else:
        score -= 20
        if score < 0:
            score = 0
        userTry -= 1

    updateInfo()

    if wordComp == wordStar:
        score += score // 2
        updateInfo()

        if score > topScore:
            messagebox.showinfo('РЕКОРД', f'Поздравляю с рекордом, сегодня ты выбил {score} очков!')
            saveTopScore()
        else:
            messagebox.showinfo('ПОБЕДА', f'Поздравляю с победой, сегодня ты выбил {score} очков!')
        startNewRound()
    elif userTry <= 0:
        messagebox.showinfo('ПОРАЖЕНИЕ', 'Увы, но в этот раз не получилось')
        quit(0)


root = Tk()

WIDTH = 1266
HEIGHT = 668
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2

root.title("Угадай слово")
root.resizable(False, False)
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")
root.bind("<Key>", pressKey)

wordLabel = Label(font='consolas 35')
scoreLabel = Label(font=', 12')
topScoreLabel = Label(font=', 12')
userTryLabel = Label(font=', 12')

scoreLabel.place(x=10, y=165)
topScoreLabel.place(x=10, y=190)
userTryLabel.place(x=10, y=215)

score = 0
topScore = getTopScore()
userTry = 10

st = ord('А')
btn = []

for i in range(32):
    btn.append(Button(text=chr(st+i), width=2, font='consolas 35'))
    btn[i].place(x=215 + (i % 11) * 60, y=150 + (i // 11) * 91)
    btn[i]["command"] = lambda x=i: pressLetter(x)

wordComp = ""
wordStar = ""

dictionary = getWordsFromFile()

startNewRound()
root.mainloop()