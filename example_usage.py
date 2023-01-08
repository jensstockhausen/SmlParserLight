try:
    # unhexlify for micropython
    from ubinascii import unhexlify
except ImportError:
    # default to python standard
    from binascii import unhexlify

from sml_parser_light import *

# using a string to have it more compact
# first / last line are nonses to show that the parser can extract valid frames.
sample_message = \
    "ff010101" \
    "1b1b1b1b01010101760500b6beae6201620072650000010176010105003cea3a0b0a0141504101055550d272620165003cea3c01630d2" \
    "e00760500b6beaf6201620072650000070177010b0a0141504101055550d2070100620affff72620165003cea3cf10677070100603201" \
    "0101010101044150410177070100600100ff010101010b0a0141504101055550d20177070100010800ff65001c010401621e52ff69000" \
    "0000000449f380177070100020800ff0101621e52ff690000000000002f210177070100100700ff0101621b52005900000000000001cf" \
    "0177070100240700ff0101621b52005900000000000000100177070100380700ff0101621b520059000000000000006401770701004c0" \
    "700ff0101621b520059000000000000015a0177070100200700ff0101622352ff6900000000000009110177070100340700ff01016223" \
    "52ff6900000000000009050177070100480700ff0101622352ff69000000000000090a01770701001f0700ff0101622152fe690000000" \
    "00000000b0177070100330700ff0101622152fe69000000000000003f0177070100470700ff0101622152fe6900000000000000d20177" \
    "070100510701ff0101620852005900000000000000760177070100510702ff0101620852005900000000000000ed0177070100510704f" \
    "f010162085200590000000000000156017707010051070fff010162085200590000000000000140017707010051071aff010162085200" \
    "59000000000000014a01770701000e0700ff0101622c52ff6900000000000001f40177070100000200000101010105313230300177070" \
    "100605a020101010101054336433801010163913300760500b6beb0620162007265000002017101632b3e00001b1b1b1b1a01fdfb" \
    "123432345f"


def get_message_as_bytes():
    byte_array = bytearray.fromhex(sample_message)
    return byte_array

def read_sml_message():

    # OBIS entries to be parsed
    obis = [
        "0100010800ff",
        "0100020800ff",
        "0100100700ff",
        "0100240700ff",
        "0100380700ff",
        "0100480700ff",
        "010048ffffff", # not part of sample message
    ]

    sml_stream_reader = SmlStreamReader()

    # simulate the input form the UART
    byte_array = get_message_as_bytes()

    # feed byte into stream ready as chuncks of 10 bytes
    for read_pos in range(0, len(byte_array), 10):

        # add bytes to reader, this sould be the output form the UART
        sml_stream_reader.add(byte_array[read_pos:read_pos+10])
        sml_frame = sml_stream_reader.get_frame()

        # full frame was read and parsing can start
        if sml_frame is not None:

            # now extract the entries
            for o in obis:

                entry = sml_get_entry(sml_frame, obis=unhexlify(o))

                # entry was found
                if entry != None:
                    print("{}".format(entry))
                    print("-> {}[{}]".format(entry.sensor_value(), entry.sensor_unit()))
                else:
                    print("ERROR: {} not found".format(o))


if __name__ == '__main__':
    read_sml_message()