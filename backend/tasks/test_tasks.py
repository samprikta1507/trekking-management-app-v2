from celery_worker import celery

@celery.task
def test_task():
    print("Background task executed!")
    return "Success"