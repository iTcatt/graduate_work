from huggingface_hub import snapshot_download


snapshot_download("openai/clip-vit-base-patch32", local_dir='./openai/clip-vit-base-patch32')