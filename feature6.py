#==============================================================================
# FEATURE 6: TEMPLATE GENERATION WITH STANDARD TEMPLATE
#==============================================================================
# Description: Generate notepad files using single standard.txt template
# Brand: MASTEC
# Developer: AKSHATHA KALLUR
#==============================================================================

import os
import re

class Feature6:
    """Feature 6: Template Generation with Standard Template"""
    
    def __init__(self, config, mapped_variables):
        """Initialize Feature 6"""
        self.config = config
        self.mapped_variables = mapped_variables
        self.templates_folder = "templates"
        self.output_folder = "output_templates"
        self.generated_files = []
        self.standard_template_path = os.path.join(self.templates_folder, "standard.txt")
    
    def ensure_folders_exist(self):
        """Ensure templates and output folders exist"""
        if not os.path.exists(self.templates_folder):
            os.makedirs(self.templates_folder)
            print(f"   ⚠️  Created '{self.templates_folder}' folder")
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"   ✅ Created '{self.output_folder}' folder")
    
    def read_standard_template(self):
        """Read the standard template file"""
        try:
            if not os.path.exists(self.standard_template_path):
                raise FileNotFoundError(f"Standard template 'standard.txt' not found in '{self.templates_folder}' folder")
            
            with open(self.standard_template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"      ❌ Error reading standard template: {str(e)}")
            return None
    
    def replace_placeholders_with_regex(self, template_content, variable_data):
        """
        Replace placeholders using REGEX for EXACT matching
        Sorted by length (longest first) to prevent partial replacements
        
        Args:
            template_content: Template file content
            variable_data: Dictionary with placeholder → value mappings
            
        Returns:
            tuple: (replaced_content, replacement_count)
        """
        replaced_content = template_content
        replacement_count = 0
        
        # CRITICAL: Sort by length (longest first) to prevent partial matches
        sorted_placeholders = sorted(
            variable_data.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        
        print(f"         🔍 Processing {len(sorted_placeholders)} placeholders...")
        
        for placeholder, value in sorted_placeholders:
            # Convert value to string
            value_str = str(value) if value is not None else ""
            
            # Use regex with escaped pattern for exact matching
            pattern = re.escape(placeholder)
            
            # Count matches
            matches = list(re.finditer(pattern, replaced_content))
            occurrences = len(matches)
            
            if occurrences > 0:
                # Replace ALL occurrences
                replaced_content = re.sub(pattern, value_str, replaced_content)
                replacement_count += occurrences
                
                if occurrences == 1:
                    print(f"         • {placeholder}: 1 occurrence → '{value_str}'")
                else:
                    print(f"         • {placeholder}: {occurrences} occurrences → '{value_str}'")
        
        return replaced_content, replacement_count
    
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
    
    def process_variable(self, variable_name, variable_data, template_content):
        """
        Process a single variable using the standard template
        
        Args:
            variable_name: Variable name (e.g., "N002_1")
            variable_data: Variable data with placeholder mappings
            template_content: Standard template content
            
        Returns:
            dict: Information about generated file
        """
        print(f"\n   📌 Processing '{variable_name}'...")
        print(f"      ✅ Using standard.txt template")
        
        # Replace placeholders using REGEX
        print(f"      🔄 Replacing placeholders (REGEX mode - longest first)...")
        replaced_content, replacement_count = self.replace_placeholders_with_regex(
            template_content,
            variable_data
        )
        
        print(f"      ✅ Replaced {replacement_count} placeholder occurrence(s)")
        
        # Generate output
        output_path = self.generate_output_file(variable_name, replaced_content)
        
        if output_path:
            print(f"      ✅ Generated: {os.path.basename(output_path)}")
            return {
                "variable_name": variable_name,
                "template_used": "standard.txt",
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
            
            print("📋 Step 2: Loading standard template")
            print("-" * 80)
            
            # Read the standard template ONCE
            template_content = self.read_standard_template()
            
            if not template_content:
                raise FileNotFoundError("Could not load standard.txt template")
            
            print(f"   ✅ Loaded 'standard.txt': {len(template_content)} characters")
            print()
            
            print("🔄 Step 3: Generating output files from standard template")
            print("-" * 80)
            print(f"   Processing {len(self.mapped_variables)} variable(s)...")
            
            # Process each variable using the SAME standard template
            for var_name, var_data in self.mapped_variables.items():
                result = self.process_variable(var_name, var_data, template_content)
                if result:
                    self.generated_files.append(result)
            
            print()
            print("=" * 80)
            print(f"✅ Generation complete: {len(self.generated_files)}/{len(self.mapped_variables)} successful")
            
            # Display summary
            self.display_summary()
            
            return self.generated_files
            
        except Exception as e:
            print(f"\n❌ Error in Feature 6: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

