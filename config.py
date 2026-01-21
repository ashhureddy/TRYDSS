#==============================================================================
# CONFIGURATION FILE
#==============================================================================
# Description: Configuration settings for the DSS Extractor
# Author: AKSHATHA KALLUR
# Agency: MASTEC
#==============================================================================

import os

class Config:
    """Configuration class for the DSS Extractor application"""
    
    def __init__(self):
        # File paths
        self.excel_file_path = None
        
        # Worksheet names
        self.target_worksheet = "5G Info"
        
        # Column names
        self.dss_column_name = "DSS"
        self.nrcelldu_column_name = "NRCellDU"
        
        # Values to exclude
        self.dss_exclude_value = "NO"
        
        # Display columns for summary
        self.summary_display_columns = [
            'gNBId', 
            'gNB Name', 
            'NRCellDU', 
            'DSS', 
            'Operating Band'
        ]
        
        # Output settings
        self.output_json_file = "dss_output.json"
        self.verbose = False  # Disable verbose for Streamlit
    
    def set_excel_file_path(self, file_path):
        """Set the Excel file path"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self.excel_file_path = file_path
    
    def validate(self):
        """Validate configuration"""
        if self.excel_file_path is None:
            raise ValueError("Excel file path is not set")
        return True

