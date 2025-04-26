from fastapi import FastAPI, Request, Path, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import uuid
import uvicorn

from handler.create_best_diagram import create_best_diagram
from handler.get_best_diagram import get_best_filename
 

app = FastAPI()

@app.post("/{targetView}/init")
async def start_creating_diagrams(targetView: str, request: Request, background_tasks: BackgroundTasks):
    process_id = uuid.uuid4()   
    try:
        json_data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Невозможно прочитать JSON: {e}")
    
    background_tasks.add_task(create_best_diagram, process_id, targetView, json_data)
    
    return {"id": process_id}


@app.get("/best/{id}")
async def get_best_diagram(id: uuid.UUID):
    image = get_best_filename(id)
    if image == None:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(path=image, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
