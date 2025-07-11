# Survey Builder with Data Vault Architecture

A modern survey builder application built with Flask frontend, FastAPI backend, and PostgreSQL database using Data Vault modeling methodology.

## 🏗️ Architecture

### Data Vault Model
This application implements a Data Vault 2.0 architecture with the following components:

#### Hubs (Business Keys)
- `hub_project`: Stores survey projects with business key `company_name + survey_title`
- `hub_client`: Stores client/company information
- `hub_objective`: Stores survey objectives (formerly categories)
- `hub_question`: Stores individual questions

#### Links (Relationships)
- `link_project_objective`: Links projects to objectives
- `link_project_question`: Links projects to questions

#### Satellites (Attributes)
- `sat_project`: Project attributes (name, duration, creation date)
- `sat_client`: Client customization (company name, logo, colors)
- `sat_objective`: Objective attributes (label, display order)
- `sat_question`: Question attributes (text, type, options, estimated time)

### Technology Stack
- **Frontend**: Flask with Tailwind CSS and Font Awesome
- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with Data Vault schema
- **Containerization**: Docker with docker-compose

## 🚀 Quick Start

### Prerequisites
- Docker and docker-compose
- Python 3.11+ (for local development)

### Running the Application

1. **Clone and navigate to the project**:
   ```bash
   cd survey_builder
   ```

2. **Start the application**:
   ```bash
   docker-compose up
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📊 Data Vault Implementation

### Key Features

#### 1. **Hub Tables**
- Store business keys for each entity
- Provide unique identification across the system
- Support audit trails with `load_dts` and `rec_src`

#### 2. **Link Tables**
- Connect related entities without denormalization
- Maintain referential integrity
- Support many-to-many relationships

#### 3. **Satellite Tables**
- Store descriptive attributes for entities
- Support point-in-time analysis
- Enable historical tracking of changes

### Database Schema

```sql
-- Hub Tables
hub_project (hk_project, bk_project, load_dts, rec_src)
hub_client (hk_client, bk_client, load_dts, rec_src)
hub_objective (hk_objective, bk_objective, load_dts, rec_src)
hub_question (hk_question, bk_question, load_dts, rec_src)

-- Link Tables
link_project_objective (hk_project_objective, hk_project, hk_objective, load_dts, rec_src)
link_project_question (hk_project_question, hk_project, hk_question, load_dts, rec_src)

-- Satellite Tables
sat_project (hk_project, name, duration_min, created_at, load_dts, rec_src)
sat_client (hk_client, company_name, logo_url, primary_color, secondary_color, load_dts, rec_src)
sat_objective (hk_objective, label, display_order, load_dts, rec_src)
sat_question (hk_question, text, q_type, est_seconds, options, load_dts, rec_src)
```

## 🔧 API Endpoints

### Survey Management
- `POST /api/save-objectives`: Save survey objectives
- `POST /api/save-customization`: Save client branding
- `POST /api/save-questions`: Save survey questions
- `GET /api/survey-data/{company_name}/{survey_title}`: Retrieve survey data
- `POST /api/export`: Export survey in various formats

### Health Check
- `GET /health`: Application health status

## 🎯 Application Flow

1. **Splash Page**: Welcome and introduction
2. **White Label**: Configure company branding and survey title
3. **Objectives**: Create survey objectives (formerly categories)
4. **Questions**: Build survey questions
5. **Review**: Preview and export survey

## 🔄 Data Persistence

### Frontend Storage
- Uses localStorage for session persistence
- Saves user progress between steps
- Maintains company name and survey title as keys

### Backend Storage
- Data Vault model ensures data integrity
- Supports historical tracking
- Enables audit trails and compliance

## 🛠️ Development

### Local Development Setup

1. **Install dependencies**:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd frontend
   pip install -r requirements.txt
   ```

2. **Set up database**:
   ```bash
   # Run migrations
   cd backend
   python scripts/run_migrations.py
   ```

3. **Start services**:
   ```bash
   # Backend
   cd backend
   uvicorn app.main:app --reload

   # Frontend
   cd frontend
   python app.py
   ```

### Database Migrations

The application includes SQL migrations for the Data Vault schema:

- `001_hubs.sql`: Create hub tables
- `002_links.sql`: Create link tables
- `003_satellites.sql`: Create satellite tables
- `004_objectives_and_customization.sql`: Add objectives and customization tables

## 📈 Benefits of Data Vault

1. **Scalability**: Easy to add new entities and relationships
2. **Audit Trail**: Complete history of all changes
3. **Flexibility**: Schema evolution without data loss
4. **Performance**: Optimized for analytical queries
5. **Compliance**: Built-in support for regulatory requirements

## 🔍 Monitoring and Health

- Health check endpoints for both frontend and backend
- Database connection monitoring
- API response time tracking
- Error logging and notification

## 🚀 Deployment

The application is containerized and ready for deployment:

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or issues, please open an issue on the repository.
