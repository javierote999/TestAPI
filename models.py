# Librerías necesarias para configurar nuestros modelos
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


# Configuraciones necesarias de Pydantic V1, para resolver el tipo de dato del atributo _id para ser compatible con MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('⛔️ ObjectId Inválido')
        return str(v)


class Customer(BaseModel):
    # Estamos definiendo un campo _id de tipo PyObjectId opcional, que si no lo definimos, usará el UID generado por MongoDB
    _id: Optional[PyObjectId] = Field(alias='_id')

    # Estamos definiendo un campo String obligatorio, es el nombre de nuestro cliente
    name: str

    # Estamos definiendo, un campo String opcional será el RUT de nuestro cliente, y que si no lo definimos, dejará el campo con un valor nulo
    run: Optional[str] = None

    # Estamos definiendo un campo String obligatorio, que será el correo de nuestro cliente
    email: str

    # Estamos definiendo un campo String obligatorio, es el WhatsApp de nuestro cliente
    whatsapp: str

    # Estamos definiendo un campo Boleano, que si no definimos, por defecto tendrá el valor False ( el objetivo de este campo, es saber si nuestro cliente es un prospecto que aun no nos ha comprado o si ya nos ha comprado )
    purchased: bool = False

    # Configuraciones necesarias de Pydantic V1, para resolver el tipo de dato del atributo _id para ser compatible con MongoDB
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class UpdateCustomer(BaseModel):
    name: Optional[str] = None
    run: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    purchased: Optional[bool] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}