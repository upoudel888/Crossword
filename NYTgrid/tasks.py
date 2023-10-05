from celery import shared_task
from celery_progress.backend import ProgressRecorder

from time import sleep

@shared_task(bind=True, acks_late=True, task_reject_on_worker_lost=True)
def go_to_sleep(self, duration):
    progress_recorder = ProgressRecorder(self)
    for i in range(20):
        sleep(duration)
        progress_recorder.set_progress(i + 1, 20, f'On iteration {i}')
    return 'Done',[1,2,3]