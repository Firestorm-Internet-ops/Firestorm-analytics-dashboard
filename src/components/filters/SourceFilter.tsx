import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { useDashboardStore } from '@/lib/store';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { ChevronDown } from 'lucide-react';

export const SourceFilter = () => {
  const { selectedSources, setSelectedSources } = useDashboardStore();

  const { data: sources = [] } = useQuery({
    queryKey: ['sources'],
    queryFn: async () => {
      // Use RPC or fetch with pagination to get all unique sources
      // Fetch in pages to ensure we get all sources
      const allSources = new Set<string>();
      let page = 0;
      const pageSize = 1000;
      
      while (true) {
        const { data, error } = await supabase
          .from('master_sheet')
          .select('source')
          .range(page * pageSize, (page + 1) * pageSize - 1);

        if (error) throw error;
        if (!data || data.length === 0) break;

        data.forEach(item => allSources.add(item.source));
        
        if (data.length < pageSize) break;
        page++;
      }

      return Array.from(allSources).sort();
    },
  });

  const handleSourceToggle = (source: string, checked: boolean) => {
    if (checked) {
      setSelectedSources([...selectedSources, source]);
    } else {
      setSelectedSources(selectedSources.filter(s => s !== source));
    }
  };

  const handleSelectAll = () => {
    if (selectedSources.length === sources.length) {
      setSelectedSources([]);
    } else {
      setSelectedSources(sources);
    }
  };

  const getButtonText = () => {
    if (selectedSources.length === 0) return 'All Sources';
    if (selectedSources.length === sources.length) return 'All Sources';
    if (selectedSources.length === 1) return selectedSources[0];
    return `${selectedSources.length} Sources`;
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="min-w-[150px] justify-between">
          {getButtonText()}
          <ChevronDown className="ml-2 h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56 p-4">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-foreground">Sources</h3>
            <button
              onClick={handleSelectAll}
              className="text-xs text-primary hover:underline"
            >
              {selectedSources.length === sources.length ? 'Deselect All' : 'Select All'}
            </button>
          </div>

          <div className="space-y-3">
            {sources.map((source) => (
              <div key={source} className="flex items-center space-x-2">
                <Checkbox
                  id={source}
                  checked={selectedSources.includes(source)}
                  onCheckedChange={(checked) => handleSourceToggle(source, checked as boolean)}
                />
                <Label
                  htmlFor={source}
                  className="text-sm font-normal cursor-pointer"
                >
                  {source}
                </Label>
              </div>
            ))}
          </div>
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
