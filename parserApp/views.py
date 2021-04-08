from django.shortcuts import render
import requests
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
	context = {}
	if request.method == 'POST':
		l1=[]
		l2 = []
		url = request.POST.get('url')
		cookie = request.POST.get('cookie')
		# cook = request.POST.get('cookies')
		# if cook != '' and cook != None:
		# 	cookie=cook
		# else:
		# 	cookie = {}
		if url != '' and url != None:
			if cookie != '' and cookie != None:
				cookD={}
				for y in cookie.split(' '):
					cookD[str(y.split('=')[0])]=y.split("=")[1][:-1]
				r=requests.get(url, cookies=cookD)
			else:
				r=requests.get(url)
			# print(cookie)
			if r.status_code == 200:
				count=0
				q = re.findall('((?://|/|https://|http://|file://|[a-zA-Z]+)([a-zA-Z\-\_\/0-9\.]+)\.js){1}', str(r.content.decode('utf-8')))
				for x in q:
					# print(x[0])
					if 'http' in x[0]:
						l2.append(x[0].strip('/'))
						# print(x)
					else:
						l1.append(x[0].strip('/'))
						# count += 1
					# print(x[0].strip('/'))
				context['data'] = l1
				context['data1'] = l2
				context['url'] = url.strip('/')
			else:
				context['message'] = 'invalid data supplied'
		else:
			context['message'] = 'invalid data supplied'
	return render(request, 'parserApp/index.html', context)


@csrf_exempt
def check(request):
	context = {}
	l1 = []
	if request.is_ajax():
		url = request.POST.get('url')
		subd = request.POST.get('subd')

		if ('http://' in subd or 'https://' in subd):
			final = subd
		else:
			final=url.strip('/')+ '/' + subd.strip('/')
		context['final'] = final

		if final != '' and final != None:
			r=requests.get(final)
			if r.status_code == 200:
				count=0
				q = re.findall('(//|/|\.\/|http://|https://|smb://|file://)([a-z\-\_\/0-9\.]+)', str(r.content.decode('utf-8')))
				for x in q:
					print(''.join(x))
					# print(''.join(x))
					if ''.join(x).strip() != '/' or ''.join(x).strip() != '//':
						l1.append(''.join(x))
						# print(x[0])
						l1.append('<p>')
				context['resultData'] = ''.join(l1)
			else:
				context['resultData'] = 'file not found.'
		else:
			context['resultData'] = 'invalid data supplied'

		# context['resultData'] = q
		return JsonResponse(context)




# (//|/|\_|\.\/|smb:|https://|http://|file://)([a-z\-\_\/0-9]+)