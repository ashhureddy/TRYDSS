#==============================================================================
# FEATURE 2: NRCELLDU GROUPING
#==============================================================================
# Description: Group extracted rows by band+carrier pattern
# Brand: MASTEC
# Developer: AKSHATHA KALLUR

#==============================================================================

import pandas as pd
from utils import DataUtils

class Feature2:
    """Feature 2: NRCellDU Grouping"""
    
    def __init__(self, config, filtered_df):
        """
        Initialize Feature 2
        
        Args:
            config: Config object with application settings
            filtered_df: DataFrame from Feature 1 with filtered rows
        """
        self.config = config
        self.filtered_df = filtered_df
        self.nrcelldu_column = None
        self.groups = {}
        self.dss_variables = {}
    
    def find_nrcelldu_column(self):
        """Locate NRCellDU column"""
        print("🔍 Step 1: Locating NRCellDU column")
        print("-" * 80)
        
        self.nrcelldu_column = DataUtils.find_column_case_insensitive(
            self.filtered_df,
            self.config.nrcelldu_column_name
        )
        
        if self.nrcelldu_column is None:
            raise ValueError("NRCellDU column not found in worksheet")
        
        print(f"✅ Found NRCellDU column: '{self.nrcelldu_column}'")
        print()
    
    def analyze_nrcelldu_values(self):
        """Analyze NRCellDU values"""
        print("📊 Step 2: Analyzing NRCellDU values")
        print("-" * 80)
        
        nrcelldu_values = self.filtered_df[self.nrcelldu_column].tolist()
        print(f"Total NRCellDU values found: {len(nrcelldu_values)}")
        print(f"NRCellDU values: {nrcelldu_values}")
        print()
    
    def create_groups(self):
        """Create groups based on band+carrier pattern"""
        print("🔎 Step 3: Grouping by band and carrier pattern")
        print("-" * 80)
        
        # Find DSS column
        dss_column = DataUtils.find_column_case_insensitive(
            self.filtered_df,
            self.config.dss_column_name
        )
        
        group_mapping = {}
        
        for idx, row in self.filtered_df.iterrows():
            nrcelldu = row[self.nrcelldu_column]
            pattern = DataUtils.extract_band_carrier_pattern(nrcelldu)
            
            if pattern not in self.groups:
                self.groups[pattern] = []
            
            # Convert row to dictionary
            row_dict = row.to_dict()
            self.groups[pattern].append(row_dict)
            
            # Track mapping
            if pattern not in group_mapping:
                group_mapping[pattern] = []
            group_mapping[pattern].append(nrcelldu)
        
        print(f"✅ Created {len(self.groups)} group(s) based on band+carrier pattern")
        print()
        
        # Display grouping details
        print("📋 Grouping Details:")
        print("-" * 80)
        for pattern, nrcelldu_list in group_mapping.items():
            print(f"Pattern: {pattern}")
            print(f"  NRCellDU values: {', '.join(map(str, nrcelldu_list))}")
            print()
    
    def create_dss_variables(self):
        """Create DSS JSON variables"""
        print("📦 Step 4: Creating DSS JSON variables")
        print("-" * 80)
        
        # Find DSS column
        dss_column = DataUtils.find_column_case_insensitive(
            self.filtered_df,
            self.config.dss_column_name
        )
        
        for i, (pattern, rows) in enumerate(sorted(self.groups.items()), start=1):
            var_name = f"DSS{i}"
            self.dss_variables[var_name] = {
                "group_name": var_name,
                "band_carrier_pattern": pattern,
                "total_rows": len(rows),
                "nrcelldu_values": [row[self.nrcelldu_column] for row in rows],
                "dss_values": [row[dss_column] for row in rows],
                "rows": rows
            }
            print(f"✅ Created {var_name}: {len(rows)} row(s) with pattern '{pattern}'")
        
        print()
    
    def display_summary(self):
        """Display grouping summary"""
        print("=" * 80)
        print("📊 GROUPING SUMMARY")
        print("=" * 80)
        print()
        
        for var_name, data in self.dss_variables.items():
            print(f"🔹 {var_name}:")
            print(f"   Band+Carrier Pattern: {data['band_carrier_pattern']}")
            print(f"   Total Rows: {data['total_rows']}")
            print(f"   NRCellDU Values: {', '.join(map(str, data['nrcelldu_values']))}")
            print(f"   DSS Values: {', '.join(map(str, data['dss_values']))}")
            print()
    
    def execute(self):
        """
        Execute Feature 2: NRCellDU Grouping
        
        Returns:
            dict: Dictionary of DSS variables with grouped data
        """
        try:
            self.find_nrcelldu_column()
            self.analyze_nrcelldu_values()
            self.create_groups()
            self.create_dss_variables()
            self.display_summary()
            
            return self.dss_variables
            
        except Exception as e:
            print(f"❌ Error in Feature 2: {str(e)}")
            raise

