import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import { Calendar as CalendarIcon } from 'lucide-react';
import { useDashboardStore } from '@/lib/store';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useState } from 'react';

export const DateRangeFilter = () => {
  const { dateRange, setDateRange, datePreset, setDatePreset } = useDashboardStore();

  const handlePresetChange = (value: string) => {
    setDatePreset(value);
    const now = new Date();
    now.setHours(23, 59, 59, 999); // Set to end of day
    let from: Date;

    switch (value) {
      case 'last7days':
        from = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        from.setHours(0, 0, 0, 0);
        break;
      case 'last30days':
        from = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        from.setHours(0, 0, 0, 0);
        break;
      case 'lastMonth':
        from = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        from.setHours(0, 0, 0, 0);
        break;
      case 'last60days':
        from = new Date(now.getTime() - 60 * 24 * 60 * 60 * 1000);
        from.setHours(0, 0, 0, 0);
        break;
      case 'last90days':
        from = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
        from.setHours(0, 0, 0, 0);
        break;
      default:
        return;
    }

    setDateRange({ from, to: now });
  };
  
  const handleCustomDateChange = (field: 'from' | 'to', date: Date | undefined) => {
    if (date) {
      if (field === 'from') {
        date.setHours(0, 0, 0, 0);
      } else {
        date.setHours(23, 59, 59, 999);
      }
    }
    setDateRange({ ...dateRange, [field]: date });
  };

  return (
    <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
      <Select value={datePreset} onValueChange={handlePresetChange}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Select range" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="last7days">Last 7 Days</SelectItem>
          <SelectItem value="last30days">Last 30 Days</SelectItem>
          <SelectItem value="lastMonth">Last Month</SelectItem>
          <SelectItem value="last60days">Last 60 Days</SelectItem>
          <SelectItem value="last90days">Last 90 Days</SelectItem>
          <SelectItem value="custom">Custom Range</SelectItem>
        </SelectContent>
      </Select>

      {datePreset === 'custom' && (
        <div className="flex gap-2">
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className={cn(
                  'justify-start text-left font-normal',
                  !dateRange.from && 'text-muted-foreground'
                )}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {dateRange.from ? format(dateRange.from, 'PPP') : 'Start date'}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={dateRange.from}
                onSelect={(date) => handleCustomDateChange('from', date)}
                defaultMonth={dateRange.from}
                initialFocus
              />
            </PopoverContent>
          </Popover>

          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className={cn(
                  'justify-start text-left font-normal',
                  !dateRange.to && 'text-muted-foreground'
                )}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {dateRange.to ? format(dateRange.to, 'PPP') : 'End date'}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={dateRange.to}
                onSelect={(date) => handleCustomDateChange('to', date)}
                defaultMonth={dateRange.to}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      )}
    </div>
  );
};
