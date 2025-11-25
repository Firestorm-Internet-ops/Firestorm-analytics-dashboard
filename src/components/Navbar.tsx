import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Upload, LogOut } from 'lucide-react';
import { useState } from 'react';
import { UploadDialog } from './UploadDialog';
import { supabase } from '@/integrations/supabase/client';
import { useToast } from '@/hooks/use-toast';

export const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [uploadOpen, setUploadOpen] = useState(false);
  const { toast } = useToast();

  const handleLogout = async () => {
    try {
      await supabase.auth.signOut();
      toast({
        title: 'Logged out',
        description: 'You have been logged out successfully',
      });
      navigate('/login');
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.message || 'Failed to logout',
        variant: 'destructive',
      });
    }
  };

  return (
    <>
      <nav className="border-b border-border bg-card sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-2">
              <img src="/firestorm-logo.png" alt="Firestorm Analytics" className="h-8 w-8" />
              <span className="text-xl font-bold text-foreground">Firestorm Analytics</span>
            </Link>
            
            <div className="flex items-center gap-1">
              <Link to="/">
                <Button 
                  variant={location.pathname === '/' ? 'default' : 'ghost'}
                  size="sm"
                >
                  Dashboard
                </Button>
              </Link>
              <Link to="/activity">
                <Button 
                  variant={location.pathname === '/activity' ? 'default' : 'ghost'}
                  size="sm"
                >
                  Activity Performance
                </Button>
              </Link>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button 
              onClick={() => setUploadOpen(true)}
              className="gap-2"
            >
              <Upload className="h-4 w-4" />
              Upload Data
            </Button>
            <Button 
              onClick={handleLogout}
              variant="outline"
              className="gap-2"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
      </nav>

      <UploadDialog open={uploadOpen} onOpenChange={setUploadOpen} />
    </>
  );
};
