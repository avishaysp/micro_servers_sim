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
                  "Small Prob. of Failure"]

lambdas = [2, 4, 8, 16, 32]
percentages = list(range(20, 121, 10))
