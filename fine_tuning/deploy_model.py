# fine_tuning/deploy_model.py
# Automated deployment management for fine-tuned models

import subprocess
from dotenv import load_dotenv

load_dotenv()


def deploy_model(model_id, deployment_name, resource_name, resource_group, capacity=1):
    """Deploy fine-tuned model to Azure OpenAI."""

    print(f"🚀 Deploying: {model_id}")
    print(f"   Deployment name: {deployment_name}")

    cmd = [
        "az",
        "cognitiveservices",
        "account",
        "deployment",
        "create",
        "--name",
        resource_name,
        "--resource-group",
        resource_group,
        "--deployment-name",
        deployment_name,
        "--model-name",
        model_id,
        "--model-version",
        "1",
        "--model-format",
        "OpenAI",
        "--sku-capacity",
        str(capacity),
        "--sku-name",
        "Standard",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("   ✅ Deployment created")
        return True
    else:
        print(f"   ❌ Failed: {result.stderr}")
        return False


def check_deployment_status(deployment_name, resource_name, resource_group):
    """Check deployment provisioning status."""

    cmd = [
        "az",
        "cognitiveservices",
        "account",
        "deployment",
        "show",
        "--name",
        resource_name,
        "--resource-group",
        resource_group,
        "--deployment-name",
        deployment_name,
        "--query",
        "properties.provisioningState",
        "-o",
        "tsv",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def list_deployments(resource_name, resource_group):
    """List all deployments."""

    cmd = [
        "az",
        "cognitiveservices",
        "account",
        "deployment",
        "list",
        "--name",
        resource_name,
        "--resource-group",
        resource_group,
        "-o",
        "table",
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    print("=" * 60)
    print("DEPLOYMENT MANAGEMENT")
    print("=" * 60)

    # Configuration
    MODEL_ID = (
        "gpt-35-turbo-0125.ft-383faf4466084382960e84f995123316-rice-thai-5pct-azure"
    )
    DEPLOYMENT_NAME = "rice-thai-5pct"
    RESOURCE_NAME = "openai-rice-sweden"
    RESOURCE_GROUP = "rg-rice-forecast-sweden"

    print("\n1. CURRENT DEPLOYMENTS")
    list_deployments(RESOURCE_NAME, RESOURCE_GROUP)

    print("\n2. DEPLOYMENT STATUS CHECK")
    status = check_deployment_status(DEPLOYMENT_NAME, RESOURCE_NAME, RESOURCE_GROUP)
    print(f"   {DEPLOYMENT_NAME}: {status}")

    print("\n" + "=" * 60)
