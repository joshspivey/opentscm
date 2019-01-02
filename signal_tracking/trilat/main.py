from math import radians, degrees, pi, asin, sin, cos, atan2
import gps #works with device BU-353s4
import threading
import SoapySDR
import numpy

class Trilat(object):
    def __init__(self):
        self.listeners = []
        self.device = gps.Device()
        self.asyncThread(self.device.run)

        #enumerate devices
        results = SoapySDR.Device.enumerate()
        for result in results: print(result)
        
        #create device instance
        args = dict(driver="hackrf")
        self.sdr = SoapySDR.Device(args)

        #query device info
        print(self.sdr.listAntennas(SoapySDR.SOAPY_SDR_RX, 0))
        print(self.sdr.listGains(SoapySDR.SOAPY_SDR_RX, 0))
        freqs = self.sdr.getFrequencyRange(SoapySDR.SOAPY_SDR_RX, 0)
        for freqRange in freqs: print(freqRange)

        #apply settings
        self.sdr.setSampleRate(SoapySDR.SOAPY_SDR_RX, 0, 1e6)
        self.sdr.setFrequency(SoapySDR.SOAPY_SDR_RX, 0, 912.3e6)

        #setup a stream
        rxStream = self.sdr.setupStream(SoapySDR.SOAPY_SDR_RX, SoapySDR.SOAPY_SDR_CF32)
        self.sdr.activateStream(rxStream)

        #create a re-usable buffer for rx samples
        buff = numpy.array([0]*1024, numpy.complex64)

        for i in range(10):
            sr = self.sdr.readStream(rxStream, [buff], len(buff))
            print(sr.ret)
            print(sr.flags)
            print(sr.timeNs)
            print(sr)


    def get_lat_lng(self):        
        record = self.device.record
        valid = record and record.valid
        lat = record.latitude if valid else 0
        lng = record.longitude if valid else 0
        return (lat, lng)
    def get_position(self):
        lat, lng = self.get_lat_lng()
        return (lat, lng)
    def asyncThread(self, func, *args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
    def update(self):
        #put hack rf data here to be returned to DB
        return self.get_lat_lng()

tril = Trilat()  

print tril.get_position()

#add all data to mongo once sdr is complete
# while True:
    # print tril.update()
