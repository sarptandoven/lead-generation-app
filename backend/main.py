from fastapi import FastAPI
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.fastapi.middleware import XRayMiddleware

# Initialize X-Ray
xray_recorder.configure(
    sampling=True,
    sampling_rules=[{"rule_name": "lead-gen", "priority": 1, "fixed_target": 1, "rate": 0.1}],
    context_missing='LOG_ERROR',
    daemon_address='127.0.0.1:2000',
    service='lead-generation-api'
)
patch_all()

app = FastAPI(title="Lead Generation API")

# Add X-Ray middleware
app.add_middleware(XRayMiddleware, recorder=xray_recorder)

# ... rest of your FastAPI code ... 