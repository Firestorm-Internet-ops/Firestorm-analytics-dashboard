import { MasterSheetData, ChartDataPoint, ViewType } from '../types';
import { format, startOfWeek, startOfMonth } from 'date-fns';

export const groupDataByView = (
  data: MasterSheetData[],
  viewType: ViewType
): ChartDataPoint[] => {
  const grouped = new Map<string, { point: ChartDataPoint; minDate: string }>();

  data.forEach((row) => {
    const date = new Date(row.date);
    let key: string;

    switch (viewType) {
      case 'week':
        key = format(startOfWeek(date), 'yyyy-MM-dd');
        break;
      case 'month':
        key = format(startOfMonth(date), 'yyyy-MM');
        break;
      default: // day
        key = row.date;
    }

    if (!grouped.has(key)) {
      grouped.set(key, {
        point: {
          date: key,
          visitors: 0,
          bookings: 0,
          conversionRate: 0,
          revenue: 0,
        },
        minDate: row.date,
      });
    }

    const entry = grouped.get(key)!;
    // Track the earliest actual date in this group
    if (row.date < entry.minDate) {
      entry.minDate = row.date;
    }
    
    entry.point.visitors = (entry.point.visitors || 0) + row.visitors;
    entry.point.bookings = (entry.point.bookings || 0) + row.bookings;
    entry.point.revenue = (entry.point.revenue || 0) + row.revenue;
  });

  // Calculate conversion rates and use actual min date for week view
  const result: ChartDataPoint[] = [];
  grouped.forEach((entry) => {
    const point = entry.point;
    point.conversionRate = point.visitors ? (point.bookings / point.visitors) * 100 : 0;
    
    // For week view, use the actual earliest date in the data instead of ISO week start
    if (viewType === 'week') {
      point.date = entry.minDate;
    }
    
    result.push(point);
  });

  return result.sort((a, b) => a.date.localeCompare(b.date));
};

export const calculateKPIs = (data: MasterSheetData[]) => {
  const visitors = data.reduce((sum, row) => sum + row.visitors, 0);
  const bookings = data.reduce((sum, row) => sum + row.bookings, 0);
  const revenue = data.reduce((sum, row) => sum + row.revenue, 0);
  const conversionRate = visitors ? (bookings / visitors) * 100 : 0;

  return { visitors, bookings, revenue, conversionRate };
};

export const getTopItems = (
  data: MasterSheetData[],
  groupBy: 'city' | 'campaign_id',
  metric: 'visitors' | 'bookings' | 'revenue',
  count: number
): string[] => {
  const grouped = new Map<string, number>();

  data.forEach((row) => {
    const key = groupBy === 'city' ? row.city : row.campaign_id || 'Unknown';
    grouped.set(key, (grouped.get(key) || 0) + row[metric]);
  });

  return Array.from(grouped.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, count)
    .map(([key]) => key);
};

export const prepareActivityChartData = (
  data: MasterSheetData[],
  items: string[],
  groupBy: 'city' | 'campaign_id',
  viewType: ViewType
) => {
  const grouped = new Map<string, any>();
  const minDates = new Map<string, string>();

  data.forEach((row) => {
    const itemKey = groupBy === 'city' ? row.city : row.campaign_id || 'Unknown';
    if (!items.includes(itemKey)) return;

    const date = new Date(row.date);
    let dateKey: string;

    switch (viewType) {
      case 'week':
        dateKey = format(startOfWeek(date), 'yyyy-MM-dd');
        break;
      case 'month':
        dateKey = format(startOfMonth(date), 'yyyy-MM');
        break;
      default:
        dateKey = row.date;
    }

    if (!grouped.has(dateKey)) {
      grouped.set(dateKey, { date: dateKey });
      minDates.set(dateKey, row.date);
      items.forEach(item => {
        grouped.get(dateKey)![item] = 0;
        grouped.get(dateKey)![`${item}_visitors`] = 0;
        grouped.get(dateKey)![`${item}_bookings`] = 0;
      });
    }

    // Track earliest actual date in this group
    const currentMin = minDates.get(dateKey)!;
    if (row.date < currentMin) {
      minDates.set(dateKey, row.date);
    }

    const point = grouped.get(dateKey)!;
    point[`${itemKey}_visitors`] = (point[`${itemKey}_visitors`] || 0) + row.visitors;
    point[`${itemKey}_bookings`] = (point[`${itemKey}_bookings`] || 0) + row.bookings;
  });

  // For week view, use actual earliest date instead of ISO week start
  if (viewType === 'week') {
    grouped.forEach((point, key) => {
      point.date = minDates.get(key);
    });
  }

  return Array.from(grouped.values()).sort((a, b) => a.date.localeCompare(b.date));
};
