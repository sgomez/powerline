# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

from os.path import isfile

from powerline.lib.shell import asrun, run_cmd
from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info, requires_filesystem_watcher

@requires_filesystem_watcher
@requires_segment_info
class VersionSegment(Segment):
	divider_highlight_group = None

	@staticmethod
	def get_directory(segment_info):
		return segment_info['getcwd']()

	@staticmethod
	def get_env(segment_info):
		return segment_info['environ'].get('SYMFONY_ENV', 'dev')

	def __call__(self, pl, segment_info, create_watcher):
		path = self.get_directory(segment_info)

		if isfile('%s/vendor/symfony/symfony/src/Symfony/Component/HttpKernel/Kernel.php' % path):
			version = run_cmd(pl, ['%s/bin/console' % path, '-V'])
			if not version:
				return

			try:
				version = '%s [%s] ' % (version.split(' ')[1], self.get_env(segment_info))
			except:
				return

			return [{
				'contents': version,
				'highlight_groups': ['virtualenv'],
				'divider_highlight_group': self.divider_highlight_group
			}]

version = with_docstring(VersionSegment(),
'''Return the current Symfony version in the main directory project.

Highlight groups used: ``virtualenv``.
''')
