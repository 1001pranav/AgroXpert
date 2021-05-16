import csv;
from chatterbot import ChatBot
'''from chatterbot.trainers import ListTrainer

data=open("dataset.csv")
chatbots = ChatBot(name='AgroXpert', read_only=True,
                 logic_adapters=[
                     {
                         'import_path': 'chatterbot.logic.BestMatch',
                     'default_response': 'I am sorry, I do not understand. I am still learning. Please contact abc@xxx.com for further assistance.',
                     'maximum_similarity_threshold': 0.5

                         }])
trainer = ListTrainer(chatbots)
for item in csv.reader(data):
    trainer.train(item)
    print(item)

for row in csv.reader(data):
    print(row)'''
'''arr=[[1,2,3],[4,5,6],[7,8,9]]
col_len=len(arr[0])
row=0
col=0
row_len=len(arr)
for i in range(row_len*col_len):
    if col_len==col:
        row+=1
        col=0
    if row==row_len:
        break
    print(arr[row][col])
    col += 1'''
n=5
for i in range(1,n+1):
    point=i%n
    space=n-point
    if point==0:
        for _ in range(n):
            print("* " ,end=" ")
    else:
        if space%2==0:
            left = space // 2
            right = space // 2
        else:
            left=(space//2)-1
            right=(space//2)
        #print(left,right,space)
        for _ in range(left+1):
            print(" ",end=" ")
        for _ in range(point):
            print("* ",end=" ")
        for _ in range(right):
            print(" ",end=" ")
    print()
n=5
for i in range(n):
    for j in range(n):
        if i==0 or i==n-1 or j==0 or j==n-1:
            print("*",end="")
        else:
            print(" ",end="")
    print()