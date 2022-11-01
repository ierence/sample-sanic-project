def to_openapi(cls):
    
    class inner(cls):
        id: str
        
    return inner