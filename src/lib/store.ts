import { create } from 'zustand';
import { ViewType, DateRange, Metric } from './types';

interface DashboardState {
  dateRange: DateRange;
  viewType: ViewType;
  selectedSources: string[];
  topCount: number;
  selectedMetrics: Metric[];
  datePreset: string;
  setDateRange: (range: DateRange) => void;
  setViewType: (view: ViewType) => void;
  setSelectedSources: (sources: string[]) => void;
  setTopCount: (count: number) => void;
  setSelectedMetrics: (metrics: Metric[]) => void;
  setDatePreset: (preset: string) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  dateRange: {
    from: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
    to: new Date(),
  },
  viewType: 'day',
  selectedSources: [],
  topCount: 5,
  selectedMetrics: ['visitors', 'bookings', 'conversionRate', 'revenue'],
  datePreset: 'last7days',
  setDateRange: (range) => set({ dateRange: range }),
  setViewType: (view) => set({ viewType: view }),
  setSelectedSources: (sources) => set({ selectedSources: sources }),
  setTopCount: (count) => set({ topCount: count }),
  setSelectedMetrics: (metrics) => set({ selectedMetrics: metrics }),
  setDatePreset: (preset) => set({ datePreset: preset }),
}));
