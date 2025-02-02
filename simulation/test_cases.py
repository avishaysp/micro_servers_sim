from tasks.task_generator import (ConstIntervalFixPacketsTask, RandIntervalFixPacketsTask,
                                  RandIntervalOrderedRandPacketsTask, RandIntervalNotOrderedPacketsTask)

test_cases_list = [(ConstIntervalFixPacketsTask, False),
                   (RandIntervalFixPacketsTask, False),
                   (RandIntervalOrderedRandPacketsTask, False),
                   (RandIntervalNotOrderedPacketsTask, False),
                   (RandIntervalNotOrderedPacketsTask, True)]


percentages = [10, 20, 30, 40, 50]
