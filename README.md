# Firestorm Analytics Dashboard

A powerful marketing campaign performance dashboard for tracking visitor metrics, bookings, and revenue across multiple partners.

## Features

- **Real-time Analytics** - Track KPIs, visualize trends, and monitor performance metrics
- **Multi-Partner Support** - Aggregate data from GetYourGuide, Tiqets, and Viator
- **Secure Authentication** - Login system with Supabase authentication
- **Campaign Intelligence** - Automatic city mapping and campaign normalization
- **Interactive Visualizations** - Charts, graphs, and breakdowns by city and campaign
- **ETL Pipeline** - Automated data processing from Excel files

## Tech Stack

- **Frontend**: React, TypeScript, Vite
- **UI Components**: shadcn-ui, Tailwind CSS
- **Backend**: Supabase (PostgreSQL)
- **Data Processing**: Python, Pandas
- **Authentication**: Supabase Auth
- **Charts**: Recharts

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Supabase account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Firestorm-Internet-ops/Firestorm-analytics-dashboard.git
   cd Firestorm-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   npm install
   pip install -r etl/requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Access the dashboard**
   Open http://localhost:8080 in your browser

## ETL Pipeline

Process daily Excel files containing campaign data:

```bash
python etl/process_data.py
```

See [etl/README.md](etl/README.md) for detailed ETL documentation.

## Security

All credentials are stored in environment variables. See [SECURITY.md](SECURITY.md) for security guidelines.

## Documentation

- [Authentication Setup](AUTH_SETUP.md)
- [City Mapping](etl/CITY_MAPPING.md)
- [Security Guidelines](SECURITY.md)
- [Git Commands](GIT_COMMANDS.md)

## Project Structure

```
├── src/                    # Frontend React application
│   ├── components/         # UI components
│   ├── pages/             # Page components
│   └── lib/               # Utilities and stores
├── etl/                   # ETL pipeline
│   ├── processors/        # Data processors for each partner
│   └── raw_data/          # Input Excel files
├── public/                # Static assets
└── supabase/             # Database migrations
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

Proprietary - All rights reserved by Firestorm Analytics

## Support

For support, email support@firestorm-analytics.com
