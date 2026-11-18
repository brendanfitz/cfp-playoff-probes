# cfp-playoff-probes

Analysis of the College Football Playoff committee's rankings, using game data from the
[CollegeFootballData.com](https://collegefootballdata.com) API.

## Setup

1. Get a free API key at <https://collegefootballdata.com/key>.
2. `cp .env.example .env` and paste your key in.
3. Create the environment and launch Jupyter:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   .venv/bin/jupyter notebook notebooks/
   ```

## Notebooks

- `01_game_results.ipynb` — pulls every FBS game result for the season into a DataFrame,
  builds team records, and joins in the weekly CFP committee rankings.
