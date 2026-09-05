import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# Ensure repository root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.api.routes import router as api_router

app = FastAPI(
    title="Healthcare - Patient Intake Triage Assistant",
    description="Clinical-grade, auditable intake triage engine adhering to PS01 governance.",
    version="2.4.0"
)

# Attach API routes
app.include_router(api_router)

# Locate built frontend directory
frontend_dist = os.path.join(BASE_DIR, "frontend", "dist")

if os.path.exists(frontend_dist):
    # Mount assets folder if present
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Ignore API calls
        if full_path.startswith("api"):
            return None
        file_path = os.path.join(frontend_dist, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def read_root():
        return {
            "system": "Healthcare - Patient Intake Triage Assistant (Clinical Core v2.4)",
            "status": "online",
            "track_id": "PS01",
            "docs": "/docs",
            "message": "Frontend is building or static files will be served here."
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"============================================================")
    print(f" Healthcare Clinical Triage Assistant (TRACK_ID=PS01)")
    print(f" Serving live at http://localhost:{port}")
    print(f" Single-command execution - No second terminal needed.")
    print(f"============================================================")
    uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info")
