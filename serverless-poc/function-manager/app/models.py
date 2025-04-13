from pydantic import BaseModel


class FunctionRegistrationRequest(BaseModel):
    function_name: str
    code: str


class FunctionExecutionRequest(BaseModel):
    function_name: str
    payload: dict
