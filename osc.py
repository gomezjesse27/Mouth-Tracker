from pythonosc import udp_client
import time
# Create an OSC client
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

multiplier = 3.0 # Amplifies the face movement

# rate limiting
period = 0.2
timer = time.time()
# Define the OSC message address
#address = "/avatar/parameters/foobar/"

# Send the OSC message
#client.send_message(address, None)

def predictions_to_osc(prediction_values):
    # global timer
    # if time.time() - timer < period:
    #     return
    # timer = time.time()
    smile_amount = max(0, min(1, prediction_values[0]))  * multiplier
    open_mouth_amount = max(0, min(1, prediction_values[1])) * multiplier
    puff_amount = max(0, min(1, prediction_values[2])) * multiplier
    frown_amount = max(0, min(1, prediction_values[3])) * multiplier
    left_amount = max(0, min(1, prediction_values[4])) * multiplier
    right_amount = max(0, min(1, prediction_values[5])) * multiplier
    if smile_amount > frown_amount:
        # Make smile_amount a 3 bit number
        smile_amount = int(smile_amount * 7)
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeft1", (smile_amount >> 0 & 1)) # 1st bit of smile_amount
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeft2", (smile_amount >> 1 & 1)) # 2nd bit of smile_amount
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeft4", (smile_amount >> 2 & 1)) # 3rd bit of smile_amount
        client.send_message("/avatar/parameters/FT/v2/SmileSadRight1", (smile_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadRight2", (smile_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadRight4", (smile_amount >> 2 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeftNegative", 0)
        client.send_message("/avatar/parameters/FT/v2/SmileSadRightNegative", 0)
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeft1", (smile_amount >> 0 & 1)) # 1st bit of smile_amount
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeft2", (smile_amount >> 1 & 1)) # 2nd bit of smile_amount
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeft4", (smile_amount >> 2 & 1)) # 3rd bit of smile_amount
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRight1", (smile_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRight2", (smile_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRight4", (smile_amount >> 2 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeftNegative", 0)
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRightNegative", 0)
    else:
        # Make frown_amount a 3 bit number
        frown_amount = int(frown_amount * 7)
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeft1", (frown_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeft2", (frown_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeft4", (frown_amount >> 2 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadRight1", (frown_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadRight2", (frown_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileSadRight4", (frown_amount >> 2 & 1)) 
        client.send_message("/avatar/parameters/FT/v2/SmileSadLeftNegative", 1)
        client.send_message("/avatar/parameters/FT/v2/SmileSadRightNegative", 1)
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeft1", (frown_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeft2", (frown_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeft4", (frown_amount >> 2 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRight1", (frown_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRight2", (frown_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRight4", (frown_amount >> 2 & 1)) 
        client.send_message("/avatar/parameters/FT/v2/SmileFrownLeftNegative", 1)
        client.send_message("/avatar/parameters/FT/v2/SmileFrownRightNegative", 1)
    
    if open_mouth_amount < 0.001:
        open_mouth_amount = 0.001
    print(open_mouth_amount)
    client.send_message("/avatar/parameters/FT/v2/JawOpen", open_mouth_amount)
    
    puff_amount = int(puff_amount * 7)
    client.send_message("/avatar/parameters/FT/v2/CheekPuffSuckLeft1", (puff_amount >> 0 & 1))
    client.send_message("/avatar/parameters/FT/v2/CheekPuffSuckLeft2", (puff_amount >> 1 & 1))
    client.send_message("/avatar/parameters/FT/v2/CheekPuffSuckLeft4", (puff_amount >> 2 & 1))
    client.send_message("/avatar/parameters/FT/v2/CheekPuffSuckRight1", (puff_amount >> 0 & 1))
    client.send_message("/avatar/parameters/FT/v2/CheekPuffSuckRight2", (puff_amount >> 1 & 1))
    client.send_message("/avatar/parameters/FT/v2/CheekPuffSuckRight4", (puff_amount >> 2 & 1))

    if left_amount > right_amount:
        left_amount = int(left_amount * 15)
        client.send_message("/avatar/parameters/FT/v2/MouthX1", (left_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthX2", (left_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthX4", (left_amount >> 2 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthX8", (left_amount >> 3 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthXNegative", 0)
    else:
        right_amount = int(right_amount * 15)
        client.send_message("/avatar/parameters/FT/v2/MouthX1", (right_amount >> 0 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthX2", (right_amount >> 1 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthX4", (right_amount >> 2 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthX8", (right_amount >> 3 & 1))
        client.send_message("/avatar/parameters/FT/v2/MouthXNegative", 1)
    
