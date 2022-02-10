# sr_hand_config

Package containing configurations necessary for running Shadow Hands

## general_info.yaml

File containing general description of the hand's configuration. Fields:
- side - defines the side of the hand. Allowed options: right/left
- type - defines the type of the hand. Allowed optins: hand_e/hand_g/hand_c.
- version - defines version for particular type of hand. Allowed options: E3M5/E2M3 (for hand_e) G1M5 (for hand_g) C6M2 (for hand_c)
- sensors - defines how sensors are located on the hand. Allows placement of sensors on tip, mid and proximal parts of the fingers as well as the palm. Allowed sensor types: pst/bt_sp/bt_2p
- mapping_path - defines the path to the hand's mapping yaml file