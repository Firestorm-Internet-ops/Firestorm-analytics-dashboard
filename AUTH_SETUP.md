# Authentication Setup Guide

## Supabase Authentication Configuration

The login system is now implemented. To enable it, you need to configure authentication in your Supabase project.

### Steps to Enable Authentication:

1. **Go to Supabase Dashboard**
   - Visit: https://supabase.com/dashboard/project/zbueoutrzlmwqakupedp

2. **Enable Email Authentication**
   - Navigate to: Authentication → Providers
   - Enable "Email" provider
   - Configure email settings (or use Supabase's default email service)

3. **Create Your First User**
   
   **Option A: Via Supabase Dashboard**
   - Go to: Authentication → Users
   - Click "Add User"
   - Enter email and password
   - Click "Create User"

   **Option B: Via SQL (for multiple users)**
   ```sql
   -- Run this in SQL Editor
   INSERT INTO auth.users (
     instance_id,
     id,
     aud,
     role,
     email,
     encrypted_password,
     email_confirmed_at,
     created_at,
     updated_at,
     confirmation_token,
     email_change,
     email_change_token_new,
     recovery_token
   ) VALUES (
     '00000000-0000-0000-0000-000000000000',
     gen_random_uuid(),
     'authenticated',
     'authenticated',
     'your-email@example.com',
     crypt('your-password', gen_salt('bf')),
     NOW(),
     NOW(),
     NOW(),
     '',
     '',
     '',
     ''
   );
   ```

4. **Test the Login**
   - Navigate to: http://localhost:8080/login
   - Enter your email and password
   - Click "Sign In"

### Features Implemented:

✅ **Login Page** - Clean, branded login interface
✅ **Protected Routes** - Dashboard and Activity pages require authentication
✅ **Session Management** - Automatic session persistence
✅ **Logout Functionality** - Logout button in navbar
✅ **Auto-redirect** - Unauthenticated users redirected to login
✅ **Loading States** - Smooth loading indicators

### Security Features:

- Passwords are securely hashed by Supabase
- Sessions stored in localStorage with auto-refresh
- Protected routes check authentication on every page load
- Automatic session validation

### Default Behavior:

- When not logged in → Redirected to `/login`
- After successful login → Redirected to `/` (Dashboard)
- After logout → Redirected to `/login`

### Troubleshooting:

**Issue: Can't login**
- Verify email provider is enabled in Supabase
- Check that user exists in Authentication → Users
- Ensure email is confirmed (email_confirmed_at is set)

**Issue: Redirects to login immediately**
- Check browser console for errors
- Verify Supabase credentials in `.env` file
- Clear browser localStorage and try again

### Next Steps (Optional):

- Add password reset functionality
- Implement email verification
- Add role-based access control
- Enable social login (Google, GitHub, etc.)
