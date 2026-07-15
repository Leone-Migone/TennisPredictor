from src.features import build_model_data


def create_model_data(data, random_state: int = 1):
    return build_model_data(
        data,
        random_state=random_state,
    )