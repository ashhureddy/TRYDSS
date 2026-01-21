#==============================================================================
# FEATURE 1: DSS VALUE EXTRACTION
#==============================================================================
# Description: Extract rows from 5G Info worksheet where DSS ≠ "NO"
# Brand: MASTEC
# Developer: AKSHATHA KALLUR
#==============================================================================

import pandas as pd
from utils import DataUtils

class Feature1:
    """Feature 1: DSS Value Extraction"""
    
    def __init__(self, config):
        """Initialize Feature 1"""
        self.config = config
        self.df = None
        self.filtered_df = None
        self.dss_column = None
    
    def read_worksheet(self):
        """Read the target worksheet from Excel file"""
        print("📊 Reading '5G Info' worksheet...")
        
        try:
            xl_file = pd.ExcelFile(self.config.excel_file_path)
            
            # Find the target sheet (case-insensitive)
            target_sheet = DataUtils.find_worksheet_case_insensitive(
                xl_file, 
                self.config.target_worksheet
            )
            
            if target_sheet is None:
                raise ValueError(
                    f"'{self.config.target_worksheet}' worksheet not found. "
                    f"Available sheets: {xl_file.sheet_names}"
                )
            
            self.df = pd.read_excel(self.config.excel_file_path, sheet_name=target_sheet)
            print(f"✅ Loaded '{target_sheet}' ({len(self.df)} rows)")
            
        except Exception as e:
            raise Exception(f"Error reading worksheet: {str(e)}")
    
    def find_dss_column(self):
        """Locate DSS column in the worksheet"""
        print("🔍 Locating DSS column...")
        
        self.dss_column = DataUtils.find_column_case_insensitive(
            self.df, 
            self.config.dss_column_name
        )
        
        if self.dss_column is None:
            raise ValueError(
                f"DSS column not found in worksheet. "
                f"Available columns: {self.df.columns.tolist()}"
            )
        
        print(f"✅ Found DSS column: '{self.dss_column}'")
    
    def filter_dss_rows(self):
        """Filter rows where DSS is not equal to exclude value"""
        print("🔎 Filtering rows where DSS ≠ 'NO'...")
        
        # Create mask for filtering
        mask = (
            (self.df[self.dss_column].notna()) & 
            (self.df[self.dss_column].astype(str).str.strip().str.upper() != 
             self.config.dss_exclude_value.upper())
        )
        
        self.filtered_df = self.df[mask].copy()
        
        no_count = (
            self.df[self.dss_column].astype(str).str.strip().str.upper() == 
            self.config.dss_exclude_value.upper()
        ).sum()
        
        print(f"✅ Extracted {len(self.filtered_df)} rows (excluded {no_count} 'NO' values)")
    
    def execute(self):
        """Execute Feature 1: DSS Extraction"""
        try:
            self.read_worksheet()
            self.find_dss_column()
            self.filter_dss_rows()
            return self.filtered_df
            
        except Exception as e:
            print(f"❌ Error in Feature 1: {str(e)}")
            raise

