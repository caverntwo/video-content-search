from pathlib import Path
import shutil
import pathlib
import os

src_root = Path("D:\\Github\\video-content-search\\output\\Keyframes")
dst_folder = Path("D:\\Github\\video-content-search\\output\\_All2")
dst_folder.mkdir(exist_ok=True)

for img in src_root.rglob("*.jpg"):
     new_name = f"{img.parent.name}_{img.name}"  # avoid name collisions
     shutil.copy(img, dst_folder / new_name)

cwd = os.getcwd()
print(cwd)