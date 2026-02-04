#==============================================================================
# FEATURE 6: TEMPLATE GENERATION WITH DYNAMIC SELECTION
#==============================================================================
# Description: Generate notepad files selecting template based on Delta sector
# Brand: MASTEC
# Developer: AKSHATHA KALLUR
#==============================================================================

import os
import re

class Feature6:
    """Feature 6: Template Generation with Dynamic Selection"""
    
    def __init__(self, config, mapped_variables):
        """Initialize Feature 6"""
        self.config = config
        self.mapped_variables = mapped_variables
        self.templates_folder = "templates"
        self.output_folder = "output_templates"
        self.generated_files = []
        
        # Define paths for both templates
        # standard.txt = 4-Sector (Delta)
        # stand.txt = 3-Sector (No Delta)
        self.template_paths = {
            "4_sector": os.path.join(self.templates_folder, "standard.txt"),
            "3_sector": os.path.join(self.templates_folder, "stand.txt")
        }
        self.loaded_templates = {}
    
    def ensure_folders_exist(self):
        """Ensure templates and output folders exist"""
        if not os.path.exists(self.templates_folder):
            os.makedirs(self.templates_folder)
            print(f"   ⚠️  Created '{self.templates_folder}' folder")
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"   ✅ Created '{self.output_folder}' folder")
    
    def read_templates(self):
        """Read both template files into memory"""
        print("      Loading templates...")
        
        for key, path in self.template_paths.items():
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        self.loaded_templates[key] = f.read()
                    print(f"      ✅ Loaded '{os.path.basename(path)}' ({key})")
                else:
                    print(f"      ⚠️  Template not found: {path}")
            except Exception as e:
                print(f"      ❌ Error reading {path}: {str(e)}")

        if not self.loaded_templates:
            raise FileNotFoundError("No templates could be loaded from templates/ folder")
    
    def replace_placeholders_with_regex(self, template_content, variable_data):
        """
        Replace placeholders using REGEX for EXACT matching
        Sorted by length (longest first) to prevent partial replacements
        """
        replaced_content = template_content
        replacement_count = 0
        
        # Sort by length (longest first)
        sorted_placeholders = sorted(
            variable_data.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        
        for placeholder, value in sorted_placeholders:
            # Convert value to string (handle None)
            value_str = str(value) if value is not None else ""
            
            # Use regex with escaped pattern for exact matching
            pattern = re.escape(placeholder)
            
            # Perform replacement
            # Only replace if the placeholder actually exists in the specific template
            if re.search(pattern, replaced_content):
                replaced_content = re.sub(pattern, value_str, replaced_content)
                replacement_count += 1
        
        return replaced_content, replacement_count
    
    def detect_template_type(self, variable_data):
        """
        Determine if we should use the 3-sector or 4-sector template
        based on the presence of Delta data.
        """
        # Check specific Delta placeholders
        # These keys must match what Feature 5 produces exactly
        delta_keys = [
            "LTE_cellidD", 
            "xx5G_celllocalidDxx", 
            "xx5G_NRSectorCarrier_Deltaxx",
            "essScPairId_D"
        ]
        
        has_delta = False
        for key in delta_keys:
            if variable_data.get(key) is not None:
                has_delta = True
                break
        
        if has_delta:
            return "4_sector", "standard.txt"
        else:
            return "3_sector", "stand.txt"

    def generate_output_file(self, variable_name, content):
        """Generate output file with replaced content"""
        output_filename = f"{variable_name}_output.txt"
        output_path = os.path.join(self.output_folder, output_filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return output_path
        except Exception as e:
            print(f"      ❌ Error writing output file: {str(e)}")
            return None
    
    def process_variable(self, variable_name, variable_data):
        """Process a single variable"""
        print(f"\n   📌 Processing '{variable_name}'...")
        
        # 1. Determine which template to use
        template_key, template_filename = self.detect_template_type(variable_data)
        
        # 2. Get template content
        if template_key not in self.loaded_templates:
             print(f"      ❌ Template '{template_filename}' required but not loaded. Skipping.")
             return None
             
        template_content = self.loaded_templates[template_key]
        print(f"      ✅ Detected {template_key.replace('_', ' ').title()} -> Using '{template_filename}'")
        
        # 3. Replace placeholders
        replaced_content, replacement_count = self.replace_placeholders_with_regex(
            template_content,
            variable_data
        )
        
        # 4. Generate output
        output_path = self.generate_output_file(variable_name, replaced_content)
        
        if output_path:
            return {
                "variable_name": variable_name,
                "template_used": template_filename,
                "output_file": output_path,
                "replacements": replacement_count
            }
        
        return None
    
    def display_summary(self):
        """Display generation summary"""
        print("\n" + "=" * 80)
        print("📊 GENERATION SUMMARY")
        print("=" * 80 + "\n")
        
        if self.generated_files:
            print(f"✅ Successfully generated {len(self.generated_files)} file(s):\n")
            
            for file_info in self.generated_files:
                print(f"🔹 {file_info['variable_name']}:")
                print(f"   Template: {file_info['template_used']}")
                print(f"   Output: {file_info['output_file']}")
                print(f"   Replacements: {file_info['replacements']}")
                print()
        else:
            print("⚠️  No files were generated")
            print()
    
    def execute(self):
        """Execute Feature 6: Template Generation"""
        try:
            print("🔍 Step 1: Setting up folders")
            print("-" * 80)
            self.ensure_folders_exist()
            print()
            
            print("📋 Step 2: Loading templates")
            print("-" * 80)
            self.read_templates()
            print()
            
            print("🔄 Step 3: Generating output files")
            print("-" * 80)
            print(f"   Processing {len(self.mapped_variables)} variable(s)...")
            
            for var_name, var_data in self.mapped_variables.items():
                result = self.process_variable(var_name, var_data)
                if result:
                    self.generated_files.append(result)
            
            print()
            print("=" * 80)
            print(f"✅ Generation complete: {len(self.generated_files)}/{len(self.mapped_variables)} successful")
            
            self.display_summary()
            
            return self.generated_files
            
        except Exception as e:
            print(f"\n❌ Error in Feature 6: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
