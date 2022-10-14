#!/usr/bin/env python3

# Copyright 2021-2022 Shadow Robot Company Ltd.
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

import rospy
import rospkg
import yaml


class LoadDiagnosticAnalyzer:
    def __init__(self, hs_list):
        self._hand_serials_list = hs_list
        self._hand_types = {}
        self._hand_sides = {}
        self._diagnostic_analyzers = {}

        self._get_hand_info()
        self._load_analyzer_params()

    def _get_hand_info(self):
        for hand_serial in self._hand_serials_list:
            general_info_file = rospkg.RosPack().get_path('sr_hand_config') + \
                '/' + str(hand_serial) + '/general_info.yaml'

            with open(general_info_file, encoding="utf-8") as gi_file:
                general_info = yaml.safe_load(gi_file)

            self._hand_types[hand_serial] = general_info['type']
            self._hand_sides[hand_serial] = general_info['side']

    def _load_analyzer_params(self):
        self._get_per_hand_analyzer()
        self._get_common_analyzers()

        rospy.set_param('analyzers', self._diagnostic_analyzers)

    def _get_per_hand_analyzer(self):
        for hand_serial in self._hand_serials_list:
            analyzer_file_path = self._get_analyzer_file(hand_serial)

            with open(analyzer_file_path, encoding="utf-8") as af_file:
                analyzer = yaml.safe_load(af_file)

            self._modify_analyzers_for_correct_index(analyzer, hand_serial)

            self._diagnostic_analyzers[self._hand_sides[hand_serial] + '_shadow_hand_' + str(hand_serial)] = \
                analyzer['analyzers']['shadow_hand']

    def _modify_analyzers_for_correct_index(self, analyzer, hand_serial):
        analyzer['analyzers']['shadow_hand']['path'] = self._hand_sides[hand_serial].capitalize() + ' ' + \
            analyzer['analyzers']['shadow_hand']['path']

        for individual_analyzer, individual_analyzer_vals in analyzer['analyzers']['shadow_hand']['analyzers'].items():
            if isinstance(individual_analyzer_vals['regex'], list):
                new_regex = []
                for element in individual_analyzer_vals['regex']:
                    new_regex.append(element.replace("([^\\s]+)", self._side_to_prefix(self._hand_sides[hand_serial])))
            else:
                new_regex = \
                    individual_analyzer_vals['regex'].replace("([^\\s]+)",
                                                              self._side_to_prefix(self._hand_sides[hand_serial]))

            analyzer['analyzers']['shadow_hand']['analyzers'][individual_analyzer]['regex'] = new_regex

    @staticmethod
    def _side_to_prefix(side):
        if not side in ('right', 'left'):
            raise ValueError("Wrong side provided")
        if side == 'right':
            return 'rh'
        return 'lh'

    def _get_analyzer_file(self, hand_serial):
        if self._hand_types[hand_serial] == 'hand_g':
            analyzer_file_suffix = '_lite'
        elif self._hand_types[hand_serial] == 'hand_extra_lite':
            analyzer_file_suffix = '_extra_lite'
        else:
            analyzer_file_suffix = ''

        return rospkg.RosPack().get_path('sr_hand_config') + \
            '/common/config/diagnostic_analyzer' + analyzer_file_suffix + '.yaml'

    def _get_common_analyzers(self):
        common_analyzers_file_path = rospkg.RosPack().get_path('sr_hand_config') + \
            '/common/config/common_diagnostic_analyzers.yaml'

        with open(common_analyzers_file_path, encoding="utf-8") as ca_file:
            common_analyzers = yaml.safe_load(ca_file)

        for analyzer, params in common_analyzers['analyzers'].items():
            self._diagnostic_analyzers[analyzer] = params


if __name__ == "__main__":
    rospy.init_node('load_diagnostic_analyzer', anonymous=True)

    hand_serials_list = rospy.get_param('~hand_serials_list')

    LoadDiagnosticAnalyzer(hand_serials_list)
