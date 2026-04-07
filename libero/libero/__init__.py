import os
import yaml

# This is a default path for localizing all the benchmark related files
libero_config_path = os.environ.get(
    "LIBERO_CONFIG_PATH", os.path.expanduser("~/.libero")
)
config_file = os.path.join(libero_config_path, "config.yaml")


def get_default_path_dict(custom_location=None):
    if custom_location is None:
        benchmark_root_path = os.path.dirname(os.path.abspath(__file__))
    else:
        benchmark_root_path = custom_location

    # This is a default path for localizing all the default bddl files
    bddl_files_default_path = os.path.join(benchmark_root_path, "./bddl_files")

    # This is a default path for localizing all the default bddl files
    init_states_default_path = os.path.join(benchmark_root_path, "./init_files")

    # This is a default path for localizing all the default datasets
    dataset_default_path = os.path.join(benchmark_root_path, "../datasets")

    # This is a default path for localizing all the default assets
    assets_default_path = os.path.join(benchmark_root_path, "./assets")

    return {
        "benchmark_root": benchmark_root_path,
        "bddl_files": bddl_files_default_path,
        "init_states": init_states_default_path,
        "datasets": dataset_default_path,
        "assets": assets_default_path,
    }


# Cached config dict (loaded once).
_config_cache = None


def _load_config():
    """Load config from file, or fall back to auto-detected defaults."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            _config_cache = dict(yaml.load(f.read(), Loader=yaml.FullLoader))
    else:
        # Auto-detect paths relative to this package — no config file needed.
        _config_cache = get_default_path_dict()

    return _config_cache


def get_libero_path(query_key):
    config = _load_config()

    assert query_key in config, (
        f"Key {query_key} not found in config. Available keys are: {config.keys()}"
    )
    return config[query_key]


def set_libero_default_path(custom_location=os.path.dirname(os.path.abspath(__file__))):
    global _config_cache
    print(
        "[Warning] You are changing the default path for Libero config. This will affect all the paths in the config file."
    )
    new_config = get_default_path_dict(custom_location)
    os.makedirs(libero_config_path, exist_ok=True)
    with open(config_file, "w") as f:
        yaml.dump(new_config, f)
    _config_cache = new_config
