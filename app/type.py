from pydantic import BaseModel
    
class AnalysisStartRequestDTO(BaseModel):
    employeeId: str
    postId: int
    boardId: int
    thumbnail: str