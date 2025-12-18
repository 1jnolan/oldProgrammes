#Open your file
file=open("TheFellowshipOfTheRing.txt","r")
dataIn=file.read()
file.close

    
#Split the data
b=dataIn.split(" ")

import statistics
list1=[]
list2=[]
string1=()
word=input("enter a word")
file=open("TheFellowshipOfTheRing.txt","r")
dataIn=file.read()
list2=dataIn.split()
wordcount1=list2.count(word)
print(wordcount1)

#Clean the data of unwanted symbols
c=[]
for i in b:      
    if "," in i:
        c.append(i.replace(",",""))
    elif "." in i:
        c.append(i.replace(".",""))
    
    elif "-" in i:
        c.append(i.replace("-",""))
    else:
        c.append(i)
#get rid of small words:
d=[]
for i in c:    
    if len(i)>0:
        d.append(i)

#Get a list of each word just once.
xdoubles=[] #A list of NO doubles.
for item in d:
    if item not in xdoubles:
        xdoubles.append(item)

#Now count the number of times each item in xdoubles happens in c
wFc=[] #wFc = word frequency count.
for words in xdoubles:
    total=d.count(words)
    wFc.append(total)


mostFreq=max(wFc)
mostcommonwordIndex=wFc.index(mostFreq)
mostFreqWord=xdoubles[mostcommonwordIndex]
print("Most common word is:", mostFreqWord)
print("It occurs:", mostFreq, "times")

wordcheck=(input("Enter a word:"))
UserWordIndexLoc=[]
thismanytimes=[]
for item in xdoubles:
    if wordcheck in xdoubles:
        UserWordIndexLoc=xdoubles.index(wordcheck)
        thismanytimes=wFc.index(UserWordIndexLoc)
        print("The word:", wordcheck, "occurs", thismanytimes, "times")
    else:
        print("The word is not in the book")
