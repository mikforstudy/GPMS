from fastapi import APIRouter
from .user_endpoint import router as user_router
from .selection_endpoint import router as selection_router
from .project_endpoint import router as project_router
from .start_docx_endpoint import router as start_docx_router
from .middle_docx_endpoint import router as middle_docx_router
from .process_endpoint import router as process_router
from .defense_endpoint import router as defense_router
from .score_endpoint import router as score_router
from .end_docx_endpoint import router as end_docx_router


router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])

router.include_router(selection_router, prefix="/selections", tags=["selections"])

router.include_router(project_router, prefix="/projects", tags=["projects"])

router.include_router(start_docx_router, prefix="/startdocx", tags=["startdocx"])

router.include_router(middle_docx_router, prefix="/middledocx", tags=["middledocx"])

router.include_router(process_router, prefix="/process", tags=["process"])

router.include_router(defense_router, prefix="/defense", tags=["defense"])

router.include_router(score_router, prefix="/score", tags=["score"])

router.include_router(end_docx_router, prefix="/enddocx", tags=["enddocx"])


