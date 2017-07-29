from collections import defaultdict, OrderedDict
from github import Github
from github.GithubException import GithubException

from app import app, cache
from app.utils.logger import logger


class GithubRepoWrapper:
    """ Singleton Wrapper Class. Serves 2 functions:
    - Simplify and abstract PyGithub check_available_years
    - Add ensure single session is created"""

    OAUTH = app.config.get('GITHUB_TOKEN')
    class __GithubRepoWrapper:
        def __init__(self):
            logger.info('Initializing Gist Session')
            self._session = Github(GithubRepoWrapper.OAUTH)
            try:
                self._session.get_user().id
            except Exception as errmsg:
                logger.error('GitWrapper Error:')
                self.nullify_session(errmsg)
            else:
                self.update_rates()
                self._user = self._session.get_user()
                self.update_content()

                self.limit = self._session.get_rate_limit().rate.limit
                logger.info('Rate Limit: {}/{}'.format(self.remaining,
                                                       self.limit))
                if self.limit < 1:
                    self.nullify_session('Rate Limit Exceeded')
        def nullify_session(self, errmsg):
            # Sets Variables to ensure error handling
            logger.info(errmsg)
            self.content = []
            self.remaining = 0
            self.limit = 0
            self.error = errmsg
            logger.error('Nullifying Session...')

        def update_rates(self):
            self.remaining = self._session.get_rate_limit().rate.remaining

        def update_content(self):
            self.repo = self._user.get_repo('revitapidocs.code')
            self.content = self.repo.get_contents('/')

    instance = None
    def __init__(self):
        if not GithubRepoWrapper.instance:
            GithubRepoWrapper.instance = GithubRepoWrapper.__GithubRepoWrapper()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __bool__(self):
        return bool(self.instance.content)

repo = GithubRepoWrapper()
@cache.cached(timeout=21600, key_prefix='gists')  # 6 Hour
def get_repo_data():
    #TODO: Clean this shit up
    folders = [f for f in repo.content if f.path.endswith('-code')]
    repo_json = {'folders': {}}
    errors = []
    for folder in folders:
        message_data = None
        files_by_group = defaultdict(dict)
        folder_name = folder.name

        for file_data in folder.raw_data:

            if file_data['name'].endswith('.name'):
                folder_name = file_data['name'].replace('.name', '')
                continue

            if file_data['name'] == 'message.html':
                message_data = file_data
                continue

            chunks = file_data['name'].split('_')
            if len(chunks) != 2:
                logger.error('Skipping Gist. Could not parse: ' + str(chunks))
                errors.append('Could not Parse: {}'.format(str(chunks)))
                continue
            file_group, file_name = chunks
            files_by_group[file_group][file_name] = {'name': file_name.split('.')[0],
                                                     'id': file_name.replace('.','-'),
                                                     'data': file_data
                                                     }

        folder_json = {'name': folder_name, 'contents': files_by_group }
        repo_json['folders'][folder.name] = folder_json
        if message_data:
            repo_json['folders'][folder.name]['message'] = message_data

    logger.info('Gettings Repo. Rate: {}/{}'.format(repo.remaining,
                                                    repo.limit))
    if hasattr(repo, 'error'):
        errors.append(repo.error.data['message'])

    if not repo_json['folders']:
        errors.append('repository did not return valid data')

    if errors:
        repo_json['error'] = errors
    return repo_json
