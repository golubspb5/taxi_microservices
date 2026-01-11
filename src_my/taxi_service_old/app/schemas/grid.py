from pydantic import BaseModel


class GridConfig(BaseModel):
    n: int
    m: int
