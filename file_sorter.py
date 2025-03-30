import asyncio
import os
import shutil
import argparse
from pathlib import Path
from typing import List

async def copy_file(source_path: Path, dest_path: Path) -> None:
    """Copies a file to the destination directory."""
    try:
        # Create destination directory if it doesn't exist
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use asyncio.to_thread for asynchronous copying
        await asyncio.to_thread(shutil.copy2, source_path, dest_path)
        print(f"Copied: {source_path} -> {dest_path}")
    except Exception as e:
        print(f"Error copying {source_path}: {e}")

async def process_file(source_path: Path, output_dir: Path) -> None:
    """Processes a file + creates a subfolder based on extension."""
    try:
        extension = source_path.suffix[1:].lower() or 'no_extension'
        
        # Create path based on extension
        dest_dir = output_dir / extension
        dest_path = dest_dir / source_path.name
        
        await copy_file(source_path, dest_path)
    except Exception as e:
        print(f"Error processing {source_path}: {e}")

async def read_folder(source_dir: Path, output_dir: Path) -> None:
    """Recursively reads all files in the source directory."""
    try:
        files = []
        for root, _, filenames in os.walk(source_dir):
            for filename in filenames:
                file_path = Path(root) / filename
                files.append(file_path)
        
        tasks = [process_file(file_path, output_dir) for file_path in files]
        
        # Run all together
        await asyncio.gather(*tasks)
        
        print(f"Processed {len(files)} files")
    except Exception as e:
        print(f"Error reading directory {source_dir}: {e}")

async def main():
    parser = argparse.ArgumentParser(description='Sort files by extension')
    parser.add_argument('source_dir', help='Path to source directory')
    parser.add_argument('output_dir', nargs='?', default='sorted_files', help='Path to destination directory (default: sorted_files)')
    
    args = parser.parse_args()
    
    source_dir = Path(args.source_dir)
    output_dir = Path(args.output_dir)
    
    # Check if source directory exists and has files
    if not source_dir.exists():
        print(f"Source directory {source_dir} does not exist")
        return
    
    # Check if source directory has any files
    if not any(source_dir.iterdir()):
        print(f"Source directory {source_dir} is empty")
        return
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    await read_folder(source_dir, output_dir)

if __name__ == '__main__':
    asyncio.run(main()) 