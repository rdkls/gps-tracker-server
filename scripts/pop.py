#!/usr/bin/env python
from models import *
u, created = User.objects.get_or_create(email='nick@nick.com')
for d in u.devices:
    d.delete()
u.reload()

d,c = GPSDevice.objects.get_or_create(imei='111111111111111')
d.latitude = -37.761283
d.longitude = 144.967334
d.save()
u.devices.append(d)

d,c = GPSDevice.objects.get_or_create(imei='222222222222222')
d.latitude = -37.755820
d.longitude = 144.945190
d.save()
u.devices.append(d)

d,c = GPSDevice.objects.get_or_create(imei='333333333333333')
d.latitude = -37.794558 
d.longitude = 144.944933
d.save()
u.devices.append(d)

d,c = GPSDevice.objects.get_or_create(imei='444444444444444')
d.latitude = -37.791438 
d.longitude = 144.994543
d.save()
u.devices.append(d)

u.save()
