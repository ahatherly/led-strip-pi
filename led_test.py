import RPi.GPIO as GPIO
import time, random, sys, os, traceback, signal
from pixel import Pixel

class LEDPatterns():
    DATA = 7
    CLOCK = 11
    BRIGHTNESS = 31
    #DC = 0
    STOP = False

    def sendBit(self,val):
        #global DC
        GPIO.output(self.DATA,val)
        GPIO.output(self.CLOCK,True)
        GPIO.output(self.CLOCK,False)
        #DC=DC+1
        #if val == True:
        #    sys.stdout.write('1')
        #else:
        #    sys.stdout.write('0')
        #if DC%8 == 0:
        #    sys.stdout.write(' ')

    def sendByte(self,val):
        for pos in range(7,-1,-1):
            mask = 2**pos
            bit = (val&mask>0)
            self.sendBit(bit)

    def sendZeros(self):
        for x in range(0,8):
            self.sendBit(False)

    def sendOnes(self):
        for x in range(0,8):
            self.sendBit(True)

    # Send the brightness byte - allows values 0-31
    def sendBrightness(self,val):
        # Three ones
        for x in range(0,3):
            self.sendBit(True)
        # Global brghtness (5 bits)
        for pos in range(4,-1,-1):
            mask = 2**pos
            bit = (val&mask>0)
            self.sendBit(bit)

    def start(self):
        self.sendZeros()
        self.sendZeros()
        self.sendZeros()
        self.sendZeros()

    def end(self):
        self.start()

    def red(self):
        self.sendBrightness(self.BRIGHTNESS)
        self.sendZeros()
        self.sendZeros()
        self.sendOnes()

    def green(self):
        self.sendBrightness(self.BRIGHTNESS)
        self.sendZeros()
        self.sendOnes()
        self.sendZeros()

    def blue(self):
        self.sendBrightness(self.BRIGHTNESS)
        self.sendOnes()
        self.sendZeros()
        self.sendZeros()

    def rgb(self,r,g,b):
        self.sendBrightness(self.BRIGHTNESS)
        self.sendByte(b)
        self.sendByte(g)
        self.sendByte(r)

    def rgbPixel(self,pixel):
        self.sendBrightness(self.BRIGHTNESS)
        self.sendByte(pixel.b)
        self.sendByte(pixel.g)
        self.sendByte(pixel.r)

    def rgbb(self,r,g,b,bright):
        self.sendBrightness(bright)
        self.sendByte(b)
        self.sendByte(g)
        self.sendByte(r)

    def off(self):
        self.sendBrightness(self.BRIGHTNESS)
        self.sendZeros()
        self.sendZeros()
        self.sendZeros()

    def allOff(self):
        self.start()
        for x in range(0,61):
            self.off()
        self.end()

    def funkyColours(self):
        r = 255
        g = 0
        b = 0
        sequence = 1
        led = 60
        while (self.stopped() == False):
            if sequence == 1:
                if g < 255:
                    g = g + 5
                else:
                    sequence = 2
            if sequence == 2:
                if r > 0:
                    r = r - 5
                else:
                    sequence = 3
            if sequence == 3:
                if b < 255:
                    b = b + 5
                else:
                    sequence = 4
            if sequence == 4:
                if g > 0:
                    g = g - 5
                else:
                    sequence = 5
            if sequence == 5:
                if r < 255:
                    r = r + 5
                else:
                    sequence = 6
            if sequence == 6:
                if b > 0:
                    b = b - 5
                else:
                    sequence = 1
            if led > 59:
                led = 0
                time.sleep(0.5)
                self.start()
            self.rgb(r, g, b)
            led = led + 1

    def larsson(self):
        ledPos=0;
        led2Pos=-1;
        led3Pos=-1;
        led4Pos=-1;
        step=1;
        
        while (self.stopped() == False):
            self.start()
            for x in range(0,60):
                if x == ledPos:
                    self.rgb(255,0,0)
                elif x == led2Pos:
                    self.rgb(120,0,0)
                elif x == led3Pos:
                    self.rgb(70,0,0)
                elif x == led4Pos:
                    self.rgb(20,0,0)
                else:
                    self.off()
            self.end()

            led4Pos=led3Pos
            led3Pos=led2Pos
            led2Pos=ledPos
            if step == 1:
                if ledPos == 59:
                    step=-1
            else:
                if ledPos == 0:
                    step=1
            ledPos=ledPos+step
            time.sleep(0.01)

    def randomColours(self):
        while (self.stopped() == False):
            self.start()
            for x in range(0,60):
                self.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.end() # End
            time.sleep(1)    

    def colourFade(self):
        # Initialise pixels
        pixelCount = 60
        pixels = []
        for x in range(0,pixelCount):
            pixels.append(Pixel(255,0,0))
            for loop in range(0,x):
                pixels[x].rotateColour()

        while (self.stopped() == False):
            self.start()
            for x in range(0,pixelCount):
                self.rgbPixel(pixels[x])
                pixels[x].rotateColour()
            self.end()
            time.sleep(0.1)

    def rainbow(self):
        # Initialise pixels
        pixelCount = 60
        pixels = []
        self.start()
        for x in range(0,pixelCount):
            pixels.append(Pixel(255,0,0))
            for loop in range(0,x):
                for r in range (0,4):
                    pixels[x].rotateColour()
            self.rgbPixel(pixels[x])
        self.end()

        while (self.stopped() == False):
            time.sleep(0.5)

    def christmas1(self):
        # Initialise pixels
        pixelCount = 60
        movecount = 0
        movedirection = 1
        pixels = []
        # Red
        for x in range(0,16):
            pixels.append(Pixel(125,0,0))
        for x in range(0,4):
            pixels.append(Pixel(0,0,0))
        # White
        for x in range(0,16):
            pixels.append(Pixel(125,125,125))
        for x in range(0,4):
            pixels.append(Pixel(0,0,0))
        # Green
        for x in range(0,16):
            pixels.append(Pixel(0,125,0))
        for x in range(0,4):
            pixels.append(Pixel(0,0,0))

        while (self.stopped() == False):
            # Display
            self.start()
            for x in range(0,pixelCount):
                self.rgbPixel(pixels[x])
            self.end()

            # Move
            if movedirection == 1:
                lastpixel=pixels[pixelCount-1]
                for x in range(pixelCount-1, 0, -1):
                    pixels[x] = pixels[x-1]
                pixels[0]=lastpixel
            else:
                firstpixel=pixels[0]
                for x in range(0, pixelCount-1):
                    pixels[x] = pixels[x+1]
                pixels[pixelCount-1]=firstpixel

            movecount = movecount + 1
            if movecount%60 == 0:
                if movedirection == 1:
                    movedirection = -1
                else:
                    movedirection = 1
            
            time.sleep(0.05)

    def christmas2(self):
        # Initialise pixels
        pixelCount = 60
        pixels = []
        sequence = 1
        r = 0
        g = 0
        b = 0
        while (self.stopped() == False):
            # Display
            self.start()
            for x in range(0,pixelCount):
                self.rgb(r, g, b)
            self.end()

            # Phase
            if sequence == 1:
                if (r == 125):
                    sequence = 2
                else:
                    r = r + 5;
            elif sequence == 2:
                if (r == 0):
                    sequence = 3
                else:
                    r = r - 5;
            elif sequence == 3:
                if (r == 125):
                    sequence = 4
                else:
                    r = r + 5;
                    g = g + 5;
                    b = b + 5;
            elif sequence == 4:
                if (r == 0):
                    sequence = 5
                else:
                    r = r - 5;
                    g = g - 5;
                    b = b - 5;
            elif sequence == 5:
                if (g == 125):
                    sequence = 6
                else:
                    g = g + 5;
            elif sequence == 6:
                if (g == 0):
                    sequence = 1
                else:
                    g = g - 5;                
            
            time.sleep(0.1)

    def christmas3(self):
        # Initialise pixels
        pixelCount = 60
        pixels = []
        phase = 1
        width = 0
        # Red
        for x in range(0,60):
            pixels.append(Pixel(125,0,0))

        while (self.stopped() == False):
            # Display
            self.start()
            for x in range(0,pixelCount):
                self.rgbPixel(pixels[x])
            self.end()

            if width < 60:
                width = width + 2
            else:
                if phase < 3:
                    phase = phase + 1
                else:
                    phase = 1
                width = 0;

            # Update
            for x in range(30-(int(width/2)),30+(int(width/2))):
                if phase == 1:
                    # White
                    pixels[x].r=128
                    pixels[x].g=128
                    pixels[x].b=128
                elif phase == 2:
                    # Green
                    pixels[x].r=0
                    pixels[x].g=128
                    pixels[x].b=0
                elif phase == 3:
                    # Red
                    pixels[x].r=128
                    pixels[x].g=0
                    pixels[x].b=0

            time.sleep(0.1)

    def christmas4(self):
        # Initialise pixels
        pixelCount = 60
        pixels = []
        for x in range(0,pixelCount):
            pixels.append(Pixel(255,0,0))
            for loop in range(0,x):
                pixels[x].rotateColourRWG()

        while (self.stopped() == False):
            self.start()
            for x in range(0,pixelCount):
                self.rgbPixel(pixels[x])
                pixels[x].rotateColourRWG()
            self.end()
            time.sleep(0.1)

    def birthday1(self, bounce_off_other_blobs):
        # Initialise pixels
        blobs=[]
        blobspeed=[]
        blobdirection=[]
        blobcount=4

        # Place our blobs
        for x in range(0,blobcount):
            blobs.append(float(random.randint(0,59)))
            blobspeed.append(random.random())
            if blobspeed[x] < 0.3:
                blobspeed[x] = blobspeed[x] + 0.3
            if (random.random()>0.5):
                blobdirection.append(1)
            else:
                blobdirection.append(-1)

        while (self.stopped() == False):
            # Draw blobs
            self.start()
            for x in range(0,60):
                on_blob = -1
                near_blob = -1
                for b in range(0,blobcount):
                    if int(round(blobs[b],0)) == x:
                        on_blob = b
                    if x>0:
                        if int(round(blobs[b],0)) == x-1:
                            near_blob = b
                    if x<59:
                        if int(round(blobs[b],0)) == x+1:
                            near_blob = b
                if on_blob == 0:
                    self.rgb(0,255,0)
                elif on_blob == 1:
                    self.rgb(255,0,0)
                elif on_blob == 2:
                    self.rgb(255,255,0)
                elif on_blob == 3:
                    self.rgb(255,0,255)
                elif near_blob == 0:
                    self.rgb(0,128,128)
                elif near_blob == 1:
                    self.rgb(128,0,128)
                elif near_blob == 2:
                    self.rgb(128,128,128)
                elif near_blob == 3:
                    self.rgb(128,0,255)
                else:
                    self.rgb(0,0,255)
            self.end()
            time.sleep(0.01)

            # Move blobs
            for b in range(0,blobcount):
                if blobdirection[b] == 1:
                    blobs[b] = blobs[b] + blobspeed[b]
                    # Bounce off edge
                    if int(round(blobs[b],0)) == 59:
                        blobdirection[b] = -1
                elif blobdirection[b] == -1:
                    blobs[b] = blobs[b] - blobspeed[b]
                    # Bounce off edge
                    if int(round(blobs[b],0)) == 0:
                        blobdirection[b] = 1

            # Bounce off other blobs
            if (bounce_off_other_blobs == True):
                for b in range(0,blobcount):
                    if blobdirection[b] == 1:
                        # Bounce off other blobs
                        for o in range(0,blobcount):
                            if o != b:
                                if blobs[b]<blobs[o] and (blobs[b]+blobspeed[b])>blobs[o]:
                                    blobdirection[b] = -1
                    elif blobdirection[b] == -1:
                        # Bounce off other blobs
                        for o in range(0,blobcount):
                            if o != b:
                                if blobs[b]>blobs[o] and (blobs[b]-blobspeed[b])<blobs[o]:
                                    blobdirection[b] = 1



    def pong_scores(self, score2, score1, point_scorer):
        self.start()
        self.allOff()
        self.end()
        time.sleep(1)
        point_direction = 1
        point_loops = 30-score1
        if point_scorer == 2:
            point_direction = -1
            point_loops = 31-score2
        point_light = 30
        
        for loop in range(0,point_loops):
            self.start()
            for x in range(0,60):
                if x == point_light:
                    self.blue()
                elif x<score2:
                    self.blue()
                elif x>(59-score1):
                    self.blue()
                else:
                    self.off()
            self.end()
            point_light = point_light + point_direction
            time.sleep(0.02)
        time.sleep(1)

    def pong_won(self, winner):
        self.start()
        self.allOff()
        self.end()
        time.sleep(0)

        for loop in range(0,5):
            self.start()
            for x in range(0,60):
                if winner == 1 and x < 30:
                    self.green()
                elif winner == 2 and x > 30:
                    self.green()
                else:
                    self.off()
            self.end()
            time.sleep(1)
            self.start()
            self.allOff()
            self.end()
            time.sleep(1)
        time.sleep(5)

    def pong(self):
        ball = 30
        speed = 1
        direction = 1
        bat_active = 10
        bat_delay = -20
        p1 = bat_delay
        p2 = bat_delay
        speed_increase = 0.05
        winning_score = 10
        score1 = 0
        score2 = 0
        
        while(self.stopped() == False):

            # Draw the board
            self.start()
            # Bat 1
            if (p1 > 0):
                self.rgb(0,255,0)
                self.rgb(0,255,0)
                p1 = p1 - 1
            elif (p1 > bat_delay):
                self.rgb(0,0,0)
                self.rgb(0,0,0)
                p1 = p1 - 1
            else:
                self.rgb(0,10,0)
                self.rgb(0,0,0)
            # Playing area
            for x in range(2,58):
                on_ball = (int(round(ball,0)) == x)
                if on_ball == True:
                    self.rgb(255,0,0)
                else:
                    self.rgb(0,0,0)
            # Bat 2
            if (p2 > 0):
                self.rgb(0,255,0)
                self.rgb(0,255,0)
                p2 = p2 - 1
            elif (p2 > bat_delay):
                self.rgb(0,0,0)
                self.rgb(0,0,0)
                p2 = p2 - 1
            else:
                self.rgb(0,0,0)
                self.rgb(0,10,0)
            self.end()

            # Move the ball
            ball = ball + (speed*direction)

            # Check for bounce
            if int(round(ball,0)) > 57:
                if p2 > 0:
                    direction = -1
                    speed = speed + speed_increase
            if int(round(ball,0)) < 2:
                if p1 > 0:
                    direction = 1
                    speed = speed + speed_increase

            # Check for lost
            if int(round(ball,0)) > 58 and direction == 1:
                self.start()
                for x in range (0,60):
                   self.red()
                self.end()
                time.sleep(2)
                ball = 30
                speed = 1
                direction = -1
                self.pong_scores(score1, score2, 2)
                score1 = score1 + 1
                if score1 == winning_score:
                    self.pong_won(1)
                    score1 = 0
                    score2 = 0
            if int(round(ball,0)) < 1 and direction == -1:
                self.start()
                for x in range (0,60):
                   self.red()
                self.end()
                time.sleep(2)
                ball = 30
                speed = 1
                direction = 1
                self.pong_scores(score1, score2, 1)
                score2 = score2 + 1
                if score2 == winning_score:
                    self.pong_won(2)
                    score1 = 0
                    score2 = 0
            # Check for button presses
            if (p1 == bat_delay):
                if GPIO.input(12) == 1:
                    p1 = bat_active
            if (p2 == bat_delay):
                if GPIO.input(13) == 1:
                    p2 = bat_active

            time.sleep(0.01)

    def allRGB(self, r, g, b):
        self.start()
        for x in range(0,60):
            self.rgb(int(r),int(g),int(b))
        self.end()
        while (self.stopped() == False):
            time.sleep(1)

    def __init__(self):
        # Initialise GPIO
        GPIO.setmode(GPIO.BOARD)

        # Data and Clock on pin 7 and 11 respectively
        GPIO.setup(self.DATA, GPIO.OUT)
        GPIO.setup(self.CLOCK, GPIO.OUT)

        # Unput buttons on pin 12 and 13
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.stop()

    def stop(self):
        self.STOP = True

    def stopped(self):
        return self.STOP

    def cleanup(self):
        self.allOff()
        GPIO.cleanup()
        print("Done")


def main(patterns):

    pattern = "colourfade"
    pattern = "rainbow"
    if len(sys.argv) == 2:
        pattern = sys.argv[1]

    if len(sys.argv) == 4:
        red = sys.argv[1]
        green = sys.argv[2]
        blue = sys.argv[3]
        patterns.allRGB(red, green, blue)
    elif pattern == "funkycolours": 
        patterns.funkyColours()
    elif pattern == "rainbow": 
        patterns.rainbow()
    elif pattern == "larsson":
        patterns.larsson()
    elif pattern == "randomcolours":
        patterns.randomColours()
    elif pattern == "colourfade":
        patterns.colourFade()
    elif pattern == "christmas1":
        patterns.christmas1()
    elif pattern == "christmas2":
        patterns.christmas2()
    elif pattern == "christmas3":
        patterns.christmas3()
    elif pattern == "christmas4":
        patterns.christmas4()
    elif pattern == "birthday1":
        patterns.birthday1(True)
    elif pattern == "pong":
        patterns.pong()
    # OFF
    patterns.cleanup()

    
if __name__ == '__main__':
    patterns = LEDPatterns()
    try:
        main(patterns)
    except KeyboardInterrupt:
        print('Interrupted')
        patterns.cleanup()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except:
        print('Error')
        traceback.print_exc()
        patterns.cleanup()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
