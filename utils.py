#==============================================================================
# UTILITY FUNCTIONS
#==============================================================================
# Description: Helper functions for data processing
# Brand: MASTEC
# Developer: AKSHATHA KALLUR

#==============================================================================

import pandas as pd
import re

class DataUtils:
    """Utility class for data processing operations"""
    
    @staticmethod
    def find_column_case_insensitive(df, target_column_name):
        """
        Find a column in DataFrame with case-insensitive matching
        
        Args:
            df: pandas DataFrame
            target_column_name: Column name to search for
            
        Returns:
            str: Actual column name if found, None otherwise
        """
        for col in df.columns:
            if col.strip().upper() == target_column_name.upper():
                return col
        return None
    
    @staticmethod
    def find_worksheet_case_insensitive(excel_file, target_sheet_name):
        """
        Find a worksheet in Excel file with case-insensitive matching
        
        Args:
            excel_file: pandas ExcelFile object
            target_sheet_name: Sheet name to search for
            
        Returns:
            str: Actual sheet name if found, None otherwise
        """
        for sheet in excel_file.sheet_names:
            if sheet.strip().upper() == target_sheet_name.upper():
                return sheet
        return None
    
    @staticmethod
    def extract_band_carrier_pattern(nrcelldu):
        """
        Extract the band+carrier pattern from NRCellDU
        
        Examples:
            NCRN002376_N066A_1 → N066_1
            NCRN002376_N066B_2 → N066_2
            NCGN013194_N077C_1 → N077_1
            
        Logic:
            - Ignore first part before first underscore (site prefix)
            - Extract band number and carrier number
            - Remove sector letter (A, B, C, etc.)
        
        Args:
            nrcelldu: NRCellDU value string
            
        Returns:
            str: Band+carrier pattern (e.g., "N066_1")
        """
        if pd.isna(nrcelldu):
            return "UNKNOWN"
        
        nrcelldu_str = str(nrcelldu).strip()
        
        # Split by underscore
        parts = nrcelldu_str.split('_')
        
        if len(parts) < 3:
            return "UNKNOWN"
        
        # Get the middle part (e.g., N066A) and last part (e.g., 1)
        middle_part = parts[1]  # N066A
        carrier_num = parts[2]   # 1
        
        # Remove the sector letter (A, B, C, etc.) from the middle part
        # Pattern: N066A → N066
        band_match = re.match(r'^([A-Z]\d+)[A-Z]?$', middle_part)
        if band_match:
            band = band_match.group(1)  # N066
            return f"{band}_{carrier_num}"
        
        return "UNKNOWN"
    
    @staticmethod
    def display_dataframe_summary(df, columns, title="Data Summary"):
        """
        Display a formatted summary of DataFrame
        
        Args:
            df: pandas DataFrame
            columns: List of columns to display
            title: Title for the summary
        """
        print(f"📋 {title}:")
        print("-" * 80)
        display_cols = [col for col in columns if col in df.columns]
        if display_cols:
            print(df[display_cols].to_string(index=False))
        print()
        print("-" * 80)
        print()

