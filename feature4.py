#==============================================================================
# FEATURE 4: JSON VARIABLE POPULATION - FINAL FIX
#==============================================================================
# Description: Populate DSS JSON variables with data from Excel worksheets
# Brand: MASTEC
# Developer: AKSHATHA KALLUR

#==============================================================================

import pandas as pd
import re
from utils import DataUtils

class Feature4:
    """Feature 4: JSON Variable Population"""
    
    def __init__(self, config, cleaned_variables):
        """Initialize Feature 4"""
        self.config = config
        self.cleaned_variables = cleaned_variables
        self.populated_variables = {}
        self.mixed_mode_df = None
        self.eutran_df = None
    
    def load_worksheets(self):
        """Load required worksheets from Excel file"""
        print("📁 Loading Excel worksheets...")
        print("-" * 80)
        
        try:
            xl_file = pd.ExcelFile(self.config.excel_file_path)
            
            # Load Mixed Mode Info
            mixed_mode_sheet = DataUtils.find_worksheet_case_insensitive(xl_file, "Mixed Mode Info")
            if mixed_mode_sheet:
                self.mixed_mode_df = pd.read_excel(self.config.excel_file_path, sheet_name=mixed_mode_sheet)
                print(f"✅ Loaded '{mixed_mode_sheet}': {len(self.mixed_mode_df)} rows")
            
            # Load eUtran Parameters
            eutran_sheet = DataUtils.find_worksheet_case_insensitive(xl_file, "eUtran Parameters")
            if eutran_sheet:
                self.eutran_df = pd.read_excel(self.config.excel_file_path, sheet_name=eutran_sheet)
                print(f"✅ Loaded '{eutran_sheet}': {len(self.eutran_df)} rows")
            
            print()
            
        except Exception as e:
            raise Exception(f"Error loading worksheets: {str(e)}")
    
    def get_primary_node_info(self, gnb_name, gnb_id):
        """Get primary node information"""
        if self.mixed_mode_df is None:
            return {}
        
        gnodeb_col = DataUtils.find_column_case_insensitive(self.mixed_mode_df, "gNodeB Name")
        gnbid_col = DataUtils.find_column_case_insensitive(self.mixed_mode_df, "gNBId")
        node_col = DataUtils.find_column_case_insensitive(self.mixed_mode_df, "Node to be built as")
        enbid_col = DataUtils.find_column_case_insensitive(self.mixed_mode_df, "eNBId")
        enodeb_col = DataUtils.find_column_case_insensitive(self.mixed_mode_df, "eNodeB Name")
        
        if not all([gnodeb_col, gnbid_col]):
            return {}
        
        mask = (self.mixed_mode_df[gnodeb_col] == gnb_name) & (self.mixed_mode_df[gnbid_col] == gnb_id)
        matching_rows = self.mixed_mode_df[mask]
        
        if matching_rows.empty:
            return {}
        
        row = matching_rows.iloc[0]
        result = {}
        
        if node_col and pd.notna(row[node_col]):
            result["primary_node"] = row[node_col]
        if enbid_col and pd.notna(row[enbid_col]):
            result["eNBId"] = int(row[enbid_col])
        if enodeb_col and pd.notna(row[enodeb_col]):
            result["lte_siteID"] = row[enodeb_col]
        
        return result
    
    def get_sector_cell_ids_for_dss(self, dss_value, greek_name):
        """
        Get sectorId and cellId for a SINGLE DSS value
        
        CRITICAL FIX: DO NOT REMOVE UNDERSCORES - Match exactly as-is!
        """
        result = {}
        
        if self.eutran_df is None:
            return result
        
        # Find column names (case-insensitive)
        eutran_col = None
        sector_col = None
        cell_col = None
        
        for col in self.eutran_df.columns:
            col_upper = str(col).strip().upper()
            if col_upper == "EUTRANCELLFDDID":
                eutran_col = col
            elif col_upper == "SECTORID":
                sector_col = col
            elif col_upper == "CELLID":
                cell_col = col
        
        if not eutran_col or not sector_col or not cell_col:
            return result
        
        # CRITICAL FIX: Use DSS value AS-IS, don't remove underscores!
        search_value = str(dss_value).strip()
        
        print(f"      🔍 Searching for EXACT match: '{search_value}'")
        
        # Search for exact match
        match_found = False
        row_data = None
        
        for idx, row in self.eutran_df.iterrows():
            cell_value = str(row[eutran_col]).strip()
            
            if cell_value == search_value:
                print(f"      ✅ MATCH FOUND at row {idx}!")
                match_found = True
                row_data = row
                break
        
        if not match_found:
            print(f"      ❌ No match found")
            return result
        
        # Extract sectorId and cellId
        if pd.notna(row_data[sector_col]):
            try:
                result[f"{greek_name}_sectorId"] = int(row_data[sector_col])
            except:
                result[f"{greek_name}_sectorId"] = row_data[sector_col]
            print(f"      ✅ {greek_name}_sectorId = {result[f'{greek_name}_sectorId']}")
        
        if pd.notna(row_data[cell_col]):
            try:
                result[f"{greek_name}_cellId"] = int(row_data[cell_col])
            except:
                result[f"{greek_name}_cellId"] = row_data[cell_col]
            print(f"      ✅ {greek_name}_cellId = {result[f'{greek_name}_cellId']}")
        
        return result
    
    def extract_sector_equipment(self, sector_eq_function):
        """Extract band+sector from SectorEquipmentFunction"""
        if pd.isna(sector_eq_function):
            return None
        parts = str(sector_eq_function).split('_')
        if len(parts) >= 2:
            return parts[-1]
        return None
    
    def populate_variable(self, var_name, var_data):
        """Populate a single DSS variable"""
        print(f"\n{'='*80}")
        print(f"🔄 POPULATING {var_name}")
        print(f"{'='*80}\n")
        
        populated = var_data.copy()
        
        # 1. Primary node info
        if "rows" in var_data and len(var_data["rows"]) > 0:
            first_row = var_data["rows"][0]
            gnb_name = first_row.get("gNB Name")
            gnb_id = first_row.get("gNBId")
            
            if gnb_name and gnb_id:
                print(f"   1️⃣ Primary Node Info:")
                primary_info = self.get_primary_node_info(gnb_name, gnb_id)
                for key, value in primary_info.items():
                    populated[key] = value
                    print(f"      ✅ {key} = {value}")
                print()
        
        # 2. Sector and Cell IDs
        print(f"   2️⃣ Sector and Cell IDs:")
        
        dss_keys = sorted([k for k in var_data.keys() if k.startswith('DSS_')])
        
        for dss_key in dss_keys:
            dss_value = var_data[dss_key]
            greek_name = dss_key.replace('DSS_', '')
            
            print(f"   📌 {greek_name.upper()}: '{dss_value}'")
            
            sector_cell_data = self.get_sector_cell_ids_for_dss(dss_value, greek_name)
            
            for key, value in sector_cell_data.items():
                populated[key] = value
        
        print()
        
        # 3. Row extractions
        print(f"   3️⃣ Row Extractions:")
        if "rows" in var_data:
            for idx, row in enumerate(var_data["rows"], start=1):
                sector_eq = row.get("SectorEquipmentFunction")
                if sector_eq:
                    extracted = self.extract_sector_equipment(sector_eq)
                    if extracted:
                        populated[f"row{idx}"] = extracted
                        print(f"      ✅ row{idx} = {extracted}")
        
        print(f"\n✅ Completed {var_name}\n")
        
        return populated
    
    def display_summary(self):
        """Display summary"""
        print("\n" + "="*80)
        print("📊 FINAL SUMMARY")
        print("="*80 + "\n")
        
        for var_name, data in self.populated_variables.items():
            print(f"🔹 {var_name}:")
            
            sector_cell_params = sorted([k for k in data.keys() if '_sectorId' in k or '_cellId' in k])
            
            if sector_cell_params:
                print(f"   ✅ Sector/Cell IDs: {len(sector_cell_params)}")
                for param in sector_cell_params:
                    print(f"      • {param}: {data[param]}")
            else:
                print(f"   ❌ No sector/cell IDs added")
            
            print()
    
    def execute(self):
        """Execute Feature 4"""
        try:
            self.load_worksheets()
            
            print("="*80)
            print("🚀 POPULATING ALL VARIABLES")
            print("="*80)
            
            for var_name, var_data in self.cleaned_variables.items():
                self.populated_variables[var_name] = self.populate_variable(var_name, var_data)
            
            self.display_summary()
            
            return self.populated_variables
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

