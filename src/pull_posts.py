import requests
import pandas as pd

def fetch_hot_posts(subreddit: str, limit: int = 25) -> pd.DataFrame:
    # Construct the URL for the subreddit's "hot" posts in JSON format
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Fetch the data
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(f"Failed to fetch data from Reddit. Status code: {response.status_code}")

    # Initialize a DataFrame
    posts_df = pd.DataFrame(columns=['title', 'url'])

    # Parse the JSON and extract relevant information
    for post in data['data']['children']:
        post_data = post['data']
        posts_df = pd.concat([posts_df, pd.DataFrame({
            'title': [post_data.get('title')],
            'url': [f"https://www.reddit.com{post_data.get('permalink')}"]
        })])

    posts_df = posts_df.reset_index(drop=True)
    return posts_df

# Example usage:
if __name__ == "__main__":
    subreddit_name = "python"  # Replace with your target subreddit
    top_posts_df = fetch_hot_posts(subreddit_name)
    print(top_posts_df)
