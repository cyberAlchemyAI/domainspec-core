class DIContainer:
    def __init__(self):
        self.services = {}

    def register(self, name: str, instance):
        self.services[name] = instance

    def resolve(self, name: str, context: str = None):
        # T03: Brain Attempts DB Access is blocked
        forbidden_for_brain = ["database_client", "memory_repository", "vector_db", "gate_runner_authority"]
        if context == "brain" and name in forbidden_for_brain:
            raise Exception("BRAIN.DB_ACCESS_FORBIDDEN")
        return self.services.get(name)

# Global singleton for tests
container = DIContainer()
