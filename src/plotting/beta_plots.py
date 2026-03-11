# %%
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta


# %%
def plot_beta(alpha, beta_param, color, label, title, save_path=None):
    dist = beta(alpha, beta_param)
    x = np.linspace(0, 1, 500)
    y = dist.pdf(x)
    mode = (alpha - 1) / (alpha + beta_param - 2)

    _, ax = plt.subplots(figsize=(9, 5))

    ax.plot(x, y, color=color, linewidth=2.5)
    ax.fill_between(x, y, alpha=0.25, color=color, label=label)
    ax.axvline(
        mode,
        color=color,
        linewidth=1.8,
        linestyle="--",
        label=f"Wahrscheinlichster Wert = {mode:.2f}",
    )

    ax.set_xlabel("Tendenz der Münze, Kopf zu zeigen", fontsize=12)
    ax.set_ylabel("Wahrscheinlichkeitsdichte", fontsize=12)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(bottom=0)
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


# %%
# Prior
plot_beta(
    alpha=20,
    beta_param=20,
    color="#2c7bb6",
    label="Prior Verteilung",
    title="Prior-Verteilung über die Tendenz der Münze",
    save_path="figures/coin_prior_beta_20_20.png",
)

# %%
# Posterior: nach 19 Kopf und 1 Zahl (prior + Daten)
plot_beta(
    alpha=39,
    beta_param=21,
    color="#1a9641",
    label="Posterior Verteilung",
    title="Posterior-Verteilung über die Tendenz der Münze",
    save_path="figures/coin_posterior_beta.png",
)

# %%
prior = beta(a=20, b=20)
posterior = beta(a=39, b=21)

prior_prob_fair = prior.cdf(0.6) - prior.cdf(0.4)
print(f"P(0.4 ≤ θ ≤ 0.6) unter dem Prior: {prior_prob_fair:.1%}")

posterior_mode = (39 - 1) / (39 + 21 - 2)
print(f"Modus der Posterior-Verteilung: {posterior_mode:.2f}")

# %%
# %%
