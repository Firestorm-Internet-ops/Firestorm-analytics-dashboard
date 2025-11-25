import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useDashboardStore } from '@/lib/store';
import { ChartDataPoint, Metric } from '@/lib/types';

interface DashboardLineChartProps {
  data: ChartDataPoint[];
}

const metricConfig = {
  visitors: { color: 'hsl(var(--chart-1))', label: 'Visitors' },
  bookings: { color: 'hsl(var(--chart-2))', label: 'Bookings' },
  conversionRate: { color: 'hsl(var(--chart-3))', label: 'Conversion Rate (%)' },
  revenue: { color: 'hsl(var(--chart-4))', label: 'Revenue (€)' },
};

export const DashboardLineChart = ({ data }: DashboardLineChartProps) => {
  const { selectedMetrics, setSelectedMetrics } = useDashboardStore();

  const toggleMetric = (metric: Metric) => {
    if (selectedMetrics.includes(metric)) {
      setSelectedMetrics(selectedMetrics.filter(m => m !== metric));
    } else {
      setSelectedMetrics([...selectedMetrics, metric]);
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between flex-wrap gap-4">
          <CardTitle>Performance Trends</CardTitle>
          <div className="flex flex-wrap gap-2">
            {Object.entries(metricConfig).map(([key, config]) => (
              <Button
                key={key}
                variant={selectedMetrics.includes(key as Metric) ? 'default' : 'outline'}
                size="sm"
                onClick={() => toggleMetric(key as Metric)}
              >
                {config.label}
              </Button>
            ))}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
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
            {selectedMetrics.includes('visitors') && (
              <Line
                type="monotone"
                dataKey="visitors"
                stroke={metricConfig.visitors.color}
                strokeWidth={2}
                name={metricConfig.visitors.label}
                dot={{ fill: metricConfig.visitors.color }}
              />
            )}
            {selectedMetrics.includes('bookings') && (
              <Line
                type="monotone"
                dataKey="bookings"
                stroke={metricConfig.bookings.color}
                strokeWidth={2}
                name={metricConfig.bookings.label}
                dot={{ fill: metricConfig.bookings.color }}
              />
            )}
            {selectedMetrics.includes('conversionRate') && (
              <Line
                type="monotone"
                dataKey="conversionRate"
                stroke={metricConfig.conversionRate.color}
                strokeWidth={2}
                name={metricConfig.conversionRate.label}
                dot={{ fill: metricConfig.conversionRate.color }}
              />
            )}
            {selectedMetrics.includes('revenue') && (
              <Line
                type="monotone"
                dataKey="revenue"
                stroke={metricConfig.revenue.color}
                strokeWidth={2}
                name={metricConfig.revenue.label}
                dot={{ fill: metricConfig.revenue.color }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};
