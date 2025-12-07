from .v1.routers import employee, notes, projects, tasks
from .v1.auth import jwt_auth
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


router.include_router(jwt_auth.router)
router.include_router(employee.router)
router.include_router(notes.router)
router.include_router(projects.router)
router.include_router(tasks.router)
