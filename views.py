#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .forms import restaurantRegistrationForm, commentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import restaurant, comments, oldComments, oldRestaurant
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from login.models import nomatUser
from datetime import datetime
import time

# Determine what type of food the restaurant serves
def determineTypeOfFood(restaurantObject):
	if restaurantObject.typeOfFood == 'korean':
		typeOfFood = '한식'
	elif restaurantObject.typeOfFood == 'chinese':
		typeOfFood = '중식'
	elif restaurantObject.typeOfFood == 'japanese':
		typeOfFood = '일식'
	elif restaurantObject.typeOfFood == 'western':
		typeOfFood = '양식'
	elif restaurantObject.typeOfFood == 'oriental':
		typeOfFood = '동양식'
	elif restaurantObject.typeOfFood == 'boonsik':
		typeOfFood = '분식'
	elif restaurantObject.typeOfFood == 'cafe':
		typeOfFood = '카페'
	elif restaurantObject.typeOfFood == 'delivery':
		typeOfFood = '야식'
	else:
		typeOfFood = '기타'
	return typeOfFood

# Determine the location of the restaurant
def determineLocation(restaurantObject):
	if restaurantObject.location == 'cheomdan':
		location = '첨단'
	elif restaurantObject.location == 'suwan':
		location = '수완'
	elif restaurantObject.location == 'terminal':
		location = '터미널'
	elif restaurantObject.location == 'cheonnamunivchungjangro':
		location = '전남대 / 충장로'
	elif restaurantObject.location == 'etcgwangju':
		location = '기타 - 광주'
	elif restaurantObject.location == 'seoulgangnamstation':
		location = '강남'
	# elif restaurantObject.location == 'seoulapgujeong':
	# 	location = '압구정'
	elif restaurantObject.location == 'seoulgarosugil':
		location = '가로수길'
	elif restaurantObject.location == 'seoulitaewon':
		location = '이태원'
	# elif restaurantObject.location == 'seoulchungdam':
	# 	location = '청담'
	elif restaurantObject.location == 'seoulsinchon':
		location = '신촌'
	elif restaurantObject.location == 'seoulhongdae':
		location = '홍대'
	# elif restaurantObject.location == 'seoulseoraevillage':
	# 	location = '서래마을'
	# elif restaurantObject.location == 'seoulinsadong':
	# 	location = '인사동'
	elif restaurantObject.location == 'seoulmyeongdong':
		location = '명동'
	elif restaurantObject.location == 'seouldaehakro':
		location = '대학로'
	elif restaurantObject.location == 'etcseoul':
		location = '기타 - 서울'
	# elif restaurantObject.location == 'seouldongdaemun':
	# 	location = '동대문'
	# elif restaurantObject.location == 'chosununiv':
	# 	location = '조선대'
	# elif restaurantObject.location == 'sangmu':
	# 	location = '상무'
	elif restaurantObject.location == 'etc':
		location = '기타'
	return location

# Check for user conditions update
def checkForUpdates(request):

	if request.user.is_authenticated():
		nu = nomatUser.objects.get(email = request.user.email)
		if not nu.agreeToConditions:
			return redirect('/updateagreetoconditions')

# Main page view
def nomat(request):
	
	# Check for updates
	if checkForUpdates(request):
		return checkForUpdates(request)
	
	# Initialize area number count
	seoulCount = 0
	gwangjuCount = 0
	etcCount = 0

	# Empty list to store restaurant values
	restaurants = []

	# Loop through restaurant database to find matching restaurants
	for restaurantObj in restaurant.objects.all():
		if restaurantObj.location == 'seoulgangnamstation' or restaurantObj.location == 'seoulgarosugil' or restaurantObj.location == 'seoulitaewon' or restaurantObj.location == 'seoulsinchon' or restaurantObj.location == 'seoulhongdae' or restaurantObj.location == 'seoulmyeongdong' or restaurantObj.location == 'seouldaehakro' or restaurantObj.location == 'etcseoul':
			seoulCount += 1
		if restaurantObj.location == 'cheomdan' or restaurantObj.location == 'suwan' or restaurantObj.location == 'terminal' or restaurantObj.location == 'cheonnamunivchungjangro' or restaurantObj.location == 'etcgwangju':
			gwangjuCount += 1
		if restaurantObj.location == 'etc':
			etcCount += 1
		koreanLocation = determineLocation(restaurantObj)
		if len(restaurantObj.description) > 83:
			shortDescription = restaurantObj.description[0:82] + '...'
			restaurants.append([restaurantObj.pk, restaurantObj.fullname, koreanLocation, shortDescription, restaurantObj.rating, restaurantObj.location])
		else:
			restaurants.append([restaurantObj.pk, restaurantObj.fullname, koreanLocation, restaurantObj.description, restaurantObj.rating, restaurantObj.location])

	# Function to use sorted function below
	# Returns the 4th item in the list
	def getKey(item):
		return item[4]

	# Sort restaurants based on their rating
	sortedRestaurants = sorted(restaurants, key = getKey)

	# Get top 3 restaurants
	top3Restaurants = [sortedRestaurants[0], sortedRestaurants[1], sortedRestaurants[2]]

	# Context to display in html
	context = {
		'seoulRestaurantNumber': seoulCount,
		'gwangjuRestaurantNumber': gwangjuCount,
		'etcRestaurantNumber': etcCount,
		'top3Restaurants': top3Restaurants,
	}

	return render(request, 'nomat.html', context)

# nomat CITY
# Seoul page view
def nomatSeoul(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# Initialize count
	gangnamCount = 0
	garosugilCount = 0
	itaewonCount = 0
	sinchonCount = 0
	hongdaeCount = 0
	myeongdongCount = 0
	daehakroCount = 0
	etcSeoulCount = 0

	# Loop through the DB to find corresponding data
	for restaurantObj in restaurant.objects.all():
		if restaurantObj.location == 'seoulgangnamstation':
			gangnamCount += 1
		if restaurantObj.location == 'seoulgarosugil':
			garosugilCount += 1
		if restaurantObj.location == 'seoulitaewon':
			itaewonCount += 1
		if restaurantObj.location == 'seoulsinchon':
			sinchonCount += 1
		if restaurantObj.location == 'seoulhongdae':
			hongdaeCount += 1
		if restaurantObj.location == 'seoulmyeongdong':
			myeongdongCount += 1
		if restaurantObj.location == 'seouldaehakro':
			daehakroCount += 1
		if restaurantObj.location == 'etcseoul':
			etcSeoulCount += 1

	# Context to display with html
	context = {
		'gangnamRestaurantNumber': gangnamCount,
		'garosugilRestaurantNumber': garosugilCount,
		'itaewonRestaurantNumber': itaewonCount,
		'sinchonRestaurantNumber': sinchonCount,
		'hongdaeRestaurantNumber': hongdaeCount,
		'myeongdongRestaurantNumber': myeongdongCount,
		'daehakroRestaurantNumber': daehakroCount,
		'etcSeoulRestaurantNumber': etcSeoulCount,
	}

	return render(request, 'nomatSeoul.html', context)

# Gwangju page view
def nomatGwangju(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# Initialize count
	cheomdanCount = 0
	suwanCount = 0
	terminalCount = 0
	cheonnamunivchungjangroCount = 0
	etcGwangjuCount = 0

	# Loop through DB to find corresponding data
	for restaurantObj in restaurant.objects.all():
		if restaurantObj.location == 'cheomdan':
			cheomdanCount += 1
		if restaurantObj.location == 'suwan':
			suwanCount += 1
		if restaurantObj.location == 'terminal':
			terminalCount += 1
		if restaurantObj.location == 'cheonnamunivchungjangro':
			cheonnamunivchungjangroCount += 1
		if restaurantObj.location == 'etcgwangju':
			etcGwangjuCount += 1

	# Context to display with html
	context = {
		'cheomdanRestaurantNumber': cheomdanCount,
		'suwanRestaurantNumber': suwanCount,
		'terminalRestaurantNumber': terminalCount,
		'cheonnamunivchungjangroRestaurantNumber': cheonnamunivchungjangroCount,
		'etcGwangjuRestaurantNumber': etcGwangjuCount,
	}

	return render(request, 'nomatGwangju.html', context)

# etc page view
def etc(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)
		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'etc':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
	# Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Etc.',
		'location': '기타',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)


# nomat SEOUL AREA
# Gangnam area
def seoulGangnam(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'seoulgangnamstation':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
	# Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Gangnam Station',
		'location': '강남역',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# def seoulApgujeong(request):

# 	restaurantDic = {}

# 	for restaurantName in restaurant.objects.all():
# 		row = restaurant.objects.get(pk = restaurantName.pk)
# 		if row.location == 'seoulapgujeong':
# 			restaurantDic[row.pk] = (row.fullname, row.location, row.description, row.rating)

# 	context = {
# 		'location': '압구정',
# 		'restaurantDic': restaurantDic,
# 	}

# 	if request.method == 'POST':
# 		if 'signIn' in request.POST:
# 			return signInFunc(request)
# 		if 'signUp' in request.POST:
# 			return signUpFunc(request)
# 		if 'signOut' in request.POST:
# 			return signOutFunc(request)

# 	return render(request, 'nomatArea.html', context)

# Garosugil area
def seoulGarosugil(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'seoulgarosugil':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Garosugil',
		'location': '가로수길',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# Itaewon area
def seoulItaewon(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'seoulitaewon':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Itaewon',
		'location': '이태원',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# def seoulChungdam(request):

# 	restaurantDic = {}

# 	for restaurantName in restaurant.objects.all():
# 		row = restaurant.objects.get(pk = restaurantName.pk)
# 		if row.location == 'seoulchungdam':
# 			restaurantDic[row.pk] = (row.fullname, row.location, row.description, row.rating)

# 	context = {
# 		'location': '청담',
# 		'restaurantDic': restaurantDic,
# 	}

# 	if request.method == 'POST':
# 		if 'signIn' in request.POST:
# 			return signInFunc(request)
# 		if 'signUp' in request.POST:
# 			return signUpFunc(request)
# 		if 'signOut' in request.POST:
# 			return signOutFunc(request)

# 	return render(request, 'nomatArea.html', context)

# Sinchon area
def seoulSinchon(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'seoulsinchon':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Sinchon',
		'location': '신촌',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# Hongdae area
def seoulHongdae(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'seoulhongdae':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Hongdae',
		'location': '홍대',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# def seoulSeoraevillage(request):

# 	restaurantDic = {}

# 	for restaurantName in restaurant.objects.all():
# 		row = restaurant.objects.get(pk = restaurantName.pk)
# 		if row.location == 'seoulseoraevillage':
# 			restaurantDic[row.pk] = (row.fullname, row.location, row.description, row.rating)

# 	context = {
# 		'location': '서래마을',
# 		'restaurantDic': restaurantDic,
# 	}

# 	if request.method == 'POST':
# 		if 'signIn' in request.POST:
# 			return signInFunc(request)
# 		if 'signUp' in request.POST:
# 			return signUpFunc(request)
# 		if 'signOut' in request.POST:
# 			return signOutFunc(request)

# 	return render(request, 'nomatArea.html', context)

# def seoulInsadong(request):

# 	restaurantDic = {}

# 	for restaurantName in restaurant.objects.all():
# 		row = restaurant.objects.get(pk = restaurantName.pk)
# 		if row.location == 'seoulinsadong':
# 			restaurantDic[row.pk] = (row.fullname, row.location, row.description, row.rating)

# 	context = {
# 		'location': '인사동',
# 		'restaurantDic': restaurantDic,
# 	}

# 	if request.method == 'POST':
# 		if 'signIn' in request.POST:
# 			return signInFunc(request)
# 		if 'signUp' in request.POST:
# 			return signUpFunc(request)
# 		if 'signOut' in request.POST:
# 			return signOutFunc(request)

# 	return render(request, 'nomatArea.html', context)

# Myeongdong area
def seoulMyeongdong(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'seoulmyeongdong':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Myeongdong',
		'location': '명동',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# Daehakro area
def seoulDaehakro(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'seouldaehakro':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Daehakro',
		'location': '대학로',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# def seoulDongdaemun(request):

# 	restaurantDic = {}

# 	for restaurantName in restaurant.objects.all():
# 		row = restaurant.objects.get(pk = restaurantName.pk)
# 		if row.location == 'seouldongdaemun':
# 			restaurantDic[row.pk] = (row.fullname, row.location, row.description, row.rating)

# 	context = {
# 		'location': '동대문',
# 		'restaurantDic': restaurantDic,
# 	}

# 	if request.method == 'POST':
# 		if 'signIn' in request.POST:
# 			return signInFunc(request)
# 		if 'signUp' in request.POST:
# 			return signUpFunc(request)
# 		if 'signOut' in request.POST:
# 			return signOutFunc(request)

# 	return render(request, 'nomatArea.html', context)

# Other Seoul area
def etcSeoul(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'etcseoul':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Etc. Seoul',
		'location': '기타 - 서울',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# nomat GWANGJU AREA
# Cheomdan area
def cheomdan(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'cheomdan':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Cheomdan',
		'location': '첨단',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# Suwan area
def suwan(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'suwan':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Suwan',
		'location': '수완',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# Terminal area
def terminal(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'terminal':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Terminal',
		'location': '터미널',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# Cheonnam univ. area
def cheonnamunivchungjangro(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'cheonnamunivchungjangro':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Cheonnam Univ.',
		'location': '전남대 / 충장로',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# def chosununiv(request):

# 	restaurantDic = {}

# 	for restaurantName in restaurant.objects.all():
# 		row = restaurant.objects.get(pk = restaurantName.pk)
# 		if row.location == 'chosununiv':
# 			restaurantDic[row.pk] = (row.fullname, row.location, row.description, row.rating)

# 	context = {
# 		'location': '조선대',
# 		'restaurantDic': restaurantDic,
# 	}

# 	if request.method == 'POST':
# 		if 'signIn' in request.POST:
# 			return signInFunc(request)
# 		if 'signUp' in request.POST:
# 			return signUpFunc(request)
# 		if 'signOut' in request.POST:
# 			return signOutFunc(request)

# 	return render(request, 'nomatArea.html', context)

# def sangmu(request):

# 	restaurantDic = {}

# 	for restaurantName in restaurant.objects.all():
# 		row = restaurant.objects.get(pk = restaurantName.pk)
# 		if row.location == 'sangmu':
# 			restaurantDic[row.pk] = (row.fullname, row.location, row.description, row.rating)

# 	context = {
# 		'location': '상무',
# 		'restaurantDic': restaurantDic,
# 	}

# 	if request.method == 'POST':
# 		if 'signIn' in request.POST:
# 			return signInFunc(request)
# 		if 'signUp' in request.POST:
# 			return signUpFunc(request)
# 		if 'signOut' in request.POST:
# 			return signOutFunc(request)

# 	return render(request, 'nomatArea.html', context)

# Other Gwangju area
def etcGwangju(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store restaurant data
	restaurantList = []

	# Fill the list with appropriate data
	for restaurantName in restaurant.objects.all():
		row = restaurant.objects.get(pk = restaurantName.pk)

		# Truncate description of the restaurant so that it will be about 3 lines
		if row.location == 'etcgwangju':
			if len(row.description) > 83:
				shortDescription = row.description[0:82] + '...'
				restaurantList.append([row.pk, row.fullname, row.location, shortDescription, row.rating])
			else:
				restaurantList.append([row.pk, row.fullname, row.location, row.description, row.rating])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the restaurant list
	sortedList = sorted(restaurantList, key = getKey)

	# Context to display with html
	context = {
		'Location': 'Etc. Gwangju',
		'location': '기타 - 광주',
		'sortedList': sortedList,
	}

	return render(request, 'nomatArea.html', context)

# Restaurant registration page
@login_required()
def register(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# Get restaurant registration form
	form = restaurantRegistrationForm(request.POST or None)

	# Context to display with html
	context = {
		'header': 'nomat registration',
		'title': '나만의 노맛집 등록하기!',
		'subtitle': '기타 지역 등록 시 음식점 설명에 음식점 위치를 꼭 써주세요~',
		'form': form,
		'button': '등록하기'
	}

	# Save the form input
	if request.method == 'POST':
		if form.is_valid():
			for restaurantObj in restaurant.objects.all():
				m = restaurantObj.fullname
				n = form.cleaned_data.get('fullname')
				o = m.replace(' ', '')
				p = n.replace(' ', '')

				# Check for duplicates
				if o.lower() == p.lower():
					if restaurantObj.location == form.cleaned_data.get('location'):
						return render(request, 'nomatRegister.html', {
						'title': '이 장소에 같은 이름의 레스토랑이 존재합니다!',
						'form': form,
						'subsubtitle': '*이 있는 항목은 필수 항목입니다.',
						})

			# Save location for future use
			location = form.cleaned_data.get('location')

			form.save()

			# Get the restaurant just saved
			restaurantObj = restaurant.objects.filter(fullname = form.cleaned_data.get('fullname'))

			# Empty string to store location and type of food
			koreanLocation = ''
			koreanTypeOfFood = ''

			# Loop through restaurant object to get the specific restaurant just registered
			# Looping in case of duplicate names
			for obj in restaurantObj:
				if obj.location == location:
					obj.rating = -1
					obj.user = request.user.username
					koreanLocation = determineLocation(obj)
					koreanTypeOfFood = determineTypeOfFood(obj)
					obj.save()

			# Context to display with html with restaurant that has specific location
			if form.cleaned_data.get('specificLocation') == '':
				context = {
					"title": "노맛집 등록 완료!",
					"subtitle": "악의적인 의도가 있을 시 관리자 검토 후 노맛집이 삭제 될 수 있습니다.",
					"bodyContent": "내용을 다시 한 번 확인해주세요!",
					"restaurantName": '음식점 이름: %s' % form.cleaned_data.get('fullname'),
					"location": '위치: %s' % koreanLocation,
					"typeOfFood": '음식 종류: %s' % koreanTypeOfFood,
					"description": '설명: %s' % form.cleaned_data.get('description'),
				}

			# Context to display with html with restaurant without specific location
			else:
				context = {
					"title": "노맛집 등록 완료!",
					"subtitle": "악의적인 의도가 있을 시 관리자 검토 후 노맛집이 삭제 될 수 있습니다.",
					"bodyContent": "내용을 다시 한 번 확인해주세요!",
					"restaurantName": '음식점 이름: %s' % form.cleaned_data.get('fullname'),
					"location": '위치: %s' % koreanLocation,
					"specificLocation": '상세 위치: %s' % form.cleaned_data.get('specificLocation'),
					"typeOfFood": '음식 종류: %s' % koreanTypeOfFood,
					"description": '설명: %s' % form.cleaned_data.get('description'),
				}

			# Send mail to admin about restaurant registration
			mail_message = """
아이디: %s

이메일: %s

음식점 이름: %s

위치: %s

상세 위치: %s

음식 종류: %s

음식점 설명: %s
			""" % (request.user.username, request.user.email, form.cleaned_data.get('fullname'), form.cleaned_data.get('location'), form.cleaned_data.get('specificLocation'), form.cleaned_data.get('typeOfFood'), form.cleaned_data.get('description'))

			send_mail('레스토랑 등록 알림', mail_message, 'splitterapps@gmail.com', ['splitterapps@gmail.com'], fail_silently=False)

			return render(request, 'nomatRegistered.html', context)

	return render(request, 'form.html', context)

# Restaurant page view
def restaurantDatabase(request, primaryKey):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# List to store comments
	restaurantCommentList = []

	# Get restaurant information
	restaurantObj = restaurant.objects.get(pk = primaryKey)
	restaurantName = restaurantObj.fullname
	description = restaurantObj.description
	specificLocation = restaurantObj.specificLocation

	# Determine type of food and the location in Korean
	typeOfFood = determineTypeOfFood(restaurantObj)
	location = determineLocation(restaurantObj)

	# Get comment form
	commentFormForm = commentForm(request.POST or None)

	# Registering comment
	if request.method == 'POST':
		if commentFormForm.is_valid():
			if request.user.is_authenticated():
				for comment in comments.objects.filter(restaurantPrimaryKey = primaryKey):
					if comment.user == request.user.username:
						url = request.build_absolute_uri()
						return redirect('/commentError')

				commentFormForm.save()

				# Get the previous comment
				row = comments.objects.get(comment = request.POST['comment'])
				row.user = request.user.username
				row.restaurantPrimaryKey = primaryKey

				# Change the rating of the restaurant
				if 'positiveComment' in request.POST:
					row.typeOfComment = False
					restaurantObj.rating += 1
					restaurantObj.save()
				else:
					row.typeOfComment = True
					restaurantObj.rating -= 1
					restaurantObj.save()
				row.save()

				#send mail
				mail_message = """
아이디: %s

이메일: %s

음식점 이름: %s

위치: %s

상세 위치: %s

음식 종류: %s

댓글: %s
			""" % (request.user.username, request.user.email, restaurantName, restaurantObj.location, restaurantObj.specificLocation, restaurantObj.typeOfFood, row.comment)

				send_mail('댓글 등록 알림', mail_message, 'splitterapps@gmail.com', ['splitterapps@gmail.com'], fail_silently=False)

				url = request.build_absolute_uri()
				return redirect(url)

			else:
				return redirect('/loginrequired')

	# Save restaurant rating
	rating = restaurantObj.rating

	# Loop through the comment DB to find matching comments for this restaurant
	for comment in comments.objects.filter(restaurantPrimaryKey = primaryKey):
		if comment.user == request.user.username:
			restaurantCommentList.append([comment.id, comment.comment, comment.typeOfComment, True, restaurantObj.id])
		else:
			restaurantCommentList.append([comment.id, comment.comment, comment.typeOfComment, False])

	# Function to use in sorted function below
    # Returns the primary key of the restaurant
	def getKey(item):
		return item[0]

	# Sort the comment list
	sortedList = sorted(restaurantCommentList, key = getKey)

	# Check to see if the user is the originial writer
	if request.user.username == restaurantObj.user:
		userIs = True
	else:
		userIs = False

	# Context to display with html
	context = {
		'restaurantName': restaurantName,
		'location': location,
		'specificLocation': specificLocation,
		'typeOfFood': typeOfFood,
		'description': description,
		'sortedList': sortedList,
		'rating': rating,
		'commentForm': commentFormForm,
		'userIs': userIs,
		'restaurantPk': primaryKey
	}

	return render(request, 'restaurantData.html', context)

# Search page view
def restaurantSearch(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)

	# Empty dictionary to store restaurant data
	restaurantDic = {}

	# Finding the restaurant
	if request.method == 'POST':

		# Loop through restaurant DB
		for restaurantObj in restaurant.objects.all():
			m = restaurantObj.fullname
			n = request.POST['restaurantSearch']
			o = m.replace(' ', '')
			p = n.replace(' ', '')

			if p.lower() in o.lower():
				# Type of food and location in Korean
				typeOfFood = determineTypeOfFood(restaurantObj)
				location = determineLocation(restaurantObj)

				# Store informatin for display
				restaurantDic[restaurantObj.pk] = (restaurantObj.fullname, location, restaurantObj.rating, typeOfFood, restaurantObj.location.lower())

		# Context to display with html
		context = {
			'restaurantDic': restaurantDic,
		}

		return render(request, 'searchPage.html', context)

	return render(request, 'searchPage.html', {})

# Comment error page view
@login_required
def commentError(request):

	# Check for user conditions update
	if checkForUpdates(request):
		return checkForUpdates(request)
		
	# Context to display with html
	context = {
		'header': 'Error',
		'title': '이미 이 노맛집에 댓글을 다셨습니다.',
		'subtitle': '악의적인 활동을 막기 위해 한 노맛집에는 한번만 댓글을 다실 수 있으니 이해해 주시기 바랍니다.',
	}
	return render(request, 'jumbotronOnly.html', context)

# Restaurant edit page view
@login_required
def editRestaurant(request, restaurantPk):

	# Get the restaurant in interest
	restaurantObj = restaurant.objects.get(pk = restaurantPk)

	# Check to see if the request is valid
	if not restaurantObj.user == request.user.username:
		context = {
			'header': 'Error',
			'title': '음식점을 등록한 유저만이 수정할 수 있습니다!',
		}
		return (request, 'jumbotronOnly.html', context)

	# Get restaurant registration form
	form = restaurantRegistrationForm(request.POST or None)

	# Initialize values with original information
	form.fields['fullname'].initial = restaurantObj.fullname
	form.fields['location'].initial = restaurantObj.location
	form.fields['specificLocation'].initial = restaurantObj.specificLocation
	form.fields['typeOfFood'].initial = restaurantObj.typeOfFood
	form.fields['description'].initial = restaurantObj.description

	# Context to display with html
	context = {
		'header': 'Change',
		'title': "'%s' 수정" % restaurantObj.fullname,
		'subtitle': '악의적인 비방 대신 솔직한 비판을 적어주세요!',
		'form': form,
		'button': '수정',
	}

	# Save the old information in oldRestaurant and save the new information
	if request.method == 'POST':
		if form.is_valid():
			oldRestaurantObj = oldRestaurant(fullname = form.cleaned_data.get('fullname'), previousFullname = restaurantObj.fullname, location = form.cleaned_data.get('location'), previousLocation = restaurantObj.location, specificLocation = form.cleaned_data.get('specificLocation'), previousSpecificLocation = restaurantObj.specificLocation, typeOfFood = form.cleaned_data.get('typeOfFood'), previousTypeOfFood = restaurantObj.typeOfFood, description = form.cleaned_data.get('description'), previousDescription = restaurantObj.description, user = restaurantObj.user)
			oldRestaurantObj.save()

			restaurantObj.fullname = form.cleaned_data.get('fullname')
			restaurantObj.location = form.cleaned_data.get('location')
			restaurantObj.specificLocation = form.cleaned_data.get('specificLocation')
			restaurantObj.typeOfFood = form.cleaned_data.get('typeOfFood')
			restaurantObj.rating = restaurantObj.rating
			restaurantObj.description = form.cleaned_data.get('description')
			restaurantObj.user = request.user.username
			restaurantObj.updated = datetime.now()

			restaurantObj.save()

			#send mail
			mail_message = """
아이디: %s

이메일: %s

음식점 이름: %s

위치: %s

상세 위치: %s

음식 종류: %s

설명: %s
		""" % (request.user.username, request.user.email, restaurantObj.fullname, restaurantObj.location, restaurantObj.specificLocation, restaurantObj.typeOfFood, restaurantObj.description)

			send_mail('음식점 수정 알림', mail_message, 'splitterapps@gmail.com', ['splitterapps@gmail.com'], fail_silently=False)

			return redirect('/%s/%s' % (restaurantObj.location, restaurantPk))

	return render(request, 'form.html', context)

# Comment edit page view
@login_required
def editComment(request, restaurantPk, commentPk):

	# Get restaurant and comment in interest
	restaurantObj = restaurant.objects.get(pk = restaurantPk)
	commentObj = comments.objects.get(pk = commentPk)

	# Check if the request is valid
	if not commentObj.user == request.user.username:
		context = {
			'header': 'error',
			'title': '댓글을 등록한 유저만이 수정할 수 있습니다!'
		}
		return (request, 'jumbotronOnly.html', context)

	# T1 = time.mktime(commentObj.timestamp.timetuple())
	# T2 = time.mktime(datetime.now().timetuple())

	# if int(T2-T1) / 60 > 10:
	# 	context = {
	# 		'error': '댓글 등록 후 10분이 지났기 때문에 수정하실 수 없습니다.',
	# 		'subtitle': '불가피하게 수정하셔야 하신다면 아래 Contact Us를 통해 연락해 주시기 바랍니다.',
	# 	}
	# 	return render(request, 'error.html', context)

	# Get comment form
	form = commentForm(request.POST or None)

	# Initialize with original values
	form.fields['comment'].initial = commentObj.comment

	# Context to display with html
	context = {
		'title': "'%s' 댓글 수정" % restaurantObj.fullname,
		'subtitle': '악의적인 비방 대신 솔직한 비판을 적어주세요!',
		'form': form,
	}

	# Save the old comment and save the new information
	if request.method == 'POST':
		if form.is_valid():
			oldCommentObj = oldComments(user = commentObj.user, comment = form.cleaned_data.get('comment'), previousComment = commentObj.comment, typeOfComment = commentObj.typeOfComment, previousTypeOfComment = commentObj.typeOfComment, restaurantPrimaryKey = commentObj.restaurantPrimaryKey)
			oldCommentObj.save()

			commentObj.comment = form.cleaned_data.get('comment')
			commentObj.user = request.user.username
			commentObj.restaurantPrimaryKey = restaurantPk
			commentObj.updated = datetime.now()

			if 'positiveComment' in request.POST:
				if commentObj.typeOfComment == True:
					commentObj.typeOfComment = False
					restaurantObj.rating += 2
					restaurantObj.save()
			else:
				if commentObj.typeOfComment == False:
					commentObj.typeOfComment = True
					restaurantObj.rating -= 2
					restaurantObj.save()

			oldCommentObj.typeOfComment = commentObj.typeOfComment
			commentObj.save()
			oldCommentObj.save()

			#send mail
			mail_message = """
아이디: %s

이메일: %s

음식점 이름: %s

위치: %s

음식 종류: %s

이전 댓글: %s

새로운 댓글: %s
		""" % (request.user.username, request.user.email, restaurantObj.fullname, restaurantObj.location, restaurantObj.typeOfFood, oldCommentObj.previousComment, commentObj.comment)

			send_mail('댓글 수정 알림', mail_message, 'splitterapps@gmail.com', ['splitterapps@gmail.com'], fail_silently=False)

			return redirect('/%s/%s' % (restaurantObj.location, restaurantPk))

	return render(request, 'editComment.html', context)