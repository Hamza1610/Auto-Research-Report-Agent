# auto-research-agent/main.py

# import functions_framework
from flask import jsonify, send_from_directory
from orchestrator.main_orchestrator import MainOrchestrator
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Register as an HTTP-triggered function
# @functions_framework.http

@app.route('/', methods=['GET', 'POST'])
def research_report_agent():
    """
    HTTP Cloud Function entry point for the Auto-Research & Report Agent.

    Expects a POST request with a JSON body:
    {
        "query": "Your research question",
        "gcs_paths": ["gs://your-bucket/doc1.txt"] (optional)
    }
    """
    if request.method == 'GET':
        return render_template('index.html') if hasattr(app, 'template_folder') else 'Auto-Research Report Agent API. Use POST method with JSON body containing "query" field.'
    
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    request_json = request.get_json(silent=True)
    if not request_json or 'query' not in request_json:
        return jsonify({"error": "Invalid request. JSON body with 'query' key is required."}), 400

    query = request_json['query']
    gcs_paths = request_json.get('gcs_paths') # Optional

    print(f"Received request for query: {query}")

    try:
        orchestrator = MainOrchestrator()
        result = orchestrator.run(query, gcs_paths)

        if result['status'] == 'success':
            # Save research data as JSON for the /view page
            import os, json
            from config import TEMP_DIR
            local_pdf_path = result.get('local_pdf_path')
            if local_pdf_path:
                filename = os.path.basename(local_pdf_path)
                json_path = os.path.join(TEMP_DIR, os.path.splitext(filename)[0] + '.json')
                # Flatten the insights dict to match the template
                insights = result.get('insights', {})
                data = {
                    "pdf_filename": filename,
                    "title": insights.get("title", "Research Report"),
                    "executive_summary": insights.get("executive_summary", ""),
                    "key_insights": insights.get("key_insights", []),
                    "source_analysis": insights.get("source_analysis", {"sentiment": "N/A", "confidence": "N/A"}),
                    "conclusion": insights.get("conclusion", "")
                }
                try:
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"Failed to save report data for view: {e}")
            return jsonify(result), 200
        else:
            return jsonify({"error": result['message']}), 500

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@app.route('/view')
def view_report():
    # Accept ?filename=... as query parameter
    from config import TEMP_DIR
    import os, json
    filename = request.args.get('filename')
    data = None
    if filename:
        # Try to load a corresponding JSON data file (same name as PDF, but .json)
        json_path = os.path.join(TEMP_DIR, os.path.splitext(filename)[0] + '.json')
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Ensure all required fields exist for the template
                data.setdefault("pdf_filename", filename)
                data.setdefault("title", "Research Report")
                data.setdefault("key_insights", [])
                data.setdefault("source_analysis", {"sentiment": "N/A", "confidence": "N/A"})
                data.setdefault("executive_summary", "")
                data.setdefault("conclusion", "")
            except Exception as e:
                print(f"Failed to load report data: {e}")
                data = None
        if data is None:
            # If no JSON, just provide minimal data with pdf_filename
            data = {"pdf_filename": filename, "title": "Research Report", "key_insights": [], "source_analysis": {"sentiment": "N/A", "confidence": "N/A"}, "executive_summary": "", "conclusion": ""}
    else:
        data = {"pdf_filename": None, "title": "No Report Selected", "key_insights": [], "source_analysis": {"sentiment": "N/A", "confidence": "N/A"}, "executive_summary": "", "conclusion": ""}
    print(f"Loaded data for /view: {data}")  # Print to ensure data is valid
    return render_template('report_template.html', data=data) if hasattr(app, 'template_folder') else 'Auto-Research Report Agent API. Use POST method with JSON body containing "query" field.'


@app.route('/download/<filename>')
def download_report(filename):
    from config import TEMP_DIR
    return send_from_directory(TEMP_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)