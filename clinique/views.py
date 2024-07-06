from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from itertools import count
from typing import Annotated
from datetime import date
from django.db.models import Sum
from .models import Produit, Patienconsult,Patienhosp,Personnel,Salle,Service,Stock,Vente,Laboratoire


# Create your views here.
#authentification avec templates

def connexion(request):
    if request.method == 'POST':
        data=request.POST
        username=data.get('username')        
        password=data.get('password') 
        user=authenticate(username=username, password=password)
        if user:
            login(request, user)
            print("la connexion a bien marché")
            return redirect('url_index')
        else:
            print("Bah la connexion n'a pas marché")   
            return redirect('urllogin')
                
    return render(request, 'authent/login.html')




def creation(request):
    
    if request.method=='POST':
        data=request.POST
        if data.get('password1') == data.get('password'):
            username = data.get('username')
            email = data.get('email')
            password =data.get('password')
            isinstance = User.objects.create_user(
                username = username,
                email = email,
                password = password
            )
            return redirect('urllogin')
    
    return render(request, 'authent/register.html')

#deconnexion

def deconnexion(request):
    logout(request)
    print('deconnexion')
    return redirect('urllogin')

# recuperation mot de passe oublier
def mail(request):
    
    if request.method=='POST':
        data=request.POST
        email=data.get('email')
        #verification d'email
        user=User.objects.filter(email=email).last()
        if user:
            print('Email correct')
            return redirect('urlreset', user.id)
        else:
            print('E-mail incorrect')
            
            return redirect('urlmail')
    
    return render(request, 'authent/email.html')


def reset(request,pk):
    
    user=User.objects.get(pk=pk)
    if request.method=='POST':
        data=request.POST
        if data.get('password')==data.get('password1'):
            newpassword=data.get('password')
            
            user.set_password(newpassword)
            user.save()
            print('mot de passe modifié avec succès')
            
            return redirect('urllogin')
        else:
            print('Désolé les deux mots de passe ne sont pas identique')
            return redirect('urlreset')
    
    return render(request, 'authent/reset.html')

#page heritage templates
@login_required(login_url='urllogin')
def heritage(request):
    return render(request, 'authent/herite.html')

@login_required(login_url='urllogin')
def secure(request):
    return render(request, 'authent/secure.html')

#fin authentification

@login_required(login_url='urllogin')
def base(request):
    return render(request, 'pages/base.html')



# pages d'accueille site
@login_required(login_url='urllogin') 
def index(request):
    
    return render(request, 'pages/index.html')


#A propos 
@login_required(login_url='urllogin') 
def about(request):
    return render(request, 'pages/about.html')

# Consultation
@login_required(login_url='urllogin')
def all(request):
    #gen=Patienconsult.objects.values('nom','date_consultation').order_by('date_consultation').annotate(total=Sum('nom')).filter(sevice='Générale')
    #spe=Patienconsult.objects.values('nom','date_consultation').order_by('date_consultation').annotate(total=Sum('nom')).filter(sevice='Spécialitée')
    
    data=Patienconsult.objects.all().order_by('-id')
    total=Patienconsult.objects.all().count()
    gen=Patienconsult.objects.filter(sevice="Général").count()
    spe=Patienconsult.objects.filter(sevice="Spécialité").count()
    dict={'data':data, 'gen':gen, 'spe':spe, 'total':total}
    return render(request, 'pages/allconsultation.html',dict)

@login_required(login_url='urllogin')
def spe(request):
    data=Patienconsult.objects.filter(sevice='Spécialité')

    return render(request,'pages/consultspe.html',{'data':data})

@login_required(login_url='urllogin')
def gen(request):

    data=Patienconsult.objects.filter(sevice='Général')
    return render(request,'pages/consultgen.html',{'data':data})

@login_required(login_url='urllogin')
def editconsult(request,pk):
    data=Patienconsult.objects.get(secrete_key = pk)
    return render(request, 'edite/editconsult.html',{'data':data})
 
@login_required(login_url='urllogin')
def consultation(request):
    if request.method == 'POST':
        isinstance=request.POST
        toto=Patienconsult.objects.create(
            nom=isinstance.get('nom'),
            prenom=isinstance.get('prenom'),
            poids=isinstance.get('poids'),
            age=isinstance.get('age'),
            sexe=isinstance.get('sexe'),
            telephone=isinstance.get('telephone'),
            avis_medecin=isinstance.get('avis_medecin'),
            examen=isinstance.get('examen'),
            sevice=isinstance.get('service'),
            date_consultation=isinstance.get('date_consultation')
        )
        messages.success(request,'Enregistrement réalisé avec succès ')
    data=Patienconsult.objects.all().order_by('-id')
    return render(request, 'pages/consultation.html',{'data':data})

@login_required(login_url='urllogin')
def upconsultation(request,pk):
    data=Patienconsult.objects.get(pk=pk)
    if request.method == 'POST':
        toto=request.POST
        data.nom=toto.get('nom')
        data.prenom=toto.get('prenom')
        data.poids=toto.get('poids')
        data.age=toto.get('age')
        data.sexe=toto.get('sexe')
        data.telephone=toto.get('telephone')
        data.avis_medecin=toto.get('avis_medecin')
        data.examen=toto.get('examen')
        data.sevice=toto.get('service')
        data.date_consultation=toto.get('date_consultation')
        data.save()
        messages.success(request,'Modification réalisée avec succès ')

        return redirect('urlallconsultation')
    return render(request, 'update/modifconsult.html',{'data':data})
#Hospitalisation

@login_required(login_url='urllogin')
def ajoutpatient(request,pk):
    data=Patienconsult.objects.get(secrete_key=pk)
    if request.method == 'POST':
        toto=request.POST
        isinstance=Patienhosp.objects.create(
            nom=toto.get('nom'),
            prenom=toto.get('prenom'),
            poids=toto.get('poids'),
            age=toto.get('age'),
            sexe=toto.get('sexe'),
            telephone=toto.get('telephone'),
            avis_medecin=toto.get('avis_medecin'),
            traitement=toto.get('traitement'),
            examen=toto.get('examen'),
            sevice=toto.get('service'),
            date_hosp=toto.get('date_hosp'),
            date_sortie=toto.get('date_sortie')
        )
        messages.success(request,'Enregistrement réalisé avec succès ')

        return redirect('urlhospitalise')
    return render(request,'pages/ajoutpatient.html',{'data':data})


@login_required(login_url='urllogin')
def affichepatient(request):
    data=Patienhosp.objects.all().order_by('-id')

    return render(request, 'pages/patienthosp.html',{'data':data})


@login_required(login_url='urllogin')
def edothosp(request,pk):
    data=Patienhosp.objects.get(secrete_key=pk)
    return render(request, 'edite/edithosp.html',{'data':data})


@login_required(login_url='urllogin')
def updatehosp(request,pk):
    data=Patienhosp.objects.get(secrete_key=pk)
    if request.method == 'POST':
        toto=request.POST
        data.nom=toto.get('nom')
        data.prenom=toto.get('prenom')
        data.poids=toto.get('poids')
        data.age=toto.get('age')
        data.sexe=toto.get('sexe')
        data.telephone=toto.get('telephone')
        data.avis_medecin=toto.get('avis_medecin')
        data.traitement=toto.get('traitement')
        data.examen=toto.get('examen')
        data.sevice=toto.get('service')
        data.date_hosp=toto.get('date_hosp')
        data.date_sortie=toto.get('date_sortie')
        data.save()
        messages.success(request,'Modification réalisés avec succès ')

        return redirect('urlhospitalise')
    return render(request, 'update/modifhospi.html',{'data':data})


#examen

@login_required(login_url='urllogin')
def ajoutexamen(request,pk):
    data=Patienconsult.objects.get(secrete_key=pk)
    if request.method == 'POST':
        toto=request.POST
        isinstance=Laboratoire.objects.create(
            nom=toto.get('nom'),
            prenom=toto.get('prenom'),
            poids=toto.get('poids'),
            age=toto.get('age'),
            sexe=toto.get('sexe'),
            examen=toto.get('examen'),
            type_examen=toto.get('type_examen'),
            date_examen=toto.get('date_examen')
        )
        messages.success(request,'Enregistrement réalisé avec succès ')

        return redirect('urlexamen')

    return render(request,'pages/examen.html',{'data':data})


# ajout examen à la demande 

@login_required(login_url='urllogin')
def addexamensimple(request):
    if request.method == 'POST':
        toto=request.POST
        isinstance=Laboratoire.objects.create(
            nom=toto.get('nom'),
            prenom=toto.get('prenom'),
            poids=toto.get('poids'),
            age=toto.get('age'),
            sexe=toto.get('sexe'),
            examen=toto.get('examen'),
            type_examen=toto.get('type_examen'),
            date_examen=toto.get('date_examen')
        )
        messages.success(request,'Enregistrement réalisé avec succès ')

        return redirect('urlexamen')

    return render(request,'pages/examen.html')

@login_required(login_url='urllogin')
def affichexamen(request):
    data=Laboratoire.objects.all().order_by('-id')
    return render(request, 'pages/afficheexamen.html',{'data':data})


@login_required(login_url='urllogin')
def updateexam(request,pk):
    data=Laboratoire.objects.get(secrete_key=pk)
    if request.method == 'POST':
        toto=request.POST
        data.nom=toto.get('nom')
        data.prenom=toto.get('prenom')
        data.poids=toto.get('poids')
        data.age=toto.get('age')
        data.sexe=toto.get('sexe')
        data.examen=toto.get('examen')
        data.type_examen=toto.get('type_examen')
        data.date_examen=toto.get('date_examen')
        data.save()
        messages.success(request,'Modification réalisée avec succès ')

        return redirect('urlexamen')

    return render(request,'update/modifexamen.html',{'data':data})

@login_required(login_url='urllogin')
def editexamen(request,pk):
    data=Laboratoire.objects.get(secrete_key=pk)
    return render(request, 'edite/editexamen.html',{'data':data})


#personnel
@login_required(login_url='urllogin')
def perso(request):
    data=Personnel.objects.all()
    if request.method == 'POST':
        toto=request.POST
        isinstance=Personnel.objects.create(
            nom=toto.get('nom'),
            prenom=toto.get('prenom'),
            fonction=toto.get('fonction'),
            telephone=toto.get('telephone')
        )
        messages.success(request,'Enregistrement réalisé avec succès ')

    return render(request,'pages/personnel.html',{'data':data})


#salle
@login_required(login_url='urllogin')
def sal(request):
    data=Salle.objects.all()
    if request.method == 'POST':
        toto=request.POST
        isinstance=Salle.objects.create(
            nom_salle=toto.get('nom_salle'),
            numero_salle=toto.get('numero_salle'),
            nombre_lit=toto.get('nombre_lit')
        )
        messages.success(request,'Enregistrement réalisé avec succès ')

    return render(request,'pages/salle.html',{'data':data})


#service
@login_required(login_url='urllogin')
def serv(request):
    data=Service.objects.all()
    if request.method == 'POST':
        toto=request.POST
        isinstance=Service.objects.create(
            nom_service=toto.get('nom_service'),
            responsable=toto.get('responsable')
        )
        messages.success(request,'Enregistrement réalisé avec succès ')

    return render(request,'pages/service.html',{'data':data})


#stock
@login_required(login_url='urllogin')
def sto(request):
    data=Stock.objects.all().order_by('-id')
    if request.method == 'POST':
        toto=request.POST
        isinstance=Stock.objects.create(
            designation=toto.get('designation'),
            prix=toto.get('prix'),
            date_recep=toto.get('date_recep'),

        )
        messages.success(request,'Enregistrement réalisé avec succès ')

    return render(request,'pages/stock.html',{'data':data})


#Vente
@login_required(login_url='urllogin')
def vent(request):
    ventes=Vente.objects.all()
    produits=Produit.objects.all()
    data={"ventes":ventes, "produits":produits}
    if request.method =="POST":
        recupere=request.POST
        produit=Produit.objects.get(id=int(recupere.get('designation')))
        if produit.diminuer_qte(int(recupere.get('qte_achete'))):
            isinstance=Vente.objects.create(
                desigation_produit=produit,
                qte_achete=int(recupere.get('qte_achete') ))
       

    return render(request,'pages/vente.html',data)
