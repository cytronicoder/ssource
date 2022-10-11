from github import Github
import random

client = Github()


def createQuery(language, topic):
    '''
    Creates a PyGithub search query.
    :param language: Programming language of choice
    :param topic: Topic of choice.
    :return: Finished query.
    '''

    if language=="*":
        return topic
    elif topic=="*":
        return "language:{}".format(language)
    return "{}+language:{}".format(topic, language)

def getData(repo):
    '''
    Extracts useful information from a PyGithub repo object.
    :param repo: A PyGithub Repository object.
    :return: A dictionary with the repo's language, # forks, # stars, and the url.
    '''
    return {
        "lang": repo.language,
         "forks": repo.forks_count,
         "stars": repo.stargazers_count,
         "url": repo.html_url
    }

def findRandomRepo(config):
    '''
    Finds a random repository that adheres to the config.
    :param config: The server config stored in the DB.
    :return: The data from a random repo.
    '''

    langs = config["langs"]
    topics = config["topics"]

    selectedTopic = random.choice(topics)
    selectedLang = random.choice(langs)

    if selectedTopic == "*" and selectedLang == "*":
        repos = client.get_repos()
    else:
        query = createQuery(selectedLang, selectedTopic)
        repos = client.search_repositories(query)

    try:
        lastPage = repos.totalCount//len(repos.get_page(0))
    except ZeroDivisionError:
        # Nothing adheres to the topics provided
        return None

    page = repos.get_page(random.randrange(0, lastPage))

    return getData(random.choice(page))





