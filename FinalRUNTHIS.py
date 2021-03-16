import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from os import path


from Merging import DataSetMaking,TFIDFMaking,FolderMaking
if not (path.exists("WholeDataTesting.csv")) or not (path.exists("WholeDataTFIDFTesting.csv")):
    print('DataSetMaking')
    FolderMaking()
    DataSetMaking()
    TFIDFMaking()
    print('DataSetMade')
df = pd.read_csv('WholeDataTFIDFTesting.csv')
Len = len(df)

def Check(Dict):
    global df
    List = Dict['Class'].tolist()
    if len(List) != 0:
        Max = max(set(List), key=List.count)
    else:
        Max = 'Empty'
    return Max


def ToMatch(Dict, ToCheck):
    global DataSet
    Count = 0
    List = Dict['Class'].tolist()
    for value in List:
        if value == ToCheck:
            Count += 1
    return Count


def Removal(Dict, ToCheck):
    indexNames = Dict[Dict['Class'] == ToCheck].index
    Dict.drop(indexNames, inplace=True)
    return Dict


def Match(Dict, ToCheck):
    global df
    DataSet = df.copy()
    Count = 0
    List = Dict["Class"].tolist()
    for value in List:
        if value == ToCheck:
            Count += 1
    return Count


def Models(cluster, k):
    global df
    print(df)
    Temp = df['Class']
    del df['Class']
    column_maxes = df.max()
    df_max = column_maxes.max()
    df = df / df_max
    df['Class'] = Temp
    dfCopy = df.copy()
    y_actual = df['Class'].tolist()
    del dfCopy['Class']

    cluster.fit_predict(dfCopy)
    labels = cluster.labels_
    y_pred=labels
    pred = pd.DataFrame(labels)
    pred.columns = ['Prediction']
    dfCopy['Class'] = df['Class']
    prediction12 = pd.concat([dfCopy, pred], axis=1)

    for i in range(0, k):
        globals()['clusT%s' % i] = prediction12.loc[prediction12.Prediction == i]

    ListClass = []######
    for i in range(0, k):
        Dict = 'clusT' + str(i)
        ListClass.append(Check(globals()[Dict]))
    ClassClassify = ListClass
    Sum = 0
    for i in range(0, k):
        # Value=int(ListClass[i])
        Dict = 'clusT' + str(i)
        Sum += Match(globals()[Dict], ClassClassify[i])
    from sklearn.metrics import classification_report
    Classif=classification_report(y_actual, y_pred)
    Purity=(Sum/Len)*100
    return Purity,Classif

############################ For Progress

def bar():
    import time
    progress['value']=20
    window.update_idletasks()
    time.sleep(1)
    progress['value']=50
    window.update_idletasks()
    time.sleep(1)
    progress['value']=80
    window.update_idletasks()
    time.sleep(1)
    progress['value']=100

def GetResult(choice,k):
    bar()
    k=int(k)
    print(choice, k)

    OPTIONS = [
        "K Means",
        "AgglomerativeClustering",
        "BIRCH"
    ]
    choice=OPTIONS.index(choice)
    if choice==0:
        print('Here')
        from sklearn import cluster
        clusterT = cluster.KMeans(n_clusters=k)
        Purity,Classif=Models(clusterT, k)

    elif choice==1:
        from sklearn.cluster import AgglomerativeClustering
        clusterT = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')
        Purity,Classif=Models(clusterT, k)
    else:
        from sklearn.cluster import Birch
        clusterT = Birch(branching_factor=50, n_clusters=k, threshold=1.5)
        Purity,Classif=Models(clusterT, k)
    Output(Purity,Classif)
def Create():
    bar()
    FolderMaking()
    DataSetMaking()
    TFIDFMaking()
    print('Create')
def Delete():
    bar()
    import os
    if  (path.exists("WholeDataTesting.csv")) or(path.exists("WholeDataTFIDFTesting.csv")):
        os.remove("WholeDataTesting.csv")
        os.remove("WholeDataTFIDFTesting.csv")

    print('Delete')
def Output(Purity,Classif):
    # bar()
    Purity=round(Purity, 4)
    labelAcc['text'] = 'Purity\n'+str(Purity)
    labelConf['text']=str(Classif)

High=700
Width=800
window=tk.Tk()
canvas=tk.Canvas(window,height=High,width=Width)
canvas.pack()

bg=tk.PhotoImage(file='information-retrieval-c.png')
bg_label=tk.Label(window,image=bg)
#bg_label.pack()
bg_label.place(relwidth=1,relheight=1)

frame=tk.Frame(window,bg='#80bfff',bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.5,relheight=0.1,anchor='n')

Button=tk.Button(frame,text='Delete DataSet',font=40,bg='#0077b3',fg='white',command= lambda:Delete())
Button.place(relx=0.5,relwidth=0.49,relheight=1)


Button=tk.Button(frame,text='Create DataSet',font=40,bg='#0077b3',fg='white',command= lambda:Create())
Button.place(relx=0.0,relwidth=0.49,relheight=1)


frame=tk.Frame(window,bg='#80bfff',bd=5)
frame.place(relx=0.5,rely=0.21,relwidth=0.5,relheight=0.1,anchor='n')


entry1=tk.Entry(frame,font=40)
entry1.place(relx=0.25,rely=0.02,relwidth=0.75,relheight=1)


display = tk.Label(frame, text="K = ",bg='#0077b3',fg='white',width=10, height=4, font=("Helvetica", 15,'bold',))
display.place(relx=0.01,rely=0.02,relwidth=0.23,relheight=1,)

#
# frame=tk.Frame(window,bg='#80bfff',bd=5)
# frame.place(relx=0.5,rely=0.21,relwidth=0.5,relheight=0.1,anchor='n')
#
#
# entry2=tk.Entry(frame,font=40)
# entry2.place(relx=0.25,rely=0.02,relwidth=0.75,relheight=1)
#
# display = tk.Label(frame, text="Team02",bg='#0077b3',fg='white',width=10, height=4, font=("Helvetica", 15,'bold',))
# display.place(relx=0.01,rely=0.02,relwidth=0.23,relheight=1,)

frame=tk.Frame(window,bg='#80bfff',bd=5)
frame.place(relx=0.5,rely=0.34,relwidth=0.5,relheight=0.1,anchor='n')


OPTIONS = [
"K Means",
"AgglomerativeClustering",
"BIRCH"
] #etc
variable = StringVar(window)
#variable.set(OPTIONS[0])
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'red',
                                        'fieldbackground': '#0077b3',
                                       'background': 'white',
                                       'color':'white'
                                       }}}
                         )
combostyle.theme_use('combostyle')
w = ttk.Combobox(frame, values=OPTIONS, width=10, height=4, font=("Helvetica", 15,'bold',),)
w.set('\tSelect Model')
#w = OptionMenu(frame, variable, *OPTIONS)
w.config(width = 20000)
display = tk.Label(frame, text="   Select Model",bg='#0077b3',fg='white',width=10, height=4, font=("Helvetica", 15,'bold',))
display.place(relwidth=0.96,relheight=1,)
w.place(relwidth=1,relheight=1)



frame=tk.Frame(window,bg='#80bfff',bd=5)
frame.place(relx=0.5,rely=0.46,relwidth=0.5,relheight=0.1,anchor='n')

button = tk.Button(frame, text=" Run ", bg='#0077b3', fg='white',width=10, height=4, font=("Helvetica", 15,'bold',),command= lambda:GetResult(w.get(),entry1.get()))
button.place(relwidth=1,relheight=1,)

frame=tk.Frame(window,bg='#80bfff',bd=5)
frame.place(relx=0.5,rely=0.58,relwidth=0.5,relheight=0.05,anchor='n')

s = Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='white', background='#0077b3')

progress=Progressbar(frame, style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=100,mode='determinate')
progress.place(relwidth=1,relheight=1,)

#Button=tk.Button(frame,text='Enter Query',font=40,command= lambda:get_res(entry.get()))
#Button.place(relx=0.7,relwidth=0.3,relheight=1)

lower_frame=tk.Frame(window,bg='#80bfff',bd=10)
lower_frame.place(relx=0.5,rely=0.70,relwidth=0.5,relheight=0.25,anchor='n')

labelAcc=tk.Label(lower_frame,wraplengt=400)
labelAcc.place(relx=0.0,relwidth=0.3,relheight=1)

labelConf=tk.Label(lower_frame,wraplengt=400)
labelConf.config(font=("Helvetica", 8))
labelConf.place(relx=0.31,relwidth=0.7,relheight=1)

#window.title("Output")

window.mainloop()
