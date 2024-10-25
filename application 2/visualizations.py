import matplotlib.pyplot as plt
from database import fetch_daily_summaries

def plot_weather_summary():
    summaries = fetch_daily_summaries()
    dates = [summary[0] for summary in summaries]
    avg_temps = [summary[1] for summary in summaries]
    max_temps = [summary[2] for summary in summaries]
    min_temps = [summary[3] for summary in summaries]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, avg_temps, label='Average Temp', color='blue')
    plt.plot(dates, max_temps, label='Max Temp', color='red')
    plt.plot(dates, min_temps, label='Min Temp', color='green')
    plt.title('Daily Weather Summary')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
