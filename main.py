from fastapi import FastAPI, HTTPException
from database import get_all_customer, save_customer, validate_exist_email, get_one_customer, remove_customer, update_customer
from models import Customer, UpdateCustomer

app = FastAPI()

### --- GET: Ruta que Devuelva un Mensaje de Bienvenida  --- ###
@app.get('/api/v1')
async def welcome():
    return { 'message': '🤟🏻 Bienvenido a Mi Primera API RESTful con FastAPI' }

### --- POST: Ruta que nos permita Crear un Nuevo Cliente | Conectado a MongoDB --- ###
@app.post('/api/v1/customers', response_model=Customer )
async def create_customers(customer: Customer ):
    email_found = await validate_exist_email(customer.email)

    if email_found:
        raise HTTPException(409, '⚠️ Ups, el correo ya existe')

    response = await save_customer(customer.dict())

    if response:
        return response
    raise HTTPException(400, '⚠️ Ups, algo salio mal 🤯')

    return {'message': '👤 Cliente Creado Exitosamente ✅'}

### --- GET: Ruta que Devuelva Todos los Clientes | Conectado a MongoDB  --- ###
@app.get('/api/v1/customers')
async def index_customers():
    customers = await get_all_customer()
    return customers

### --- GET: Ruta que nos Devuelva un cliente específico a través de su ID | Conectado a MongoDB  --- ###

@app.get('/api/v1/customers/{id}')
async def get_one_customer(id):
    return { 'message': '👤 Datos de un cliente especifico' }


### --- POST Requests --- ###
@app.post('/api/v1/customers')
async def create_customers():
    return { 'message': '📦 Creación de un nuevo cliente' }


### --- DELETE: Ruta que nos permita ELIMINAR un cliente específico a través de su ID | Conectado a MongoDB  --- ###
@app.delete('/api/v1/customers/{id}')
async def delete_customers(id: str):
    response = await remove_customer(id)

    if response:
        return f"El Cliente con el ID {id} Ha sido Eliminado Correctamente "

    raise HTTPException(404, f"Cliente con el ID {id} ya ha sido eliminado ❌")

### --- PUT: Ruta que nos permita editar los Atributos de un Cliente | Conectado a MongoDB --- ###
@app.put('/api/v1/customers/{id}', response_model=Customer)
async def edit_customer(id: str, data: UpdateCustomer):
    response = await update_customer(id, data)

    if response:
        return response

    raise HTTPException(404, f"Cliente con el ID {id} No ha Sido Encontrado 😰")