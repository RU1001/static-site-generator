import os
import shutil
import logging

def setup_logging():
    """Set up logging to console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def copy_directory_recursive(source_dir, dest_dir):
    """
    Recursively copy files from source_dir to dest_dir.
    First cleans the destination directory.
    
    Args:
        source_dir (str): Path to source directory (e.g., 'static')
        dest_dir (str): Path to destination directory (e.g., 'public')
    """
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        logger.error(f"Source directory '{source_dir}' does not exist!")
        return
    
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        logger.info(f"Creating destination directory '{dest_dir}'")
        os.makedirs(dest_dir)
    else:
        # Clean destination directory first
        logger.info(f"Cleaning destination directory '{dest_dir}'")
        for item in os.listdir(dest_dir):
            item_path = os.path.join(dest_dir, item)
            try:
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                logger.error(f"Error cleaning '{item_path}': {e}")
    
    # Start recursive copy
    _copy_contents(source_dir, dest_dir, logger)
    logger.info("Copy completed successfully")

def _copy_contents(src, dst, logger):
    """
    Helper function to recursively copy contents.
    
    Args:
        src (str): Current source directory path
        dst (str): Current destination directory path
        logger: Logger instance
    """
    # Ensure the destination directory exists
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    # Walk through source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isdir(src_path):
            # Recursively copy subdirectory
            logger.info(f"Copying directory: {src_path} -> {dst_path}")
            _copy_contents(src_path, dst_path, logger)
        else:
            # Copy file
            logger.info(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)

if __name__ == "__main__":
    # Example usage
    copy_directory_recursive('static', 'public')
