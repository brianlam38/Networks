#!/usr/bin/python3

# REQUIRED STATISTICS FORMAT:
#   total number of virtual circuit requests: 200
#   total number of packets: 4589
#   number of successfully routed packets: 2000
#   percentage of successfully routed packets: 43.58
#   number of blocked packets: 2589
#   percentage of blocked packets: 56.42
#   average number of hops per circuit: 5.42
#   average cumulative propagation delay per circuit: 120.54

# CHECKLIST FOR PLACING STATS UPDATES:
"""
STATISTIC 		 STATUS   INCREMENT LOCATION
----------------------------------------------------------
total_requests   = YES  : routing_performance.start_requests()
total_pkts       = YES  : routing_performance.start_requests()
pkt_success_num  = YES  : routing_performance.start_requests()
pkt_success_rate = N/A  : [ calculated from existing stats ]
pkt_blocked_num  = YES  : routing_performance.start_requests()
pkt_blocked_rate = N/A  : [ calculated from existing stats ]
circuit_success  = YES  : routing_performance.start_requests()
total_hops       = YES  : routing_performance.start_requests()
total_delay      = YES  : routing_performance.start_requests()
ave_hops         = N/A  : [ calculated from existing stats ]
ave_delay        = N/A  : [ calculated from existing stats ]
"""


class StatisticsManager:
    def __init__(self, network_scheme, packet_rate):
        self.total_requests = 0  # total VC requests
        # total pkts in VC = pkts per sec * request duration
        self.total_pkts = 0

        self.pkt_success_num = 0  # success pkts = total - blocked
        self.pkt_success_rate = 0  # success rate = total - blocked / total

        self.pkt_blocked_num = 0  # blocked pkts
        self.pkt_blocked_rate = 0  # blocked rate = blocked / total

        self.circuit_success = 0  # success circuits
        self.total_hops = 0  # cumulative hops (successful)
        self.total_delay = 0  # cumulative prop delay (successful)
        # average hops = total hops / success circuits
        self.ave_hops = 0
        # average delay = total prop delay / success circuits
        self.ave_delay = 0

        self.network_scheme = network_scheme
        self.packet_rate = packet_rate

    # main stats update method
    def update_stats(self, key, increment):
        # update VC request
        if key == "request":
            self.total_requests += increment
        # update total packets
        if key == "packets":
            self.total_pkts += increment
        # update success and rate
        if key == "pkt_success":
            self.pkt_success_num += increment
        # update blocked and rate
        if key == "pkt_blocked":
            self.pkt_blocked_num += increment
        # update circuit success
        if key == "circuit_success":
            self.circuit_success += increment
        # update hops + average hops
        if key == "hops":
            self.total_hops += increment
            self.ave_hops = self.total_hops / self.circuit_success
        # update total propagation delay
        if key == "delays":
            self.total_delay += increment
            self.ave_delay = self.total_delay / self.circuit_success

    # output statistics to terminal
    def print_statistics(self):
        # final success % calculations
        self.pkt_success_rate = self.pkt_success_num / self.total_pkts
        self.pkt_success_rate = self.pkt_success_rate * 100
        # final blocked % calculations
        self.pkt_blocked_rate = self.pkt_blocked_num / self.total_pkts
        self.pkt_blocked_rate = self.pkt_blocked_rate * 100
        # print output
        print("total number of virtual circuit requests: {}".format(
            self.total_requests))
        print("total number of packets: {}".format(self.total_pkts))
        print("number of successfully routed packets: {}".format(
            self.pkt_success_num))
        print("percentage of successfully routed packets: {0:.2f}".format(
            self.pkt_success_rate))
        print("number of blocked packets: {}".format(self.pkt_blocked_num))
        print("percentage of blocked packets: {0:.2f}".format(
            self.pkt_blocked_rate))
        print("average number of hops per circuit: {0:.2f}".format(
            self.ave_hops))
        print("average cumulative propagation delay per circuit: {0:.2f}".
              format(self.ave_delay))
