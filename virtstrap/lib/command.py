from argparse import ArgumentParser
from virtstrap.log import logger

class Command(object):
    name = None
    args = None
    parser = ArgumentParser()
    description = None
    options = None

    def __init__(self):
        # Ensure that name, usage, and description
        # are defined
        assert self.name
        self.options = []
        self.logger = logger

    def execute(self, config, **options):
        self.logger.info('Running "%s" command' % self.name)
        try:
            self.run(config, **options)
        except:
            self.logger.exception('An error occured executing command "%s"' %
                    self.__class__.__name__)
            return 2
        return 0

    def run(self, *args, **options):
        raise NotImplementedError('This command does nothing')
