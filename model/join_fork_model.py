from model.load_balancer import LoadBalancer
from model.micro_service import MicroService
from model.aggregator import Aggregator


class JoinForkModel:

    def __init__(self, number_of_tasks, env, method, mu_list, number_of_services, task_list, process_time_list, fail_perc=0, time_down=0, network_lambda=1.0):
        self.env = env
        self.aggregator = Aggregator(number_of_tasks, self.env, task_list)
        self.micro_services = [MicroService(i, mu_list[i], self.env, self.aggregator, fail_perc, time_down, process_time_list, network_lambda) for i in range(number_of_services)]
        
        # Set the reference to all microservices for each microservice
        for micro_service in self.micro_services:
            micro_service.set_all_services(self.micro_services)
            
        self.load_balancer = LoadBalancer(self.micro_services, method, self.env, task_list)

    def run_model(self):
        yield self.env.timeout(0)
        self.env.process(self.aggregator.aggregate_tasks())
        for micro_service in self.micro_services:
            self.env.process(micro_service.process_subtask())
        self.env.process(self.load_balancer.send_packet())





