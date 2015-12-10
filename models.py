#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Restaurant model
class restaurant(models.Model):

	# Location choice to choose from
	locationChoice = (
		('-- 서울 --',
			(
				('seoulgangnamstation', '강남'),
				# ('seoulapgujeong', '압구정'),
				('seoulgarosugil', '가로수길'),
				('seoulitaewon', '이태원'),
				# ('seoulchungdam', '청담'),
				('seoulsinchon', '신촌'),
				('seoulhongdae', '홍대'),
				# ('seoulseoraevillage', '서래마을'),
				# ('seoulinsadong', '인사동'),
				('seoulmyeongdong', '명동'),
				('seouldaehakro', '대학로'),
				# ('seouldongdaemun', '동대문'),
				('etcseoul', '기타 - 서울'),
			)
		),
		('-- 광주 --',
			(
				('cheomdan', '첨단'), 
				('suwan', '수완'),
				('terminal', '터미널'),
				('cheonnamunivchungjangro', '전남대 / 충장로'),
				# ('chosununiv', '조선대'),
				# ('sangmu', '상무'),
				('etcgwangju', '기타 - 광주')
			)
		),
		('-- 기타 --',
			(
				('etc', '기타'), 
			)
		),
	)

	# Type of food to choose from
	typeOfFoodChoice = (
		('korean', '한식'),
		('chinese', '중식'),
		('japanese', '일식'),
		('western', '양식'),
		('oriental', '동양식'),
		('boonsik', '분식'),
		('cafe', '카페'),
		('delivery', '야식'),
		('etc', '기타')
		)

	fullname = models.CharField('음식점 이름', max_length = 50)
	location = models.CharField('위치', max_length = 50, choices = locationChoice, default = 'Cheomdan')
	typeOfFood = models.CharField('음식 종류', max_length = 50, choices = typeOfFoodChoice, default = 'Korean')
	rating = models.IntegerField(null=True, blank=True)
	description = models.TextField('음식점 설명', max_length = 10000, validators = [MinLengthValidator(100)])
	specificLocation = models.CharField('상세 위치', max_length = 50, null=True, blank=True)
	user = models.CharField(max_length = 50)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)

	# To view in admin page
	def __unicode__(self):
		return self.fullname

# Comment form
class comments(models.Model):
	# requires a foreign key to relate to the restaurant model
	user = models.CharField(max_length = 50)
	comment = models.TextField('댓글', max_length = 10000)
	typeOfComment = models.NullBooleanField()
	restaurantPrimaryKey = models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)

	# To view in admin page
	def __unicode__(self):
		return self.comment

	# Override default django admin page plural
	class Meta:
		verbose_name_plural = 'comments'

# Model to store restaurants after change
class oldRestaurant(models.Model):

	fullname = models.CharField('음식점 이름', max_length = 50)
	previousFullname = models.CharField('이전 음식점 이름', max_length = 50)
	location = models.CharField('위치', max_length = 50)
	previousLocation = models.CharField('이전 위치', max_length = 50)
	specificLocation = models.CharField('상세 위치', max_length = 50, null=True, blank=True)
	previousSpecificLocation = models.CharField('상세 위치', max_length = 50, null=True, blank=True)
	typeOfFood = models.CharField('음식 종류', max_length = 50)
	previousTypeOfFood = models.CharField('이전 음식 종류', max_length = 50)
	description = models.TextField('음식점 설명', max_length = 1000)
	previousDescription = models.TextField('이전 음식점 설명', max_length = 1000)
	user = models.CharField(max_length = 50)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)

	# To view in admin page
	def __unicode__(self):
		return self.fullname

# Model to store comments after change
class oldComments(models.Model):
	# requires a foreign key to relate to the restaurant model
	user = models.CharField(max_length = 50)
	comment = models.TextField('댓글', max_length = 10000)
	previousComment = models.TextField('이전 댓글', max_length = 10000)
	typeOfComment = models.NullBooleanField()
	previousTypeOfComment = models.NullBooleanField()
	restaurantPrimaryKey = models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)

	# To view in admin page
	def __unicode__(self):
		return self.comment

	# Override default django admin page plural
	class Meta:
		verbose_name_plural = 'comments'