#!/usr/bin/env python3
import os, serial, time, argparse

# Mitsubishi E800 MODBUS protocol example

# P.117 = 17   # device address
# P.118 = 192  # 19200 baud
# P.119 = 1    # 2 stop bits
# P.120 = 2    # even parity
# P.122 = 0    # don't check PU connection
# P.549 = 1    # MODBUS protocol

# TO APPLY PARAMETERS
# TURN INVERTER OFF/ON

starting_reg = 40001

# P.4 is 41004
# P.6 is 41006
# etc.

# check crc16
# print(19255, crc16(b'\x31\x32\x33\x34\x35\x36\x37\x38\x39'))

def crc16(data):
  '''
  CRC-16 Modbus
  '''
  poly= 0xA001
  crc = 0xFFFF
  for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 1):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)
  return crc

# read multiple (n) regs starting from reg
def packet_read_regs(addr, reg, n):
  r = reg-starting_reg
  packet = bytearray()
  packet.append(addr)
  packet.append(0x03)
  packet.append(r >> 8)
  packet.append(r & 0xFF)
  packet.append(n >> 8)
  packet.append(n & 0xFF)
  crc = crc16(packet)
  packet.append(crc & 0xFF)
  packet.append(crc >> 8)
  return packet

# write single reg
def packet_write_reg(addr, reg, value):
  r = reg-starting_reg
  packet = bytearray()
  packet.append(addr)
  packet.append(0x06)
  packet.append(r >> 8)
  packet.append(r & 0xFF)
  packet.append(value >> 8)
  packet.append(value & 0xFF)
  crc = crc16(packet)
  packet.append(crc & 0xFF)
  packet.append(crc >> 8)
  return packet

# write multiple regs (max 125)
def packet_write_regs(addr, reg, values):
  r = reg-starting_reg
  packet = bytearray()
  packet.append(addr)
  packet.append(0x10)
  packet.append(r >> 8)
  packet.append(r & 0xFF)
  n = len(values)
  packet.append(n >> 8)
  packet.append(n & 0xFF)
  packet.append(2*n)
  for value in values:
    packet.append(value >> 8)
    packet.append(value & 0xFF)
  crc = crc16(packet)
  packet.append(crc & 0xFF)
  packet.append(crc >> 8)
  return packet
  
def print_hex(p):
  print(' '.join(format(x, '02X') for x in p))

def run():

    # page 176
    # write single register
    # p = packet_write_reg(0x05, 40014, 6000)

  print("for this request:")
  print("11 03 03 EB 00 03 77 2B")
  print("expected response is:")
  print("11 03 06 17 70 0B B8 03 E8 2C E6")
  print("")

  # p = packet_read_regs(0, 41004, 3)
  # p = packet_write_reg(0, 40014, 6000)

  rs485 = serial.Serial(
    # port='/dev/ttyUSB.RS485',
    port='/dev/ttyUSB0',
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_TWO,
    timeout=0.5)

  print("writing regs")

  request = packet_write_regs(17,41004,(6000,3000,1000))
  print_hex(request)
  rs485.write(request)
  response = rs485.read(8)
  print_hex(response)

  #rs485.write(packet_write_reg(17,41004,6000))
  #response = rs485.read(8)
  #print_hex(response)
  #rs485.write(packet_write_reg(17,41005,3000))
  #response = rs485.read(8)
  #print_hex(response)
  #rs485.write(packet_write_reg(17,41006,1000))
  #response = rs485.read(8)
  #print_hex(response)
  
  print("reading regs")

  # https://www.lcautomation.com/wb_documents/Mitsubishi/Mitsubishi%20E800%20Manual%20-%20Comms.pdf
  # page 175
  # Example) Read the register values of 41004 (Pr.4) to 41006 (Pr.6) from slave address 17 (H11).
  request = packet_read_regs(17, 41004, 3)
  print_hex(request)
  rs485.write(request)
  response = rs485.read(11)
  print_hex(response)


# main
parser = argparse.ArgumentParser(
       prog="E800 MODBUS Parameters",
       description="RS485 half or full duplex",
       epilog="P.117=17 P.118=192 P.119=1 P.120=2 P.122=0 P.549=1")

parser.add_argument("-p", "--port")               # serial port /dev/ttyUSB0 default
parser.add_argument("-b", "--baud")               # [bps] 19200
# parser.add_argument('-s', '--bits-parity-stop') # 8E2 8N1 7N2 etc serial line signaling
parser.add_argument("reg")                        # positional argument

args = parser.parse_args()
print(
  args.port,
  args.baud,
  args.reg,
)

port = "/dev/ttyUSB0"
if args.port != None:
  port = args.port

baud = 19200
if args.baud != None:
  baud = args.baud

print(
  port,
  baud,
  args.reg
)

run()
