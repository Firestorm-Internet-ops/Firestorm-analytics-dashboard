import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { ChartDataPoint } from '@/lib/types';

interface BreakdownTableProps {
  data: ChartDataPoint[];
}

export const BreakdownTable = ({ data }: BreakdownTableProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Performance Breakdown</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead className="text-right">Visitors</TableHead>
                <TableHead className="text-right">Bookings</TableHead>
                <TableHead className="text-right">Conversion Rate</TableHead>
                <TableHead className="text-right">Revenue</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {[...data].reverse().map((row, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{row.date}</TableCell>
                  <TableCell className="text-right">{row.visitors?.toLocaleString() || 0}</TableCell>
                  <TableCell className="text-right">{row.bookings?.toLocaleString() || 0}</TableCell>
                  <TableCell className="text-right">{row.conversionRate?.toFixed(2)}%</TableCell>
                  <TableCell className="text-right">€{row.revenue?.toLocaleString() || 0}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};
