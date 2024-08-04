#!/usr/bin/env python3
import os, serial, time

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

def packet_read_regs(addr, reg, bytes):
  r = reg-starting_reg
  packet = bytearray()
  packet.append(addr)
  packet.append(0x03)
  packet.append(r >> 8)
  packet.append(r & 0xFF)
  packet.append(bytes >> 8)
  packet.append(bytes & 0xFF)
  crc = crc16(packet)
  packet.append(crc & 0xFF)
  packet.append(crc >> 8)
  return packet

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
  
def print_hex(p):
  print(' '.join(format(x, '02X') for x in p))

def run():
    # https://www.lcautomation.com/wb_documents/Mitsubishi/Mitsubishi%20E800%20Manual%20-%20Comms.pdf
    # page 175
    # Example) Read the register values of 41004 (Pr.4) to 41006 (Pr.6) from slave address 17 (H11).
    request = packet_read_regs(17, 41004, 3)

    # page 176
    # write single register
    # p = packet_write_reg(0x05, 40014, 6000)

    print("for this request:")
    print("11 03 03 EB 00 03 77 2B")
    print("expected response is:")
    print("11 03 06 17 70 13 88 0F")
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
    rs485.write(packet_write_reg(17,41004,0x1770))
    response = rs485.read(8)
    print_hex(response)
    rs485.write(packet_write_reg(17,41005,0x0BB8))
    response = rs485.read(8)
    print_hex(response)
    rs485.write(packet_write_reg(17,41006,0x03E8))
    response = rs485.read(8)
    print_hex(response)
    
    print("reading regs")

    print_hex(request)
    rs485.write(request)
    response = rs485.read(11)
    print_hex(response)

run()
