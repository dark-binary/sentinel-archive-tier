from azure.mgmt.loganalytics import LogAnalyticsManagementClient
import azure.mgmt.loganalytics.operations
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
import logging
import automationassets

load_dotenv(".env")
    
# Acquire a credential object
token_credential = DefaultAzureCredential()

resource_group_name = automationassets.get_automation_variable("resource_group_name")
log_analytics_workspace_name = automationassets.get_automation_variable("log_analytics_workspace_name")
subscription_id = automationassets.get_automation_variable("subscription_id")
excluded_tables = automationassets.get_automation_variable("excluded_tables").split(",")

# Acquire a client object
client = LogAnalyticsManagementClient( token_credential, subscription_id)

# Allowed values for Archive Retention: [4-730], 1095, 1460, 1826, 2191, 2556, 2922, 3288, 3653, 4018, 4383 days.
total_retention_in_days = automationassets.get_automation_variable("total_retention_in_days")
        
def update_table_retention(client, resource_group_name, log_analytics_workspace_name, total_retention_in_days, excluded_tables):
    # Get the list of workspaces in the subscription
    tables = client.tables.list_by_workspace(resource_group_name, log_analytics_workspace_name)
    for table in tables:
        if table.name not in excluded_tables and table.total_retention_in_days != total_retention_in_days:
            client.tables.begin_update("rg-dev-jira", "egems-dev-jira", table.name, parameters={"total_retention_in_days": total_retention_in_days})
            print(f"Updated {table.name} to {total_retention_in_days} days")

# Usage
update_table_retention(client, resource_group_name, log_analytics_workspace_name, total_retention_in_days, excluded_tables)