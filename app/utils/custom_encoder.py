from bson import ObjectId

class PyObjectId(str):
    """Custom class for MongoDB ObjectId validation."""
    
    @classmethod
    def __get_validators__(cls):
        """Get the validators that should be applied to the field."""
        print("Calling __get_validators__")  # Log when validators are called
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Validate the value."""
        print(f"Validating value: {value}")  # Log the value being validated
        if isinstance(value, ObjectId):
            print(f"ObjectId received: {value}")  # Log the ObjectId if it's detected
            return str(value)  # Convert ObjectId to string
        elif isinstance(value, str):
            print(f"String received: {value}")  # Log if a string is passed
            return value  # Return string as is
        else:
            raise ValueError(f"Invalid ObjectId: {value}")  # Raise error if not valid

