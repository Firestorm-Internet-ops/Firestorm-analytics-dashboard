-- Create the master_sheet table to store all uploaded data
CREATE TABLE IF NOT EXISTS public.master_sheet (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL,
  day TEXT NOT NULL,
  month TEXT NOT NULL,
  year TEXT NOT NULL,
  source TEXT NOT NULL,
  city TEXT NOT NULL,
  campaign_id TEXT,
  visitors INTEGER NOT NULL DEFAULT 0,
  bookings INTEGER NOT NULL DEFAULT 0,
  revenue DECIMAL(10, 2) NOT NULL DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_master_sheet_date ON public.master_sheet(date);
CREATE INDEX IF NOT EXISTS idx_master_sheet_source ON public.master_sheet(source);
CREATE INDEX IF NOT EXISTS idx_master_sheet_city ON public.master_sheet(city);
CREATE INDEX IF NOT EXISTS idx_master_sheet_campaign ON public.master_sheet(campaign_id);

-- Enable RLS
ALTER TABLE public.master_sheet ENABLE ROW LEVEL SECURITY;

-- Allow anyone to read the data (public dashboard)
CREATE POLICY "Allow public read access"
  ON public.master_sheet
  FOR SELECT
  USING (true);

-- Allow anyone to insert data (for uploads)
CREATE POLICY "Allow public insert"
  ON public.master_sheet
  FOR INSERT
  WITH CHECK (true);

-- Create function to update timestamps
CREATE OR REPLACE FUNCTION public.update_master_sheet_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic timestamp updates
CREATE TRIGGER update_master_sheet_updated_at
  BEFORE UPDATE ON public.master_sheet
  FOR EACH ROW
  EXECUTE FUNCTION public.update_master_sheet_updated_at();