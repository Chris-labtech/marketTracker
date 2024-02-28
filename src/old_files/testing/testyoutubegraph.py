import tkinter as tk
from tkinter import ttk
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import YOUTUBE_DATA_API_KEY

# Function to search for videos mentioning "Bitcoin" within the last year
def search_videos(query):
    # Calculate the date 1 year ago
    date_1_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_DATA_API_KEY)
    request = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        publishedAfter=date_1_year_ago,
        order='date',  # Sort by date
    )

    response = request.execute()
    return response.get('items', [])

# Function to retrieve statistics for a video
def get_video_stats(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_DATA_API_KEY)
    request = youtube.videos().list(
        part='statistics',
        id=video_id
    )

    response = request.execute()
    items = response.get('items', [])
    if items:
        return items
    else:
        return None

# Function to populate the table with actual video data
def populate_table(tree):
    query = "Bitcoin"
    videos = search_videos(query)
    
    for index, video in enumerate(videos, start=1):
        video_id = video['id']['videoId']
        stats = get_video_stats(video_id)
        
        if stats:
            title = video['snippet']['title']
            published_date = video['snippet']['publishedAt']
            view_count = stats[0]['statistics']['viewCount']
            like_count = stats[0]['statistics']['likeCount']
            dislike_count = stats[0]['statistics'].get('dislikeCount', 'N/A')
            comment_count = stats[0]['statistics'].get('commentCount', 'N/A')
            
            tree.insert("", tk.END, values=(index, title, published_date, view_count, comment_count, like_count, dislike_count))
        else:
            title = video['snippet']['title']
            tree.insert("", tk.END, values=(index, "N/A", "No", "N/A", "N/A", "N/A", "N/A"))

# Function to create a line graph
def create_line_graph():
    query = "Bitcoin"
    videos = search_videos(query)
    
    dates = []
    for video in videos:
        try:
            published_at = video['snippet']['publishedAt']
            date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').date()
            dates.append(date)
        except KeyError:
            pass
    
    unique_dates = list(set(dates))
    video_count_by_date = [dates.count(date) for date in unique_dates]
    
    plt.figure(figsize=(8, 6))
    plt.plot(unique_dates, video_count_by_date, marker='o', linestyle='-')
    plt.title('Number of Bitcoin Videos in Last 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Number of Videos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt

# Main function
def main():
    root = tk.Tk()
    root.title("YouTube Data Analysis")

    tabs = ttk.Notebook(root)

    # Configure Tab
    configure_tab = ttk.Frame(tabs)
    tabs.add(configure_tab, text="Configure")

    # YouTube Data Analysis Tab
    youtube_data_analysis_tab = ttk.Frame(tabs)
    tabs.add(youtube_data_analysis_tab, text="YouTube Data Analysis")

    # YouTube Table Tab
    youtube_table_tab = ttk.Frame(tabs)
    tabs.add(youtube_table_tab, text="YouTube Table")

    tabs.pack(expand=1, fill="both")

    # Line graph
    plt = create_line_graph()
    canvas = FigureCanvasTkAgg(plt.gcf(), master=youtube_data_analysis_tab)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Table
    columns = ("Item", "Description", "Published", "Views", "Comments", "Likes", "Dislikes")
    tree = ttk.Treeview(youtube_table_tab, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)
    populate_table(tree)

    root.mainloop()

if __name__ == "__main__":
    main()
