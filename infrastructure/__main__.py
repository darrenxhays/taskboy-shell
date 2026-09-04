# flake8: noqa
import pulumi
import pulumi_aws as aws

# configure the AWS Provider
aws.Provider("aws", region="us-east-1")

# every stack must run with its own account's credentials: a stack applied with another account's
# credentials puts its diagnostics role in the wrong account and looks healthy until a task needs it
config = pulumi.Config("taskboy")
environment = config.require("environment")
expected_account_id = config.require("account_id")
caller_account_id = aws.get_caller_identity().account_id
if caller_account_id != expected_account_id:
    raise RuntimeError(f"stack '{environment}' expects AWS account {expected_account_id} but the active credentials are for {caller_account_id} — switch profiles and rerun")


# import all infrastructure components
import alb
import audit_bucket
import deployment
import ec2
import iam
import issue_uploads_bucket
import secrets_manager
