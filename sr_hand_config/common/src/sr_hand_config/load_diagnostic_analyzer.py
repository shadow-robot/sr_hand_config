#!/usr/bin/env python3

# Copyright 2021 Shadow Robot Company Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation version 2 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
import rospy
import rospkg
from os import walk
import yaml

class LoadDiagnosticAnalyzer(object):
    def __init__(self, hand_serials_list):
        self._hand_serials_list = hand_serials_list
        self._hand_types = {}
        self._hand_sides = {}
        self._diagnostic_analyzers = {}

        self._get_hand_info()
        self._load_analyzer_params()


    def _load_analyzer_params(self):
        for hand_serial in self._hand_serials_list:
            if self._hand_types[hand_serial] == 'hand_g':
                analyzer_file_suffix = '_lite'
            elif self._hand_types[hand_serial] == 'hand_extra_lite':
                analyzer_file_suffix = '_extra_lite'
            else:
                analyzer_file_suffix = ''
            
            analyzer_file_path = rospkg.RosPack().get_path('sr_hand_config') + \
                '/common/config/diagnostic_analyzer' + analyzer_file_suffix + '.yaml'

            with open(analyzer_file_path) as f:
              analyzer = yaml.safe_load(f)

            self._diagnostic_analyzers[self._hand_sides[hand_serial] + '_shadow_hand_' + str(hand_serial)] = \
                analyzer['analyzers']['shadow_hand']

        common_analyzers_file_path = rospkg.RosPack().get_path('sr_hand_config') + \
                '/common/config/common_diagnostic_analyzers.yaml'

        with open(common_analyzers_file_path) as f:
              common_analyzers = yaml.safe_load(f)

        for analyzer, params in common_analyzers['analyzers'].items():
            self._diagnostic_analyzers[analyzer] = params

        rospy.set_param('analyzers', self._diagnostic_analyzers)


    def _get_hand_info(self):
        for hand_serial in self._hand_serials_list:
            general_info_file = rospkg.RosPack().get_path('sr_hand_config') + \
                '/' + str(hand_serial) + '/general_info.yaml'

            with open(general_info_file) as f:
              general_info = yaml.safe_load(f)

            self._hand_types[hand_serial] = general_info['type']
            self._hand_sides[hand_serial] = general_info['side']

if __name__ == "__main__":
    rospy.init_node('load_diagnostic_analyzer', anonymous=True)

    hand_serials_list = rospy.get_param('~hand_serials_list')

    LoadDiagnosticAnalyzer(hand_serials_list)