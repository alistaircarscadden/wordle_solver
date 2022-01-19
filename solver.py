from wordle import Colours, Game
from dictionary import dictionary


def get_word_list():
    '''Load 5 letter words from dictionary'''

    return [w for w in dictionary if len(w) == 5]


def word_list_histogram(wl):
    '''Count the letters in the word list and return it in the form {'A': 2000, 'B': 1500'...}'''

    h = [0] * 26
    for w in wl:
        for l in w:
            h[ord(l) - ord('A')] += 1
    d = {}
    s = sum(h)
    for l in range(26):
        d[chr(l + ord('A'))] = h[l]/s
    return d


def score_word(letter_scores, word):
    '''Score a word based on the quality of letters it contains. Duplicate letters ignored.'''

    word = set(word)
    s = 0
    for l in word:
        # do not score vowels. perhaps vowels will just naturally find themselves in the words that are guessed
        # or something.
        if l not in 'AEIOU':
            s += letter_scores[l]
    return s


def score_and_sort_word_list(letter_scores, word_list):
    '''Score each word in the word list and sort them descending according to their values.'''

    scored = [[w, score_word(letter_scores, w)] for w in word_list]
    scored.sort(key=lambda x: -x[1])
    return [p[0] for p in scored]


def is_guess_consistent_with_all_results(game, guess):
    '''Is the guess consistent with all the results the game has given previously.'''

    for result in zip(game.get_guesses(), game.get_results()):
        if is_guess_consistent_with_result(result, guess) == False:
            return False
    
    return True


def is_guess_consistent_with_result(result, guess):
    '''Is guess consistent with this previous GuessResult?'''

    result_guess = result[0]
    result_colours = result[1]

    for i in range(5):
        if result_colours[i] == Colours.GREEN:
            # ensure the guess includes the correct letter here
            if guess[i] != result_guess[i]:
                return False
        elif result_colours[i] == Colours.YELLOW:
            # ensure the guess has the correct letter somewhere else
            found = False
            for j in range(5):
                if i != j and result_colours[j] != Colours.GREEN and result_guess[i] == guess[j]:
                    found = True
            if not found:
                return False
        else:
            ok = True
            for j in range(5):
                if result_colours[j] != Colours.GREEN and result_guess[i] == guess[j]:
                    ok = False
            if not ok:
                return False

    return True


def solve(game, word_list):
    '''Solve this game. Might succeed.'''

    next_loc_word_list = 0

    for n_guess in range(6):
        for loc_word_list in range(next_loc_word_list, len(word_list)):
            word = word_list[loc_word_list]
            if is_guess_consistent_with_all_results(game, word):
                next_guess = word
                next_loc_word_list = loc_word_list + 1
                break

        game.guess(next_guess)

        if game.guessed_correctly():
            break


if __name__ == '__main__':
    wl = get_word_list()
    hist = word_list_histogram(wl)
    wl = score_and_sort_word_list(hist, wl)

    # how often will print 10% done etc.
    update_step = len(wl) // 10

    wins = 0
    losses = 0

    for i, w in enumerate(wl):
        # update terminal
        if i % update_step == 0:
            print(f'{i/len(wl)*100:.4}% done')

        g = Game(wl, answer=w)
        solve(g, wl)

        if g.guessed_correctly():
            wins += 1
        else:
            losses += 1
    
    print(f'{wins} wins, {losses} losses, {wins/(wins+losses)*100:.4}% correct')
