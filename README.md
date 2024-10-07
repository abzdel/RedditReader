# RedditReader

## TODO

1. find better voice/text to speech solution
   - breaking down with longer comments
   - voice changing in between files (for non eleven labs)
     - either need a different model, shorter comment filter, or a way to pass things in sentence by sentence
   - new openai voice model?
1. ~~organize output + folder structure to work better for video generation purposes~~
1. ~~develop script to pull screenshots of each post thats being read~~
1. ~~develop scraper to pull in lots of different videos for short form content~~
   - see background video scraper repo
1. develop python script to edit videos together
   - create voice to text over video
1. develop tik tok script to schedule these uploads daily
1. change max characters based on tts model?
1. test on linux vps
1. move frontend to separate repo
1. decide on reddit post screenshot vs. generating fake one. maybe go back to the verified checkmark being there (removed currently)
   - maybe put the subreddit name instead of author's name if we go with the generated one
1. parse out more garbage from comments/post strings

### later

1. build frontend
1. host app
1. create sqlite database
   - unique for each user
   - stores history of all previous posts they've requested
1. add functionality - more voices
1. update front-end to:
   - choose between voices
   - choose historical files more cleanly
1. (somewhere during these steps) create architectural diagram. probably after the preceding steps, but after creating sqlite database at the earliest
1. retry connecting to source if failed
   - error message not specific enough - should differentiate between being rate limited vs other connection errors
