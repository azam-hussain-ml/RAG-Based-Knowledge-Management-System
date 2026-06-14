import os
import logging
from config import Config

logger = logging.getLogger(__name__)

class S3Storage:
    def __init__(self):
        """
        Initialize the local file storage directory path as a mock/fallback for cloud storage.
        """
        self.storage_path = Config.LOCAL_STORAGE_PATH
        
        # Automatically generate the root storage directory if it does not exist
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            logger.info(f"Created local storage directory at: {self.storage_path}")

    def upload_file(self, file_obj, filename):
        """
        Persist an uploaded document stream into the designated local directory.
        """
        try:
            target_path = os.path.join(self.storage_path, filename)
            logger.debug(f"Saving file locally to: {target_path}")
            
            # Commit the binary file stream to disk storage
            file_obj.save(target_path)
            print(f"✅ File successfully saved locally at: {target_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Local File Save failed: {str(e)}")
            raise e

    def get_file(self, filename):
        """
        Retrieve and open a file from the local storage path in binary read mode.
        """
        try:
            target_path = os.path.join(self.storage_path, filename)
            if os.path.exists(target_path):
                # Return an open binary file handle to match cloud/object storage delivery interfaces
                logger.debug(f"Retrieving file locally from: {target_path}")
                return open(target_path, 'rb')
            else:
                logger.warning(f"⚠️ File not found locally: {filename}")
                return None
        except Exception as e:
            print(f"Error retrieving file locally: {e}")
            return None