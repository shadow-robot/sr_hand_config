# sr_hand_config

Package containing configurations necessary for running Shadow Hands.

## general_info.yaml

File containing general description of the hand's configuration. Fields:
- side - defines the side of the hand. Allowed options: right/left
- type - defines the type of the hand. Allowed optins: hand_e/hand_g/hand_c.
- version - defines version for particular type of hand. Allowed options: E3M5/E2M3 (for hand_e) G1M5 (for hand_g) C6M2 (for hand_c)
- sensors - defines how sensors are located on the hand. Allows placement of sensors on tip, mid and proximal parts of the fingers as well as the palm. Allowed sensor types: pst/bt_sp/bt_2p
- mapping_path - defines the path to the hand's mapping yaml file

## sensor_data_polling.yaml

File containing the desired update rates for each data type available on different sensors. Different sensors can be defined, but only one sensor type (at most) can be installed on the hand.
For each sensor data type you can specify:
- any positive number, defining the respective frequency of polling in Hz.
- -1, defining "poll as frequently as possible". If there's only one type of data, and it is configured like this, polling will occur at 1Khz. If 2 types of data are configured like this, polling occurs at 500Hz, and so on. However, if other data types are configures with positve values, data types defined as "-1" will be polled between gaps when no other data types are being pollled.
- -2, defining that this type of data is only polled once at initialization.

The later is used when defining the data types related to `generic_sensor_data_update_rate`, which need to be set for all hands expected to have distal tactile sensors installed:
```
generic_sensor_data_update_rate: {
  TACTILE_SENSOR_TYPE_SAMPLE_FREQUENCY_HZ: -2.,
  TACTILE_SENSOR_TYPE_MANUFACTURER: -2.,
  TACTILE_SENSOR_TYPE_SERIAL_NUMBER: -2.,
  TACTILE_SENSOR_TYPE_SOFTWARE_VERSION: -2.,
  TACTILE_SENSOR_TYPE_PCB_VERSION: -2.,
  TACTILE_SENSOR_TYPE_WHICH_SENSORS: -2.
}
```


