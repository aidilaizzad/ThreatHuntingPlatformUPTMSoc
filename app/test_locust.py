from locust import HttpUser, task, between
import random

class ThreatHuntingTest(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def view_dashboard(self):
        self.client.get("/")

    @task(2)
    def simulate_brute_force(self):
        # Send logs that look like a brute force attempt
        self.client.post("/add_log", json={
            "message": "multiple failed logins detected from suspicious IP",
            "value": random.randint(100, 200)  # High value to trigger anomaly
        })

    @task(2)
    def simulate_sql_injection(self):
        self.client.post("/add_log", json={
            "message": "sql error from malicious query ' OR '1'='1",
            "value": random.randint(100, 200)
        })

    @task(2)
    def simulate_ddos(self):
        self.client.post("/add_log", json={
            "message": "traffic spike detected from botnet",
            "value": random.randint(1000, 2000)  # Spikes to trigger anomaly
        })

    @task(1)
    def search_logs(self):
        self.client.get("/search?query=sql")

    @task(1)
    def get_all_logs(self):
        self.client.get("/logs")