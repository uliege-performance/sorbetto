import inspect

import matplotlib.pyplot as plt
from utils import run_and_save

from sorbetto.ranking.ranking_score import RankingScore


def draws_in_ROC(ranking_score: RankingScore):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for index, prior_pos in enumerate([0.1, 0.9]):
        ranking_score.drawInROC(fig, ax[index], priorPos=prior_pos)
    plt.tight_layout()


rank_members = inspect.getmembers(RankingScore)
get_scores = [
    m
    for m in rank_members
    if inspect.isfunction(m[1])
    and m[0].startswith("get")
    and m[1].__code__.co_argcount == 0
]

for name, func in get_scores:
    score = func()
    plt.close("all")
    run_and_save(draws_in_ROC, f"{name[3:]}_in_ROC", score)
