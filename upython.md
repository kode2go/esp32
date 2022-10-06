# Cam usage

```
>>> import camera
>>> camera.init(0, format=camera.JPEG)
True
>>> buf = camera.capture()
>>> f = open('image.jpg','w')
>>> f.write(buf)
64664
>>> f.close()
>>> camera.speffect(camera.EFFECT_BW)
>>> 
>>> buf = camera.capture()
>>> f = open('image2.jpg','w')
>>> 
>>> f.write(buf)
59897
>>> f.close()

>>> buf = camera.capture()
>>> mylist = list(buf)
>>> mylist
```

