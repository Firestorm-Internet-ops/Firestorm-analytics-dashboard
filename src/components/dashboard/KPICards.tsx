import { Card, CardContent } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Users, ShoppingCart, Percent, Euro } from 'lucide-react';
import { cn } from '@/lib/utils';

interface KPICardProps {
  title: string;
  value: string | number;
  change: number;
  icon: React.ReactNode;
}

const KPICard = ({ title, value, change, icon }: KPICardProps) => {
  const isPositive = change >= 0;

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center justify-between mb-4">
          <div className="p-2 bg-primary/10 rounded-lg">
            {icon}
          </div>
          <div className={cn(
            'flex items-center gap-1 text-sm font-medium',
            isPositive ? 'text-success' : 'text-destructive'
          )}>
            {isPositive ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
            {Math.abs(change).toFixed(1)}%
          </div>
        </div>
        <div>
          <p className="text-sm text-muted-foreground mb-1">{title}</p>
          <p className="text-3xl font-bold text-foreground">{value}</p>
        </div>
      </CardContent>
    </Card>
  );
};

interface KPICardsProps {
  visitors: number;
  bookings: number;
  conversionRate: number;
  revenue: number;
  visitorsChange: number;
  bookingsChange: number;
  conversionRateChange: number;
  revenueChange: number;
}

export const KPICards = ({
  visitors,
  bookings,
  conversionRate,
  revenue,
  visitorsChange,
  bookingsChange,
  conversionRateChange,
  revenueChange,
}: KPICardsProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <KPICard
        title="Visitors"
        value={visitors.toLocaleString()}
        change={visitorsChange}
        icon={<Users className="h-5 w-5 text-primary" />}
      />
      <KPICard
        title="Bookings"
        value={bookings.toLocaleString()}
        change={bookingsChange}
        icon={<ShoppingCart className="h-5 w-5 text-primary" />}
      />
      <KPICard
        title="Conversion Rate"
        value={`${conversionRate.toFixed(2)}%`}
        change={conversionRateChange}
        icon={<Percent className="h-5 w-5 text-primary" />}
      />
      <KPICard
        title="Total Revenue"
        value={`€${revenue.toLocaleString()}`}
        change={revenueChange}
        icon={<Euro className="h-5 w-5 text-primary" />}
      />
    </div>
  );
};
