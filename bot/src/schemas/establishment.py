from pydantic import BaseModel, ConfigDict






class EstablishmentSchemaIn(BaseModel):
    title: str
    description: str
    address: str
    photo_url: str


class EstablishmentSchemaOut(EstablishmentSchemaIn):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)