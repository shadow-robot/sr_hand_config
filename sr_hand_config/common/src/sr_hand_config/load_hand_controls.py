#!/usr/bin/env python3

# Copyright 2020, 2022 Shadow Robot Company Ltd.
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

from os import walk
import yaml
import rospy
import rospkg


class LoadHandControls:
    def __init__(self, hand_serials_list, control_mode):
        self._hand_serials_list = hand_serials_list
        self._control_mode = control_mode
        self._load_control_params()

    def _load_control_params(self):
        for hand_serial in self._hand_serials_list:
            # Load files from common folder no matter what the control mode is
            common_files_path = rospkg.RosPack().get_path('sr_hand_config') + \
                '/' + str(hand_serial) + '/controls/host/common'

            control_mode_files_path = rospkg.RosPack().get_path('sr_hand_config') + \
                '/' + str(hand_serial) + '/controls/host/' + self._control_mode

            common_control_files = [common_files_path + '/' + control_file
                                    for control_file in self._get_all_files_in_dir(common_files_path)]
            mode_control_files = [control_mode_files_path + '/' + control_file
                                  for control_file in self._get_all_files_in_dir(control_mode_files_path)]

            for control_file_path in common_control_files + mode_control_files:
                self._load_params_from_file(control_file_path)

    @staticmethod
    def _get_all_files_in_dir(path):
        return next(walk(path), (None, None, []))[2]

    @staticmethod
    def _load_params_from_file(file_path):
        with open(file_path, encoding="utf-8") as param_file:
            config = yaml.safe_load(param_file)
        for param in config:
            rospy.set_param(param, config[param])


if __name__ == "__main__":
    rospy.init_node('load_hand_controls', anonymous=True)

    hand_serials_list_param = rospy.get_param('~hand_serials_list')
    control_mode_param = rospy.get_param('~control_mode', 'pwm')

    LoadHandControls(hand_serials_list_param, control_mode_param)
