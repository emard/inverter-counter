#!/usr/bin/env python3
import os, serial, time

# Mitsubishi E800 inverter protocol example

# P.117 = 1    # device address
# P.118 = 192  # 19200 baud
# P.119 = 1    # 2 stop bits
# P.120 = 2    # even parity
# P.121 = 1    # retry count
# P.122 = 0    # don't check PU connection
# P.123 = 9999 # [ms] waiting time
# P.124 = 1    # with CR
# P.549 = 0    # Mitsubishi inverter protocol

# TO APPLY PARAMETERS
# TURN INVERTER OFF/ON

def checksum(data):
  '''
  Simple 8-bit checksum
  '''
  sum = 0
  for b in data:
    sum += b
  return sum & 0xFF

def packet_read_regs(addr):
  adrstr = b"%02X" % addr
  payload = adrstr + b"FF001"
  sum = b"%02X" % checksum(payload)
  # \x05 is ENQ (Enquiry) 
  packet = bytearray(b"\x05" + payload + sum + b"\r")
  return packet

def print_hex(p):
  print(' '.join(format(x, '02X') for x in p))

def run():
    # https://www.lcautomation.com/wb_documents/Mitsubishi/Mitsubishi%20E800%20Manual%20-%20Comms.pdf
    # page 169

    print("for this request:")
    print("05 30 31 46 46 30 30 31 37 45 0D")
    print("expected response is:")
    print("06 30 31 0D")
    print("")

    request = packet_read_regs(1)

    rs485 = serial.Serial(
      # port='/dev/ttyUSB.RS485',
      port='/dev/ttyUSB0',
      baudrate=19200,
      bytesize=serial.EIGHTBITS,
      parity=serial.PARITY_EVEN,
      stopbits=serial.STOPBITS_TWO,
      timeout=0.5)

    print_hex(request)
    rs485.write(request)
    response = rs485.read(4)
    print_hex(response)

run()
