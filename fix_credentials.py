"""
Script to remove hardcoded credentials from Python files
"""
import re
from pathlib import Path

# Files to update
files_to_fix = [
    'check_all_sources.py',
    'check_db_count.py',
    'check_db_july1.py',
    'check_sources.py',
    'clear_and_upload.py',
    'compare_sources.py',
    'final_verify.py',
    'upload_clean.py',
    'upload_to_supabase.py',
    'verify_db_data.py',
    'verify_db_full.py',
    'enrich_cities.py',
]

# Pattern to match hardcoded credentials
url_pattern = r'SUPABASE_URL\s*=\s*"https://[^"]+\.supabase\.co"'
key_pattern = r'SUPABASE_KEY\s*=\s*"eyJ[^"]+"'

replacement_import = 'from config import SUPABASE_URL, SUPABASE_KEY'

for filename in files_to_fix:
    filepath = Path(filename)
    if not filepath.exists():
        print(f"⊘ {filename} not found, skipping")
        continue
    
    content = filepath.read_text(encoding='utf-8')
    original_content = content
    
    # Remove hardcoded URL and KEY
    content = re.sub(url_pattern, '', content)
    content = re.sub(key_pattern, '', content)
    
    # Add import at the top (after other imports)
    if 'from config import' not in content:
        # Find the last import statement
        lines = content.split('\n')
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                last_import_idx = i
        
        # Insert the config import after the last import
        lines.insert(last_import_idx + 1, replacement_import)
        content = '\n'.join(lines)
    
    # Clean up extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original_content:
        filepath.write_text(content, encoding='utf-8')
        print(f"✓ Fixed {filename}")
    else:
        print(f"- {filename} already clean")

print("\n✅ All files updated to use environment variables!")
print("Make sure your .env file contains:")
print("  VITE_SUPABASE_URL=your_url")
print("  VITE_SUPABASE_PUBLISHABLE_KEY=your_key")
