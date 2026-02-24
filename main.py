from fsrs import Scheduler, Card, Rating, ReviewLog

scheduler = Scheduler()

# NOTE: all new cards are due immediately upon creation
card = Card()

# Rating.Again (==1) forgot the card
# Rating.Hard (==2) remembered the card with serious difficulty
# Rating.Good (==3) remembered the card after a hesitation
# Rating.Easy (==4) remembered the card easily

rating = Rating.Easy

card, review_log = scheduler.review_card(card, rating)

print(f"Card rated {review_log.rating} at {review_log.review_datetime}")
# > Card rated 3 at 2024-11-30 17:46:58.856497+00:00

from datetime import datetime, timezone

due = card.due

# how much time between when the card is due and now
time_delta = due - datetime.now(timezone.utc)

print(f"Card due on {due}")
# Este exemplo não é bom, pois fica parecendo que o delta é apenas os segundos, quando na verdade
# temos dias também
print(f"Card due in {time_delta.seconds} seconds")
