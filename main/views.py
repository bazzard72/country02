from django.shortcuts import render, redirect
from models import Country, Review
from forms import CreateCountryForm, CreateUserForm, SigninForm, CreateReviewForm, EditReviewForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime
# only for admin login
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def countrylist(request):
	context={}
	countries=Country.objects.all()
	context['country_list']=countries
	print context
	return render(request,'country_list.html',context)

def countrydetail(request, pk):
	context = {}
	country = Country.objects.get(pk=pk)
	context['country'] = country

	# return HttpResponse(country)
	context['form'] = CreateReviewForm()

	if request.method == 'POST':
		form = CreateReviewForm(request.POST)
		context['form']=form
		if form.is_valid():
			review = form.save(commit=False)
			review.date = datetime.now()
			review.country = country
			review.user = request.user
			review.save()
			return redirect('/countrylist/')

	return render(request, 'countrydetail.html', context)

@login_required
def createcountryform(request):
	context = {}
	context['form'] = CreateCountryForm()
	#print request.method
	if request.method == 'POST':
		#make sure form is valid
		form = CreateCountryForm(request.POST, request.FILES)
		context['form'] = form

		if form.is_valid():
			form.save()
		return render(request, 'countrycreated.html', context)
		#save form to database
	return render(request, 'CreateCountry.html', context)

def sign_up(request):
	context = {}
	context['form'] = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		context['form'] == form
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			#print username
			new_user = User.objects.create_user(username=username , password=password )
			new_user.save()

			auth_user = authenticate(username=username , password=password)
			login(request, auth_user)

			return redirect('/countrylist/')


	return render(request, 'Sign_Up.html', context)

def signin(request):
	context = {}
	context['form'] = SigninForm()

	if request.method == 'POST':
		form = SigninForm(request.POST)
		context['form'] == form
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			try:
				auth_user = authenticate(username=username , password=password)
				
				login(request, auth_user)

				return redirect('/countrylist/')

			except Exception, e:
				
				return HttpResponse('Wrong USERNAME or PASSWORD! Please <a href="/signin/">Try Again </a>')

	return render(request, 'Signin.html', context)

def signout(request):
	logout(request)
	return redirect('/countrylist/')

@login_required
def editreview(request, pk):
	context = {}
	review = Review.objects.get(pk=pk)

	if request.user == review.user:
		context['review'] = review
		form =  EditReviewForm(request.POST or None, instance=review)
		context['form'] = form

		if form.is_valid():
			form.save()
			return redirect('/countrylist/')
	else:
		return HttpResponse('USER ERROR')
	return render(request,'editreview.html',context)

@login_required
def deletereview(request, pk):
	review = Review.objects.get(pk=pk)

	if request.user == review.user:
		review.delete()

	return redirect('/countrylist/')