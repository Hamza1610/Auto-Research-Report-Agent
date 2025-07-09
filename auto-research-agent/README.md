# Auto-Research Report Agent

An intelligent agent that automatically researches topics, analyzes content, and generates professional PDF reports.

## Features

- 🔍 **Web Search**: Automatically searches the web for relevant information
- 📊 **AI Analysis**: Uses Google Gemini to analyze and structure content
- 📄 **PDF Generation**: Creates professional PDF reports with custom templates
- ☁️ **Cloud Storage**: Optional Google Cloud Storage integration for document storage(Yet to be fullly implemented)
- 🌐 **Web Interface**: Simple web UI for submitting research queries

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

You have two options:


#### Setup
Create a `.env` file in the project root with the following variables:

```env
# Required API Keys
GEMINI_API_KEY=your-gemini-api-key-here
SERPER_API_KEY=your-serper-api-key-here

# Optional Google Cloud Storage (only needed if using GCS)
GCP_PROJECT_ID=your-gcp-project-id
GCS_SOURCE_BUCKET=your-source-bucket-name
GCS_REPORTS_BUCKET=your-reports-bucket-name
```

### 3. Get API Keys

#### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

#### Serper API (Web Search)
1. Go to [Serper.dev](https://serper.dev/)
2. Sign up and get your API key
3. Add it to your `.env` file

### 4. Run the Application

```bash
cd Auto-Research-Report-Agent/
```
```bash
python main.py
```

The application will start a web server at `http://localhost:5000`

## Troubleshooting

### "Your default credentials were not found" Error

This error occurs when the application tries to use Google Cloud Storage without proper authentication. The application has been updated to handle this gracefully:

- **If you don't need GCS**: The app will work with web search only. Reports will be saved locally.
- **If you need GCS**: Set up Google Cloud credentials using one of these methods:

#### Method 1: Service Account Key (Recommended for Production)
1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

#### Method 2: Application Default Credentials (Development)
```bash
gcloud auth application-default login
```

#### Method 3: Use API Keys Only (Simplest)
The application now works without GCS credentials. It will:
- Perform web searches using Serper API
- Generate PDF reports locally
- Skip GCS upload if credentials are not available

## Usage

### Web Interface
1. Open `http://localhost:5000` in your browser
2. Enter your research query
3. Optionally add GCS document paths
4. Click "Generate Research Report"

### API Usage
Send a POST request to `/` with JSON body:

```json
{
  "query": "What is artificial intelligence?",
  "gcs_paths": ["gs://your-bucket/doc1.txt"]  // optional(yet to be implemented)
}
```

## Project Structure

```
auto-research-agent/
├── agents/                 # Agent implementations
│   ├── research_agent.py   # Web search and document reading
│   ├── analysis_agent.py   # AI content analysis
│   ├── reporting_agent.py  # PDF generation
│   └── delivery_agent.py   # Cloud storage upload
├── orchestrator/           # Workflow coordination
├── utils/                  # Utility functions
├── templates/              # HTML templates
├── prompts/                # AI prompts
├── tests/                  # Unit tests
├── config.py              # Configuration
├── main.py                # Flask application
└── requirements.txt       # Dependencies
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Create new agents in the `agents/` directory
2. Update the orchestrator to include new workflow steps
3. Add corresponding tests

## License

This project is open source. Feel free to contribute! 

## Contributing

This project is open source and welcomes contributions from developers of all backgrounds! If you are interested in connecting, collaborating, or contributing, please follow these guidelines:

- **Fork the repository** and create your feature branch (`git checkout -b feature/YourFeature`)
- **Commit your changes** (`git commit -am 'Add new feature'`)
- **Push to the branch** (`git push origin feature/YourFeature`)
- **Open a Pull Request** describing your changes and why they should be merged

### Ways to Contribute
- Add new features or agents
- Improve documentation or templates
- Report bugs or suggest enhancements via Issues
- Help with testing and code review
- Complet the Google Cloud implementation for file download

Feel free to connect with other contributors through Issues and Pull Requests. All constructive feedback and collaboration are appreciated! 