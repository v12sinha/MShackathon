import logging
import azure.functions as func
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing log data for errors.')

    # Example log data processing
    log_data = req.get_json()
    if 'error' in log_data:
        create_ado_item(log_data['error'])

    return func.HttpResponse('Processed successfully.')

def create_ado_item(error_message):
    organization_url = 'https://dev.azure.com/your_organization'
    personal_access_token = 'your_pat'
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    work_item_client = connection.clients.get_work_item_tracking_client()

    work_item = {
        'fields': {
            'System.Title': 'Error detected in Azure logs',
            'System.Description': error_message,
            'System.AssignedTo': 'your_email@example.com'
        }
    }

    work_item_client.create_work_item(document=work_item, project='your_project', type='Task')
