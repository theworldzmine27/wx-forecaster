import json, os, requests
import azure.functions as func

USER_AGENT = os.getenv("WEATHERGOV_USER_AGENT", "wx-forecaster/1.0 (ray@example.com)")
DEFAULT_POINTS = os.getenv("DEFAULT_POINTS", "33.4484,-112.0740")

def normalize_period(p):
    return {
        "name": p.get("name"),
        "startTime": p.get("startTime"),
        "endTime": p.get("endTime"),
        "isDaytime": p.get("isDaytime"),
        "temperature": p.get("temperature"),
        "temperatureUnit": p.get("temperatureUnit"),
        "windSpeed": p.get("windSpeed"),
        "windDirection": p.get("windDirection"),
        "shortForecast": p.get("shortForecast"),
        "detailedForecast": p.get("detailedForecast"),
        "probabilityOfPrecipitation": (p.get("probabilityOfPrecipitation") or {}).get("value"),
    }

def main(req: func.HttpRequest) -> func.HttpResponse:
    latlon = req.params.get("latlon")
    if not latlon:
        try:
            latlon = req.get_json().get("latlon")
        except Exception:
            latlon = DEFAULT_POINTS

    r = requests.get(
        f"https://api.weather.gov/points/{latlon}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
        timeout=20,
    )
    r.raise_for_status()
    props = r.json()["properties"]
    forecast_url = props["forecast"]
    office = props["gridId"]
    grid_x, grid_y = props["gridX"], props["gridY"]

    f = requests.get(
        forecast_url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
        timeout=20,
    )
    f.raise_for_status()
    periods = [normalize_period(p) for p in f.json()["properties"]["periods"]]

    body = {
        "latlon": latlon,
        "office": office,
        "gridX": grid_x,
        "gridY": grid_y,
        "forecastUrl": forecast_url,
        "periods": periods
    }
    return func.HttpResponse(json.dumps(body), mimetype="application/json")
