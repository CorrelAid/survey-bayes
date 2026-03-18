# %% [markdown]
# # Erste Bayessche Auswertung
#
# Analyse der Unsicherheit zu Ja/Nein (binären) Fragen. Bleiben wir bei dem Beispiel zum
# Event im Verein. wir hätten die Umfrage Teilnehmer:innen gefragt ob sie an unserer
# nächsten Veranstaltung teilnehmen wollen. Wir haben 20 zufällig ausgewählte Mitlgieder
# befragt und 18/20 Teilnehmer:innen antworten, dass sie gern dabei seien wollen. Was
# sagt uns das darüber aus welche Anteile an der Gesamtheit der (z.B. 1000) Mitglieder
# plausibel dabei sein wollen?
#
# Wir können an diesem Beispiel in der Praxis sehen wie man von einer Prior Verteilung
# mit Daten zu einer Posterior Verteilung kommt.

# %%
import arviz as az
import bambi as bmb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.special import expit

# %%
# Beispiel-Daten: Umfrage bei einem Verein "Würden Sie am Sommerfest
# teilnehmen?"
np.random.seed(42)

n_befragte = 20
n_ja = 18
# %%
# %%
# Daten als DataFrame (Bambi bevorzugt DataFrames)
antworten = np.concatenate([np.ones(n_ja), np.zeros(n_befragte - n_ja)])
df = pd.DataFrame(
    {
        "teilnahme": antworten  # 1 = Ja, 0 = Nein
    }
)

print(f"Umfrage-Ergebnis: {n_ja} von {n_befragte} würden teilnehmen")
print(f"Beobachteter Anteil: {n_ja / n_befragte:.1%}\n")

# %% [markdown]
# ### Bambi
# Wir nutzen für Bayessche Statistik hier das Package Bambi. Bambi ermöglicht es
# statistische Modelle mit einem String zu spezifizieren. Unsere Daten bestehen aus der
# binären Variable "teilnahme" und wir wollen herausfinden welche Anteile an
# Vereinsmitgliedern realistischerweise Ja sagen würden wenn wir statt den 20 alle 1000
# befragen würden. Das ist aus mathematischer Sicht vergleichbar mit der Tendenz einer
# Münze Kopf zu zeigen. Wir suchen also wie im Eingangsbeispiel nach einer Tendenz oder
# einem Anteil. Anteile liegen wieder zwischen 0 und 1.
#
# Nun fehlt uns noch ein statistisches Modell um zu beschreiben wie wir uns vereinfacht
# vorstellen wie die Daten, die wir gesammelt haben generiert wurden. Nahezu alle
# statistischen Verfahren, ob klassisch oder Bayessch treffen solche Modellannahmen. In
# der Bayesschen Statistik ist es sehr typisch diese Annahmen transparent darzustellen.
#
# $p(teilnahme) \sim logit(\beta_0)$

# %%
model = bmb.Model("teilnahme ~ 1", df, family="bernoulli")

# %%
# Bambi benutzt per default gute "weakly infomative priors", die sich als
# Standard etabliert haben. Wir wollen einmal Daten aus dem Prior simulieren
# (prior predictive distribution) um besser zu verstehen, welche Daten das
# Modell für wahrscheinlich hält, bevor wir ihm unseren Datensatz zeigen.
model.build()

# Wir simulieren 10000 Datensätze der Größe 20 (Prior Predictive Distribution)
prior_pred = model.prior_predictive(draws=100000)

# Visualize prior predictive distribution
print("\nPrior Predictive Distribution:")
print("=" * 50)

# Extract prior predictive samples
prior_samples = prior_pred.prior_predictive["teilnahme"].values
# Sum over individuals to get total number of "yes" responses per sample
prior_n_ja = prior_samples.sum(axis=-1).flatten()

print("Prior predictive - erwartete Anzahl 'Ja'-Antworten:")
print(f"  Mittelwert: {np.mean(prior_n_ja):.1f} von {n_befragte}")
print(f"  Median: {np.median(prior_n_ja):.1f} von {n_befragte}")
print(
    f"  95% Prior Interval: [{np.percentile(prior_n_ja, 2.5):.1f}, "
    f"{np.percentile(prior_n_ja, 97.5):.1f}]"
)
print(f"  Beobachtet: {n_ja} von {n_befragte}\n")
# %%
# Plot prior predictive distribution
fig_prior, ax_prior = plt.subplots(1, 1, figsize=(10, 6))

# Histogram of prior predictive
ax_prior.hist(
    prior_n_ja,
    bins=range(0, n_befragte + 2),
    density=True,
    alpha=0.6,
    edgecolor="black",
    color="skyblue",
    label="Prior Predictive",
    align="left",
)
ax_prior.axvline(
    n_ja, color="red", linestyle="--", linewidth=2, label=f"Beobachtete Daten: {n_ja}"
)
ax_prior.axvline(
    np.mean(prior_n_ja),
    color="blue",
    linestyle="--",
    linewidth=2,
    label=f"Prior Erwartung: {np.mean(prior_n_ja):.1f}",
)
ax_prior.set_xlabel('Anzahl "Ja"-Antworten (von {})'.format(n_befragte), fontsize=12)
ax_prior.set_ylabel("Wahrscheinlichkeitsdichte", fontsize=12)
ax_prior.set_title(
    "Prior Predictive Distribution\n(Was erwarten wir vor dem Sehen der Daten?)",
    fontsize=14,
    fontweight="bold",
)
ax_prior.legend(fontsize=11)
ax_prior.grid(alpha=0.3)
# plt.tight_layout()
plt.show()

# %%
# Wir sehen, dass bambi einen prior gewählt hat, der kaum Einschränkungen
# macht. Alle Anzahlen an wahrscheinlichen Ja Antworten sind etwa gleich
# wahrscheinlich, außer die beiden Extreme von 0 oder 20 Ja Antworten.

# %%
# Als nächstes fitten wir das Modell zu den Daten (MCMC sampling)
results = model.fit(draws=5000, chains=4, random_seed=42)

# %%
# Zusammenfassung der Posterior-Verteilung
print("Posterior-Zusammenfassung:")
print(az.summary(results, var_names=["Intercept"]))
# Hierbei ist besonders wichtig darauf zu achten, dass der R-Hat Wert (ein Wert für die Güte der MCMC approximation) möglichst nahe bei 1 liegt. Falls der Wert über 1.05 sein sollte, ist das ein schlechtes Zeichen für die Approximation und das MCMC sampling sollte verbessert werden.

# %%
# Posterior auf Wahrscheinlichkeits-Skala transformieren
# (Intercept ist auf logit-Skala)

intercept_samples = results.posterior["Intercept"].values.flatten()
theta_samples = expit(intercept_samples)  # logit^-1 transformation

print("\nGeschätzte Teilnahme-Wahrscheinlichkeit:")
print(f"  Mittelwert: {np.mean(theta_samples):.2%}")
print(f"  Median: {np.median(theta_samples):.2%}")
print(
    f"  95% Credible Interval: [{np.percentile(theta_samples, 2.5):.2%}, "
    f"{np.percentile(theta_samples, 97.5):.2%}]"
)
# %%
# Wir sehen, dass wir nach dem Erhalt der Daten in denen 90% der 20 Befragten mit Ja geantwortet haben, auch einen 70%-igen Anteil in der Gesamtheit der Vereinsmitglieder noch für plausibel halten (auch wenn wir 87% als den wahrscheinlichsten Wert ansehen). Dies verdeutlicht, dass wir nach der Befragung von nur 20 Mitgliedern noch erhebliche Unsicherheit haben.
# Probiere selbst einmal aus wie sich das ändert, wenn wir bei 100 Befragten einen 90% Anteil an Ja-Antowrten bekommen hätten. (Hint: das Credible Intervall sollte auf ca. 82%-94% schrumpfen.)
# %%
