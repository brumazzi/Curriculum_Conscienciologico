# *-* coding: utf-8 *-*
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail as sm
#import ctypes

import datetime as dt

from .models import Author ,School, Education, Jobs, Projects, Lectures

#lib = ctypes.cdll.LoadLibrary("./sendmail.so")

no_login_menu = [
    {'href':'/', 'icon':'fontawesome-home', 'text':'Home'},
    {'href':'/register', 'icon':'fontawesome-signin', 'text':'Registrar'},
    {'href':'/search', 'icon':'fontawesome-search', 'text':'Buscar'},
]

login_menu = [
    {'href':'/', 'icon':'fontawesome-home', 'text':'Home'},
    {'href':'/curriculum', 'icon':'fontawesome-file-alt', 'text':'Curriculo'},
    {'href':'/search', 'icon':'fontawesome-search', 'text':'Buscar'},
    {'href':'/logout', 'icon':'fontawesome-off', 'text':'Logout'},
]

curr_items = [
    {'descr':'Meus Dados', 'icon':'fontawesome-edit', 'form':'author', 'memo':'Mantenha os dados de seu currículo atualizados.'},
    {'descr':'Escolaridade', 'icon':'fontawesome-plus', 'form':'school', 'memo':'Informe em quais instituições você estudou.','icon_edit':'fontawesome-pencil'},
    {'descr':'Meus Cursos', 'icon':'fontawesome-plus', 'form':'education', 'memo':'Diga suas especializações e cursos.','icon_edit':'fontawesome-pencil'},
    {'descr':'Experiencia', 'icon':'fontawesome-plus', 'form':'jobs', 'memo':'Informe os lugares onde você trabalhou.','icon_edit':'fontawesome-pencil'},
    {'descr':'Projetos', 'icon':'fontawesome-plus', 'form':'projects', 'memo':'Registre seus tramalhos e artigos.','icon_edit':'fontawesome-pencil'},
    {'descr':'Palestras,...', 'icon':'fontawesome-plus', 'form':'lecture', 'memo':'Registre palestras e cursos aqui','icon_edit':'fontawesome-pencil'},
]

def index(request):
    define_session_keys(request)
    Menu = (lambda x: login_menu if x else no_login_menu)(request.session['user'])
    if request.session['user']:
        uid = int(request.session['user'].split('|')[0])
        at,ed,jb,pj,sc,le = get_curriculum(uid)
        return render(request, 'home.html', {'menu':Menu,'self':at,'school':sc,'education':ed,'projects':pj,'jobs':jb,'lecture':le})
    if request.method == 'POST':
        login = request.POST['login']
        passwd = request.POST['passwd']
        
        try:
            a = Author.objects.get(login=login, password=passwd)
        except:
            return render(request, 'login.html', {'menu':Menu,'error':'Login e/ou Senha Inválidos!'})

        request.session['user'] = "%i|%s" %(a.id, str(a))
        return redirect('home')
    res = send_mail(request);
    if res == 1:
        return render(request, 'login.html', {'menu':Menu,'error':"E-mail enviado para %s!" % request.GET['email']})
    elif res == 2:
        return render(request, 'login.html', {'menu':Menu,'error':"E-mail inálido!"})

    return render(request, 'login.html', {'menu':Menu})

def register(request):
    define_session_keys(request)
    Menu = (lambda x: login_menu if x else no_login_menu)(request.session['user'])
    if request.session['user']:
        return redirect('home')
    if request.method == 'POST':
        post = request.POST
        name = post['name']
        login = post['login']
        email = post['email']
        passwd = post['passwd']
        passre = post['passwd_re']
        date = post['niver']
        del(post)

        try:
            Author.objects.get(email=email)
	    Author.objects.get(login=login)
	    return render(request, 'register.html', {'menu':Menu,'error':'E-mail ou Login já existente'})
        except: pass

        if passwd != passre:
            return render(request, 'register.html', {'menu':Menu,'error':'Senhas diferentes.'})

        now = dt.datetime.now()
        new = Author()
        new.name = name
        new.email = email
        new.login = login
        new.password = passwd
        new.register = "%i/%i/%i" %(now.day, now.month, now.year)
        new.niver = date
        new.save()
        
        return redirect('home')
    return render(request, 'register.html', {'menu':Menu})

def view(request, offset):
    define_session_keys(request)
    Menu = (lambda x: login_menu if x else no_login_menu)(request.session['user'])
    at,ed,jb,pj,sc,le = get_curriculum(int(offset))
    return render(request, 'home.html', {'menu':Menu,'self':at,'school':sc,'education':ed,'projects':pj,'jobs':jb,'lecture':le})

def logout_view(request):
    define_session_keys(request)
    if request.session['user']:
        request.session['user'] = None
    return redirect('home')

def search(request):
    define_session_keys(request)
    Menu = (lambda x: login_menu if x else no_login_menu)(request.session['user'])
    if request.method == 'POST':
        opt = request.POST['radio']
        key = request.POST['keys']
        obs = Author.objects
        if opt == '1':
            auth = obs.order_by('name').filter(name__contains=key)#,middle_name__contains=key,last_name__contains=key)
            res = auth
        elif opt == '2':
            now = dt.datetime.now()
            year = now.year - int(key)
            auth = obs.order_by('name').filter(niver__contains=str(year))
            res = auth
        elif opt == '3':
            auth = obs.order_by('name').filter(name__contains=key)
            res = [{'author':auth[x],'articles':Projects.objects.filter(author=auth[x])} for x in range(len(auth))]
        elif opt == '4':
            artc = Projects.objects.filter(title__contains=key)
            res = artc
        elif opt == '5':
            artc = Projects.objects.filter(char_key__contains=key)
            res = artc
        if len(res) != 0:
            return render(request, 'search.html', {'menu':Menu,'detect':int(opt),'data':res})
        else:
            return render(request,'search.html',{'menu':Menu,'error':'Nenhuma informação encontrada.'})
    return render(request,'search.html',{'menu':Menu})

def curriculum(request):
    define_session_keys(request)
    Menu = (lambda x: login_menu if x else no_login_menu)(request.session['user'])
    if not request.session['user']:
        return redirect('home')

    if(request.method == 'GET' and 'form' in request.GET):
        form = request.GET['form']
        if form == 'author':
            auth = Author.objects.get(id=int(request.session['user'].split('|')[0]))
            fields = ['niver','nation','country','city','district','address','number','complement','phone','cell1','cell2','email','CEP']
            box = {}
            for x in fields:
                box[x] = (lambda(r): '' if not r else r)(auth.__getattribute__(x))
            return render(request,"form/%s.html" % form,{'menu':Menu,'box':box});
        return render(request,"form/%s.html" % form,{'menu':Menu});

    if request.method == 'POST':
        post = request.POST
        uid = int(request.session['user'].split('|')[0])
        if post['form_action'] == 'author':
            fields = ['nation','country','city','district','address','number','complement','phone','cell1','cell2','CEP']
            reg = Author.objects.get(id=uid)
        elif post['form_action'] == 'education':
            fields = ['date','institute','educ_type','tecnologies']
            reg = Education()
        elif post['form_action'] == 'jobs':
            fields = ['start','end','foundation','office','description']
            reg = Jobs()
        elif post['form_action'] == 'projects':
            fields = ['date_pub','title','char_key','description','url']
            reg = Projects()
        elif post['form_action'] == 'school':
            fields = ['date','grade','institute','phase']
            reg = School()
        elif post['form_action'] == 'lecture':
            fields = ['date','area','event_name','theme','place']
            reg = Lectures()

        for x in fields:
                reg.__setattr__(x,(lambda(r): None if r == '' else r)(post[x]))

        if post['form_action'] != 'author':
            if post['form_action'] == 'projects':
                reg.save()
                reg.author.add(Author.objects.get(id=uid))
            else:
                reg.author = Author.objects.get(id=uid)
                reg.save()
        else:
            reg.save()
    return render(request, 'curriculum.html', {'menu':Menu, 'list_items': curr_items})

def define_session_keys(req):
    keys = ['user']
    for x in keys:
        if not x in req.session.keys():
            req.session[x] = None

def get_curriculum(uid):
    sc = School.objects.filter(author=uid)
    pj = Projects.objects.filter(author=uid)
    ed = Education.objects.filter(author=uid)
    jb = Jobs.objects.filter(author=uid)
    at = Author.objects.get(id=uid)
    le = Lectures.objects.filter(author=uid)

    return [at,ed,jb,pj,sc,le]

def edit(request, offset, f_id=None):
    define_session_keys(request)
    Menu = (lambda x: login_menu if x else no_login_menu)(request.session['user'])
    if not request.session['user']:
        return redirect('home')

    uid = int(request.session['user'].split('|')[0])
    if offset == 'school':
        vec = ['date','grade','institute','phase']
        oget = School.objects.get
        if f_id:
            f_edit = School.objects.get(id=f_id, author=Author.objects.get(id=uid))
        else:
            fields = School.objects.filter(author=Author.objects.get(id=uid))
    elif offset == 'education':
        vec = ['date','institute','educ_type','tecnologies']
        oget = Education.objects.get
        if f_id:
            f_edit = Education.objects.get(id=f_id, author=Author.objects.get(id=uid))
        else:
            fields = Education.objects.filter(author=Author.objects.get(id=uid))
    elif offset == 'jobs':
        oget = Jobs.objects.get
        vec = ['start','end','foundation','office','description']
        if f_id:
            f_edit = Jobs.objects.get(id=f_id, author=Author.objects.get(id=uid))
        else:
            fields = Jobs.objects.filter(author=Author.objects.get(id=uid))
    elif offset == 'projects':
        oget = Projects.objects.get
        vec = ['date_pub','title','char_key','description','url']
        if f_id:
            f_edit = Projects.objects.get(id=f_id, author=Author.objects.get(id=uid))
        else:
            fields = Projects.objects.filter(author=Author.objects.get(id=uid))
    elif offset == 'lecture':
        oget = Lectures.objects.get
        vec = ['date','area','event_name','theme','place']
        if f_id:
            f_edit = Lectures.objects.get(id=f_id, author=Author.objects.get(id=uid))
        else:
            fields = Lectures.objects.filter(author=Author.objects.get(id=uid))

    if 'act' in request.GET:
        if remove(request, offset, int(request.GET['item'])) == True:
		return render(request,'edit.html',{'menu':Menu,'offset':offset,'fields':fields,'error':'Item removido!'})
	return render(request,'edit.html',{'menu':Menu,'offset':offset,'fields':fields,'error':'Item inválido'})

    if request.method == 'POST':
        post = request.POST

        f_edit = oget(id=int(post['id']))
        for x in vec:
                f_edit.__setattr__(x,post[x])
        f_edit.save()

    try: return render(request,'edit.html',{'menu':Menu,'fields':fields,'offset':offset})
    except: return render(request,'edit.html',{'menu':Menu,'fields':f_edit,'offset':offset,'edit':True})

def send_mail(request):
    define_session_keys(request)
    Menu = (lambda x: login_menu if x else no_login_menu)(request.session['user'])
    if request.session['user']:
        return redirect('home')

    if 'email' in request.GET:
        try:
            a = Author.objects.get(email=request.GET['email'])
            subject = "Currículo Conscienciológico - Recuperar Senha"
            message = "Login: %s | Password: %s" %(a.login, a.password)
            sm(subject, message, settings.EMAIL_HOST_USER, [a.email], fail_silently=False)
            return 1
	except:
            return 2
    return 0

def remove(request, cat, item):
	uid = int(request.session['user'].split('|')[0])
	try:
		if cat == 'school':
			i = School.objects.get(id=int(item),author=Author.objects.get(id=uid))
		elif cat == 'education':
			i = Education.objects.get(id=int(item),author=Author.objects.get(id=uid))
		elif cat == 'projects':
			i = Projects.objects.get(id=int(item),author=Author.objects.get(id=uid))
		elif cat == 'jobs':
			i = Jobs.objects.get(id=int(item),author=Author.objects.get(id=uid))
		elif cat == 'lecture':
			i = Lectures.objects.get(id=int(item),author=Author.objects.get(id=uid))
		i.delete()
		return True
	except:
		return False;

	return False;

def home_redirect(request):
    return redirect('home')
