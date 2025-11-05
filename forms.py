from wtforms import Form, StringField, EmailField, IntegerField
from wtforms import FloatField, RadioField 
from wtforms import validators

class UserForm(Form):
    matricula=IntegerField('Matricula', [validators.DataRequired(message="La matricula es obligatoria")])
    nombre=StringField('Nombre', [validators.DataRequired(message="El campo es requerido")])
    apellido=StringField('Apellido', [validators.DataRequired(message="El campo es requerido")])
    correo=EmailField('Correo', [validators.Email(message="Ingrese Correo valido")])
    
class FigurasForm(Form):
    figura = RadioField('Selecciona Figura',
                        choices=[('triangulo', 'Triángulo'),
                                 ('rectangulo', 'Rectángulo'),
                                 ('circulo', 'Círculo'),
                                 ('pentagono', 'Pentágono')],
                        default='triangulo')
    
    valor1 = FloatField('Valor 1', [validators.DataRequired(message="El valor 1 es requerido")])
    valor2 = FloatField('Valor 2', [validators.Optional()]) 
