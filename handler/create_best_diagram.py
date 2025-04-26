from pathlib import Path
from PIL import Image
from model import model, processor, device

import torch
import subprocess
import json
import cairosvg
import io

from utils.temp_dir import TEMP_DIR


Image.MAX_IMAGE_PIXELS = None

def create_best_diagram(process_id, view, data) -> Path:
    work_dir = TEMP_DIR / str(process_id)
    work_dir.mkdir(parents=True, exist_ok=True)

    json_path = work_dir / "workspace.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    run_structurizr(json_path)

    target_dot_file = next(work_dir.glob(f"*{view}.dot"), None)
    if target_dot_file == None:
        print(f".dot файл с окончанием '{view}' не найден.")
        return
    
    improve_dot_file(target_dot_file)

    generate_png(target_dot_file, work_dir)
    
    best_layout = select_best_layout(work_dir)
   
    print(f'best layout: {best_layout}')
    
    for file in work_dir.iterdir():
        if file.is_file() and file != best_layout:
            file.unlink()

    return best_layout

        
def run_structurizr(json_path):
    structurizr_cmd = ["structurizr-cli", "export", "-f", "dot", "-w", json_path]
    try:
        subprocess.run(structurizr_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении structurizr-cli export: {e}")
        return
    

def improve_dot_file(dot_file):
    with open(dot_file, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.replace(
            'digraph {',
            'digraph {\n overlap=prism;\nsplines=true;\noverlap_scaling=-6;\n'
        )

    with open(dot_file, 'w', encoding='utf-8') as file:
        file.write(content)


def generate_png(dot_file, work_dir):
    layout_engines = ["dot", "neato", "fdp", "sfdp", "twopi", "circo"]

    for layout in layout_engines:
        graphviz_cmd = [layout, "-Tsvg", dot_file, "-o", f'{work_dir}/{layout}.svg']
        try:
            print(f"Генерация SVG с раскладкой '{layout}'")
            subprocess.run(graphviz_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при генерации изображения с раскладкой '{layout}': {e}")

    
def select_best_layout(work_dir: Path):
    description = [
        "Architectural diagram. In the diagram, the objects are well separated from each other. "
        "There are few intersections of lines in the diagram. The objects do not overlap each other. "
        "The text is contrasting. "
        "A diagram with clear symmetry: mirrored components, balanced layout, and evenly spaced elements across a vertical, horizontal, or radial axis."
    ]

    scores = []
    image_paths = work_dir.glob('*.svg')
    for path in image_paths:
        print("best run", str(path))
        png_bytes = cairosvg.svg2png(url=str(path), scale=0.1)
        image = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        inputs = processor(text=description, images=image, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            scores.append((probs.item(), path))

    best_score, best_image_path = max(scores, key=lambda x: x[0])
    return best_image_path
