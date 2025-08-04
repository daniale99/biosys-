from pyairtable import Api 

api = Api("pattLhdx847VGiQFf.bcc6c3a471647d426987a63d5b932102fe59e34e331cbe0b2ebc1443873d0b1f")
tabla = api.table("appm3pqt6YX7RBfNf", "usuario")

#altas 
yo={'clave': 'gordillo', 
'contra': 'gordillo',
'nombre': 'daniel gordillo', 
'admin': 1
}
tabla.create(yo)

registros= tabla.all()
for r in registros:
    print(r["fields"])

