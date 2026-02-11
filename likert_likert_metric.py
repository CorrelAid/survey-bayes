# %% [markdown]
#  We want to model the correlation between two Likert items. This cannot
# be done well with Bambi as we need to use a bivariate ordinal model.

# %%
# import arviz.preview as az

import arviz as az
import bambi as bmb
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.synthetic_data.likert import generate_correlated_likert_data

az.style.use("arviz-variat")
colors = np.array(list(mcolors.TABLEAU_COLORS.values()))

# %%
# Mock survey data in long format
np.random.seed(42)
n = 200
likert_levels = 5
std = np.array([2.5, 2.5]) ** 0.5
corr = 0.7

likert_responses, latent_likert = generate_correlated_likert_data(
    n, likert_levels, std, corr
)

latent_recovered_correlation = np.corrcoef(latent_likert, rowvar=False)[0, 1]
print(latent_recovered_correlation)
likert_recovered_correlation = np.corrcoef(likert_responses, rowvar=False)[0, 1]
print(likert_recovered_correlation)

# likert_responses = latent_likert
# plt.scatter(latent_likert[:, 0], latent_likert[:, 1], c=colors[likert_responses[:,0]])
plt.scatter(
    likert_responses[:, 0] + np.random.uniform(-0.1, 0.1, size=n),
    likert_responses[:, 1] + np.random.uniform(-0.1, 0.1, size=n),
    alpha=0.5,
)
# %%
data = pd.DataFrame(
    {
        "respondent_id": range(1, n + 1),
        # "program": np.random.choice(["Youth", "Adult", "Senior"], n),
        # "q1_confidence": np.random.choice(
        #     np.arange(likert_levels) + 1,
        #     n,
        #     p=np.random.dirichlet(np.ones(likert_levels)),
        # ),
        # "q2_satisfaction": np.random.choice(
        #     np.arange(likert_levels) + 1,
        #     n,
        #     p=np.random.dirichlet(np.ones(likert_levels)),
        # ),
        "q1": likert_responses[:, 0],
        "q2": likert_responses[:, 1],
        "age": np.random.randint(18, 75, n),
        "year": np.random.choice([2023, 2024], n),
    }
)

# # Add some correlation between q1 and q2
# correlation_boost = (data["q1"] > 3).astype(int)
# data.loc[data.index[:100], "q2"] = np.clip(
#     data.loc[data.index[:100], "q2"] + correlation_boost[:100], 1, 5
# )


# %%
model = bmb.Model("q2 ~ q1", data)  # , family="cumulative")
model.build()
# %%
model.plot_priors()
# %%
idata = model.prior_predictive(draws=200)
# %%
az.plot_ppc(
    idata,
    group="prior",
    observed=True,
    observed_rug=True,
    num_pp_samples=50,
    kind="cumulative",
)
# %%
idata.extend(model.fit())

# %%
model.predict(idata, kind="response")
# # %%
az.plot_ppc(idata, alpha=0.1, num_pp_samples=50, kind="cumulative", observed_rug=True)
# %%
# az.plot_ppc(az.extract(idata, num_samples=10, group="posterior_predictive"), alpha=0.1)
# %%
plt.hist(data["q2"], bins=np.arange(likert_levels + 1) + 0.5, alpha=0.5)
# %%
az.summary(idata, group="posterior")
# %%
az.plot_posterior(idata, group="posterior", var_names=["q1"])
# %%
