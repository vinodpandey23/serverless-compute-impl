from pydantic import BaseModel


class FunctionRequest(BaseModel):
    function_name: str
    code: str


class ExecutionRequest(BaseModel):
    function_name: str
    payload: dict