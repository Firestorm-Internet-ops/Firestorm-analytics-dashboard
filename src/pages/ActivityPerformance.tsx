import { Navbar } from '@/components/Navbar';
import { DateRangeFilter } from '@/components/filters/DateRangeFilter';
import { ViewTabs } from '@/components/filters/ViewTabs';
import { SourceFilter } from '@/components/filters/SourceFilter';
import { TopCountControl } from '@/components/filters/TopCountControl';
import { TopCitiesCharts } from '@/components/activity/TopCitiesCharts';
import { TopCampaignsCharts } from '@/components/activity/TopCampaignsCharts';
import { useDashboardStore } from '@/lib/store';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';
import { getTopItems, prepareActivityChartData } from '@/lib/utils/dataProcessing';

const ActivityPerformance = () => {
  const { dateRange, viewType, selectedSources, topCount } = useDashboardStore();

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

        const { data, error} = await query;
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
  });

  // Get top cities for each metric
  const topCitiesByVisitors = getTopItems(masterData, 'city', 'visitors', topCount);
  const topCitiesByBookings = getTopItems(masterData, 'city', 'bookings', topCount);
  const topCitiesByRevenue = getTopItems(masterData, 'city', 'revenue', topCount);

  // Get top campaigns for each metric
  const topCampaignsByVisitors = getTopItems(masterData, 'campaign_id', 'visitors', topCount);
  const topCampaignsByBookings = getTopItems(masterData, 'campaign_id', 'bookings', topCount);
  const topCampaignsByRevenue = getTopItems(masterData, 'campaign_id', 'revenue', topCount);

  // Prepare chart data for cities
  const prepareChartForMetric = (items: string[], groupBy: 'city' | 'campaign_id', metric: 'visitors' | 'bookings' | 'revenue') => {
    const baseData = prepareActivityChartData(masterData, items, groupBy, viewType);
    
    return baseData.map(point => {
      const newPoint: any = { date: point.date };
      items.forEach(item => {
        if (metric === 'visitors') {
          newPoint[item] = point[`${item}_visitors`] || 0;
        } else if (metric === 'bookings') {
          newPoint[item] = point[`${item}_bookings`] || 0;
        } else {
          const visitors = point[`${item}_visitors`] || 0;
          const bookings = point[`${item}_bookings`] || 0;
          newPoint[item] = visitors ? (bookings / visitors) * 100 : 0;
        }
      });
      return newPoint;
    });
  };

  const citiesVisitorsData = prepareChartForMetric(topCitiesByVisitors, 'city', 'visitors');
  const citiesBookingsData = prepareChartForMetric(topCitiesByBookings, 'city', 'bookings');
  const citiesConversionData = prepareChartForMetric(topCitiesByVisitors, 'city', 'visitors');
  const citiesRevenueData = prepareChartForMetric(topCitiesByRevenue, 'city', 'revenue');

  const campaignsVisitorsData = prepareChartForMetric(topCampaignsByVisitors, 'campaign_id', 'visitors');
  const campaignsBookingsData = prepareChartForMetric(topCampaignsByBookings, 'campaign_id', 'bookings');
  const campaignsConversionData = prepareChartForMetric(topCampaignsByVisitors, 'campaign_id', 'visitors');
  const campaignsRevenueData = prepareChartForMetric(topCampaignsByRevenue, 'campaign_id', 'revenue');

  return (
    <>
      <Navbar />
      <div className="container mx-auto p-6 space-y-6">
        <div className="flex flex-col gap-6">
          <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
            <h1 className="text-3xl font-bold text-foreground">Activity Performance</h1>
            <DateRangeFilter />
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <ViewTabs />
            <SourceFilter />
            <TopCountControl />
          </div>
        </div>

        <TopCitiesCharts
          visitorsData={citiesVisitorsData}
          bookingsData={citiesBookingsData}
          conversionData={citiesConversionData}
          revenueData={citiesRevenueData}
          topCities={topCitiesByVisitors}
        />

        <TopCampaignsCharts
          visitorsData={campaignsVisitorsData}
          bookingsData={campaignsBookingsData}
          conversionData={campaignsConversionData}
          revenueData={campaignsRevenueData}
          topCampaigns={topCampaignsByVisitors}
        />
      </div>
    </>
  );
};

export default ActivityPerformance;
