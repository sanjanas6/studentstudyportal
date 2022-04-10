from asyncio.base_futures import _FINISHED
from pyexpat.errors import messages
from turtle import title
from django.shortcuts import redirect, render
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
# Create your views here.
def home(request):
	return render(request,'dashboard/home.html')

def notes(request):
	if request.method == "POST":
		form = NotesForm(request.POST)
		if form.is_valid():
			notes = Notes(user=request.user,title=request.POST['title'],descripttion=request.POST['description'])
			notes.save()
		messages.success(request,f"Notes Added from {request.user.username} Successfully!")
	else:
			form=NotesForm()

	form = NotesForm()
	notes=Notes.objects.filter(user=request.user)
	context = {'notes':notes,'form':form}
	return render(request,'dashboard/notes.html',context)

def delete_note(request,pk=None):
	Notes.objects.get(id=pk).delete()
	return redirect("notes")
	
class NotesDetailView(generic.DetailView):
	model = Notes
	
def homework(request):
	if request.method == "POST":
		form = HomeworkForm(request.POST)
		if form.is_valid():
			try:
				finished = request.POST['is_finished']
				if finished == 'on':
					finished = True
				else:
				    finished = False
			except:
				finished = False
			homeworks = Homework(
				user = request.user,
				subject = request.POST['subject'],
				title = request.POST['title'],
				description = request.POST['description'],
			    due = request.POST['due'],
				is_finished = finished
			)
			homeworks.save()
			messages.success(request,f'Homework Added from {request.user.username}!!')
	else:
		form = HomeworkForm()
	homework = Homework.objects.filter(user=request.user)
	if len(homework)==0:
		homework_done = True
	else:
		homework_done = False
	context = {'homeworks':homework , 
	           'homeworks_done':homework_done,
	           'form':form}
	return render(request, 'dashboard/homework.html',context)


def update_homework(request,pk=None):
	homework = Homework.objects.get(id=pk)
	if homework.is_finished == True:
		homework.is_finished = True
	else:
		homework.is_finished = True
	homework.save()
	return redirect('homework')

def delete_homework(request,pk=None):
	Homework.objects.get(id=pk).delete()
	return redirect("homework")

def youtube(request):
	return render(request,"dashboard/youtube.html")

def youtube(request):
	if request.method == "POST":
		form = DashboardForm(request.POST)
		text = request.POST['text']
		video = VideosSearch(text,limit=10)
		result_list = []
		for i in video.result()['result']:
			result_dict = {
				'input':text,
				'title':i['title'],
				'duration':i['duration'],
				'thumbnails':i['thumbnails'][0]['url'],
				'channel':i['channel']['name'],
				'link':i['link'],
				'views':i['viewCount']['short'],
				'published':i['publishedTime'],
			}
			desc = ''
			if i['descriptionSnippet']:
				for j in i['descriptionSnippet']:
					desc += j['text']
			result_dict['description'] = desc
			result_list.append(result_dict)
			context={
				'form':form,
				'results':result_list
			}
		return render(request,'dashboard/youtube.html')

	else:
		form = DashboardForm()
	context = {'form':form}
	return render(request,"dashboard/youtube.html",context)

def todo(request):
	form = TodoForm()
	todo = Todo.objects.filter(user=request.user)
	context = {
		'form' :form,
		'todos':todo
		
	}
	return render(request, "dashboard/todo.html",context)

