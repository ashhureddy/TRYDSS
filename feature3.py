#==============================================================================
# FEATURE 3: JSON VARIABLE CLEANING AND TRANSFORMATION
#==============================================================================
# Description: Clean and transform DSS JSON variables with flattened structure
# Brand: MASTEC
# Developer: AKSHATHA KALLUR

#==============================================================================

import re
from collections import defaultdict

class Feature3:
    """Feature 3: JSON Variable Cleaning and Transformation"""
    
    def __init__(self, config, dss_variables):
        """
        Initialize Feature 3
        
        Args:
            config: Config object with application settings
            dss_variables: Dictionary of DSS variables from Feature 2
        """
        self.config = config
        self.dss_variables = dss_variables
        self.cleaned_variables = {}
        
        # Greek letter mapping for sectors
        self.sector_mapping = {
            'A': 'alpha',
            'B': 'beta',
            'C': 'gamma',
            'D': 'delta',
            'E': 'epsilon',
            'F': 'zeta'
        }
        
        # Parameters to keep in rows (case-insensitive)
        self.keep_parameters = [
            'gNBId',
            'gNB Name',
            'SectorEquipmentFunction',
            'cellLocalId',
            'Carrier',
            'ssbFrequency'
        ]
    
    def extract_sector(self, value):
        """
        Extract sector letter from value string
        
        Args:
            value: String like "WCL03194_9A_1" or "NCGN003194_N002A_1"
            
        Returns:
            str: Sector letter (A, B, C, etc.) or None
        """
        if not value or str(value) == 'nan':
            return None
        
        value_str = str(value)
        
        # Pattern to find sector letter (usually between underscores or at end)
        # Example: WCL03194_9A_1 → A
        # Example: NCGN003194_N002A_1 → A
        match = re.search(r'_([A-Z]\d+)([A-Z])_', value_str)
        if match:
            return match.group(2)
        
        # Alternative pattern
        match = re.search(r'_(\d+)([A-Z])_', value_str)
        if match:
            return match.group(2)
        
        return None
    
    def get_greek_name(self, sector, sector_counts):
        """
        Get Greek letter name for sector with duplicate handling
        
        Args:
            sector: Sector letter (A, B, C, etc.)
            sector_counts: Dictionary tracking sector occurrences
            
        Returns:
            str: Greek letter name (alpha, beta, alpha1, alpha2, etc.)
        """
        if sector not in self.sector_mapping:
            return f"sector_{sector.lower()}"
        
        greek = self.sector_mapping[sector]
        
        # Handle duplicates
        if sector in sector_counts:
            sector_counts[sector] += 1
            return f"{greek}{sector_counts[sector]}"
        else:
            sector_counts[sector] = 0
            return greek
    
    def filter_row_parameters(self, row):
        """
        Filter row to keep only specified parameters (case-insensitive)
        
        Args:
            row: Dictionary representing a row
            
        Returns:
            dict: Filtered row with only required parameters
        """
        filtered_row = {}
        
        # Create case-insensitive lookup
        row_keys_map = {key.strip().upper(): key for key in row.keys()}
        
        for param in self.keep_parameters:
            param_upper = param.strip().upper()
            if param_upper in row_keys_map:
                original_key = row_keys_map[param_upper]
                filtered_row[param] = row[original_key]
        
        return filtered_row
    
    def transform_variable(self, var_name, var_data):
        """
        Transform a single DSS variable
        
        Args:
            var_name: Variable name (DSS1, DSS2, etc.)
            var_data: Variable data dictionary
            
        Returns:
            dict: Transformed variable with flattened structure
        """
        print(f"🔄 Transforming {var_name}...")
        
        # Initialize cleaned variable with basic info
        cleaned = {
            "group_name": var_data.get("group_name"),
            "band_carrier_pattern": var_data.get("band_carrier_pattern"),
            "total_rows": var_data.get("total_rows")
        }
        
        # Track sector occurrences for duplicate handling
        dss_sector_counts = {}
        nr_sector_counts = {}
        
        # Process DSS values
        dss_values = var_data.get("dss_values", [])
        for dss_value in dss_values:
            sector = self.extract_sector(dss_value)
            if sector:
                greek_name = self.get_greek_name(sector, dss_sector_counts)
                cleaned[f"DSS_{greek_name}"] = dss_value
        
        # Process NRCellDU values
        nrcelldu_values = var_data.get("nrcelldu_values", [])
        for nr_value in nrcelldu_values:
            sector = self.extract_sector(nr_value)
            if sector:
                greek_name = self.get_greek_name(sector, nr_sector_counts)
                cleaned[f"NR_{greek_name}"] = nr_value
        
        # Process rows - filter parameters
        rows = var_data.get("rows", [])
        cleaned["rows"] = []
        
        for row in rows:
            filtered_row = self.filter_row_parameters(row)
            cleaned["rows"].append(filtered_row)
        
        print(f"   ✅ Added {len(dss_values)} DSS parameters")
        print(f"   ✅ Added {len(nrcelldu_values)} NR parameters")
        print(f"   ✅ Filtered {len(cleaned['rows'])} rows to {len(self.keep_parameters)} parameters each")
        
        return cleaned
    
    def display_summary(self):
        """Display transformation summary"""
        print()
        print("=" * 80)
        print("📊 TRANSFORMATION SUMMARY")
        print("=" * 80)
        print()
        
        for var_name, data in self.cleaned_variables.items():
            print(f"🔹 {var_name}:")
            print(f"   Pattern: {data.get('band_carrier_pattern')}")
            print(f"   Total Rows: {data.get('total_rows')}")
            
            # Show DSS parameters
            dss_params = [k for k in data.keys() if k.startswith('DSS_')]
            print(f"   DSS Parameters: {', '.join(dss_params)}")
            
            # Show NR parameters
            nr_params = [k for k in data.keys() if k.startswith('NR_')]
            print(f"   NR Parameters: {', '.join(nr_params)}")
            
            print()
    
    def execute(self):
        """
        Execute Feature 3: JSON Cleaning and Transformation
        
        Returns:
            dict: Dictionary of cleaned DSS variables
        """
        try:
            print("🔍 Step 1: Analyzing DSS variables")
            print("-" * 80)
            print(f"Total variables to transform: {len(self.dss_variables)}")
            print()
            
            print("🔄 Step 2: Transforming variables")
            print("-" * 80)
            
            # Transform each variable
            for var_name, var_data in self.dss_variables.items():
                self.cleaned_variables[var_name] = self.transform_variable(var_name, var_data)
            
            print()
            print(f"✅ Successfully transformed {len(self.cleaned_variables)} variable(s)")
            
            # Display summary
            self.display_summary()
            
            return self.cleaned_variables
            
        except Exception as e:
            print(f"❌ Error in Feature 3: {str(e)}")
            raise

