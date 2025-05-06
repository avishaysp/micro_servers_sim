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

lambdas = [0.5, 1.0, 2.0, 4.0, 8.0]
percentages = list(range(20, 121, 20))
