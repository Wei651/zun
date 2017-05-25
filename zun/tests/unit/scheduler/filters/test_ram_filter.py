#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from zun.common import context
from zun import objects
from zun.scheduler.filters import ram_filter
from zun.tests import base


class TestRamFilter(base.TestCase):

    def setUp(self):
        super(TestRamFilter, self).setUp()
        self.context = context.RequestContext('fake_user', 'fake_project')

    def test_ram_filter_pass(self):
        self.filt_cls = ram_filter.RamFilter()
        container = objects.Container(self.context)
        container.memory = '1024M'
        host = objects.ComputeNode(self.context)
        host.mem_total = 1024 * 128
        host.mem_used = 1024
        self.assertTrue(self.filt_cls.host_passes(host, container))

    def test_ram_filter_fail(self):
        self.filt_cls = ram_filter.RamFilter()
        container = objects.Container(self.context)
        container.memory = '4096M'
        host = objects.ComputeNode(self.context)
        host.mem_total = 1024 * 128
        host.mem_used = 1024 * 127
        self.assertFalse(self.filt_cls.host_passes(host, container))
