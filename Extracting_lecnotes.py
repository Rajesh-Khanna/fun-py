import os
import shutil
name = []
destination = 'G:\\3rdsem\\algo\\mit tut\\notes'
os.chdir('G:\\3rdsem\\algo\\mit tut')
if not 'notes' in os.listdir():
    os.mkdir('notes')
os.chdir('G:\\3rdsem\\algo\\mit tut\\6-046j-fall-2005\\6-046j-fall-2005\\contents\\video-lectures')
print('moved to ' + os.getcwd())

for f in os.listdir():
    if not 'htm' in f:
        name.append(f)
        os.chdir('G:\\3rdsem\\algo\\mit tut\\6-046j-fall-2005\\6-046j-fall-2005\\contents\\video-lectures\\'+f)
        for l in os.listdir():
            if ('lec' in l) and ('.pdf' in  l) :
                if not '.xml' in l:
                    shutil.copy(l,destination)
os.chdir(destination)
i=0
for f in os.listdir():
    os.rename(f,name[i]+'.pdf')
    i=i+1
print('finish')
