import time
import os, psutil, sys
from numbers import Number
# import resource

#TAKE INPUT FROM USER
path_to_file=sys.argv[1]
# input("Enter the path to your file: ")
line4=""
line5=""
time_start = time.perf_counter()


def generateString(s1,arr):
    temp=s1
    for index in arr:
        temp=temp[:index+1]+temp+temp[index+1:]
        
    return temp


penalty=0
def getMinPenalty(string1, string2, alpha, delta):
    s1_len = len(string1)
    s2_len = len(string2)
    # print("S1 length= ",s1_len)
    # print("S2 length= ",s2_len)
    
    dp = [[0 for x in range(s1_len+s2_len+1)] for y in range(s1_len+s2_len+1)] 
    # print("dp array size= ", len(dp), len(dp[0]))
    for i in range (0,s1_len+s2_len+1):
        dp[i][0] = i*delta
        dp[0][i]=i*delta

    for i in range (1, s1_len+1):
        for j in range (1, s2_len+1):
            if string1[i-1] == string2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                key=string1[i-1]+string2[j-1]
                mismatchError=alpha[key]
                dp[i][j] = min(dp[i-1][j-1]+mismatchError, dp[i-1][j]+delta, dp[i][j-1]+delta)
    
    penalty=dp[s1_len][s2_len]
    # print("total penalty= ",dp[s1_len][s2_len])


#   Retrive the solution
    l=s1_len+s2_len
    i=s1_len
    j=s2_len
    x=l
    y=l
    
    ans1=[0]*(l+1)
    ans2=[0]*(l+1)
    
    while(not(i==0 or j==0)):
        char1=string1[i-1]
        char2=string2[j-1]
        
        if(char1!=char2):
            key=char1+char2
            value=alpha[key]
        if(char1==char2):
            ans1[x]=string1[i-1]
            ans2[y]=string2[j-1]
            x-=1
            y-=1
            i-=1
            j-=1
        elif(dp[i-1][j-1]+value== dp[i][j]):
            ans1[x]=string1[i-1]
            ans2[y]=string2[j-1]
            x-=1
            y-=1
            i-=1
            j-=1
        elif(dp[i-1][j]+delta==dp[i][j]):
            ans1[x]=string1[i-1]
            ans2[y]="_"
            x-=1
            y-=1
            i-=1
        elif (dp[i][j-1]+delta==dp[i][j]):
            ans1[x]="_"
            ans2[y]=string2[j-1]
            x-=1
            y-=1
            j-=1
        
    while (x>0):
        if(i>0):
            i-=1
            ans1[x]=string1[i]
        else:
            ans1[x]="_"
        x-=1
    
    while (y>0):
        if(j>0):
            j-=1
            ans2[y]=string2[j]
        else:
            ans2[y]="_"
        y-=1
            
    
    idx=1
    i=l
    while(i>=1):
        if(ans1[i]=="_" and ans2[i]=="_"):
            idx=i+1
            break
        i-=1
    
    output1=""
    output2=""
    for i in range(idx,l+1):
        output1+=ans1[i]
    for i in range(idx, l+1):
        output2+=ans2[i]
        
    # print("output for s1= ",output1)
    # print("output for s2= ", output2)
    with open("output.txt","w") as outputFile:
        line1=output1[0:50]+" "+output1[-50:]+"\n"
        line2=output2[0:50]+" "+ output2[-50:]+"\n"
        line3=(str)(penalty)+"\n"
        time_elapsed = (time.perf_counter() - time_start)
        line4=((str)(time_elapsed)).split(" ")[0][:7]+"\n"
        line5=str(psutil.Process(os.getpid()).memory_info().rss / 1024)
        # print("Time= ",line4)
        # print("Memory= ", line5)
        outputFile.write(line1)
        outputFile.write(line2)
        outputFile.write(line3)
        outputFile.write(line4)
        outputFile.write(line5)


# path_to_file=r"C:\Users\urjit\Downloads\input1.txt"
with open(path_to_file) as f:
    lines = f.readlines()
    lines=[s.strip() for s in lines]
    # print(lines)

    new_list = list(filter(lambda x: isinstance(x, Number), lines))
    strings = []
    j = []
    k = []
    
    for i in range(0, len(lines)):
        if lines[i].isalpha():
            strings.append(lines[i])
        elif len(strings) == 1:
            j.append(lines[i])
        else:
            k.append(lines[i])
    base1, base2 = strings[0], strings[1]
    j = list(map(int, j))
    k = list(map(int, k))

    # print(strings)
    # print(j)
    # print(k)

    s1= generateString(strings[0],j)
    s2=generateString(strings[1],k)
    # print("String 1 length= ",len(s1))
    # print("String 2 length= ",len(s2))
    # print("s1.len * s2.len= ",len(s1)*len(s2))
    
    # if (2**len(j))*len(strings[0]) == len(s1):
    #     print(" String 1 Verified")

    # if (2**len(k))*len(strings[1]) == len(s2):
    #     print(" String 2 Verified")


    alpha={"AC":110, "AG":48, "AT": 94, "CA": 110, "CG":118, "CT": 48, "GA": 48, "GC": 118,  "GT": 110, "TA":94, "TC": 48,  "TG":110}
    delta= 30

    getMinPenalty(s1,s2,alpha,delta)
    
