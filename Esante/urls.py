from django.contrib import admin
from django.urls import path, include
from clinique import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.base, name='urlbase'),
    
    #authentification templates
    
    path('creer', views.creation, name='urlregister'),
    path('login', views.connexion, name='urllogin'),
    
    #deconnexion
    path('logout', views.deconnexion, name='decon'),
    
    
    path('re/<int:pk>', views.reset, name='urlreset'),
    path('mail', views.mail, name='urlmail'),
    
    
    #page heritage
    path('herite', views.heritage, name='herite'),
    path('secure', views.heritage, name='secure'),
    
    
    
    
    
    # pages acceulle
     path('', views.index, name='url_index'),
     path('about', views.about, name='urlabout'),
     
   
    #sites
    #path('',include('clinique.urls')),
    
    path('Allconsultation',views.all,name='urlallconsultation'),
    path('AddConsult',views.consultation, name='consultations'),
    path('editeconsult/<pk>/', views.editconsult, name='editconsultations'),
    path('updateconsult/<int:pk>/', views.upconsultation, name='upconsultations'),
    path('consultgeneral', views.gen, name='generale'),
    path('consultspecial', views.spe, name='specialite'),
    
    #hospitalisation
    path('Unhealthy', views.affichepatient, name='urlhospitalise'),
    path('Hospitalisation/<pk>/', views.ajoutpatient, name='addpatients'),
    path('edithospitalisation/<pk>/', views.edothosp, name='editpatient'),
    path('updatehospitalisation/<pk>/', views.updatehosp, name='updatepatient'),

    #examen
    path('examen', views.affichexamen, name='urlexamen'),
    path('demandeexamen', views.addexamensimple, name='urldemandeexamen'),
    path('Addexam/<pk>/', views.ajoutexamen, name='examenurl'),
    path('Updateexamens/<pk>/', views.updateexam, name='updateexamenurl'),
    path('editeexamens/<pk>/', views.editexamen, name='editeexamensurl'),
    #personnel
    path('members', views.perso, name='personnels'),
    path('room', views.sal, name='salle'),
    path('service', views.serv, name='services'),
    path('stock', views.sto, name='stocks'),
    path('sold', views.vent, name='vente'),
]
