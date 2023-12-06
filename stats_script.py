from scipy.stats import hypergeom

DECK_SIZE = 60
LANDS = 18

sample_size = 7
lands_in_hand = 2

# Create a hypergeometric distribution object
hypergeom_dist = hypergeom(DECK_SIZE, LANDS, sample_size)

# Calculate the probability of getting exactly 1 success in the sample
probability = hypergeom_dist.pmf(lands_in_hand)

# Calculate the odds
odds = probability / (1 - probability)

print(f"odds: {odds}")
