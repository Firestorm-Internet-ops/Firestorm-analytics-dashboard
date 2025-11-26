"""
Security verification script
Checks that no hardcoded credentials exist in the codebase
"""
import re
from pathlib import Path

# Patterns to search for
PATTERNS = {
    'Supabase URL': r'https://[a-z0-9]+\.supabase\.co',
    'JWT Token': r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
    'API Key Pattern': r'["\'](?:SUPABASE_KEY|SUPABASE_ANON_KEY)["\']:\s*["\'][^"\']{20,}["\']',
}

# Files/folders to exclude
EXCLUDE = {
    '.git', 'node_modules', '__pycache__', 'dist', 'build',
    '.env', '.env.local', '.env.production',  # These should not be in repo anyway
    'verify_security.py',  # This file
    'SECURITY.md',  # Documentation
    'fix_credentials.py',  # Helper script
}

# File extensions to check
EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx', '.html', '.toml', '.json', '.md'}

def should_check_file(filepath):
    """Determine if file should be checked"""
    # Skip excluded paths
    for exclude in EXCLUDE:
        if exclude in str(filepath):
            return False
    
    # Only check certain extensions
    if filepath.suffix not in EXTENSIONS:
        return False
    
    # Skip example files
    if '.example' in filepath.name:
        return False
    
    return True

def check_file(filepath):
    """Check a single file for hardcoded credentials"""
    issues = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
        
        for pattern_name, pattern in PATTERNS.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                # Get line number
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'file': str(filepath),
                    'line': line_num,
                    'type': pattern_name,
                    'match': match.group()[:50] + '...' if len(match.group()) > 50 else match.group()
                })
    except Exception as e:
        print(f"⚠️  Error reading {filepath}: {e}")
    
    return issues

def main():
    print("🔍 Scanning codebase for hardcoded credentials...\n")
    
    all_issues = []
    files_checked = 0
    
    # Scan all files
    for filepath in Path('.').rglob('*'):
        if filepath.is_file() and should_check_file(filepath):
            files_checked += 1
            issues = check_file(filepath)
            all_issues.extend(issues)
    
    print(f"📁 Files checked: {files_checked}\n")
    
    if all_issues:
        print("❌ SECURITY ISSUES FOUND:\n")
        for issue in all_issues:
            print(f"  File: {issue['file']}")
            print(f"  Line: {issue['line']}")
            print(f"  Type: {issue['type']}")
            print(f"  Match: {issue['match']}")
            print()
        print(f"Total issues: {len(all_issues)}")
        return 1
    else:
        print("✅ No hardcoded credentials found!")
        print("✅ All credentials are properly using environment variables")
        return 0

if __name__ == '__main__':
    exit(main())
