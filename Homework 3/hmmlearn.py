import util
import constant
import datetime

def getTagInfo(filename):
    """
    Getting the tag information from the data file
    :param filename: The name of the data file
    :return: the list of object, where each object would be dict representing tag and word
    """
    return util.getTaggedWords(filename)

def getStartingTagCount(tag_info):
    """
    Getting the count of the starting tag count
    :param tag_info: the tag information list
    :return: a dict containing the count of starting TAG
    """
    starting_prob = {}
    index = 0
    for sentence in tag_info:
        startingTagInfo = sentence[0]

        tag = startingTagInfo['tag']

        # Raise an exception, if the length of the tag is not 2
        if len(tag) != 2:
            raise ValueError('The length of the tag is not 2')

        if tag in starting_prob:
            starting_prob[tag] += 1
        else:
            starting_prob[tag] = 1
        index += 1
    return starting_prob

def isStartProbCorrect(tag_info, start_prob):
    """
    Checking if any starting probability is missed or added extra
    :param tag_info: the tag info list
    :param start_prob: the dict representing the tag with count
    :return:
    """
    sentence_count = len(tag_info)
    tag_count = 0
    for tag, count in start_prob.iteritems():
        tag_count += count

    if sentence_count < tag_count:
        # Missing starting probability
        return False
    elif tag_count > sentence_count:
        # Missed tag information
        return False
    else:
        return True

def getStartProb(start_prob, totalCount):
    """
    Computing the starting probability
    :param start_prob: the dict representing the tag with the count
    :param totalCount: the total number of sentences in the data file
    :return: a dict representing the tag with their probability
    """
    starting_prob = {}

    totalCount = float(totalCount)

    for tag, count in start_prob.iteritems():
        starting_prob[tag] = count/totalCount
    return starting_prob

def getPOSTransitionCount(tag_info):
    """
    Compute the transition probability
    :param tag_info: the tag information
    :return: a dictionary with key as 'curr' and the value is an dict as prev and count
    """

    transitionProb = {}

    count = 0
    # For every set of tags for a sentence
    for tags in tag_info:

        # print 'Reading sentence : ' + str(count)
        count += 1

        # Initialize the previous and current tag to empty string
        prev = ''
        curr = ''

        for tag in tags:
            # Store the tag to the current tag
            curr = tag['tag']

            # Would cover the first tag
            if prev != '':
                # Already seen the current tag
                if curr in transitionProb:
                    # Get the transitions to the curr tag
                    transition_array = transitionProb[curr]

                    # Loop over the transitions

                    index = getPreviousTagIndex(prev, transition_array)
                    if index > -1:
                        prevTagInfo = transition_array[index]
                        prevTagInfo['count'] += 1
                    else:
                        transition = {
                            'previous': prev,
                            'count': 1
                        }
                        transition_array.append(transition)
                        transitionProb[curr] = transition_array
                else:
                    transition = {
                        'previous': prev,
                        'count': 1
                    }
                    transition_array = [transition]
                    transitionProb[curr] = transition_array
                # Store the current to the previous
                prev = curr
                continue
            else:
                # Store the current to the previous
                prev = curr
                # Clear the current
                curr = ''

    return transitionProb

def getPreviousTagIndex(previous, transition_array):
    """
    Find the index in the transition array. If the previous tag is not present, returning -1
    :param previous: the previous tag, being searched
    :param transition_array: the transition array
    :return: the index in the transition array
    """
    index = 0

    for previousTagInfo in transition_array:
        if previousTagInfo['previous'] == previous:
            return index
        index += 1
    return -1

def getWordCount(tag_info):
    """
    Count the words in the data file
    :param tag_info: the tag information
    :return: number of words in the data file
    """
    count = 0
    for sentence in tag_info:
        count += len(sentence)
        pass
    return count

def getTransitionCount(transition_count):
    """
    Counting the number of transtion in the transition_count
    :param transition_count: the transition dictionary
    :return: number of transitions
    """
    count = 0
    for curr, previousInfoList in transition_count.iteritems():
        for previousObj in previousInfoList:
            count += previousObj['count']
    return count


def getTagCount(transition_count):
    """
    Calculate the number of times a particular tag occurs
    :param transition_count: the transition from 'a tag' to 'another tag'
    :return: a dict representing the nubmer of times a 'tag' occurred in the data
    """
    tag_count = {}
    for tag in transition_count:
        count = 0
        for nextTag in transition_count[tag]:
            count += nextTag['count']
        tag_count[tag] = count

    return tag_count

if __name__ == '__main__':
    start = datetime.datetime.now()

    # Tag Information
    tag_info = getTagInfo(constant.DEV_TAGGED_DATA)

    # First Tag Count
    starting_tag_count = getStartingTagCount(tag_info)

    # If we found the correct number of starting tag
    if isStartProbCorrect(tag_info, starting_tag_count):

        # Starting Probability
        starting_prob = getStartProb(starting_tag_count, len(tag_info))

        # Transition Count
        POS_transition_count = getPOSTransitionCount(tag_info)

        # Total number of words
        word_count = getWordCount(tag_info)

        # Total number of transitions
        transition_count = getTransitionCount(POS_transition_count)

        # Expected number of transitions
        expected_transition = word_count - len(tag_info)

        # If missed any transitions!
        if expected_transition == transition_count:
            tag_count = getTagCount(POS_transition_count)
        else:
            raise ValueError('Missing transition count!')
    else:
        raise ValueError('Missed')

    end = datetime.datetime.now()
    print 'Took ' + str(end-start) + ' time.'

