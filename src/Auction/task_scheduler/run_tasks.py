
from .tasks import start_auction_task
import time

def stop_task(task_id):
    start_auction_task.AsyncResult(task_id).revoke()

if __name__ == '__main__':
    result = start_auction_task.delay(1,2)
    # at this time, our task is not finished, so it will return False
    print ('Task finished? ', result.ready())
    print( 'Task result: ', result.result)
    # sleep 10 seconds to ensure the task has been finished
    time.sleep(10)
    # now the task should be finished and ready method will return True
    print ('Task finished? ', result.ready())
    print( 'Task result: ', result.result)