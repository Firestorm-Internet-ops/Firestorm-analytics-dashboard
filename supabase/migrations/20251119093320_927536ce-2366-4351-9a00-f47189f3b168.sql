-- Fix the search_path issue for the update function
CREATE OR REPLACE FUNCTION public.update_master_sheet_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public;