import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Upload, BarChart3, TrendingUp, FileSpreadsheet } from 'lucide-react';

interface WelcomeScreenProps {
  onUpload: () => void;
}

export const WelcomeScreen = ({ onUpload }: WelcomeScreenProps) => {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-4">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center space-y-4">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-primary/10 rounded-full">
              <img src="/firestorm-logo.png" alt="Firestorm Analytics" className="h-16 w-16" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-foreground">Welcome to Firestorm Analytics</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Transform your data into actionable insights with powerful analytics and visualization tools
          </p>
        </div>

        <Card className="border-2 border-dashed">
          <CardContent className="pt-6">
            <div className="text-center space-y-6">
              <div className="flex justify-center">
                <FileSpreadsheet className="h-20 w-20 text-muted-foreground" />
              </div>
              <div>
                <h2 className="text-2xl font-semibold text-foreground mb-2">Get Started</h2>
                <p className="text-muted-foreground">
                  Upload your Excel or CSV file to begin analyzing your data
                </p>
              </div>
              <Button 
                size="lg" 
                onClick={onUpload}
                className="gap-2"
              >
                <Upload className="h-5 w-5" />
                Upload Your Data
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="p-3 bg-primary/10 rounded-lg w-fit mx-auto mb-4">
                <BarChart3 className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Dashboard Analytics</h3>
              <p className="text-sm text-muted-foreground">
                Track KPIs, visualize trends, and monitor performance metrics in real-time
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6 text-center">
              <div className="p-3 bg-accent/10 rounded-lg w-fit mx-auto mb-4">
                <TrendingUp className="h-6 w-6 text-accent" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Activity Performance</h3>
              <p className="text-sm text-muted-foreground">
                Analyze top cities and campaigns with detailed performance breakdowns
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6 text-center">
              <div className="p-3 bg-success/10 rounded-lg w-fit mx-auto mb-4">
                <Upload className="h-6 w-6 text-success" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">Easy Data Import</h3>
              <p className="text-sm text-muted-foreground">
                Simply upload Excel/CSV files and let us handle the rest automatically
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
