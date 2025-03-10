import logging
import uuid
import os
from state_manager import set_workflow_state
from email_sender import send_email
from connectors import LocalConnector, GoogleDriveConnector
from llm import summarize_text
from celery_app import celery_app

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_connector(connector_type):
    """
    Returns the correct connector instance based on the type.
    """
    if connector_type == "gdrive":
        return GoogleDriveConnector()
    elif connector_type == "local":
        return LocalConnector()
    else:
        raise ValueError(f"Unsupported connector type: {connector_type}")


def process_workflow(source, destination):
    """
    Reads files from the source connector, processes each file using LLM summarization,
    and writes the summary to the destination connector.
    Returns a list of results for logging or further processing.
    """
    source_connector = get_connector(source)
    dest_connector = get_connector(destination)
    results = []

    # Read files using the selected source connector.
    files = source_connector.read_files()

    # Process each file.
    if source == "local":
        for file_path in files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                summary = summarize_text(content)
                filename = "summary_" + os.path.basename(file_path)
                dest_connector.write_file(filename, summary)
                results.append(
                    {"source": file_path, "destination": filename, "summary": summary}
                )
                logger.info(f"Processed file {file_path} successfully.")
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
    elif source == "gdrive":
        for file_obj in files:
            try:
                content = file_obj.GetContentString()
                summary = summarize_text(content)
                filename = "summary_" + file_obj["title"]
                dest_connector.write_file(filename, summary)
                results.append(
                    {
                        "source": file_obj["title"],
                        "destination": filename,
                        "summary": summary,
                    }
                )
                logger.info(f"Processed file {file_obj['title']} successfully.")
            except Exception as e:
                logger.error(
                    f"Error processing file {file_obj['title']}: {e}", exc_info=True
                )
    return results


@celery_app.task
def run_workflow(source, destination, email):
    """
    Runs the workflow:
    - Reads from the selected source connector.
    - Summarizes content using the LLM.
    - Writes the summarized text to the destination connector.
    - Updates workflow state and sends notification email if provided.
    """
    workflow_id = str(uuid.uuid4())
    logger.info(f"Workflow {workflow_id}: Initiated")
    set_workflow_state(workflow_id, "initiated")

    try:
        logger.info(f"Workflow {workflow_id}: Processing started")
        set_workflow_state(workflow_id, "processing")
        results = process_workflow(source, destination)
        set_workflow_state(workflow_id, "completed")
        logger.info(
            f"Workflow {workflow_id}: Processing completed successfully with {len(results)} results"
        )

        if email:
            send_email(
                email,
                "Workflow Completed",
                f"Your summarization workflow has completed successfully! Processed {len(results)} file(s).",
            )
            logger.info(f"Workflow {workflow_id}: Email notification sent to {email}")
    except Exception as e:
        logger.error(f"Workflow {workflow_id}: Failed with error: {e}", exc_info=True)
        set_workflow_state(workflow_id, "failed")
        raise e

    return workflow_id
