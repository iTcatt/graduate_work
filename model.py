import torch
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizerFast, CLIPImageProcessor

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Используется устройство: {device}")

model_path = "./openai/clip-vit-base-patch32"

tokenizer = CLIPTokenizerFast.from_pretrained(
    model_path,
    from_slow=True,
    local_files_only=True,
)
image_processor = CLIPImageProcessor.from_pretrained(
    model_path,
    local_files_only=True,
)
processor = CLIPProcessor(
    tokenizer=tokenizer,
    image_processor=image_processor,
)

model = CLIPModel.from_pretrained(
    model_path,
    local_files_only=True,
).to(device)