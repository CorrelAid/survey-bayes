import numpy as np


def generate_correlated_likert_data(n, likert_levels, std, corr, seed=42):
    """
    Generate synthetic Likert data with specified correlation.

    Parameters:
    n (int): Number of observations
    likert_levels (int): Number of Likert levels
    std (float | np.ndarray): Standard deviation of the latent variables
    corr (float): Correlation between the latent variables
    seed (int): Random seed

    Returns:
    likert_responses (np.ndarray): Responses on a Likert scale
    latent_likert (np.ndarray): Latent 2D Normal variables that are binned to produce the Likert responses
    """
    np.random.seed(seed)

    if isinstance(std, float):
        std = np.array([std, std])

    cov = corr * std[0] * std[1]
    cov_mat = [[std[0] ** 2, cov], [cov, std[1] ** 2]]

    latent_likert = np.random.multivariate_normal(
        mean=np.ones(2) * (likert_levels + 1) / 2, cov=cov_mat, size=n
    )
    likert_responses = (
        np.digitize(latent_likert, np.arange(likert_levels - 1) + 1.5) + 1
    )

    return likert_responses, latent_likert
