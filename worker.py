import os
import json
import time
import glob


QUEUE_DIR = "queue"
RESULTS_DIR = "results"


os.makedirs(QUEUE_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


print("[WORKER] Started")


while True:
    files = sorted(
        glob.glob(os.path.join(QUEUE_DIR, "*.json"))
    )

    if not files:
        time.sleep(1)
        continue

    path = files[0]

    print(f"[WORKER] Processing: {path}")

    try:
        with open(path, "r", encoding="utf-8") as file:
            body = json.load(file)

        job_id = body["job_id"]
        message = body["message"]

        time.sleep(2)

        result = message.upper()

        result_data = {
            "job_id": job_id,
            "result": result
        }

        result_path = os.path.join(
            RESULTS_DIR,
            f"{job_id}.json"
        )

        with open(
            result_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                result_data,
                file,
                ensure_ascii=False
            )

        os.remove(path)

        print(
            f"[WORKER] Done: {job_id}"
        )

    except (json.JSONDecodeError, KeyError) as error:
        print(
            f"[WORKER] Invalid job: {path}"
        )

        print(error)

        os.remove(path)