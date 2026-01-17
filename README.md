# Executive Business Health Dashboard

A comprehensive data analysis project providing leadership with a single, clear view of company performance, highlighting growth, risks, and actionable insights to support data-driven decision-making.

## 🎯 Project Overview

This project delivers a complete executive dashboard solution with both **Next.js frontend** and **Python backend** components, demonstrating advanced data analysis capabilities including:

- Real-time KPI monitoring and trend analysis
- Customer segmentation with RFM modeling
- Business health scoring algorithm
- AI-powered insights and recommendations
- Interactive visualizations and reporting

## 🏗️ Architecture

### Frontend (Next.js)
- **Technology Stack**: Next.js 16, React 19, TypeScript, TailwindCSS, Framer Motion
- **Features**: Executive KPI cards, interactive charts, risk indicators, recommendations
- **Location**: `/src/` directory

### Backend (Python)
- **Technology Stack**: FastAPI, Pandas, NumPy, Scikit-learn, Streamlit
- **Features**: Data processing, KPI calculations, ML-powered analytics, API endpoints
- **Location**: `/backend/` directory

### Data Pipeline
1. **Synthetic Data Generation**: Realistic business data using Pandas
2. **KPI Calculation**: 15+ business metrics with health scoring
3. **Advanced Analytics**: Customer segmentation, trend analysis, risk detection
4. **Insight Generation**: AI-powered business recommendations

## 📊 Key Features

### Core Dashboard Components
- **Executive KPI Summary Cards** - Real-time metrics with health status indicators
- **Interactive Analytics** - Trend charts and comparison visualizations
- **Customer Segmentation Analysis** - Value distribution and growth patterns
- **Risk Indicators** - Visual Red/Yellow/Green health status warnings
- **Actionable Recommendations** - "What to do next" executive guidance
- **Business Health Scoring** - Overall and category-specific health metrics

### Advanced Features
- **Dark/Light Mode Toggle** - Accessible interface design
- **Interactive Filters** - Date range, region, and product filtering
- **Time-Based Trend Analysis** - Month-over-Month growth tracking
- **Responsive Design** - Mobile and desktop optimized
- **Real-time Updates** - Live data refresh capabilities

## 🏗️ Technical Architecture

### Frontend Stack
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Recharts** - Interactive data visualizations
- **Lucide React** - Modern icon library

### Key Business KPIs Tracked
- **Financial**: Revenue, Revenue Growth, Profit Margin, Expense Ratio, MRR, ARR, CAC, LTV:CAC Ratio
- **Customer**: Customer Health Score, Churn Rate, CLV, NPS, CSAT
- **Operational**: Operational Efficiency, Employee Satisfaction, Market Share

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd executive-dashboard
```

2. **Install Frontend Dependencies**
```bash
npm install
```

3. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Start the Applications**

**Backend API Server** (Terminal 1):
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Next.js Frontend** (Terminal 2):
```bash
npm run dev
```

**Streamlit Dashboard** (Optional - Terminal 3):
```bash
cd backend
streamlit run streamlit_app.py
```

5. **Access the Applications**
- Next.js Dashboard: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Streamlit Dashboard: http://localhost:8501

## � Project Structure

```
executive-dashboard/
├── src/                          # Next.js Frontend
│   ├── app/                      # App Router pages
│   ├── components/               # React components
│   │   ├── kpi-cards/           # KPI display components
│   │   ├── charts/              # Chart components
│   │   └── insights/            # Insight components
│   ├── services/                # API services
│   ├── lib/                     # Utility functions
│   └── types/                   # TypeScript definitions
├── backend/                     # Python Backend
│   ├── app/
│   │   ├── main.py             # FastAPI application
│   │   ├── models.py           # Data models
│   │   └── services/           # Business logic
│   │       ├── data_generator.py    # Synthetic data generation
│   │       ├── kpi_calculator.py    # KPI calculations
│   │       ├── business_analyzer.py  # Advanced analytics
│   │       ├── health_scorer.py     # Health scoring algorithm
│   │       └── insight_engine.py     # AI insights
│   ├── streamlit_app.py        # Streamlit dashboard
│   └── requirements.txt        # Python dependencies
└── README.md                   # This file
```

## 🔧 API Endpoints

### Core Dashboard Data
- `GET /api/dashboard/kpis` - All KPI data
- `GET /api/dashboard/insights` - Business insights
- `GET /api/dashboard/risks` - Risk indicators
- `GET /api/dashboard/recommendations` - Actionable recommendations
- `GET /api/dashboard/executive-summary` - Executive summary
- `GET /api/dashboard/business-health` - Health scores
- `GET /api/dashboard/complete` - Complete dashboard data

### Advanced Analytics
- `GET /api/analytics/customer-segments` - Customer segmentation
- `GET /api/analytics/revenue-trends` - Revenue trend analysis
- `GET /api/analytics/expense-breakdown` - Expense analysis

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm run build
vercel --prod
```

### Docker
```bash
docker build -t executive-dashboard .
docker run -p 3000:3000 executive-dashboard
```

### Static Export
```bash
npm run build
npm run start
```

## 🧪 Testing

### Unit Tests
```bash
npm run test
```

### Integration Tests
```bash
npm run test:integration
```

### E2E Tests
```bash
npm run test:e2e
```

## 📚 Documentation

### Component Documentation
- **KPI Cards** - Executive metric display components
- **Charts** - Recharts-based visualizations
- **Filters** - Interactive data filtering
- **Risk Indicators** - Health status warnings

### Business Logic
- **Threshold Calculations** - Health status determination
- **Insight Generation** - Automated business insights
- **Recommendation Scoring** - Action prioritization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow TypeScript best practices
- Use semantic HTML elements
- Implement responsive design
- Add appropriate error handling
- Include accessibility features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Next.js Team** - Excellent React framework
- **Vercel** - Hosting and deployment platform
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Data visualization library
- **Framer Motion** - Animation library

## 📞 Support

For questions, support, or feature requests:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

**Built with ❤️ for executive decision-making**

## 📊 Business Metrics Explained

### Financial KPIs
- **Revenue**: Total sales revenue with growth tracking
- **Revenue Growth**: Month-over-month growth percentage
- **Profit Margin**: (Revenue - Costs) / Revenue × 100
- **Expense Ratio**: Operating expenses as percentage of revenue
- **MRR/ARR**: Monthly/Annual Recurring Revenue

### Customer KPIs
- **Customer Health**: Weighted score of satisfaction and engagement
- **Churn Rate**: Customer attrition percentage
- **CLV**: Customer Lifetime Value
- **CAC**: Customer Acquisition Cost
- **LTV:CAC Ratio**: Lifetime value to acquisition cost ratio
- **NPS**: Net Promoter Score
- **CSAT**: Customer Satisfaction Score

### Operational KPIs
- **Operational Efficiency**: Process efficiency metrics
- **Employee Satisfaction**: Staff engagement and satisfaction
- **Market Share**: Market position relative to competitors

## 🤖 AI-Powered Features

### Insight Generation
The system automatically generates insights using:
- **Pattern Recognition**: Identifies trends and anomalies
- **Business Rules**: Applies industry-standard thresholds
- **Cross-KPI Analysis**: Detects relationships between metrics
- **Priority Scoring**: Ranks insights by business impact

### Recommendation Engine
Provides actionable recommendations based on:
- **Historical Performance**: Learns from past data
- **Best Practices**: Industry-standard strategies
- **Resource Constraints**: Considers effort and timeframe
- **Confidence Scoring**: Estimates success probability

## 📊 Data Analysis Techniques

### Customer Segmentation (RFM Analysis)
- **Recency**: How recently customers purchased
- **Frequency**: How often customers purchase
- **Monetary**: How much customers spend
- **ML Clustering**: K-means for advanced segmentation

### Time-Series Analysis
- **Trend Detection**: Linear regression for trend analysis
- **Seasonality**: Monthly pattern identification
- **Forecasting**: Predictive analytics for future performance
- **Anomaly Detection**: Statistical outlier identification

### Health Scoring Algorithm
- **Weighted Metrics**: Different importance for each KPI
- **Category Balancing**: Financial, Customer, Operational categories
- **Trend Adjustment**: Considers improvement/decline patterns
- **Threshold Logic**: Industry-standard health thresholds

## 🎯 Project Deliverables

### ✅ Completed Features
- [x] Synthetic business data generation
- [x] KPI calculation and monitoring
- [x] Customer segmentation analysis
- [x] Business health scoring algorithm
- [x] AI-powered insights generation
- [x] Risk detection and alerting
- [x] Actionable recommendations
- [x] Next.js executive dashboard
- [x] Streamlit analytics dashboard
- [x] RESTful API with FastAPI
- [x] Time-series trend analysis
- [x] Interactive visualizations

### 🎯 Business Value
- **Improved Decision Making**: Data-driven insights for leadership
- **Early Risk Detection**: Proactive identification of business risks
- **Performance Transparency**: Clear visibility across departments
- **Time Savings**: Automated reporting and analysis
- **Strategic Planning**: Forward-looking insights and forecasts
