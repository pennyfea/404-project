
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post
from posts.forms import PostForm
from users.models import User
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

from .forms import ProfileChangeForm as changeForm

from django.urls import reverse

from friends.views import follows

import requests
import re



# TODO: use the REST API once it is established
def home(request):

	# TODO: If the user is not authenticated then don't show the home page,
	# but instead show soe other page reporting the error. (Maybe just the login page).

	# Searches for content
	# Needs to search for user name as well
	# Needs a way to show the searched results
	# Should use pagination
	###################################################################################
	queryset_list = Post.objects.all()
	query = request.GET.get("query")
	if query:
		queryset_list = queryset_list.filter(content__icontains=query)
		print("These are the q's", queryset_list)
	#####################################################################################

	if request.method == "POST":

		#Validate user github?
		#make call to Github API
		build_request = 'https://api.github.com/users/' + request.user.github + '/events'
		r=requests.get(build_request)
		response = r.json()
		#print(response)
		events =[]
		for event in response:
			#parse through output of API call and formulate into coherent message
			event_type = ''
			#Parse event type into multiple words
			#eg: PushEvent -> Push event
			for word in re.findall('[A-Z][^A-Z]*', event['type']):
				event_type += word + ' '
			#Parse date into more readbale format
			#https://stackoverflow.com/questions/18795713/parse-and-format-the-date-from-the-github-api-in-python
			#Credit: IQAndreas (https://stackoverflow.com/users/617937/iqandreas)
			date = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
			event_datetime = date.strftime('%A %b %d, %Y at %H:%M GMT')
			#Parse url
			event_repo = 'https://github.com/' + event['repo']['name']
			message = "You had a " + event_type + 'on ' + event_datetime + ' for repo ' + event_repo
			events.append(message)

		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.publish = datetime.now()
			instance.save()
		queryset = list(Post.objects.all().order_by("-timestamp"))
		queryset.extend(events)
		user = request.user

		context = {
			"object_list": queryset,
			"user": user,
			"form": form,
			"events": events
		}
	else:

		#Validate user github?
		#make call to Github API
		build_request = 'https://api.github.com/users/' + request.user.github + '/events'
		r=requests.get(build_request)
		response = r.json()
		#print(response)
		events =[]
		for event in response:
			#parse through output of API call and formulate into coherent message
			event_type = ''
			#Parse event type into multiple words
			#eg: PushEvent -> Push event
			for word in re.findall('[A-Z][^A-Z]*', event['type']):
				event_type += word + ' '
			#Parse date into more readbale format
			#https://stackoverflow.com/questions/18795713/parse-and-format-the-date-from-the-github-api-in-python
			#Credit: IQAndreas (https://stackoverflow.com/users/617937/iqandreas)
			date = datetime.datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
			event_datetime = date.strftime('%A %b %d, %Y at %H:%M GMT')
			#Parse url
			event_repo = 'https://github.com/' + event['repo']['name']
			message = "You had a " + event_type + 'on ' + event_datetime + ' for repo ' + event_repo
			events.append(message)

		form = PostForm()
		user = request.user
		queryset = list(Post.objects.all().order_by("-timestamp"))
		#queryset = list(queryset)
		queryset.extend(events)
		context = {
			"object_list": queryset,
			"user": user,
			"form": form,
			"events": events
		}

	return render(request, "home.html", context)


def profile(request, pk = None):

	if not request.user.is_authenticated:
		return HttpResponseForbidden()

	# If no pk is provided, just default to the current user's page
	if pk is None:
		pk = request.user.id

	try:
		user = User.objects.get(pk=pk)
	except ObjectDoesNotExist:
		# TODO: Return a custom 404 page
		return HttpResponseNotFound("That user does not exist")

	# Check if we follow the user whose profile we are looking at
	following = False
	if request.user.id is not pk:
		following = follows(request.user.id, pk)

	return render(request, 'profile.html', {'user': user, 'following': following})


def edit_profile(request):
	
	if not request.user.is_authenticated:
		return HttpResponseForbidden()

	#if they submitted new changes create change form
	if request.method == "POST":
		form = changeForm(request.POST,instance=request.user)
	   
		#check for validity of entered data. save to db if valid and redirect
		# back to profile page
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('http://127.0.0.1:8000/home/profile/') #TODO need to fix this so not hardcoded
		
		#TODO else statement when form isn't valid

	#if not POST, then must be GET'ing the form itself. so pass context
	else:
		form = changeForm(instance=request.user,initial={'first_name':request.user.first_name,
														'last_name':request.user.last_name,
														'email':request.user.email,
														'github':request.user.github})
		
		context = {'form':form}
		return render(request,'profileEdit.html',context)

