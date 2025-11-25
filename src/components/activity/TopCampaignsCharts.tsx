import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Download } from 'lucide-react';

interface CampaignData {
  date: string;
  [key: string]: number | string;
}

interface TopCampaignsChartsProps {
  visitorsData: CampaignData[];
  bookingsData: CampaignData[];
  conversionData: CampaignData[];
  revenueData: CampaignData[];
  topCampaigns: string[];
}

const colors = [
  'hsl(var(--chart-1))',
  'hsl(var(--chart-2))',
  'hsl(var(--chart-3))',
  'hsl(var(--chart-4))',
  'hsl(var(--chart-5))',
];

const downloadCSV = (data: CampaignData[], filename: string) => {
  const headers = Object.keys(data[0] || {});
  const csvContent = [
    headers.join(','),
    ...data.map(row => headers.map(header => row[header]).join(','))
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
};

const ChartCard = ({ 
  title, 
  data, 
  campaigns,
  filename 
}: { 
  title: string; 
  data: CampaignData[]; 
  campaigns: string[];
  filename: string;
}) => (
  <Card>
    <CardHeader>
      <div className="flex items-center justify-between">
        <CardTitle className="text-lg">{title}</CardTitle>
        <Button
          variant="outline"
          size="sm"
          onClick={() => downloadCSV(data, filename)}
          className="gap-2"
        >
          <Download className="h-4 w-4" />
          CSV
        </Button>
      </div>
    </CardHeader>
    <CardContent>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis 
            dataKey="date" 
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
          />
          <YAxis 
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'hsl(var(--card))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '8px',
            }}
          />
          <Legend />
          {campaigns.map((campaign, index) => (
            <Line
              key={campaign}
              type="monotone"
              dataKey={campaign}
              stroke={colors[index % colors.length]}
              strokeWidth={2}
              dot={{ fill: colors[index % colors.length] }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </CardContent>
  </Card>
);

export const TopCampaignsCharts = ({
  visitorsData,
  bookingsData,
  conversionData,
  revenueData,
  topCampaigns,
}: TopCampaignsChartsProps) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-foreground">Top Campaigns Performance</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Top Campaigns by Visitors"
          data={visitorsData}
          campaigns={topCampaigns}
          filename="top-campaigns-visitors.csv"
        />
        <ChartCard
          title="Top Campaigns by Bookings"
          data={bookingsData}
          campaigns={topCampaigns}
          filename="top-campaigns-bookings.csv"
        />
        <ChartCard
          title="Top Campaigns by Conversion Rate"
          data={conversionData}
          campaigns={topCampaigns}
          filename="top-campaigns-conversion.csv"
        />
        <ChartCard
          title="Top Campaigns by Revenue"
          data={revenueData}
          campaigns={topCampaigns}
          filename="top-campaigns-revenue.csv"
        />
      </div>
    </div>
  );
};
