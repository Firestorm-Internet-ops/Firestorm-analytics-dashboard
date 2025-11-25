# Git Push Commands

## Step 1: Add Git to PATH (if needed)
Run this in PowerShell if git command doesn't work:
```powershell
$env:Path += ";C:\Program Files\Git\bin"
```

## Step 2: Navigate to Your Project
```bash
cd "C:\Users\alvin\OneDrive\Desktop\Dashboard"
```

## Step 3: Check Git Status
```bash
git status
```

## Step 4: Stage All Changes
```bash
git add .
```

## Step 5: Commit Changes
```bash
git commit -m "feat: Complete Firestorm Analytics dashboard

- Rebranded to Firestorm Analytics with custom logo
- Implemented secure login with Supabase authentication
- Added password visibility toggle on login page
- Redesigned filters: removed tabs, added source dropdown
- Fixed week grouping to show actual data dates
- Implemented campaign suffix normalization
- Added intelligent city mapping from campaign IDs (100+ cities)
- Updated calendar to default to selected month
- Added logout functionality in navbar
- Protected routes with authentication
- Session management with auto-refresh"
```

## Step 6: Check Remote Repository
```bash
git remote -v
```

If no remote is set up, add it:
```bash
git remote add origin YOUR_GITHUB_REPO_URL
```

## Step 7: Push to GitHub
```bash
# If this is your first push
git push -u origin main

# Or if branch is named 'master'
git push -u origin master

# For subsequent pushes
git push
```

## Troubleshooting

### If you get "branch not found" error:
```bash
# Check current branch
git branch

# If on master but remote expects main
git branch -M main
git push -u origin main
```

### If you need to pull first:
```bash
git pull origin main --rebase
git push
```

### If you need to force push (use carefully):
```bash
git push -f origin main
```

## Quick One-Liner (after navigating to project)
```bash
git add . && git commit -m "feat: Complete Firestorm Analytics dashboard with authentication and city mapping" && git push
```

## Files Added/Modified in This Session

### New Files:
- `src/pages/Login.tsx` - Login page with authentication
- `src/components/ProtectedRoute.tsx` - Route protection component
- `etl/processors/city_mapper.py` - City extraction from campaign IDs
- `etl/processors/campaign_normalizer.py` - Campaign suffix removal
- `enrich_cities.py` - Database city enrichment script
- `AUTH_SETUP.md` - Authentication setup guide
- `etl/CITY_MAPPING.md` - City mapping documentation
- `public/firestorm-logo.png` - New logo
- `public/firestorm-logo.svg` - New logo SVG

### Modified Files:
- `src/App.tsx` - Added protected routes
- `src/components/Navbar.tsx` - Added logout, updated branding
- `src/pages/Index.tsx` - Redesigned filters
- `src/pages/ActivityPerformance.tsx` - Redesigned filters
- `src/components/filters/SourceFilter.tsx` - Converted to dropdown
- `src/components/filters/DateRangeFilter.tsx` - Fixed calendar month
- `src/lib/utils/dataProcessing.ts` - Fixed week grouping
- `etl/process_data.py` - Added city enrichment
- `index.html` - Updated branding and favicon
- `src/components/WelcomeScreen.tsx` - Updated branding
