import requests
from bs4 import BeautifulSoup
import re
import hashlib
import pandas as pd


def get_titles_urls_and_comment_links(soup, base_url):
    """Scrape titles, URLs, and comment links from the main page."""
    title_spans = soup.find_all("span", class_="titleline")
    titles = [span.find("a").get_text(strip=True) for span in title_spans]
    urls = [span.find("a")["href"] for span in title_spans]

    comment_pattern = re.compile(r"^\d+\s+comments$")  
    comment_links = []

    for a_tag in soup.find_all("a"):
        text = a_tag.get_text(strip=True)
        if comment_pattern.match(text):
            href = a_tag["href"]
            if href.startswith("item?id="):
                href = base_url + href
            comment_links.append(href)

    return titles, urls, comment_links
def generate_deterministic_key(username,comment,posted_time):
    combined =f"{username}+{comment}+{posted_time}"
    comment_id = hashlib.md5(combined.encode("utf-8")).hexdigest()
    return comment_id


def scrape_comments_for_post(post_url, post_title, soup):
    """Scrape all comments, usernames, and posted times for a given post."""
    comment_blocks = soup.find_all("tr", class_="athing comtr")
    comments_data = []

    for block in comment_blocks:
   
        comment_div = block.find("div", class_="commtext c00")
        if comment_div:
            comment_text = comment_div.get_text(strip=True)
            paragraphs = [p.get_text(strip=True) for p in comment_div.find_all("p")]
            comment_text += " ".join(paragraphs)
        else:
            comment_text = "the data"

        user_tag = block.find("span", class_="comhead")
        user_link = user_tag.find("a") if user_tag else None
        username = "anonymous"
        if user_link:
            match = re.search(r"user\?id=([a-zA-Z0-9_-]+)", user_link["href"])
            if match:
                username = match[1]
            else:
                username = user_link.get_text(strip=True) or "anonymous"

        time_tag = block.find("span", class_="age")
        time_link = time_tag.find("a") if time_tag else None
        posted_time = "unknown"
        if time_link:
            match_time = re.search(r"item\?id=([0-9]+)", time_link["href"])
            if match_time:
                posted_time = match_time[1]
            else:
                posted_time = time_link.get_text(strip=True) or "unknown"

        comments_data.append({
            "username": username,
            "comment": f"comment: {comment_text} | title: {post_title}",
            "posted_time": posted_time,
            "comment_id":generate_deterministic_key(username,comment_text,posted_time)
        })

    return comments_data


if __name__ == "__main__":
    BASE_URL = "https://news.ycombinator.com/"
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    all_comments_data = []
    

    titles, urls, comment_links = get_titles_urls_and_comment_links(soup, base_url=BASE_URL)
    
    
    # Loop over posts and scrape their comments
    for i in range(len(comment_links)):
        post_url = comment_links[i]
        post_title = titles[i]

        post_response = requests.get(post_url)
        post_soup = BeautifulSoup(post_response.text, "html.parser")

        comments_for_post = scrape_comments_for_post(post_url, post_title, post_soup)
        all_comments_data.extend(comments_for_post)
        # saving as a datafram first 
        
        df = pd.DataFrame(all_comments_data)

        df.to_csv("hn_comments_for_rag.csv", index=False)

    total_comments = len(all_comments_data)
    total_usernames = len(all_comments_data)
    total_posted_times = len(all_comments_data)

 

  
    print("\nFirst 5 comments with username and time:")
    print(all_comments_data[1000])
