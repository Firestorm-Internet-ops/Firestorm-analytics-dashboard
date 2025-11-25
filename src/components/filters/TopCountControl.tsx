import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useDashboardStore } from '@/lib/store';
import { useState } from 'react';

export const TopCountControl = () => {
  const { topCount, setTopCount } = useDashboardStore();
  const [customValue, setCustomValue] = useState(topCount.toString());

  const handleChange = (value: string) => {
    if (value === 'custom') return;
    setTopCount(parseInt(value));
    setCustomValue(value);
  };

  const handleCustomChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setCustomValue(value);
    const num = parseInt(value);
    if (!isNaN(num) && num > 0) {
      setTopCount(num);
    }
  };

  return (
    <div className="flex items-center gap-4">
      <Label className="text-sm font-semibold text-foreground">Top Cities/Campaigns:</Label>
      <div className="flex gap-2">
        <Select
          value={[5, 10, 20].includes(topCount) ? topCount.toString() : 'custom'}
          onValueChange={handleChange}
        >
          <SelectTrigger className="w-[120px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="5">Top 5</SelectItem>
            <SelectItem value="10">Top 10</SelectItem>
            <SelectItem value="20">Top 20</SelectItem>
            <SelectItem value="custom">Custom</SelectItem>
          </SelectContent>
        </Select>

        {![5, 10, 20].includes(topCount) && (
          <Input
            type="number"
            min="1"
            value={customValue}
            onChange={handleCustomChange}
            className="w-[80px]"
          />
        )}
      </div>
    </div>
  );
};
