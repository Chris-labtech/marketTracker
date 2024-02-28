import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to perform sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Function to scrape YouTube search results for the last 30 days
def scrape_youtube(query):
    date_30_days_ago = datetime.now() - timedelta(days=30)
    date_str = date_30_days_ago.strftime("%Y-%m-%d")

    # Create Chrome options with headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    # Create a Chrome webdriver instance with the specified options
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(f"https://www.youtube.com/results?search_query={query}&sp=EgQIAhAB&sp=CAI%253D")
        
        # Wait for the views count to be visible
        WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='style-scope ytd-video-meta-block']")))
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        videos = []
        for vid in soup.find_all("div", class_="text-wrapper style-scope ytd-video-renderer"):
            title_elem = vid.find("a", class_="yt-simple-endpoint style-scope ytd-video-renderer")
            title = title_elem.get("title") if title_elem else "N/A"
            link = "https://www.youtube.com" + title_elem.get("href") if title_elem else "N/A"
            
            # Extract views count
            views_elem = vid.find("span", class_="style-scope ytd-video-meta-block")
            views = views_elem.get_text().strip() if views_elem else "N/A"
            
            # Extract likes count using the provided XPath expression
            likes_elem = vid.select_one("ytd-menu-renderer.ytd-watch-metadata > div:nth-child(1) > segmented-like-dislike-button-view-model:nth-child(1) > yt-smartimation:nth-child(1) > div:nth-child(1) > div:nth-child(1) > like-button-view-model:nth-child(1) > toggle-button-view-model:nth-child(1) > button-view-model:nth-child(1) > button:nth-child(1) > div:nth-child(2)")
            likes = likes_elem.get_text().strip() if likes_elem else "N/A"
            
            # Extract dislikes count
            dislikes_elem = vid.find_all("a", class_="yt-simple-endpoint style-scope ytd-toggle-button-renderer")
            dislikes = dislikes_elem[1].get_text().strip() if len(dislikes_elem) > 1 else "N/A"
            
            # Extract comments count
            comments_elem = vid.find_all("yt-formatted-string", class_="style-scope ytd-comment-renderer")
            comments = comments_elem[0].get_text().strip() if comments_elem else "N/A"
            
            sentiment = analyze_sentiment(title)
            
            videos.append({"title": title, "link": link, "views": views, "likes": likes, "dislikes": dislikes, "comments": comments, "sentiment": sentiment})
    finally:
        driver.quit()  # Close the browser window
    return videos

# Function to display YouTube data
def display_youtube_data():
    try:
        query = entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return
        
        videos = scrape_youtube(query)
        for video in videos:
            tree.insert("", "end", values=(video["title"], video["link"], video["views"], video["likes"], video["dislikes"], video["comments"], video["sentiment"]))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the tkinter GUI
root = tk.Tk()
root.title("YouTube Scraping")

# Create notebook widget
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create tab
tab = ttk.Frame(notebook)
notebook.add(tab, text="YouTube Scraping")

# Create frame
frame = ttk.Frame(tab)
frame.pack(fill='both', expand=True)

# Create label widget
label = ttk.Label(frame, text="Search Query:")
label.pack(pady=5)

# Create entry widget
entry = ttk.Entry(frame, width=40)
entry.pack(pady=5)

# Create button widget
button = ttk.Button(frame, text="Scrape YouTube", command=display_youtube_data)
button.pack(pady=5)

# Define columns for treeview
columns = ("Title", "Link", "Views", "Likes", "Dislikes", "Comments", "Sentiment")

# Create treeview widget
tree = ttk.Treeview(frame, columns=columns, show="headings")

# Set headings for columns
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

# Pack treeview widget
tree.pack(fill='both', expand=True)

# Run the tkinter event loop
root.mainloop()
