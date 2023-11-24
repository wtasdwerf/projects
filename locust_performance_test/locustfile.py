from locust import HttpUser, task, between, TaskSet


class UserBehavior(TaskSet):
    @task
    def start_c(self):
        self.client.get('myapp/C/')


class LocustUser(HttpUser):
    wait_time = between(1, 4)
    tasks = [UserBehavior]