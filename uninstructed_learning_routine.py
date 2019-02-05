#       Unsupervised learning method - Eva Viviani PhD - Languge learning and reading lab @ SISSA
#                  This experiment runs on Psychopy
#In this exp we want to have 10 words seen three times in each block. Followed by 25 nonwords (55 trials in total * block).
#After the 3rd block, 5 words taken from the previous blocks are displayed from the 4th block until the 8th block, accompanied by other 5 new words never seen before.
# from the 8th block all the words are already seen at least once, so are taken randomly.
#At the end of the exp each word is shown 9 times, for a total of 450 times (50 words in total). Nonwords are shown only once, 
#for a total of 375 nonwords in 15 blocks.
#-------Keyboard is used for debugging: z for SI/YES, m for NO
#-------1 flag: word, 2 flag: nonword
#-------Arduino: 2 for SI/YES, 1 for NO. -1 for no response (timeout of 2001 milliseconds programmed in Arduino)
#coding: utf-8

from psychopy import visual, data , core, event, gui
import numpy as np
import os 
import datetime 
import serial

#-------------------------------------------------------------------------------------------------#
#                                          DEMOGRAPHICS                                           #
#-------------------------------------------------------------------------------------------------#
# user GUI for storing subject's information
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

#-------------------------------------------------------------------------------------------------#
#                                        TIMELINE                                                 #
#-------------------------------------------------------------------------------------------------#
fixT = 0.5 #fixation cross duration
wordT = 0.5 #word duration on screen
iti= 1 #fixed parameter of ITI between trials

#--------------------------------------------------------------------------#
#---------------------------INITIALIZING ARDUINO---------------------------# 
#--------------------------------------------------------------------------#
#enables only when Arduino is connected 
portName="COM4" #set serial port address
ser=serial.Serial(portName, 9600) 

#-------------------------------------------------------------------------------------------------#
#                                    INITIALIZING SCREEN                                          #
#-------------------------------------------------------------------------------------------------#
win = visual.Window(size=(1920, 1080), fullscr = True, screen = 1, rgb=(-1,-1,-1)) #set the window's size=(700,500) for debugging
clock = core.Clock() #set the clock
tmpData=str(datetime.datetime.now())[0:10] #get the current date
tmpOra=str(datetime.datetime.now())[11:19] #get the current time

#-------------------------------------------------------------------------------------------------#
#                                        INSTRUCTIONS                                             #
#-------------------------------------------------------------------------------------------------#
instrList=["Benvenuto",
"In questo esperimento dovrai imparare delle nuove parole appartenenti ad una lingua sconosciuta. \n\nIl modo in cui le imparerai sara\' distinguerle da stringhe di lettere che invece non sono parole di questa lingua.",
"Nell'esperimento vedrai queste parole mescolate a delle stringhe di lettere \"fasulle\" e dovrai cercare di indovinare se l\' item che stai vedendo e\' una parola oppure no.",
"Vedrai un item alla volta.\n\nSe quella che vedi pensi sia una parola: \n\npremi il pulsante SI.\n\nSe quella che vedi pensi NON sia una parola:\n\npremi il pulsante NO",
"Ogni volta che la tua risposta sara\' corretta vedrai la stringa di lettere colorarsi di verde, altrimenti di rosso.",
"Cerca di rispondere nel modo piu\' RAPIDO e ACCURATO possibile. \n\nHai due secondi per rispondere.","Quando lo sperimentatore ti da\' l\'OK,\n\npremi la barra spaziatrice per vedere otto esempi."]
instrList4=["Sessione di apprendimento terminata. Aspetta lo sperimentatore per sapere cosa fare."]

#-------------------------------------------------------------------------------------------------#
#                                      IMPORT WORD LISTS                                          #
#-------------------------------------------------------------------------------------------------#
Acc, wordList_A, wordList_B, words_A, words_B, warmup, nonwords, nonwordList, warmupList, used_words, used_twice, blocks= ([] for i in range(12)) #create empty objects

with open('warmupList.txt', 'r') as f: #import warmup trials
    for x in f:
        warmup.append(x.strip().split('\t')) 
        warmupList = warmup 
f.close()

with open('lista_A.txt', 'r') as f: #import word list
    for x in f:
        words_A.append(x.strip().split('\t')) 
        wordList_A = zip(*words_A) 
f.close()

with open('lista_B.txt', 'r') as f: #import word list
    for x in f:
        words_B.append(x.strip().split('\t')) 
        wordList_B = zip(*words_B) 
f.close()

with open('nonwordList.txt', 'r') as f: #import nonword list
    for x in f:
        nonwords.append(x.strip().split('\t')) 
        nonwordList = zip(*nonwords) 
f.close()
nonwords=[]
for i in nonwordList[0]:
    nonwords.append([i,2])

#-------------------------------------------------------------------------------------------------#
#                                 CREATION OF STIMULI                                             #
#-------------------------------------------------------------------------------------------------#
rect = visual.Rect(win, width=0.2, height=0.2, pos=[-1,-0.99])
rect.setFillColor("white")
fix = visual.TextStim(win,text="+",units = "pix",height = 40, pos=(0,0), color = 'white', alignHoriz='center', alignVert='center')
word=visual.TextStim(win,text="ciccipicci",units = "pix", height = 40, color = (0.9,0.9,0.9),alignHoriz='center', alignVert='center')
wordWrong=visual.TextStim(win,text="ciccipicci",units = "pix", height = 40, color = (1.0,-1,-1),alignHoriz='center', alignVert='center') # feedback in red
wordRight=visual.TextStim(win,text="ciccipicci",units = "pix", height = 40, color = (0, 1, 0), alignHoriz='center', alignVert='center') 
#feedback in green
clockText = visual.TextStim(win, text="ciccipicci",units = "pix", height = 40, color = (0, 1, 0), alignHoriz='center', pos=(0, -100))

#-------------------------------------------------------------------------------------------------#
#                                      FUNCTIONS                                                  #
#-------------------------------------------------------------------------------------------------#
def istruzioni(testo): 
    istruzioni = visual.TextStim(win, text = testo, units = "pix", height = 32, color = (0.9,0.9,0.9)) 
    spazio = visual.TextStim(win, text = "Premi SPAZIO per continuare", units = "pix", height = 32, color = (0.9,0.9,0.9), alignHoriz='center', pos=(0, -400))
    event.Mouse(visible=False)
    istruzioni.draw()
    spazio.draw()
    win.flip()
    return event.waitKeys(keyList = ['space']) #wait button press

def arrivederci(testo): 
    arrivederci = visual.TextStim(win, text = testo, units = "pix", height = 32, color = (0.9,0.9,0.9)) #, alignHoriz='center', alignVert='center'
    spazio = visual.TextStim(win, text = "Premi SPAZIO per proseguire l\' esperimento", units = "pix", height = 32, color = (0.9,0.9,0.9), alignHoriz='center', pos=(0, -400))
    event.Mouse(visible=False)
    arrivederci.draw()
    spazio.draw()
    win.flip()
    return event.waitKeys(keyList = ['space']) #wait button press

def trial(t1):
    global word, rt, fixT, isi, resp, answer, rect
    event.Mouse(visible=False)
    word.setText(t1)
    wordRight.setText(t1)
    wordWrong.setText(t1)
    fix.draw()
    win.flip()
    core.wait(fixT)
    win.flip()
    #flag 'GO' signal for Arduino
    ser.write(b'go\r')
    replay = ""
    wait = True
    while (wait):
        replay = ser.readline()
        if (replay <> ""):
            wait = False
    #end flag
    word.draw()
    rect.draw()
    ser.flush()
    core.wait(0.1)
    win.flip()
    resp=[]
    #Serial read section
    while True:
        rt = ser.readline().rstrip()
        resp = ser.readline().rstrip()
        print "seriale",rt
        print "response",resp
        core.wait(iti+np.random.normal(0, .2, 1)) #random value added to the fixed ITI
        if event.getKeys(keyList = ['escape']): 
            core.quit()
        return
    win.flip()
#for keyboard debugging:
#    while True:
#        clock.reset()
#        answer = event.waitKeys(maxWait = 2, keyList = ['z','m'],timeStamped=clock) #here the keyboard
#        if not answer:
#            rt = 0
#            resp = 0
#        else:
#            rt = answer[0][1]
#            print rt
#            resp = answer[0][0]
#            print resp
#        if event.getKeys(keyList = ['escape']): 
#            core.quit()
#        return

def feedbackArduino(list):
    if list== '1': 
        if (resp == '2'): 
            Acc=1
            wordRight.draw()
            win.flip()
        else:
            Acc=0
            wordWrong.draw()
            win.flip()
        return Acc
    else :
        if (resp == '1'):
            Acc=1
            wordRight.draw()
            win.flip()
        else:
            Acc=0
            wordWrong.draw()
            win.flip()
        return Acc

def feedbackKeyboard(list):
    if list== '1': 
        if (resp == 'z'): 
            Acc=1
            wordRight.draw()
            win.flip()
        else:
            Acc=0
            wordWrong.draw()
            win.flip()
        return Acc
    else :
        if (resp == 'm'):
            Acc=1
            wordRight.draw()
            win.flip()
        else:
            Acc=0
            wordWrong.draw()
            win.flip()
        return Acc

def myClock():
    clock.reset()
    t1 = clock.getTime()
    t2 = t1
    aspetta = visual.TextStim(win, text = "Fai una pausa. L\'esperimento riprendera\' allo scadere del tempo.", units = "pix", height = 32, color = (0.9,0.9,0.9), alignHoriz='center', alignVert='center')
    while t2 < (t1+120) and t2>0:
        event.Mouse(visible=False)
        t2pausa = clock.getTime()      # end of timeout loop
        t2=t2pausa
        clockText.setText(str(int(120-t2pausa))) # you can format/round this as required
        clockText.draw()
        aspetta.draw()
        win.flip()
        if event.getKeys(keyList = ['escape']): 
            core.quit()


#-------------------------------------------------------------------------------------------------#
#                                          OUTPUT FILE                                            #
#-------------------------------------------------------------------------------------------------#
Eva=open("Output_Exp2_UninstructedLearning_Subj_%s.txt"%(Subj),"a")
Eva.write(u"Blocco;Subject;Age;Gender;Handedness;Session;List;Data;OraStart;TrialCount;Word;rt;Resp;Acc\n")

#-------------------------------------------------------------------------------------------------#
#                                      CREATING ITEMS BLOCKS                                      #
#-------------------------------------------------------------------------------------------------#
###                                     Spring Edition                                         #
if int(Subj)%2 == 0:
    new_words=words_A
else:
    new_words=words_B

np.random.shuffle(new_words)
blocks=[]
for i in range(3):
    block=new_words[:10]
    used_words+=new_words[:10]
    new_words=new_words[10:]
    blocks.append(block*3)     
    
for i in range(4,8):
    block=new_words[:5]
    temp=block
    new_words=new_words[5:]
    np.random.shuffle(used_words)
    block=block+used_words[:5]
    used_twice=used_twice+used_words[:5]
    used_words=used_words[5:]+temp
    blocks.append(block*3)
for i in range(6):
    block = used_words[:5] 
    temp = block
    used_words = used_words[5:]
    np.random.shuffle(used_twice)
    block = block + used_twice[:5]
    used_twice = used_twice[5:] + temp
    blocks.append(block*3)
    
for i in range(2): #last 8 blocks
    block=used_twice[:10]
    used_twice=used_twice[10:]
    blocks.append(block*3)     

    #25 random nonwords added to each block
nonwords1=nonwords
for i in range(len(blocks)): 
    np.random.shuffle(nonwords1)
    blocks[i]=blocks[i] + nonwords1[:40]
    nonwords1=nonwords1[40:]
    np.random.shuffle(blocks[i])


#Print finalList of all blocks
f = open("finalList.txt", "w")
for i in range(len(blocks)):
    f.write("BLOCCO"+str(i+1)+"\n")
    for j in range(len(blocks[i])):
        f.write(str(blocks[i][j][0])+" "+str(blocks[i][j][1])+"\n")
f.close()

#--------------------------------------------------------------------------------------------------#
#                                          EVENTS                                                  #
#--------------------------------------------------------------------------------------------------#
Performance=np.zeros(1) # create variable to store accuracy

#Warmup Trials
for x in instrList:
    istruzioni(x)
    performance=[]
for x in range(len(warmupList)):
    trial(warmupList[x][0])
    Acc=feedbackArduino(warmupList[x][1]) #enable only when Arduino is connected
    #Acc=feedbackKeyboard(warmupList[x][1]) #enable only when debugging with the Keyboard
    rt=str(round(float(rt),4))
    performance.extend([Acc])
    core.wait(iti+np.random.normal(0, .2, 1)) #random value added to the fixed ITI
    win.flip()
    Eva.write("warmup;%s;%s;%s;%s;%s;%s;%s;%s;%i;%s;%s;%s;%s\n"%(Subj,age,gender,handedness,session,list,tmpData,tmpOra,(x+1), warmupList[x][0], rt,resp, Acc))
Performance=round(float(np.mean(performance)),2)*100

instrList2=["Molto bene. La tua accuratezza media e\' stata del: "+str(Performance)+"%\nHai qualche domanda?","Ricorda:\n\nSe quella che vedi e\' una parola:\n\npremi il pulsante SI\n\nSe quella che vedi NON e\' una parola:\n\n premi il pulsante NO.",
"Se la tua risposta sara\' corretta vedrai la stringa di lettere colorarsi di verde, altrimenti di rosso.",
"Cerca di ricordare tutte le stringhe di lettere che correttamente categorizzerai come parole. \n\nL\'esperimento durera\' almeno 30min.\n\nPremi la barra spaziatrice per iniziare l'esperimento."]


#Experimental Trials
for x in instrList2:
    istruzioni(x)
for i in range(len(blocks)):
    if i == 4 or i == 9 or i == 13:
        myClock()
    performance=[]
    for x in range(len(blocks[i])):
        trial(blocks[i][x][0])
        Acc=feedbackArduino(blocks[i][x][1]) #enable only when Arduino is connected
        #Acc=feedbackKeyboard(blocks[i][x][1]) #enable only when debugging with the Keyboard
        rt=str(round(float(rt),4))
        performance.extend([Acc])
        core.wait(iti+np.random.normal(0, .2, 1)) #random value added to the fixed ITI
        win.flip()
        Eva.write(str(i+1)+";%s;%s;%s;%s;%s;%s;%s;%s;%i;%s;%s;%s;%s\n"%(Subj,age,gender,handedness,session,list,tmpData,tmpOra,(x+1),blocks[i][x][0],rt,resp, Acc))
    Performance=round(float(np.mean(performance)),2)*100
    instrList3=["La tua accuratezza media in questa sessione e\' stata del: "+str(Performance)+"%\nNumero di blocchi ancora da completare: "+str(len(blocks)-1-i)+"\n","Premi la barra spaziatrice per continuare l\'esperimento." ]
    if i<(len(blocks)-1):
        for x in instrList3:
            istruzioni(x)

        
#Saluti
for x in instrList4:
    arrivederci(x)
    print 'experiment ended correctly!'
Eva.close()
win.close