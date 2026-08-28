import pulumi
import pulumi_aws as aws

config = pulumi.Config("taskboy")
environment = config.require("environment")
# the harness is deployed once, on the host environment — the bundle only exists there
host_environment = config.get("host_environment") or environment
# secrets manager bundle name; default derives from the environment
secret_name = config.get("secret_name") or f"TASKBOY_SECRETS_{environment.upper()}"

if environment == host_environment:
    # empty shell only: pulumi never writes secret values. the setup wizard (or a manual
    # `aws secretsmanager put-secret-value`) fills in the json bundle — see taskboy/secrets.py
    aws.secretsmanager.Secret(
        "secrets",
        name=secret_name,
        recovery_window_in_days=0,
    )
