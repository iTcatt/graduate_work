from fastapi import FastAPI, Request, Path, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import uuid
import uvicorn

from handler.create_best_diagram import create_best_diagram
 

app = FastAPI()

def is_view_exist(data, target_view) -> bool:
    data = data['views']
    all_views = ['componentViews', 'containerViews', 'deploymentViews', 'dynamicViews', 'systemContextViews']
    result = False
    for view in all_views:
        if view not in data:
            continue

        if any(item.get("key") == target_view for item in data[view]):
            result = True
            break
        
    return result


@app.post("/api/best/{target_view}")
async def start_creating_diagrams(target_view: str, request: Request):
    process_id = uuid.uuid4()   
    try:
        json_data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid JSON: {e}")
    
    if not is_view_exist(json_data, target_view):
        raise HTTPException(status_code=400, detail='Target view not found')    
   
    image = create_best_diagram(process_id, target_view, json_data)
    if image == None:
        raise HTTPException(status_code=500, detail="Failed create diagram")

    return FileResponse(path=image, media_type="image/svg+xml")
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
