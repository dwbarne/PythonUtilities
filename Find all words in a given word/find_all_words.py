""" Find all words that can be made with the letters of a given word """

def contains(word, letters):
    ''' Test whether all letters of word are in letters.
        Letters must be a sorted list.'''
    letterIndex = 0;
    for letter in sorted(word):
        if letterIndex >= len(letters):
            # Ran out of letters
            return False

        while letter > letters[letterIndex] and letterIndex < len(letters) -1:
            # Skip letters that are too small
            letterIndex += 1

        if letter == letters[letterIndex]:
            # A match, keep checking
            letterIndex += 1
            continue

        # No match for current letter
        return False

    return True


def findWordsIn(targetWord, minLen=3):
    letters = sorted(targetWord)

    for word in open('/usr/share/dict/words'):
        word = word.strip()

        if len(word) < minLen:
            continue

        if contains(word, letters):
            print word

findWordsIn('python', 3)

