#==============================================================================
# FEATURE 5: PLACEHOLDER MAPPING WITH VALIDATION
#==============================================================================
# Brand: MASTEC
# Developer: AKSHATHA KALLUR
#==============================================================================

import re

class Feature5:
    """Feature 5: Placeholder Mapping and New Variable Creation"""
    
    def __init__(self, config, populated_variables):
        """Initialize Feature 5"""
        self.config = config
        self.populated_variables = populated_variables
        self.mapped_variables = {}
        
        # Hard-coded lookup for essScPairId and essScLocalId
        # UPDATED: Added Delta (D) sector values
        self.ess_sc_lookup = {
            # N066_1
            "N066A_1": {"essScPairId": 2222, "essScLocalId": 20},
            "N066B_1": {"essScPairId": 2223, "essScLocalId": 21},
            "N066C_1": {"essScPairId": 2224, "essScLocalId": 22},
            "N066D_1": {"essScPairId": 2225, "essScLocalId": 23},
            
            # N066_2
            "N066A_2": {"essScPairId": 2225, "essScLocalId": 23},
            "N066B_2": {"essScPairId": 2226, "essScLocalId": 24},
            "N066C_2": {"essScPairId": 2227, "essScLocalId": 25},
            "N066D_2": {"essScPairId": 2228, "essScLocalId": 26},
            
            # N002_1
            "N002A_1": {"essScPairId": 3322, "essScLocalId": 30},
            "N002B_1": {"essScPairId": 3323, "essScLocalId": 31},
            "N002C_1": {"essScPairId": 3324, "essScLocalId": 32},
            "N002D_1": {"essScPairId": 3325, "essScLocalId": 33},
            
            # N002_2
            "N002A_2": {"essScPairId": 3325, "essScLocalId": 33},
            "N002B_2": {"essScPairId": 3326, "essScLocalId": 34},
            "N002C_2": {"essScPairId": 3327, "essScLocalId": 35},
            "N002D_2": {"essScPairId": 3328, "essScLocalId": 36},
            
            # N005_1
            "N005A_1": {"essScPairId": 1122, "essScLocalId": 10},
            "N005B_1": {"essScPairId": 1123, "essScLocalId": 11},
            "N005C_1": {"essScPairId": 1124, "essScLocalId": 12},
            "N005D_1": {"essScPairId": 1125, "essScLocalId": 13},
            
            # N005_2
            "N005A_2": {"essScPairId": 1125, "essScLocalId": 13},
            "N005B_2": {"essScPairId": 1126, "essScLocalId": 14},
            "N005C_2": {"essScPairId": 1127, "essScLocalId": 15},
            "N005D_2": {"essScPairId": 1128, "essScLocalId": 16},
        }
        
        # FIXED: Correct placeholder names matching template EXACTLY
        # UPDATED: Added Delta sector placeholders
        self.placeholders = {
            "primary_node": "xxMMBB_Primary_Node_Namexx",
            "lte_site_id": "xxLTE_Site_IDxx",
            "nr_node_name": "xx5G_NR_Node_Namexx",
            "lte_enbid": "xxLTE_eNBIDxx",
            "nr_gnbid": "xx5G_NR_gNBIDxx",
            
            # Cell IDs
            "lte_cellid_a": "LTE_cellidA",
            "lte_cellid_b": "LTE_cellidB",
            "lte_cellid_c": "LTE_cellidC",
            "lte_cellid_d": "LTE_cellidD",  # New
            
            "nr_celllocalid_a": "xx5G_celllocalidAxx",
            "nr_celllocalid_b": "xx5G_celllocalidBxx",
            "nr_celllocalid_c": "xx5G_celllocalidCxx",
            "nr_celllocalid_d": "xx5G_celllocalidDxx",  # New
            
            "nr_ssbfrequency_a": "xx5G_ssbfrequencyAxx",
            
            # NR Sector Carriers
            "nr_sector_carrier_alpha": "xx5G_NRSectorCarrier_Alphaxx",
            "nr_sector_carrier_beta": "xx5G_NRSectorCarrier_Betaxx",
            "nr_sector_carrier_gamma": "xx5G_NRSectorCarrier_Gammaxx",
            "nr_sector_carrier_delta": "xx5G_NRSectorCarrier_Deltaxx",  # New
            
            # LTE Sector Carriers
            "lte_sector_carrier_alpha": "xxLTE_SectorCarrier_No_Alphaxx",
            "lte_sector_carrier_beta": "xxLTE_SectorCarrier_No_Betaxx",
            "lte_sector_carrier_gamma": "xxLTE_SectorCarrier_No_Gammaxx",
            "lte_sector_carrier_delta": "xxLTE_SectorCarrier_No_Deltaxx",  # New
            
            # LTE Site IDs
            "lte_site_xa_1": "xxLTE_Site_IDxx_XA_1",
            "lte_site_xb_1": "xxLTE_Site_IDxx_XB_1",
            "lte_site_xc_1": "xxLTE_Site_IDxx_XC_1",
            "lte_site_xd_1": "xxLTE_Site_IDxx_XD_1",  # New
            
            # NR Nodes
            "nr_node_n00xa_1": "xx5G_NR_Node_Namexx_N00XA_1",
            "nr_node_n00xb_1": "xx5G_NR_Node_Namexx_N00XB_1",
            "nr_node_n00xc_1": "xx5G_NR_Node_Namexx_N00XC_1",
            "nr_node_n00xd_1": "xx5G_NR_Node_Namexx_N00XD_1",  # New
            
            # Rows/Patterns
            "n00xa": "N00XA",
            "n00xb": "N00XB",
            "n00xc": "N00XC",
            "n00xd": "N00XD",  # New
            "n00x": "N00X",
            
            # ESS IDs
            "ess_sc_pair_id_a": "essScPairId_A",
            "ess_sc_pair_id_b": "essScPairId_B",
            "ess_sc_pair_id_c": "essScPairId_C",
            "ess_sc_pair_id_d": "essScPairId_D",  # New
            
            "ess_sc_local_id_a": "essScLocalId_A",
            "ess_sc_local_id_b": "essScLocalId_B",
            "ess_sc_local_id_c": "essScLocalId_C",
            "ess_sc_local_id_d": "essScLocalId_D",  # New
            
            "nr_node_n00x": "xx5G_NR_Node_Namexx_N00X"
        }
    
    def get_value_case_insensitive(self, data, key):
        """Get value from dictionary with case-insensitive key matching"""
        if key in data:
            return data[key]
        
        key_upper = key.upper()
        for k, v in data.items():
            if k.upper() == key_upper:
                return v
        
        return None
    
    def extract_pattern_from_nr_value(self, nr_value):
        """Extract pattern from NR value for essScPairId/essScLocalId lookup"""
        if not nr_value:
            return None
        
        # UPDATED: Regex expanded to include [A-D] for Delta sector
        match = re.search(r'_(N\d{3}[A-D]_\d)$', str(nr_value))
        if match:
            return match.group(1)
        
        return None
    
    def get_ess_sc_values(self, nr_value):
        """Get essScPairId and essScLocalId from hard-coded lookup"""
        pattern = self.extract_pattern_from_nr_value(nr_value)
        
        if pattern and pattern in self.ess_sc_lookup:
            return self.ess_sc_lookup[pattern]
        
        return {"essScPairId": None, "essScLocalId": None}
    
    def extract_n00x_from_nr_node(self, nr_node_value):
        """Extract N00X pattern from NR node value"""
        if not nr_node_value:
            return None
        
        # UPDATED: Regex expanded to include [A-D] for Delta sector
        match = re.search(r'^(.+_N\d{3})[A-D]_\d$', str(nr_node_value))
        if match:
            return match.group(1)
        
        return None
    
    def extract_n00x_from_variable_name(self, variable_name):
        """Extract N00X from variable name"""
        parts = variable_name.split('_')
        if len(parts) > 0:
            return parts[0]
        return variable_name
    
    def validate_mapped_data(self, var_name, mapped):
        """Validate that all critical placeholders have values"""
        print(f"      🔍 Validating {var_name}...")
        
        missing = []
        none_values = []
        
        for key, placeholder in self.placeholders.items():
            if placeholder not in mapped:
                missing.append(placeholder)
            elif mapped[placeholder] is None:
                none_values.append(placeholder)
        
        if missing:
            print(f"      ⚠️  Missing placeholders: {len(missing)}")
            for m in missing[:5]:  # Show first 5
                print(f"         - {m}")
        
        if none_values:
            print(f"      ⚠️  Placeholders with None values: {len(none_values)}")
            for n in none_values[:5]:  # Show first 5
                print(f"         - {n}")
        
        if not missing and not none_values:
            print(f"      ✅ All {len(mapped)} placeholders validated")
        
        return len(missing) == 0 and len(none_values) == 0
    
    def map_variable(self, var_name, var_data):
        """Map a single populated variable to placeholder format"""
        print(f"🔄 Mapping {var_name}...")
        
        mapped = {}
        
        # Get rows array
        rows = var_data.get("rows", [])
        
        # Extract basic values
        primary_node = self.get_value_case_insensitive(var_data, "primary_node")
        lte_site_id = self.get_value_case_insensitive(var_data, "lte_siteID")
        lte_enbid = self.get_value_case_insensitive(var_data, "eNBId")
        
        # From rows
        gnb_name = rows[0].get("gNB Name") if len(rows) > 0 else None
        gnb_id = rows[0].get("gNBId") if len(rows) > 0 else None
        celllocalid_a = rows[0].get("cellLocalId") if len(rows) > 0 else None
        celllocalid_b = rows[1].get("cellLocalId") if len(rows) > 1 else None
        celllocalid_c = rows[2].get("cellLocalId") if len(rows) > 2 else None
        # UPDATED: Add celllocalid_d extraction
        celllocalid_d = rows[3].get("cellLocalId") if len(rows) > 3 else None
        
        ssbfrequency_a = rows[0].get("ssbFrequency") if len(rows) > 0 else None
        
        # Cell IDs
        alpha_cellid = self.get_value_case_insensitive(var_data, "alpha_cellId")
        beta_cellid = self.get_value_case_insensitive(var_data, "beta_cellId")
        gamma_cellid = self.get_value_case_insensitive(var_data, "gamma_cellId")
        # UPDATED: Add delta_cellId
        delta_cellid = self.get_value_case_insensitive(var_data, "delta_cellId")
        
        # Sector IDs
        alpha_sectorid = self.get_value_case_insensitive(var_data, "alpha_sectorId")
        beta_sectorid = self.get_value_case_insensitive(var_data, "beta_sectorId")
        gamma_sectorid = self.get_value_case_insensitive(var_data, "gamma_sectorId")
        # UPDATED: Add delta_sectorId
        delta_sectorid = self.get_value_case_insensitive(var_data, "delta_sectorId")
        
        # NR values
        nr_alpha = self.get_value_case_insensitive(var_data, "NR_alpha")
        nr_beta = self.get_value_case_insensitive(var_data, "NR_beta")
        nr_gamma = self.get_value_case_insensitive(var_data, "NR_gamma")
        # UPDATED: Add NR_delta
        nr_delta = self.get_value_case_insensitive(var_data, "NR_delta")
        
        # DSS values
        dss_alpha = self.get_value_case_insensitive(var_data, "DSS_alpha")
        dss_beta = self.get_value_case_insensitive(var_data, "DSS_beta")
        dss_gamma = self.get_value_case_insensitive(var_data, "DSS_gamma")
        # UPDATED: Add DSS_delta
        dss_delta = self.get_value_case_insensitive(var_data, "DSS_delta")
        
        # Row values
        row1 = self.get_value_case_insensitive(var_data, "row1")
        row2 = self.get_value_case_insensitive(var_data, "row2")
        row3 = self.get_value_case_insensitive(var_data, "row3")
        # UPDATED: Add row4
        row4 = self.get_value_case_insensitive(var_data, "row4")
        
        # Get essScPairId and essScLocalId
        ess_alpha = self.get_ess_sc_values(nr_alpha)
        ess_beta = self.get_ess_sc_values(nr_beta)
        ess_gamma = self.get_ess_sc_values(nr_gamma)
        # UPDATED: Add ess_delta
        ess_delta = self.get_ess_sc_values(nr_delta)
        
        # Extract N00X patterns
        # Use Gamma or Delta to find node pattern, prioritize Delta if available
        nr_node_ref = nr_gamma if nr_gamma else nr_delta
        nr_node_n00x = self.extract_n00x_from_nr_node(nr_node_ref)
        n00x = self.extract_n00x_from_variable_name(var_data.get("band_carrier_pattern", ""))
        
        # Map to placeholders
        mapped[self.placeholders["primary_node"]] = primary_node
        mapped[self.placeholders["lte_site_id"]] = lte_site_id
        mapped[self.placeholders["nr_node_name"]] = gnb_name
        mapped[self.placeholders["lte_enbid"]] = lte_enbid
        mapped[self.placeholders["nr_gnbid"]] = gnb_id
        
        mapped[self.placeholders["lte_cellid_a"]] = alpha_cellid
        mapped[self.placeholders["lte_cellid_b"]] = beta_cellid
        mapped[self.placeholders["lte_cellid_c"]] = gamma_cellid
        mapped[self.placeholders["lte_cellid_d"]] = delta_cellid # New
        
        mapped[self.placeholders["nr_celllocalid_a"]] = celllocalid_a
        mapped[self.placeholders["nr_celllocalid_b"]] = celllocalid_b
        mapped[self.placeholders["nr_celllocalid_c"]] = celllocalid_c
        mapped[self.placeholders["nr_celllocalid_d"]] = celllocalid_d # New
        
        mapped[self.placeholders["nr_ssbfrequency_a"]] = ssbfrequency_a
        
        mapped[self.placeholders["nr_sector_carrier_alpha"]] = nr_alpha
        mapped[self.placeholders["nr_sector_carrier_beta"]] = nr_beta
        mapped[self.placeholders["nr_sector_carrier_gamma"]] = nr_gamma
        mapped[self.placeholders["nr_sector_carrier_delta"]] = nr_delta # New
        
        mapped[self.placeholders["lte_sector_carrier_alpha"]] = alpha_sectorid
        mapped[self.placeholders["lte_sector_carrier_beta"]] = beta_sectorid
        mapped[self.placeholders["lte_sector_carrier_gamma"]] = gamma_sectorid
        mapped[self.placeholders["lte_sector_carrier_delta"]] = delta_sectorid # New
        
        mapped[self.placeholders["lte_site_xa_1"]] = dss_alpha
        mapped[self.placeholders["lte_site_xb_1"]] = dss_beta
        mapped[self.placeholders["lte_site_xc_1"]] = dss_gamma
        mapped[self.placeholders["lte_site_xd_1"]] = dss_delta # New
        
        mapped[self.placeholders["nr_node_n00xa_1"]] = nr_alpha
        mapped[self.placeholders["nr_node_n00xb_1"]] = nr_beta
        mapped[self.placeholders["nr_node_n00xc_1"]] = nr_gamma
        mapped[self.placeholders["nr_node_n00xd_1"]] = nr_delta # New
        
        mapped[self.placeholders["n00xa"]] = row1
        mapped[self.placeholders["n00xb"]] = row2
        mapped[self.placeholders["n00xc"]] = row3
        mapped[self.placeholders["n00xd"]] = row4 # New
        
        mapped[self.placeholders["ess_sc_pair_id_a"]] = ess_alpha["essScPairId"]
        mapped[self.placeholders["ess_sc_pair_id_b"]] = ess_beta["essScPairId"]
        mapped[self.placeholders["ess_sc_pair_id_c"]] = ess_gamma["essScPairId"]
        mapped[self.placeholders["ess_sc_pair_id_d"]] = ess_delta["essScPairId"] # New
        
        mapped[self.placeholders["ess_sc_local_id_a"]] = ess_alpha["essScLocalId"]
        mapped[self.placeholders["ess_sc_local_id_b"]] = ess_beta["essScLocalId"]
        mapped[self.placeholders["ess_sc_local_id_c"]] = ess_gamma["essScLocalId"]
        mapped[self.placeholders["ess_sc_local_id_d"]] = ess_delta["essScLocalId"] # New
        
        mapped[self.placeholders["nr_node_n00x"]] = nr_node_n00x
        mapped[self.placeholders["n00x"]] = n00x
        
        # Validate
        self.validate_mapped_data(var_name, mapped)
        
        print(f"   ✅ Mapped {len(mapped)} placeholder parameters")
        
        return mapped
    
    def display_summary(self):
        """Display mapping summary"""
        print()
        print("=" * 80)
        print("📊 MAPPING SUMMARY")
        print("=" * 80)
        print()
        
        for var_name, data in self.mapped_variables.items():
            print(f"🔹 {var_name}:")
            print(f"   Total placeholders: {len(data)}")
            print()
    
    def execute(self):
        """Execute Feature 5: Placeholder Mapping"""
        try:
            print("🔍 Step 1: Analyzing populated variables")
            print("-" * 80)
            print(f"Total variables to map: {len(self.populated_variables)}")
            print()
            
            print("🔄 Step 2: Creating mapped variables")
            print("-" * 80)
            print()
            
            for var_name, var_data in self.populated_variables.items():
                new_var_name = var_data.get("band_carrier_pattern", var_name)
                print(f"   Creating '{new_var_name}' from {var_name}...")
                self.mapped_variables[new_var_name] = self.map_variable(var_name, var_data)
            
            print()
            print(f"✅ Successfully mapped {len(self.mapped_variables)} variable(s)")
            
            self.display_summary()
            
            return self.mapped_variables
            
        except Exception as e:
            print(f"❌ Error in Feature 5: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
