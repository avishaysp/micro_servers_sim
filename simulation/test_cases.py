from tasks.task_generator import (ConstIntervalFixPacketsTask, RandIntervalFixPacketsTask,
                                  RandIntervalOrderedRandPacketsTask, RandIntervalNotOrderedPacketsTask)

test_cases_list = [(ConstIntervalFixPacketsTask, False),
                   (RandIntervalFixPacketsTask, False),
                   (RandIntervalOrderedRandPacketsTask, False),
                   (RandIntervalNotOrderedPacketsTask, False),
                   (RandIntervalNotOrderedPacketsTask, True)]

test_case_name = ["Constant Interval Tasks",
                  "Random Interval Tasks",
                  "Fragmented Tasks",
                  "Overlapping Tasks",
                  "Small Prob. of Servers Failure"]


percentages = [10, 20]
