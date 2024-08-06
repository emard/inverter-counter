#!/usr/bin/env python3
import serial, argparse

# Mitsubishi E800 MODBUS protocol example

# P.117 = 17   # device address
# P.118 = 192  # 19200 baud
# P.119 = 1    # 2 stop bits
# P.120 = 2    # even parity
# P.122 = 0    # don't check PU connection
# P.549 = 1    # MODBUS protocol

# TO APPLY PARAMETERS
# TURN INVERTER OFF/ON

# usage

# read parameters
# ./e800p.py -d17 4 -n3
# P.4=6000
# P.5=3000
# P.6=1000

# write parameters
# ./e800p.py -d17 4=6000,3000,1000

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

  regstr = args.reg.split("=")
  reg = int(regstr[0])
  if reg < 1000:
    regmodbus = reg + 41000
  else:
    regmodbus = reg + 44000
  val = []
  if len(regstr) == 2:
    valstr = regstr[1].split(",")
    val = [int(i) for i in valstr]
  if args.verbose != None:
    print("P.", reg, "=", val)

    # page 176
    # write single register
    # p = packet_write_reg(0x05, 40014, 6000)

  if args.verbose:
    print("for this request:")
    print("11 03 03 EB 00 03 77 2B")
    print("expected response is:")
    print("11 03 06 17 70 0B B8 03 E8 2C E6")
    print("")

  # p = packet_read_regs(0, 41004, 3)
  # p = packet_write_reg(0, 40014, 6000)

  if args.verbose != None:
    print(port, baud, bytesize, parity, stopbits, timeout)
  rs485 = serial.Serial(
    port=port,
    baudrate=baud,
    bytesize=bytesize,
    parity=parity,
    stopbits=stopbits,
    timeout=timeout)

  if(len(val)):
    request = packet_write_regs(device, regmodbus, val)
    if args.verbose != None:
      print("writing regs")
      print_hex(request)
    rs485.write(request)
    response = rs485.read(8)
    if args.verbose != None:
      print_hex(response)
  else:
    request = packet_read_regs(device, regmodbus, number)
    if args.verbose != None:
      print("reading regs")
      print_hex(request)
    rs485.write(request)
    response = rs485.read(5+2*number)
    if args.verbose != None:
      print_hex(response)
    for i in range(number):
      print("P.%d=%d" % (i+reg,response[3+2*i]*256+response[4+2*i]))

  #rs485.write(packet_write_reg(17,41004,6000))
  #response = rs485.read(8)
  #print_hex(response)
  #rs485.write(packet_write_reg(17,41005,3000))
  #response = rs485.read(8)
  #print_hex(response)
  #rs485.write(packet_write_reg(17,41006,1000))
  #response = rs485.read(8)
  #print_hex(response)
  
# main
parser = argparse.ArgumentParser(
       prog="E800 MODBUS Parameters",
       description="RS485 half or full duplex",
       epilog="P.117=17 P.118=192 P.119=1 P.120=2 P.122=0 P.549=1")

parser.add_argument("-p", "--port")               # serial port /dev/ttyUSB0 default
parser.add_argument("-b", "--baud")               # [bps] 19200
parser.add_argument('-c', '--comm')               # 8E2 8N1 7N2 etc serial line signaling
parser.add_argument("-t", "--timeout")            # [s] 0.5
parser.add_argument('-d', '--device')             # 1-31
parser.add_argument('-n', '--number')             # 1-30 number of registers to read
parser.add_argument('-v', '--verbose')            # print protocol in hex
parser.add_argument("reg")                        # positional argument

args = parser.parse_args()

port = "/dev/ttyUSB0"
if args.port != None:
  port = args.port

baud = 19200
if args.baud != None:
  baud = args.baud

bytesize = serial.EIGHTBITS
parity   = serial.PARITY_EVEN
stopbits = serial.STOPBITS_TWO
if args.comm != None:
  comm = args.comm.replace(",","").upper()
  if comm[0] == "8":
    bytesize = serial.EIGHTBITS
  if comm[0] == "7":
    bytesize = serial.SEVENBITS
  if comm[1] == "N":
    parity = serial.PARITY_NONE
  if comm[1] == "E":
    parity = serial.PARITY_EVEN
  if comm[1] == "O":
    parity = serial.PARITY_ODD
  if comm[2] == "1":
    stopbits = serial.STOPBITS_ONE
  if comm[2] == "2":
    stopbits = serial.STOPBITS_TWO

timeout = 0.5
if args.timeout != None:
  timeout = float(args.timeout)

device = 0
if args.device != None:
  device = int(args.device)

number = 1
if args.number != None:
  number = int(args.number)

if args.verbose != None:
  print(args)

run()
