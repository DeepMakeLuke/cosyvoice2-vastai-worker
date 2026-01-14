"""
CosyVoice2 PyWorker Configuration for Vast.ai Serverless

This file configures the Vast.ai PyWorker to proxy requests to the CosyVoice2
model server running on port 18000.

CRITICAL: This file lives in a PUBLIC GitHub repo and is cloned by the
Vast.ai bootstrap script when PYWORKER_REPO is set.
"""
import os
from vastai import Worker, WorkerConfig, HandlerConfig, LogActionConfig, BenchmarkConfig

# Model server configuration
MODEL_SERVER_URL = "http://127.0.0.1"
MODEL_SERVER_PORT = int(os.environ.get("MODEL_SERVER_PORT", 18000))
MODEL_LOG_FILE = os.environ.get("MODEL_LOG_FILE", "/workspace/model.log")
MODEL_HEALTHCHECK_ENDPOINT = "/health"

# Log patterns for PyWorker detection
# CRITICAL: These must match EXACTLY what the model server prints (PREFIX match at start of line)
MODEL_LOAD_LOG_MSG = ["COSYVOICE2_READY"]
MODEL_ERROR_LOG_MSGS = [
    "Traceback",
    "Error:",
    "Exception:",
    "CUDA out of memory",
    "RuntimeError",
    "ModuleNotFoundError",
]
MODEL_INFO_LOG_MSGS = [
    "Starting CosyVoice2",
    "Loading CosyVoice2",
    "Model loaded",
    "Warmup",
]


def benchmark_generator():
    """
    Generate benchmark payload for Vast.ai worker validation.

    The benchmark runs after on_load is detected to validate the worker
    is functioning correctly before joining the standby pool.
    """
    return {
        "text": "Hello, this is a benchmark test.",
        "mode": "sft",
        "speaker": "english_female",
    }


# PyWorker configuration
worker_config = WorkerConfig(
    model_server_url=MODEL_SERVER_URL,
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    model_healthcheck_url=MODEL_HEALTHCHECK_ENDPOINT,  # CRITICAL: Required for health checks
    handlers=[
        HandlerConfig(
            route="/generate",
            allow_parallel_requests=False,  # TTS generation uses GPU, no parallelism
            max_queue_time=600.0,  # Long queue time for voice cloning
            benchmark_config=BenchmarkConfig(
                generator=benchmark_generator,
                concurrency=1,
                runs=1,  # Single run for GPU model
            ),
        ),
    ],
    log_action_config=LogActionConfig(
        on_load=MODEL_LOAD_LOG_MSG,
        on_error=MODEL_ERROR_LOG_MSGS,
        on_info=MODEL_INFO_LOG_MSGS,
    ),
)

# Start the worker
Worker(worker_config).run()
