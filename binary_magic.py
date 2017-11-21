print("Select Number between 0 - 60 \n")
a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
a6 = []
for i in range(61):
    if bin(i)[-1] == '1':
       a1.append(i)
    try :
        if bin(i)[-2] == '1':
            a2.append(i)
    except:
        pass
    try :
        if bin(i)[-3] == '1':
            a3.append(i)
    except:
        pass
    try :
        if bin(i)[-4] == '1':
            a4.append(i)
    except:
        pass
    try :
        if bin(i)[-5] == '1':
            a5.append(i)
    except:
        pass
    try :
        if bin(i)[-6] == '1':
            a6.append(i)
    except:
        pass

cout = 0

print(a1)
print("Is your number here (Y/N)")
inp = input(" : ")
if(inp.upper() == "Y"):
    cout = cout + 1

print(a2)


print("Is your number here (Y/N)")
inp = input(" : ")
if(inp.upper() == "Y"):
    cout = cout + 2

print(a3)

print("Is your number here (Y/N)")
inp = input(" : ")
if(inp.upper() == "Y"):
    cout = cout + 4
print(a4)
print("Is your number here (Y/N)")
inp = input(" : ")
if(inp.upper() == "Y"):
    cout = cout + 8
    

print(a5)
print("Is your number here (Y/N)")
inp = input(" : ")
if(inp.upper() == "Y"):
    cout = cout + 16
    
print(a6)
print("Is your number here (Y/N)")
inp = input(" : ")
if(inp.upper() == "Y"):
    cout = cout + 32

print("the number you gussed is : " + str(cout)) 

    
