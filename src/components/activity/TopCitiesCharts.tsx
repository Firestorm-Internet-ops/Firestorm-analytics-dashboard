import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Download } from 'lucide-react';
import { useDashboardStore } from '@/lib/store';

interface CityData {
  date: string;
  [key: string]: number | string;
}

interface TopCitiesChartsProps {
  visitorsData: CityData[];
  bookingsData: CityData[];
  conversionData: CityData[];
  revenueData: CityData[];
  topCities: string[];
}

const colors = [
  'hsl(var(--chart-1))',
  'hsl(var(--chart-2))',
  'hsl(var(--chart-3))',
  'hsl(var(--chart-4))',
  'hsl(var(--chart-5))',
];

const downloadCSV = (data: CityData[], filename: string) => {
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
  cities,
  filename 
}: { 
  title: string; 
  data: CityData[]; 
  cities: string[];
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
          {cities.map((city, index) => (
            <Line
              key={city}
              type="monotone"
              dataKey={city}
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

export const TopCitiesCharts = ({
  visitorsData,
  bookingsData,
  conversionData,
  revenueData,
  topCities,
}: TopCitiesChartsProps) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-foreground">Top Cities Performance</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Top Cities by Visitors"
          data={visitorsData}
          cities={topCities}
          filename="top-cities-visitors.csv"
        />
        <ChartCard
          title="Top Cities by Bookings"
          data={bookingsData}
          cities={topCities}
          filename="top-cities-bookings.csv"
        />
        <ChartCard
          title="Top Cities by Conversion Rate"
          data={conversionData}
          cities={topCities}
          filename="top-cities-conversion.csv"
        />
        <ChartCard
          title="Top Cities by Revenue"
          data={revenueData}
          cities={topCities}
          filename="top-cities-revenue.csv"
        />
      </div>
    </div>
  );
};
