from django.db import models
import uuid

# Create your models here.


class Laboratoire(models.Model):
    examen=models.CharField(max_length=60)
    type_examen=models.CharField(max_length=60)
    def __str__(self):
        return self.examen
    
#modele/table salle
class Salle(models.Model):
    
    nom_salle=models.CharField(max_length=50)
    numero_salle=models.IntegerField()
    nombre_lit=models.IntegerField()
    secrete_key=models.UUIDField(default=uuid.uuid4)
    def __str__(self):

        return self.nom_salle

#modele/table stock des produits     
class Produit(models.Model):
    designation=models.CharField(max_length=50)
    prix=models.IntegerField()
    date_recep=models.DateField()
    secrete_key=models.UUIDField(default=uuid.uuid4)
    def __str__(self):

        return self.designation
    
    def diminuer_qte(self,qte):
        if(self.qte_produit.qte_stock >= qte):
            self.qte_produit.qte_stock-=qte
            self.qte_produit.save()
            return True
        return False



class Stock(models.Model):
    produit=models.OneToOneField(Produit, on_delete=models.CASCADE,related_name="qte_produit")
    qte_stock=models.IntegerField()
    def __str__(self):

        return f" Quantité: {self.qte_stock} "
     
#modele/table vente
class Vente(models.Model):

    desigation_produit=models.ForeignKey(Produit, on_delete=models.CASCADE,related_name="qt_produit")
    qte_achete=models.IntegerField()
    pu=models.IntegerField(editable=False)
    pttc=models.IntegerField(default=0, editable=False)
   # id_stock=models.ForeignKey(Stock, on_delete=models.CASCADE)
    secrete_key=models.UUIDField(default=uuid.uuid4)

    def __str__(self):

        return f"{self.desigation_produit.designation} {self.pttc} {self.pu} {self.qte_achete}"
    
    def save(self,*args,**kwargs):
        self.pu=self.desigation_produit.prix
        self.pttc= int(self.pu*self.qte_achete)
        super().save(*args,**kwargs)

    
#modele/table patient_consulté
class Patienconsult(models.Model):

    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    poids=models.FloatField()
    age=models.IntegerField()
    sexe=models.CharField(max_length=10)
    telephone=models.CharField(max_length=20)
    avis_medecin=models.TextField(null=True)
    examen=models.CharField(max_length=50,null=True)
    sevice=models.CharField(max_length=50)
    date_consultation=models.DateField()
    #id_examen=models.ForeignKey(Examens, on_delete=models.CASCADE )
    #id_service=models.ForeignKey(Service, on_delete=models.CASCADE)
    secrete_key=models.UUIDField(default=uuid.uuid4)

    def __str__(self):

        return self.nom


#modele/table patient_hospitalisé
class Patienhosp(models.Model):

    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    poids=models.FloatField()
    age=models.IntegerField()
    sexe=models.CharField(max_length=10)
    telephone=models.CharField(max_length=20)
    avis_medecin=models.TextField()
    traitement=models.TextField()
    examen=models.CharField(max_length=50)
    sevice=models.CharField(max_length=50)
    date_hosp=models.DateField(null=True)
    date_sortie=models.DateField(null=True)
    secrete_key=models.UUIDField(default=uuid.uuid4)
   # id_examen=models.ForeignKey(Examens, on_delete=models.CASCADE )
   # id_service=models.ForeignKey(Service, on_delete=models.CASCADE)
   # id_consultation=models.ForeignKey(Patienconsult, on_delete=models.CASCADE )

    def __str__(self):

        return self.nom

class Personnel(models.Model):

    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    fonction=models.CharField(max_length=50)
    telephone=models.CharField(max_length=20)
    secrete_key=models.UUIDField(default=uuid.uuid4)

class Service(models.Model):

    nom_service=models.CharField(max_length= 50)
    responsable=models.CharField(max_length= 50)
    secrete_key=models.UUIDField(default=uuid.uuid4)
    def __str__(self):

        return self.nom_service
    
class Laboratoire(models.Model):

    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    poids=models.FloatField()
    age=models.IntegerField()
    sexe=models.CharField(max_length=10)
    examen=models.CharField(max_length=60)
    type_examen=models.CharField(max_length=60)
    date_examen=models.DateField(null=True)
    secrete_key=models.UUIDField(default=uuid.uuid4)
    def __str__(self):
        return self.examen
   