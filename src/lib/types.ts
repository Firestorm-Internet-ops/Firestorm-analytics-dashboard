export interface MasterSheetData {
  id: string;
  date: string;
  day: string;
  month: string;
  year: string;
  source: string;
  city: string;
  campaign_id: string | null;
  visitors: number;
  bookings: number;
  revenue: number;
  created_at?: string;
  updated_at?: string;
}

export interface KPIData {
  visitors: number;
  bookings: number;
  conversionRate: number;
  revenue: number;
  visitorsChange: number;
  bookingsChange: number;
  conversionRateChange: number;
  revenueChange: number;
}

export interface ChartDataPoint {
  date: string;
  visitors?: number;
  bookings?: number;
  conversionRate?: number;
  revenue?: number;
}

export type ViewType = 'day' | 'week' | 'month';

export interface DateRange {
  from: Date | undefined;
  to: Date | undefined;
}

export type Metric = 'visitors' | 'bookings' | 'conversionRate' | 'revenue';
