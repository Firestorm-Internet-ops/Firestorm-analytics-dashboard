# Security Guidelines

## Environment Variables

All sensitive credentials are stored in environment variables and **never** committed to the repository.

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your-anon-public-key-here
```

### Setup Instructions

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Get your credentials:**
   - Go to: https://supabase.com/dashboard/project/YOUR_PROJECT/settings/api
   - Copy your Project URL and anon/public key

3. **Update the .env file** with your actual credentials

4. **Never commit the .env file** - It's already in `.gitignore`

## Supabase Configuration

The Supabase project ID is stored in `supabase/config.toml`:

1. **Copy the example file:**
   ```bash
   cp supabase/config.toml.example supabase/config.toml
   ```

2. **Update with your project ID** from the Supabase dashboard

3. **Never commit config.toml** - It's already in `.gitignore`

## How Credentials Are Used

### Frontend (TypeScript/React)
Uses Vite's environment variable system:
```typescript
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;
```

### Backend (Python Scripts)
Uses `python-dotenv` and a centralized config:
```python
from config import SUPABASE_URL, SUPABASE_KEY
```

## Files That Should NEVER Be Committed

- `.env` - Contains actual credentials
- `.env.local` - Local overrides
- `.env.production` - Production credentials
- `supabase/config.toml` - Contains project ID
- `etl/raw_data/` - Raw data files
- `etl/processed/` - Processed data files
- `etl/logs/` - Log files

All of these are already in `.gitignore`.

## What IS Safe to Commit

- `.env.example` - Template with placeholder values
- `supabase/config.toml.example` - Template with placeholder project ID
- `config.py` - Loads from environment variables (no secrets)
- All source code files

## Key Rotation

If credentials are ever exposed:

1. **Rotate Supabase Keys:**
   - Go to: https://supabase.com/dashboard/project/YOUR_PROJECT/settings/api
   - Click "Reset" on the anon/public key
   - Update your local `.env` file with the new key

2. **Update All Environments:**
   - Development: Update `.env`
   - Production: Update environment variables in your hosting platform

3. **Restart Services:**
   - Development: Restart `npm run dev`
   - Production: Redeploy your application

## Security Checklist

Before pushing to GitHub:

- [ ] No hardcoded credentials in any files
- [ ] `.env` file is in `.gitignore`
- [ ] `supabase/config.toml` is in `.gitignore`
- [ ] All credentials come from environment variables
- [ ] `.env.example` contains only placeholder values
- [ ] Test files with credentials are removed or use env vars

## Reporting Security Issues

If you discover a security vulnerability, please email: security@firestorm.com

Do not create a public GitHub issue for security vulnerabilities.
