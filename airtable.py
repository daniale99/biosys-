from pyairtable.orm import Model
from pyairtable.orm import fields

class Usuario(Model):
    clave = fields.TextField("clave")
    contra = fields.TextField("contra")
    nombre = fields.TextField("nombre")
    admin = fields.CheckboxField("admin")

    class Meta: 
        api_key = "pattLhdx847VGiQFf.bcc6c3a471647d426987a63d5b932102fe59e34e331cbe0b2ebc1443873d0b1f"
        base_id = "appm3pqt6YX7RBfNf"
        table_name = "usuario"


class Bioenergia(Model):
    cultivo = fields.TextField("cultivo")
    parte = fields.TextField("parte")
    cantidad = fields.FloatField("cantidad")
    area = fields.FloatField("area")
    energia = fields.FloatField("energia")
    municipio = fields.SelectField("municipio")
    latitud = fields.FloatField("latitud")
    longitud = fields.FloatField("longitud")

    class Meta:
        api_key = "pattLhdx847VGiQFf.bcc6c3a471647d426987a63d5b932102fe59e34e331cbe0b2ebc1443873d0b1f"
        base_id = "appm3pqt6YX7RBfNf"
        table_name = "bioenergia"



cacao = Bioenergia(
    cultivo="cacao",
    parte="fruto",          
    cantidad=10.0,          
    area=5.0,               
    energia=100.0,          
    municipio="Tapijulapa",
    latitud=18.076169,
    longitud=-93.123456     
)

cacao.save()
