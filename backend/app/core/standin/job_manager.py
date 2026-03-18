import uuid

jobs = {}

def create_job():

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "created",
        "steps": [],
        "result": None,
        "finished": False
    }

    return job_id


def update_job(job_id, step):

    jobs[job_id]["steps"].append(step)
    jobs[job_id]["status"] = step


def finish_job(job_id, result):

    jobs[job_id]["status"] = "finished"
    jobs[job_id]["result"] = result
    jobs[job_id]["finished"] = True


def get_job(job_id):

    return jobs.get(job_id)