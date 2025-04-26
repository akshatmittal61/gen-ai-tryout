import os

script_dir = os.path.dirname(os.path.abspath(__file__))

class ConfigManager:
    @staticmethod
    def load_env():
        try:
            file_path = os.path.join(script_dir, '.env')
            with open(file_path, 'r') as f:
                for line in f:
                    # Ignore comments and empty lines
                    if line.startswith('#') or line.startswith(' ') or line.startswith('\n'):
                        continue

                    # Split the line into key and value
                    splits = line.strip().split('=')
                    key = splits[0]

                    # Join the rest of the line as the value
                    value = '='.join(splits[1:])
                    key = key.strip()
                    value = value.strip()

                    # Remove surrounding quotes
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key] = value
        except FileNotFoundError:
            raise FileNotFoundError('.env file not found')
        except Exception as e:
            raise Exception(f'Error loading environment variables: {e}')

    def __init__(self):
        self.load_env()

    def get_all(self):
        env_file_variables = {key: self.get(key) for key in self.__dict__ if not key.startswith('_')}
        os_env_variables = {key: os.getenv(key) for key in os.environ}
        return {**env_file_variables, **os_env_variables}

    def get(self, key):
        """
        Get a configuration variable from either the .env file or environment variables.
        If the variable is not found in either, an AttributeError is raised.

        :param key: The name of the configuration variable
        :return: The value of the configuration variable
        :raises AttributeError: If the variable is not found
        """
        if hasattr(self, key):
            return getattr(self, key)
        elif key in os.environ:
            return os.environ[key]
        else:
            raise AttributeError(f"Attribute '{key}' not found")

    def set(self, key, value):
        """
        Set a configuration variable. If the variable does not exist in .env or environment variables, an AttributeError
        is raised.

        :param key: The name of the configuration variable
        :param value: The value of the configuration variable
        :raises AttributeError: If the variable is not found
        """
        if hasattr(self, key):
            setattr(self, key, value)
        elif key in os.environ:
            os.environ[key] = value
        else:
            raise AttributeError(f"Attribute '{key}' not found")

    def safe_get(self, key, fallback):
        """
        A wrapper around get that allows a fallback value to be specified in case the variable is not found.

        :param key: The name of the configuration variable
        :param fallback: The value to return if the variable is not found
        :return: The value of the configuration variable, or the fallback value if the variable is not found
        :raises AttributeError: If the variable is not found and no fallback is specified
        """
        try:
            value = self.get(key)
            return value
        except AttributeError:
            return fallback

    def __iter__(self):
        return iter(self.__dict__.items())

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)


config = ConfigManager()

groq_key = config.get("GROQ_KEY")
