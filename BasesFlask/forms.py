from wtforms import Form, StringField, EmailField, IntegerField
from wtforms import FloatField, RadioField 
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, IntegerField, SubmitField, validators

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

class PizzaForm(FlaskForm):
    
    nombre = StringField('Nombre', [validators.DataRequired('El nombre es requerido.')])
    direccion = StringField('Dirección', [validators.DataRequired('La dirección es requerida.')])
    telefono = StringField('Teléfono', [validators.DataRequired('El teléfono es requerido.')])
    
    
    tamano = RadioField('Tamaño Pizza', choices=[
        ('Chica', 'Chica $40'),
        ('Mediana', 'Mediana $80'),
        ('Grande', 'Grande $120')
    ], validators=[validators.DataRequired('Elige un tamaño.')])
    
    jamon = BooleanField('Jamón $10')
    pina = BooleanField('Piña $10')
    champinones = BooleanField('Champiñones $10')
    
    num_pizzas = IntegerField('Num. de Pizzas', [
        validators.DataRequired('Ingresa un número.'),
        validators.NumberRange(min=1, message='Debe ser al menos 1 pizza.')
    ], default=1)
    
    
    agregar = SubmitField('Agregar')
    terminar = SubmitField('Terminar')
    mostrar_ventas = SubmitField('Ventas totales por dia')
