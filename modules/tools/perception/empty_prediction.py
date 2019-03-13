"""
this module creates a node and fake prediction data based
on json configurations
"""
import argparse
import math
import time

import numpy
import simplejson
from cyber_py import cyber
from std_msgs.msg import String

from modules.prediction.proto.prediction_obstacle_pb2 import PredictionObstacle
from modules.prediction.proto.prediction_obstacle_pb2 import PredictionObstacles


def prediction_publisher(prediction_topic, rate):
    """publisher"""
    cyber.init()
    node = cyber.Node("prediction")
    writer = node.create_writer(prediction_topic, String)
    sleep_time = 1.0 / rate
    seq_num = 1
    while not rospy.is_shutdown():
        prediction = PredictionObstacles()
        prediction.header.sequence_num = seq_num
        prediction.header.timestamp_sec = rospy.Time.now().to_sec()
        prediction.header.module_name = "prediction"
        print str(prediction)
        s = String()
        s.data = prediction.SerializeToString()
        #pub.publish(s)
        writer.write(s)
        seq_num += 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="create empty prediction message",
            prog="replay_prediction.py")
    parser.add_argument("-t", "--topic", action="store", type=str, default="/pnc/prediction",
            help="set the prediction topic")
    parser.add_argument("-r", "--rate", action="store", type=int, default=10,
            help="set the prediction topic publish time duration")
    args = parser.parse_args()
    prediction_publisher(args.topic, args.rate)
