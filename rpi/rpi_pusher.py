#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/07
#

import pusher

# Pusher constants
temperature_monitoring_channel = 'temp-channel'

# Pusher app configuration
pusher_client = pusher.Pusher(
  app_id='573623',
  key='9c3b69d78c3088e46d6c',
  secret='5dd54a2e543746465100',
  cluster='us2',
  ssl=True
)


# New temperature measure to push on the temp monitoring channel
def temperature_measure_trigger(sensor_id, sensor_name, temperature):
    pusher_client.trigger(temperature_monitoring_channel, sensor_id, {'message': temperature})


# For testing purposes (sensor1_id)
def main():
    pusher_client.trigger('temp-channel', '28-0217c038c3ff', {'message': "ALLO", 'name': "senseur 12039"})


if __name__ == "__main__":
    main()
