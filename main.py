from sys import exit
charTable=[-1]*256
occurenceTable=[]
marginTable=[]
def Create_Char_Table(pattern):
    global charTable
    n=len(pattern)
    for i in range(n):
        charTable[ord(pattern[i])]=i

def Create_Occurence_Table(pattern):
    global occurenceTable
    m=len(pattern)
    occurenceTable=[-1]*m
    occurenceTable[0]=-1
    for i in range(1,m):
        for j in range(i-1,-1,-1):
            if pattern[i]==pattern[j]:
                occurenceTable[i]=j
                break


def Create_Margin_Table(pattern):
    global marginTable
    m=len(pattern)
    marginTable=[0]*m
    suffix=''
    i=m-2
    while i>=0:
        suffix=pattern[i+1]+suffix
        n=len(suffix)
        prefix=''
        for j in range(n):
            prefix+=pattern[j]
        if prefix==suffix:
            marginTable[i]=len(suffix)
        else:
            marginTable[i]=marginTable[i+1]
        i=i-1
def getPairedChar(text,i):
    if i!=0:
        return text[i-1]+text[i]
    return text[i]

def isInPair(pattern,pairedchar,j):
    global occurenceTable,charTable
    if len(pairedchar)==1:
        return pairedchar[0]==pattern[0],-1
    char1=pairedchar[0]
    char2=pairedchar[1]
    lastoccurence1=charTable[ord(char1)]
    lastoccurence2=charTable[ord(char2)]
    if lastoccurence1>0 and lastoccurence2>0:
        while lastoccurence1 > j-1 :
            lastoccurence1=occurenceTable[lastoccurence1]
        while lastoccurence2 >j:
            lastoccurence2=occurenceTable[lastoccurence2]
    if lastoccurence2!=0 and lastoccurence2==lastoccurence1+1:
        return True,lastoccurence1
    elif lastoccurence2==0:
        return True,-1
    return False,-1


def matchedJumping(pattern,index):
    return index+1


def marginJumping(pattern,j):
    global marginTable
    return len(pattern)-marginTable[j]

def fullJumping(pattern,j):
    return len(pattern)

def isStringFound(text,pattern):
    global charTable,occurenceTable,marginTable
    Create_Char_Table(pattern)
    Create_Occurence_Table(pattern)
    Create_Margin_Table(pattern)
    i,j=0,len(pattern)-1
    matched=[]
    comparisons=0
    Found=False
    while j>=0 and i+j<len(text):

        #print(i+j,j,text[i+j]==pattern[j])
        #print(i+j,j,matched)
        if j in matched:
            matched.remove(j)
            j=j-1
            if j==-1:
                Found = True
                print('pattern found at index {} of text'.format(i))
                i = i + marginJumping(pattern, 0)
                for k in range(marginTable[0]):
                    matched.append(k)
                j = len(pattern) - 1
            continue
        elif text[i+j]==pattern[j]:
            j=j-1
            if j==-1:
                Found=True
                print('pattern found at index {} of text'.format(i))
                i=i+marginJumping(pattern,0)
                for k in range(marginTable[0]):
                    matched.append(k)
                j=len(pattern)-1
        else:
            matched=[]
            pairedchar=getPairedChar(text,i+j)
            #print(pairedchar)
            paired,index=isInPair(pattern,pairedchar,j)
            if paired:
                if index==-1:
                    i=i+j
                    matched.append(0)
                else:
                    i+=j-matchedJumping(pattern,index)
                    matched.append(index)
                    matched.append(index+1)
            elif marginTable[j]!=0:
                i=i+marginJumping(pattern,j)
                for k in range(marginTable[j]):
                    matched.append(k)
            else:
                i=i+fullJumping(pattern,j)
            #print('paired={} and index={}'.format(paired,index))
            j = len(pattern) - 1
        comparisons += 1
    if not Found:
        print('Pattern Not found in Text')
    print('number of comparisons=', comparisons)


def main():
    global marginTable
    #text="bacxybaabababaxbaacaabacxaba"
    #pattern="bacxaba"
    #text="aaaaaaaaaaa"
    #pattern="aaaa"
    #text="abaaabcd"
    pattern="abc"
    #text="abcdefghi"
    #pattern="lmn"
    text=input('enter the text')
    pattern=input('enter the pattern')
    if len(pattern)==0:
        print('sorry enter pattern of length 1 atleast')
        exit(1)

    isStringFound(text,pattern)

main()
