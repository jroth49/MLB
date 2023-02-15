# MLB

This is a work in progress

Webscraping Baseballreference.com for statistics, Hitting sports books API's to get odds, implement arbitrage betting and other automated calculations in a spreadsheet.




MLB Model Software Outline

Brainstorm/Features/Websites
  Brainstorm
    Make sports betting models to predict odds based on historical data and current stats
    Will need to collect historical data and current data
    Need to compare based on current matchups checking for information pre-first pitch
    Will need to test with seasons prior
    Trickiest part will be comparing old data to new data, while keeping new data up to date
    Potential DB and WebApp And Twitter Picks
    Create graphs and charts per season to see trends
  Features
    Compare previous player data to current matchup
    Live odds (updating them and line shopping)
    Give feedback on what the best pick is based on stats
    Have different comparison models for the big 3 bets on a game
    Look into different bets as well to see a trend with smaller bets (i.e. RSIF)
  Websites
    Baseball reference
      Has historical data, starting lineups, pitching/batting stats, box score, play by play, etc.
      Great website to get basis knowledge
      Website has great path manipulation for pulling information needed (really easy web scrape)
    Odds Jam
      Potential to show line shops and live odds
      Has injuries
      Free to use
    MLB.com
      Has depth chart
      Starting lineups
      Easy to scrape?
    Sportsbookreviews
      https://sportsbookreviewsonline.com/scoresoddsarchives/mlb/mlboddsarchives.htm
      Has Historical Betting odds IMPORTANT
  Data Needed & Comparisons
    Players
    Teams
    Odds
    Lineups
    Injuries
    PreGame Stats
    Depth Charts/Rotations


Project Progression Outline
  Collecting Data
  Being able to read data and calculate percentages
  Saving information and utilizing it for future calculations
  Build some models based on stats checkout odds and pricing
  Test models on Seasons to see what they can predict
  Evaluate and prep to set up for a starting season
  Make it better$$$$


Other Notes
  Search functionality by Matchup so find past games when these teams faced each other compare their records
  Big spreadsheet every game every odd every point system stat we come up with base on game and put it into a db to do searches and crunch numbers
  Season Averages Directory
  Position Lead

Here's a screenshot of a test spreadsheet I've utilized
![mlb](https://user-images.githubusercontent.com/52512047/218917221-d0a55f19-0e8f-43ac-8517-dd4f5d431008.png)

