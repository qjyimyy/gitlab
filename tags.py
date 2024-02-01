import logging

import info
from info import gl

logging.basicConfig(level=logging.DEBUG)

# get the runner id
runner_id = gl.runners.list()[0].id
runner = gl.runners.get(runner_id)

print("runner id #", runner_id)

old_tags = runner.tag_list
print("old tags:", old_tags)

new_tags = ['tag', 'new_tag']

if old_tags != new_tags:
    runner.tag_list = new_tags
    print("new tags:", runner.tag_list)
    runner.save()
    print("runner returns:", runner.id, runner.description, runner.tag_list)
else: print("no change")

# runner.save()