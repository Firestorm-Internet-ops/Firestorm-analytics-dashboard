import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useDashboardStore } from '@/lib/store';

export const ViewTabs = () => {
  const { viewType, setViewType } = useDashboardStore();

  return (
    <Tabs value={viewType} onValueChange={(value: any) => setViewType(value)}>
      <TabsList>
        <TabsTrigger value="day">Day</TabsTrigger>
        <TabsTrigger value="week">Week</TabsTrigger>
        <TabsTrigger value="month">Month</TabsTrigger>
      </TabsList>
    </Tabs>
  );
};
