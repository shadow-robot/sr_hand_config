#!/usr/bin/env python3

# Copyright 2020 Shadow Robot Company Ltd.
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

class LoadHandControls(object):
    def __init__(self, hand_serials_list):
        self._hand_serials_list = hand_serials_list
        self._load_control_params()

    def _load_control_params(self):
        for hand_serial in self._hand_serials_list:
            files_path = rospkg.RosPack().get_path('sr_hand_config') + '/' + str(hand_serial) + '/controls'
            control_files = self._get_all_files_in_dir(files_path)

            for control_file in control_files:
                with open(files_path + '/' + control_file) as f:
                    config = yaml.safe_load(f)
                for param in config:
                    rospy.set_param(param, config[param])

    def _get_all_files_in_dir(self, path):
        return next(walk(path), (None, None, []))[2]

if __name__ == "__main__":
    rospy.init_node('load_hand_controls', anonymous=True)
    hand_serials_list = rospy.get_param("~hand_serials_list")
    LoadHandControls(hand_serials_list)
