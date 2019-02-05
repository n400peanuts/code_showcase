#       Instructed learning routine - Eva Viviani PhD - Languge learning and reading lab @ SISSA
#                  This experiment runs on Psychopy
#This is a typing game in which the participant have to copy the word displayed on the monitor.
#Accuracy and RTs are stored in a file.txt

#------Keyboard is used to type down the word
#------Feedback given 

from psychopy import visual, data , core, event, gui
import numpy as np
import os #library that enables system operations
import datetime

#--------------------------------------------------------------------------#
#                               DEMOGRAPHICS                               #
#--------------------------------------------------------------------------#
#User GUI for storing info about subjects
def demographics():
    global Subj, age, gender, handedness, session, list
    myDlg = gui.Dlg(title="Info")
    myDlg.addField('Subject:')
    myDlg.addField('Age:', 28)
    myDlg.addField('Gender:', choices=["Female", "Male"])
    myDlg.addField('Handedness:', choices=["Left", "Right"])
    myDlg.addField('Session', choices=["Morning", "Afternoon"])
    myDlg.addField('List', choices=["A", "B"])
    myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        try:
            Subj = str(myDlg.data[0])
            age = str(myDlg.data[1])
            gender = str(myDlg.data[2])
            handedness = str(myDlg.data[3])
            session = str(myDlg.data[4])
            list = str(myDlg.data[5])
            return
        except ValueError:
            demographics()
    else:
        print('user cancelled')
demographics()

#--------------------------------------------------------------------------#
#                           FIXED PARAMETERS                               #
#--------------------------------------------------------------------------#
fix = 1 #cross duration
fixWord = 1 #duration of word presentation

#--------------------------------------------------------------------------#
#                           INITIALIZING SCREEN                            #
#--------------------------------------------------------------------------#
win = visual.Window( size=(700, 500), fullscr = True, screen = 1, rgb=(-1,-1,-1)) #set the window's size=(700,500) 
clock = core.Clock() #set the clock
tmpData=str(datetime.datetime.now())[0:10] #get the current date
tmpOra=str(datetime.datetime.now())[11:19] #get the current time

#--------------------------------------------------------------------------#
#                              INSTRUCTIONS                                #
#--------------------------------------------------------------------------#
instr1 = ["Benvenuto.", "In questo esperimento vedrai delle stringhe di lettere scritte in minuscolo che dovrai cercare di memorizzare.", 
"Per ogni presentazione dovrai prestare attenzione alle stringhe di lettere e ricopiarle sullo schermo scrivendole con la tastiera e premendo ENTER.", 
"Quando lo sperimentatore ti dara\' l\'OK,\n\npremi la barra spaziatrice per vedere degli esempi."]
instr2 = ["Molto bene. Hai qualche domanda?", "L\'esperimento durera\' circa 30 minuti.", "Cerca di rimanere concentrato dall'inizio alla fine,\n\ne\' molto importante.",
"Quando lo sperimentatore ti da\' l\'OK,\n\npremi la barra spaziatrice per iniziare."]
instr4 = ["Sessione di apprendimento terminata. Aspetta lo sperimentatore per sapere cosa fare."]

#--------------------------------------------------------------------------#
#                           IMPORT WORD LISTS                              #
#--------------------------------------------------------------------------#
wordList_A, wordList_B, warmupList, block, wordList1, blocks= ([] for i in range(6)) #create empty objects

with open('warmupList.txt', 'r') as f: #import warmup trials
        warmup = [line.strip() for line in f]
        warmupList=warmup
f.close()

with open('lista_A.txt', 'r') as f: #import word trials lista A
        words = [line.strip() for line in f]
        wordList_A=words
f.close()

with open('lista_B.txt', 'r') as f: #import word trials lista B
        words = [line.strip() for line in f]
        wordList_B=words
f.close()

#--------------------------------------------------------------------------#
#                           CREATION OF STIMULI                            #
#--------------------------------------------------------------------------#
cross = visual.TextStim(win, text="+",units = "pix",height = 40, pos=(0,0), color = 'white', alignHoriz='center', alignVert='center')
word = visual.TextStim(win, text="words",units = "pix", height = 40, color = (0.9,0.9,0.9),alignHoriz='center', alignVert='center')
letter = visual.TextStim(win, text="letters", units= "pix", height = 40, color = (0.9,0.9,0.9),alignHoriz='center', alignVert='center')
wordWrong=visual.TextStim(win,text="ciccipicci",units = "pix", height = 40, color = (1,-1,-1),alignHoriz='center', alignVert='center') #in red
wordRight=visual.TextStim(win,text="ciccipicci",units = "pix", height = 40, color = (0, 1, 0), alignHoriz='center', alignVert='center') #in green

#--------------------------------------------------------------------------#
#                               OUTPUT                                     #
#--------------------------------------------------------------------------#
Eva = open("Output_Exp2_instructedLearning_Subj_%s.txt"%(Subj),"a")
Eva.write(u"Blocco;Subject;Age;Gender;Handedness;Session;List;Data;OraStart;TrialCount;Word;Resp;Acc;rt\n")

#--------------------------------------------------------------------------#
#                               FUNCTIONS                                  #
#--------------------------------------------------------------------------#
def instructions(testo):
    istruzioni = visual.TextStim(win, text= testo, units = "pix",height = 32, pos=(0,0), color = 'white', alignHoriz='center', alignVert='center')
    spazio = visual.TextStim(win, text= 'Premi SPAZIO per continuare', units = "pix", height = 32, pos=(0,-400), color = 'white', alignHoriz='center')
    event.Mouse(visible = False)
    istruzioni.draw()
    spazio.draw()
    win.flip()
    return event.waitKeys(keyList = ['space'])

def arrivederci(testo): 
    arrivederci = visual.TextStim(win, text = testo, units = "pix", height = 32, color = (0.9,0.9,0.9)) #, alignHoriz='center', alignVert='center'
    spazio = visual.TextStim(win, text = "Premi SPAZIO per proseguire l\' esperimento", units = "pix", height = 32, color = (0.9,0.9,0.9), alignHoriz='center', pos=(0, -200))
    event.Mouse(visible=False)
    arrivederci.draw()
    spazio.draw()
    win.flip()
    return event.waitKeys(keyList = ['space']) #wait button press

#presentation of the word
def trial(t1):
    global cross, word, rt
    word.setText(t1)
    wordRight.setText(t1)
    wordWrong.setText(t1)
    cross.draw()
    win.flip()
    core.wait(fix)
    win.flip()
    word.draw()
    win.flip()
    while True:
        if event.getKeys(keyList = ['escape']):
            core.quit()
        return    

    #typing task
def printKeys(t1):
    global myString, K, letter, rt, wholeWord, timefirstButton
    myString = ''
    wholeWord = []
    while True:
        clock.reset()
        answer = event.waitKeys(maxWait=2, timeStamped=clock)
        if not answer:
            buttonTime = 0
            win.flip()
            wholeWord.append(buttonTime)
            timefirstButton = wholeWord[0]
            return
        else:
            buttonTime = answer[0][1]
            K = ''.join(answer[0][0])
            if K == 'backspace':
                myString = myString[:-1]
            elif K == 'return':
                return
            elif K == 'escape':
                core.quit()
            elif K == 'space':
                myString= myString+' '
            elif K == 'left':
                myString=myString[:-1] 
            elif K == 'right':
                myString=myString+ ' '
            else:
                myString += K
            letter.setText(myString)
            letter.draw()
            win.flip()
            wholeWord.append(buttonTime)
            timefirstButton = wholeWord[0]
    
#--------------------------------------------------------------------------#
#                               ITEMS BLOCK                                #
#--------------------------------------------------------------------------#
if int(Subj)%2 == 0:
    wordList=wordList_A
else:
    wordList=wordList_B

wordList1=wordList*9
np.random.shuffle(wordList1)
for x in range(6):
    block=wordList1[:75]
    wordList1=wordList1[75:]
    blocks.append(block)

#--------------------------------------------------------------------------#
#                               EVENTS                                     #
#--------------------------------------------------------------------------#
#Warmup trials
for x in instr1:
    instructions(x)
    Acc = [0]*len(blocks)*len(blocks[0])
for x in range(len(warmupList)):
    trial(warmupList[x])
    printKeys(x)
    rt=str(round(float(timefirstButton),4))
    if myString == warmupList[x]:
        Acc[x] = 1
        wordRight.draw()
        win.flip()
        core.wait(fixWord)
        win.flip()
        #print 'accuracy: %s'%Acc 
    else:
        Acc[x] = 0
        wordWrong.setText(myString)
        wordWrong.draw()
        win.flip()
        core.wait(fixWord)
        win.flip()
        #print 'accuracy: %s'%Acc
    Eva.write("warmup;%s;%s;%s;%s;%s;%s;%s;%s;%i;%s;%s;%s;%s\n"%(Subj,age,gender,handedness,session,list,tmpData,tmpOra,(x+1), warmupList[x], myString, Acc[x],rt))
  
#Experimental Trials
for x in instr2:
    instructions(x)
for i in range(len(blocks)):
    for x in range(len(blocks[i])):
        trial(blocks[i][x])
        printKeys(x)
        rt=str(round(float(timefirstButton),4))
        if myString == blocks[i][x]:
            Acc[x] = 1
            wordRight.draw()
            win.flip()
            core.wait(fixWord)
            win.flip()
            #print 'accuracy: %s'%Acc 
        else:
            Acc[x] = 0
            wordWrong.setText(myString)
            wordWrong.draw()
            win.flip()
            core.wait(fixWord)
            win.flip()
            #print 'accuracy: %s'%Acc
        Eva.write(str(i+1)+";%s;%s;%s;%s;%s;%s;%s;%s;%i;%s;%s;%s;%s\n"%(Subj,age,gender,handedness,session,list,tmpData,tmpOra,(x+1), blocks[i][x], myString, Acc[x],rt))
    instr3 = ["Ora puoi fare una pausa.\n\nNumero di blocchi ancora da completare: "+str(len(blocks)-1-i)+"\n\nQuando ti senti pronto a ricominciare l\'esperimento, premi la barra spaziatrice."]    
    if i<(len(blocks)-1):
        for x in instr3:
            instructions(x)
            

#Saluti
for x in instr4:
    arrivederci(x)
    print 'experiment ended correctly!'
Eva.close()
win.close() 

