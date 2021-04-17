from django.http import JsonResponse
import csv
import sqlite3 as sql
import csv
conn=sql.connect('db.sqlite3')
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
set_pairs = [#vandana
            ['hello','Hi i am Agroxpert the Farmer\'s expert chatbot, How May i Help you?'],
             ['quit','I am always there at your service'],
["How many varieties of rice are grown in India?","Approximately 6,000 different varieties,But we have also lost tens thounsands of varieties from last 40 years"],
["which is the most popular rice grown in India?",'Basumati rice'],
["what is the history behind basumati","In 1997 American got patent over basumati rice by biopiracy"],
['what is  biopiracy?','Biopiracy is the commercial exploitation of naturally occurring biochemical or genetic material, without proper authorisation is known as biopiracy'],
['How many varieties of basumati are documented?','27 types of basumati rice are documented'],
['what is the life span of paddy?','It is  perennial plant which lives for more than 2 years'],
['In which month paddy is harvested?','In November-December the paddy should be harvested'],
['In which month paddy should be grown','we should start cultivating paddy in the month of june-july'],
['How long does it take to harvest paddy?','It normally takes 3 months to harvest paddy'],
['how is rice stored after harvesting?',' it should be threshed immediately after harvesting and maintain it by storing the grains at ambient temperature and Humidity <60% in dedicated area'],
['How to protect the rice from pest?','Using pesticides or by packing the well treated, quality rice'] ,
['what should we do after harvesting?','After harvesting it should be dried to certain duration,in certain temperature and store it.Delays in drying, incomplete drying or ineffective drying will reduce grain quality and result in losses'],
['why are paddy fields drained?','Mid-season drainage reduces methane emissions of paddy fields, with reductions ranging from 7 to 95%'],
['when is paddy fields drained?','About 7 days towards the end of tillering in the middle of the season'],
['what are the steps taken to grow paddy?','preparation of fields,transplantations or seedling,field maintenance,threshing,winnowing and milling'],
['How field is prepared for growing paddy?','Removal of weeds,ploughing the field,adding mannures and fertilizers,covered with water of about 2.5 cm,seedling'],
['How seedling is done?','Sown directly in the field and the seedlings sprout when the rain comes'],
['How is seedling  done?','Sown directly in the field and the seedlings sprout when the rain comes'],
['how is transplating of seed is done?','Manual transplanting is done either at random or in straight-rows'],
['what is random transplanting method?','seedlings are transplanted without a definite distance or space between plants'],
['what is straight-row transplanting?','The straight-row method follows a uniform spacing between plants'],
]


data=open("dataset.csv")
#creating a new chatbot
chatbots = ChatBot(name='AgroXpert', read_only=True,
                 logic_adapters=[
                     {
                         'import_path': 'chatterbot.logic.BestMatch',
                     'default_response': 'I am sorry, I do not understand. I am still learning. Please contact abc@xxx.com for further assistance.',
                     'maximum_similarity_threshold': 0.5

                         }])
trainer = ListTrainer(chatbots)
#for item in csv.reader(data):
for item in set_pairs:
    trainer.train(item)
    print(item)
# Create your views here.
from django.shortcuts import render

# Create your views here.
def Home(request):
    if request.method=="POST" and request.POST['check']=="Admin":
        return (AddQuestion(request))
    else:
        return Chatbot(request)
def Chatbot(request):
    print("req")
    Reply=""
    query=""
    response={}
    if request.method=="POST":

        query=request.POST["Search"]
        Reply=chatbots.get_response(query)
        print(query,Reply)
        data=str(Reply)
        print(type(data))
    return JsonResponse({'query':query,'Reply':data})
def AddQuestion(request):

    if request.method=='POST':
        method=request.POST
        set_pairs.append([method["question"],method["answer"]])
    return(render(request,'administrator.html',{"qna":set_pairs}))