# %%
import os
if os.path.basename(os.getcwd()) == "src":
    os.chdir("..")

import pandas as pd
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.proportion import proportions_ztest

preds = pd.read_csv("data/processed/predictions.csv", index_col=0)


threshold = preds["churn_proba"].quantile(0.70)
risk_group = preds[preds["churn_proba"] >= threshold].copy()
print("Размер группы риска:", len(risk_group))
print("Реальный отток:", round(risk_group["churn_actual"].mean(), 3))

p_control = 0.594
p_treatment = 0.594 - 0.04
effect_size = proportion_effectsize(p_control, p_treatment)

analysis = NormalIndPower()
n_per_group = analysis.solve_power(
    effect_size=effect_size, alpha=0.05, power=0.80, alternative="larger")
print("Нужно на группу:", round(n_per_group), "| у нас:", 529)


np.random.seed(42)

risk_group = risk_group.sample(frac=1, random_state=42).reset_index(drop=True)
half = len(risk_group) // 2
control = risk_group.iloc[:half].copy()
treatment = risk_group.iloc[half:].copy()

print("Control:", len(control), "| Treatment:", len(treatment))


p_control = control["churn_actual"].mean()
effect = 0.08
p_treatment_true = p_control - effect

treatment_churn = np.random.binomial(1, p_treatment_true, size=len(treatment))

churn_rate_control = control["churn_actual"].mean()
churn_rate_treatment = treatment_churn.mean()

print(f"Отток control:   {churn_rate_control:.3f}")
print(f"Отток treatment: {churn_rate_treatment:.3f}")
print(f"Наблюдаемый uplift (снижение): {churn_rate_control - churn_rate_treatment:.3f}")


churned_control = control["churn_actual"].sum()
churned_treatment = treatment_churn.sum()

count = np.array([churned_control, churned_treatment])
nobs  = np.array([len(control), len(treatment)])

z_stat, p_value = proportions_ztest(count, nobs, alternative="larger")

print(f"Ушло в control:   {churned_control} из {len(control)}")
print(f"Ушло в treatment: {churned_treatment} из {len(treatment)}")
print(f"\nz-статистика: {z_stat:.4f}")
print(f"p-value:      {p_value:.4f}")
print(f"\nЗначимо на уровне 0.05: {'ДА' if p_value < 0.05 else 'НЕТ'}")


n_bootstrap = 10000
uplifts = []

control_outcomes = control["churn_actual"].values
treatment_outcomes = treatment_churn

for _ in range(n_bootstrap):
    c_sample = np.random.choice(control_outcomes, size=len(control_outcomes), replace=True)
    t_sample = np.random.choice(treatment_outcomes, size=len(treatment_outcomes), replace=True)
    uplifts.append(c_sample.mean() - t_sample.mean())

uplifts = np.array(uplifts)

ci_low = np.percentile(uplifts, 2.5)
ci_high = np.percentile(uplifts, 97.5)

print(f"Средний uplift: {uplifts.mean():.3f}")
print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]")
print(f"Включает 0: {'ДА' if ci_low <= 0 <= ci_high else 'НЕТ'}")


n_risk = len(risk_group)

avg_mrr = risk_group["monthlycharges"].mean()

uplift_point = uplifts.mean()
uplift_low = ci_low
uplift_high = ci_high

def saved_revenue(uplift):
    saved_customers = n_risk * uplift
    return saved_customers * avg_mrr

print(f"Клиентов в группе риска: {n_risk}")
print(f"Средний чек: ${avg_mrr:.2f}")
print(f"\nСпасённая выручка в месяц:")
print(f"  Оценка:      ${saved_revenue(uplift_point):,.0f}")
print(f"  Диапазон CI: ${saved_revenue(uplift_low):,.0f} — ${saved_revenue(uplift_high):,.0f}")
print(f"\nВ год (×12): ${saved_revenue(uplift_point)*12:,.0f}")


# предположение: стоимость удержания одного клиента (звонок + скидка)
cost_per_customer = 20  # $ на клиента в группе риска

total_campaign_cost = n_risk * cost_per_customer
saved_monthly = saved_revenue(uplift_point)

print(f"Стоимость кампании (разово): ${total_campaign_cost:,.0f}")
print(f"Спасённая выручка в месяц:   ${saved_monthly:,.0f}")
print(f"\nОкупаемость: {total_campaign_cost / saved_monthly:.1f} месяцев")
print(f"Чистая выгода за год: ${saved_monthly*12 - total_campaign_cost:,.0f}")