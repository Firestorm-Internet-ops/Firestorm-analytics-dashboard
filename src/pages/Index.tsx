import { useState } from 'react';
import { Navbar } from '@/components/Navbar';
import { WelcomeScreen } from '@/components/WelcomeScreen';
import { DateRangeFilter } from '@/components/filters/DateRangeFilter';
import { ViewTabs } from '@/components/filters/ViewTabs';
import { SourceFilter } from '@/components/filters/SourceFilter';
import { KPICards } from '@/components/dashboard/KPICards';
import { DashboardLineChart } from '@/components/dashboard/DashboardLineChart';
import { BreakdownTable } from '@/components/dashboard/BreakdownTable';
import { useDashboardStore } from '@/lib/store';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';
import { groupDataByView, calculateKPIs } from '@/lib/utils/dataProcessing';
import { UploadDialog } from '@/components/UploadDialog';

const Dashboard = () => {
  const [uploadOpen, setUploadOpen] = useState(false);
  const { dateRange, viewType, selectedSources } = useDashboardStore();

  // Check if data exists
  const { data: hasData } = useQuery({
    queryKey: ['hasData'],
    queryFn: async () => {
      const { count } = await supabase
        .from('master_sheet')
        .select('*', { count: 'exact', head: true });
      return (count || 0) > 0;
    },
  });

  // Fetch master data with pagination to handle Supabase's 1000 row limit
  const { data: masterData = [] } = useQuery({
    queryKey: ['masterData', dateRange, selectedSources],
    queryFn: async () => {
      const allData: any[] = [];
      const pageSize = 1000;
      let page = 0;
      let hasMore = true;

      while (hasMore) {
        let query = supabase
          .from('master_sheet')
          .select('*')
          .order('date')
          .range(page * pageSize, (page + 1) * pageSize - 1);

        if (dateRange.from) {
          query = query.gte('date', dateRange.from.toISOString().split('T')[0]);
        }
        if (dateRange.to) {
          query = query.lte('date', dateRange.to.toISOString().split('T')[0]);
        }
        if (selectedSources.length > 0) {
          query = query.in('source', selectedSources);
        }

        const { data, error } = await query;
        if (error) throw error;
        
        if (data && data.length > 0) {
          allData.push(...data);
          hasMore = data.length === pageSize;
          page++;
        } else {
          hasMore = false;
        }
      }

      return allData;
    },
    enabled: hasData,
  });

  const chartData = groupDataByView(masterData, viewType);
  const currentKPIs = calculateKPIs(masterData);

  // Calculate previous period for change percentages
  const previousData = masterData.slice(0, Math.floor(masterData.length / 2));
  const previousKPIs = calculateKPIs(previousData);

  const calculateChange = (current: number, previous: number) => {
    if (previous === 0) return 0;
    return ((current - previous) / previous) * 100;
  };

  if (!hasData) {
    return (
      <>
        <Navbar />
        <WelcomeScreen onUpload={() => setUploadOpen(true)} />
        <UploadDialog open={uploadOpen} onOpenChange={setUploadOpen} />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="container mx-auto p-6 space-y-6">
        <div className="flex flex-col gap-6">
          <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
            <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
            <DateRangeFilter />
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <ViewTabs />
            <SourceFilter />
          </div>
        </div>

        <KPICards
          visitors={currentKPIs.visitors}
          bookings={currentKPIs.bookings}
          conversionRate={currentKPIs.conversionRate}
          revenue={currentKPIs.revenue}
          visitorsChange={calculateChange(currentKPIs.visitors, previousKPIs.visitors)}
          bookingsChange={calculateChange(currentKPIs.bookings, previousKPIs.bookings)}
          conversionRateChange={calculateChange(currentKPIs.conversionRate, previousKPIs.conversionRate)}
          revenueChange={calculateChange(currentKPIs.revenue, previousKPIs.revenue)}
        />

        <DashboardLineChart data={chartData} />
        <BreakdownTable data={chartData} />
      </div>
    </>
  );
};

export default Dashboard;
