"""Team records and conference standings built from the long `team_games` table (one row per team per game)."""

import pandas as pd

INDEPENDENTS = "FBS Independents"


def format_record(wins, losses):
    """Element-wise "W-L" strings from two numeric Series."""
    return wins.astype(int).astype(str) + "-" + losses.astype(int).astype(str)


def records_entering(team_games, games):
    """Each FBS team's record entering every game, as a "W-L" Series indexed by (game_id, team).

    `games` supplies `start_date` so games are counted in kickoff order. FCS teams are left out:
    we only have their games against FBS teams, so their records would be wrong.
    """
    tg = (
        team_games[team_games["classification"] == "fbs"]
        .merge(games[["game_id", "start_date"]], on="game_id")
        .sort_values("start_date")
    )
    wins_before = tg.groupby("team")["win"].cumsum() - tg["win"]
    games_before = tg.groupby("team").cumcount()
    return (
        tg.assign(record_then=format_record(wins_before, games_before - wins_before))
        .set_index(["game_id", "team"])["record_then"]
    )


def conference_standings(team_games):
    """Current record and place within conference for every FBS team, indexed by team.

    Teams are ordered by conference win %, then overall win %. This is a simple ordering, not the
    official conference tiebreakers. Independents get no rank.
    """
    fbs = team_games[team_games["classification"] == "fbs"]
    in_conf = (fbs["conference"] == fbs["opp_conference"]) & (fbs["conference"] != INDEPENDENTS)
    standings = (
        fbs.assign(conf_win=fbs["win"] & in_conf, conf_game=in_conf)
        .groupby(["team", "conference"])
        .agg(wins=("win", "sum"), games=("win", "size"), conf_wins=("conf_win", "sum"), conf_games=("conf_game", "sum"))
        .reset_index()
        .assign(
            record_now=lambda d: format_record(d["wins"], d["games"] - d["wins"]),
            conf_pct=lambda d: d["conf_wins"] / d["conf_games"].where(d["conf_games"] > 0),
            pct=lambda d: d["wins"] / d["games"],
        )
    )
    standings["conf_rank"] = (
        standings.sort_values(["conf_pct", "pct"], ascending=False)
        .groupby("conference").cumcount().add(1)
        .where(standings["conference"] != INDEPENDENTS)
        .astype("Int64")
    )
    return standings.set_index("team")[["record_now", "conf_rank"]]
