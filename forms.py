#-*- coding: utf-8 -*-

from django import forms
from .models import restaurant, comments
from django.forms import Textarea
from django.db import models

# Restautrant registration form
class restaurantRegistrationForm(forms.ModelForm):
	class Meta:
		model = restaurant
		fields = ['fullname', 'location', 'specificLocation', 'typeOfFood', 'description']
		widgets = {
			'description': forms.Textarea(
				attrs = {
				'placeholder': '악의적인 비방 대신 솔직한 비판을 적어주세요!'
				}),
			'specificLocation': forms.TextInput(
				attrs = {
				'placeholder': '기타 지역 등록 시 꼭 써주세요!'
				}),
		}
		error_messages = {
            'fullname': {
                'required': '음식점 이름을 적어주세요!',
            },
            'description': {
            	'required': '음식점 설명을 적어주세요!',
            	'min_length': '조금 더 긴 설명(100자 이상)을 적어주세요!',
        	},
        }

    # Custom form field
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
	}

# Comment form
class commentForm(forms.ModelForm):
	class Meta:
		model = comments
		fields = ['comment']
		widgets = {
			'comment': forms.Textarea(
				attrs = {
				'placeholder': '악의적인 비방 대신 솔직한 비판을 적어주세요!'
				}),
		}
		error_messages = {
            'comment': {
                'required': '댓글을 적어주세요!',
            },
        }

    # Custom form field
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
	}







