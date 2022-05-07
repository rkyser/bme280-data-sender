from pydantic import BaseModel

class BME280SensorSample(BaseModel):
    timestamp: int 
    temp_c: float
    temp_f: float
    pressure: float
    humidity: float
