# filename = r'C:\Users\urjit\Downloads\input1.txt'
import sys
import time
import os, psutil
filename=sys.argv[1]
# input("Enter file path:")
with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    # print(lines)

string_array=[]
j=[]
k=[]

for line in lines:
    if line.isalpha():
        string_array.append(line)
    elif len(string_array)==1:
        j.append(line)
    else:
        k.append(line)
        
j=list(map(int, j))
k=list(map(int, k))

def generateString(s, pos):
    for i in pos:
        s=s[:i+1]+s+s[i+1:]
    return s

s1=generateString(string_array[0],j)
s2=generateString(string_array[1],k)
# print(s1)
# print(s2)

# if (2**len(j))*len(string_array[0])==len(s1):
#     print("String 1 verified")
# if (2**len(k))*len(string_array[1])==len(s2):
#     print("String 2 verified")

alpha={'AA': 0,'CC': 0,'GG': 0,'TT': 0,'AC': 110, 'AG': 48, 'AT': 94, 'CG': 118, 'CT': 48, 'GT': 110, 'CA': 110, 'GA': 48, 'TA': 94, 'GC': 118, 'TC': 48, 'TG': 110}
delta=30

def baseCase(x, y, alpha, delta):
    n=len(x)
    m=len(y)
    mat=[]
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j]=delta*j
    for i in range(n+1):
        mat[i][0]=delta*i
    for i in range(1, n+1):
        for j in range(1, m+1):
            key=x[i-1]+y[j-1]
            mat[i][j] = min(mat[i-1][j-1] + alpha[key], mat[i][j-1] + delta, mat[i-1][j] + delta)

    x_ans=""
    y_ans=""
    i=n
    j=m
    while i and j:
        score=mat[i][j]
        score_diag=mat[i-1][j-1]
        score_up=mat[i-1][j]
        score_left=mat[i][j-1]
        key=x[i-1]+y[j-1]
        if score==score_diag+alpha[key]:
            x_ans=x[i-1]+x_ans
            y_ans=y[j-1]+y_ans
            i-=1
            j-=1
        elif score==score_up+delta:
            x_ans=x[i-1]+x_ans
            y_ans='_'+y_ans
            i-=1
        elif score==score_left+delta:
            x_ans='_'+x_ans
            y_ans=y[j-1]+y_ans
            j-=1
    while i:
        x_ans=x[i-1]+x_ans
        y_ans='_'+y_ans
        i-=1
    while j:
        x_ans='_'+x_ans
        y_ans=y[j-1]+y_ans
        j-=1
    return [x_ans, y_ans, mat[n][m]]

def memEff(str1, str2, alpha, delta):
    n = len(str1)
    m = len(str2)
    if n<2 or m<2:
        return baseCase(str1,str2,alpha, delta)
    else:
        F = forwardPass(str1[:n//2], str2, alpha, delta)
        B = backwardPass(str1[n//2:], str2, alpha, delta)
        partition = [F[j] + B[m-j] for j in range(m+1)]
        cut = partition.index(min(partition))
        F=[]
        B=[]
        partition=[]
        call_left = memEff(str1[:n//2], str2[:cut], alpha, delta)
        call_right = memEff(str1[n//2:], str2[cut:], alpha, delta)
        return [call_left[r] + call_right[r] for r in range(3)]

def backwardPass(str1,str2,alpha,delta):
    n = len(str1)
    m = len(str2)
    mat = []
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j] = delta*j
    for i in range(1, n+1):
        mat[i][0] = mat[i-1][0] + delta
        for j in range(1, m+1):
            key=str1[n-i]+str2[m-j]
            mat[i][j] = min(mat[i-1][j]+delta, mat[i][j-1]+delta, mat[i-1][j-1]+alpha[key])
        mat[i-1] = []
    return mat[n]

def forwardPass(str1,str2,alpha,delta):
    n = len(str1)
    m = len(str2)
    mat = []
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j] = delta*j
    for i in range(1, n+1):
        mat[i][0] = mat[i-1][0]+delta
        for j in range(1, m+1):
            key=str1[i-1]+str2[j-1]
            mat[i][j]=min(mat[i-1][j]+delta, mat[i-1][j-1]+alpha[key], mat[i][j-1]+delta)
        mat[i-1]=[]
    return mat[n]



# begin=time.time()
time_start = time.perf_counter()
z=memEff(s1, s2, alpha, delta)
end=time.time()
# print("Memory effecient= ",psutil.Process(os.getpid()).memory_info().rss / 1024)
with open("output.txt","w") as outputFile:
    line1=z[0][0:50]+" "+z[0][-50:]+"\n"
    line2=z[1][0:50]+" "+z[1][-50:]+"\n"
    line3=str(z[2])+"\n"
    time_elapsed = (time.perf_counter() - time_start)
    line4=((str)(time_elapsed)).split(" ")[0][:7]+"\n"
    line5=str(psutil.Process(os.getpid()).memory_info().rss / 1024)
    # print("Memory=",line5)
    # print("time= ",line4)
    outputFile.write(line1)
    outputFile.write(line2)
    outputFile.write(line3)
    outputFile.write(line4)
    outputFile.write(line5)

