
try:
    # hexlify for micropython
    from ubinascii import hexlify
except ImportError:
    # default to python standard
    from binascii import hexlify

import struct

SmlUnits = {
    1: 'a',
    2: 'mo',
    3: 'wk',
    4: 'd',
    5: 'h',
    6: 'min',
    7: 's',
    8: '°',
    9: '°C',
    10: 'currency',
    11: 'm',
    12: 'm/s',
    13: 'm³',
    14: 'm³',
    15: 'm³/h',
    16: 'm³/h',
    17: 'm³/d',
    18: 'm³/d',
    19: 'l',
    20: 'kg',
    21: 'N',
    22: 'Nm',
    23: 'Pa',
    24: 'bar',
    25: 'J',
    26: 'J/h',
    27: 'W',
    28: 'VA',
    29: 'var',
    30: 'Wh',
    31: 'VAh',
    32: 'varh',
    33: 'A',
    34: 'C',
    35: 'V',
    36: 'V/m',
    37: 'F',
    38: 'Ω',
    39: 'Ωm²/m',
    40: 'Wb',
    41: 'T',
    42: 'A/m',
    43: 'H',
    44: 'Hz',
    45: '1/(Wh)',
    46: '1/(varh)',
    47: '1/(VAh)',
    48: 'V²h',
    49: 'A²h',
    50: 'kg/s',
    51: 'S',
    52: 'K',
    53: '1/(V²h)',
    54: '1/(A²h)',
    55: '1/m³',
    56: '%',
    57: 'Ah',
    60: 'Wh/m³',
    61: 'J/m³',
    62: 'Mol%',
    63: 'g/m³',
    64: 'Pas',
    65: 'J/kg',
    66: 'g/cm²',
    67: 'arm',
    70: 'dBm',
    71: 'dBµV',
    72: 'dB',
}


# https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm
# adjust for translations
OBIS_NAMES = {
    '0100000009ff': 'Geräteeinzelidentifikation',
    '0100010800ff': 'Zählerstand Total',
    '0100010801ff': 'Zählerstand Tarif 1',
    '0100010802ff': 'Zählerstand Tarif 2',
    '0100011100ff': 'Total-Zählerstand',
    '0100020800ff': 'Wirkenergie Total',
    '0100100700ff': 'aktuelle Wirkleistung',
    '0100170700ff': 'Momentanblindleistung L1',
    '01001f0700ff': 'Strom L1',
    '0100200700ff': 'Spannung L1',
    '0100240700ff': 'Wirkleistung L1',
    '01002b0700ff': 'Momentanblindleistung L2',
    '0100330700ff': 'Strom L2',
    '0100340700ff': 'Spannung L2',
    '0100380700ff': 'Wirkleistung L2',
    '01003f0700ff': 'Momentanblindleistung L3',
    '0100470700ff': 'Strom L3',
    '0100480700ff': 'Spannung L3',
    '01004c0700ff': 'Wirkleistung L3',
    '0100510701ff': 'Phasenabweichung Spannungen L1/L2',
    '0100510702ff': 'Phasenabweichung Spannungen L1/L3',
    '0100510704ff': 'Phasenabweichung Strom/Spannung L1',
    '010051070fff': 'Phasenabweichung Strom/Spannung L2',
    '010051071aff': 'Phasenabweichung Strom/Spannung L3',
    '010060320002': 'Aktuelle Chiptemperatur',
    '010060320003': 'Minimale Chiptemperatur',
    '010060320004': 'Maximale Chiptemperatur',
    '010060320005': 'Gemittelte Chiptemperatur',
    '010060320303': 'Spannungsminimum',
    '010060320304': 'Spannungsmaximum',
    '01000e0700ff': 'Netz Frequenz',
    '8181c78203ff': 'Hersteller-Identifikation',
    '8181c78205ff': 'Öffentlicher Schlüssel',
}


CRC16_X25_TABLE = (
    0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
    0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
    0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
    0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
    0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
    0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
    0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
    0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
    0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
    0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
    0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
    0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
    0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
    0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
    0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
    0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
    0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
    0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
    0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
    0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
    0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
    0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
    0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
    0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
    0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
    0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
    0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
    0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
    0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
    0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
    0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
    0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78
)

def get_crc(buf):
    crc = 0xffff
    for byte in buf:
        crc = CRC16_X25_TABLE[(byte ^ crc) & 0xff] ^ (crc >> 8 & 0xff)
    crc ^= 0xffff
    return (crc & 0xFF) << 8 | crc >> 8


class SmlStreamReader:
    MAX_SIZE = 50 * 1024

    def __init__(self):
        self.bytes = b''

    def add(self, _bytes):
        self.bytes += _bytes
        if len(self.bytes) > SmlStreamReader.MAX_SIZE:
            self.bytes = self.bytes[-1 * SmlStreamReader.MAX_SIZE:]

    def clear(self):
        self.bytes = b''

    def get_frame(self):
        start = self.bytes.find(b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01')
        if start == -1:
            return None

        # if we start reading in the mid of a message
        if start != 0:
            self.bytes = self.bytes[start:]
            start = 0

        end = -1
        while (end := self.bytes.find(b'\x1B\x1B\x1B\x1B\x1A', end + 1)) != -1:
            pre = self.bytes[end - 4: end]
            if pre != b'\x1B\x1B\x1B\x1B':
                break

        if end == -1:
            return None

        end += 8
        if len(self.bytes) < end:
            return None

        # remove msg from buffer
        msg = self.bytes[start:end]
        self.bytes = self.bytes[end:]

        # Last three bytes are PADDING, CRC PART 1, CRC PART 2
        padding = msg[-3]

        # check crc
        crc_msg = msg[-2] << 8 | msg[-1]
        crc_calc = get_crc(msg[:-2])
        if crc_msg != crc_calc:
            print("CRC error")
            return None

        frame = msg
        return frame


class SmlField():

    def __init__(self, date_type_name, value, bin_value):
        self.date_type_name = date_type_name
        self.value = value
        self.hex_value = bin_value

class SmlEntry():

    def __init__(self, obis, status, val_time, unit, scaler, base_value, value_signature):
        self.obis = obis
        self.status = status
        self.val_time = val_time
        self.unit = SmlUnits[unit.value] if 0 < unit.value < 73 else ""
        self.scaler = scaler
        self.base_value = base_value
        self.value_signature = value_signature

    def sensor_value(self):
        if self.base_value.date_type_name != "string":
            return float(self.base_value.value)*10**float(self.scaler.value)
        else:
            return self.base_value.value

    def sensor_unit(self):
        return self.unit

    def __str__(self):

        str = "{} ({})  ".format(self.obis, OBIS_NAMES.get(self.obis))

        if self.base_value.date_type_name != "string":
            str += "{}*10^{}: {}[{}]".format(self.base_value.value, self.scaler.value,
                                             self.sensor_value(), self.sensor_unit())
        else:
            str += "{}".format(self.base_value.value)
        return str



def sml_parse_fields_from_position(message, position):

    fields = []
    while len(fields) != 6:

        value = 0
        date_type_name = 'none'

        data_type = message[position] & 0x70
        length = message[position] & 0x0F

        bin_value = message[position + 1:position + length]

        # skip the 0x01
        if message[position] == 0x01:
            date_type_name = "oct"
            bin_value = 0x01
            value = 0

        # unpacking signed and unsigned
        # SML supports widths with 1,2,4,8 bit

        elif data_type == 0x50:
            date_type_name = "signed"
            if len(bin_value) == 1:
                value =  struct.unpack('>b', bin_value)[0]
            elif len(bin_value) == 2:
                value =  struct.unpack('>h', bin_value)[0]
            elif len(bin_value) == 4:
                value =  struct.unpack('>i', bin_value)[0]
            elif len(bin_value) == 8:
                value =  struct.unpack('>q', bin_value)[0]
            else:
                value = 0

        elif data_type == 0x60:
            date_type_name = "unsigned"
            if len(bin_value) == 1:
                value =  struct.unpack('>B', bin_value)[0]
            elif len(bin_value) == 2:
                value =  struct.unpack('>H', bin_value)[0]
            elif len(bin_value) == 4:
                value =  struct.unpack('>I', bin_value)[0]
            elif len(bin_value) == 8:
                value =  struct.unpack('>Q', bin_value)[0]
            else:
                value = 0

        # try to convert byte lists to strings
        elif data_type == 0x00:
            date_type_name = "string"
            try:
                value = bin_value.decode('ascii')
            except Exception:
                value = hexlify(bin_value).decode('ascii')

        position = position + length
        fields.append(SmlField(date_type_name=date_type_name, value=value, bin_value=bin_value))

    return fields


def sml_get_entry(frame, obis):

    pos = frame.find(obis)

    if pos == -1:
        return None

    pos = pos + len(obis)

    # enable to debug the parsing of the entry
    #print("obis {}".format(hexlify(obis).decode('ascii')))
    #print("{}".format(hexlify(message[pos-len(obis):pos+40]).decode('ascii')))
    #print('^^'*len(obis))

    fields = sml_parse_fields_from_position(frame, pos)

    sml_entry = SmlEntry(obis=hexlify(obis).decode('ascii'),
                         status=fields[0], val_time=fields[1],
                         unit=fields[2], scaler=fields[3], base_value=fields[4],
                         value_signature=fields[5])

    return sml_entry


