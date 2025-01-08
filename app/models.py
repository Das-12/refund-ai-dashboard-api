from pydantic import BaseModel, Field
from typing import Any, Dict
from bson import ObjectId
from app.utils.custom_encoder import PyObjectId
from fastapi import HTTPException, status


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo(cls, data: Dict[str, Any]):
        """Method to convert a MongoDB document to Pydantic model."""
        print(f"Raw Mongo data: {data}")  # Log the raw MongoDB data
        
        # Explicitly convert ObjectId to string for all keys in the data
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
        
        print(f"Converted Mongo data: {data}")  # Log the converted data
        
        # Use parse_obj instead of model_validate
        try:
            return cls.parse_obj(data)
        except Exception as e:
            print(f"Error during model validation: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during model validation: {e}"
        )
