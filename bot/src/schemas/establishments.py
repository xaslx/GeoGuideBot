from pydantic import BaseModel, ConfigDict




class Establishment(BaseModel):
    description: str
    address: str
    type_id: int



    model_config: ConfigDict = ConfigDict(from_attributes=True)