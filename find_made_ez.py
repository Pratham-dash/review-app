import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

#creation of reddit api
reddit=praw.Reddit(
    client_id="h12N3ltINLKR4leTjMsaPw",
    client_secret="exSyXqor0h4N_Tfrnnm01ao733vecg",
    user_agent="review app/0.1 by u/east_coder001"
)
analyzer = SentimentIntensityAnalyzer()#pos nev comp

#search for reviews in the subreddit that match the query
def fetch_reviews(subreddit_name, query, limit=100):
    try: 
        subreddit = reddit.subreddit(subreddit_name)
        reviews=[]
        print(f"Searching in subreddit: {subreddit_name} with query: {query}")
        if subreddit.display_name.lower() != subreddit_name.lower():
            print(f"Subreddit {subreddit_name} does not exist.")
            return []
        
        for submission in subreddit.search(query, limit=limit):
            
            submission.comments.replace_more(limit=0)  #to replace more comments as reddit shortens long threads to more comment and this line goes inside those more comments limit=0 opens up all more comments in the thread
            for comment in submission.comments.list():
                reviews.append(comment.body)   
        
        
        return reviews
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        
        return[]
def identify_issues(reviews):
    issues=[]
    keywords_input=input("Enter keywords to filter {separate each of them by commas} ")

    try:
        keywords=[keyword.strip() for keyword in keywords_input.replace(".",",").split(",")] #keyword stores keyword as a list
                #the user is extremely friendly since he has to work and hence he will not troll 
                #but he mght mistake '.' for ',' so i dealt with it
        
        for review in reviews:
            if any(re.search(keyword, review, re.IGNORECASE)for keyword in keywords):
                sentiment=analyzer.polarity_scores(review)#gives neg pos com values of reviews
                if sentiment['neg']>0.0:
                    issues.append(review)
        return issues
    except Exception as e:
        print(f"Error identifying issues: {e}")
        return []
def main():
    subreddit_name=input("Please copy the subreddit name without the r/ and paste it here and press |enter| -- ").strip()
    
    query=input("Please enter key-phrases or key-words to filter posts inside the subreddit according to your needs e.g. for filtering posts having the phrase \"vaccum cleaner reviews\" you will write \"vaccuum cleaner\" to filter out the posts  -- ").strip()
    reviews=fetch_reviews(subreddit_name,query,limit=100)
    if not reviews:
        print("no reviews found")
        return
    
    issues=identify_issues(reviews)
    if not issues:
        print("no issues. Please check your keywords and try again")
    else:
        print(issues)
        for issue in issues:
            print(issue)


if __name__=="__main__":
    main()


        
     
    
    




