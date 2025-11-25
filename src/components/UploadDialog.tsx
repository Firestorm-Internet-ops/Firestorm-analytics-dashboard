import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Button } from './ui/button';
import { Upload, FileSpreadsheet, CheckCircle2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { supabase } from '@/integrations/supabase/client';
import * as XLSX from 'xlsx';

interface UploadDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const UploadDialog = ({ open, onOpenChange }: UploadDialogProps) => {
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState(false);
  const { toast } = useToast();

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setSuccess(false);

    try {
      const data = await file.arrayBuffer();
      const workbook = XLSX.read(data);
      const worksheet = workbook.Sheets[workbook.SheetNames[0]];
      const jsonData = XLSX.utils.sheet_to_json(worksheet);

      // Transform data to match master_sheet schema
      const transformedData = jsonData.map((row: any) => {
        // Handle Excel date formats (Excel stores dates as numbers since 1900-01-01)
        let date: Date;
        const rawDate = row.Date || row.date;
        
        if (typeof rawDate === 'number') {
          // Excel date number format
          const excelEpoch = new Date(1899, 11, 30);
          date = new Date(excelEpoch.getTime() + rawDate * 86400000);
        } else {
          // String date format
          date = new Date(rawDate);
        }
        
        return {
          date: date.toISOString().split('T')[0],
          day: date.getDate().toString(),
          month: (date.getMonth() + 1).toString(),
          year: date.getFullYear().toString(),
          source: row.Source || row.source || 'Unknown',
          city: row.City || row.city || 'Unknown',
          campaign_id: row.CampaignId || row.campaign_id || row.campaignId || null,
          visitors: parseInt(row.Visitors || row.visitors || '0'),
          bookings: parseInt(row.Bookings || row.bookings || '0'),
          revenue: parseFloat(row.Revenue || row.revenue || '0'),
        };
      });

      // Insert data into master_sheet
      const { error } = await supabase
        .from('master_sheet')
        .insert(transformedData);

      if (error) throw error;

      setSuccess(true);
      toast({
        title: 'Upload successful!',
        description: `${transformedData.length} records added to database.`,
      });

      // Reset after delay
      setTimeout(() => {
        setSuccess(false);
        onOpenChange(false);
        window.location.reload(); // Refresh to show new data
      }, 2000);

    } catch (error: any) {
      toast({
        title: 'Upload failed',
        description: error.message || 'Please check your file format and try again.',
        variant: 'destructive',
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Upload Excel/CSV File</DialogTitle>
          <DialogDescription>
            Upload your analytics data file. The data will be added to your master database.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {success ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <CheckCircle2 className="h-16 w-16 text-success mb-4" />
              <p className="text-lg font-semibold text-foreground">Upload Successful!</p>
              <p className="text-sm text-muted-foreground">Refreshing dashboard...</p>
            </div>
          ) : (
            <>
              <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={handleFileUpload}
                  disabled={uploading}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <FileSpreadsheet className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-sm text-foreground font-medium mb-2">
                    {uploading ? 'Uploading...' : 'Click to upload or drag and drop'}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Excel (.xlsx, .xls) or CSV files
                  </p>
                </label>
              </div>

              <div className="text-xs text-muted-foreground space-y-1">
                <p className="font-semibold">Expected columns:</p>
                <ul className="list-disc list-inside space-y-0.5 ml-2">
                  <li>Date, Source, City, CampaignId (optional)</li>
                  <li>Visitors, Bookings, Revenue</li>
                </ul>
              </div>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};
